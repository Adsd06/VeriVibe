import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

PROMPT_FILE = os.path.join(os.path.dirname(__file__), 'References', 'mentor_prompt')

FALLBACK_PROMPT = """Role: Patient Senior Mentor for Non-Technical Builders and Students.
Objective: Convert raw code vulnerabilities and technical errors into plain-language explanations.

Guidelines:
1. Avoid intimidating enterprise audit jargon or complex compiler diagnostics.
2. Explain the real-world consequence of the flaw in everyday terms.
3. Output the exact corrected, secure code snippet.
4. Provide a single short "takeaway rule" to foster long-term technical competence."""

def get_system_prompt() -> str:
    if os.path.exists(PROMPT_FILE):
        try:
            with open(PROMPT_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return content
        except Exception:
            pass
    return FALLBACK_PROMPT

def get_api_keys():
    """Parses comma-separated keys from Streamlit secrets or environment variables."""
    raw_keys = ""
    try:
        if hasattr(st, "secrets"):
            raw_keys = st.secrets.get("GEMINI_API_KEY", "") or st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        pass
    
    if not raw_keys:
        raw_keys = os.environ.get("GEMINI_API_KEY", "") or os.environ.get("GROQ_API_KEY", "")
        
    keys = [k.strip() for k in raw_keys.split(",") if k.strip() and "your_api_key" not in k.lower()]
    return keys

def get_mentorship_feedback(code_snippet: str, regex_violations: list) -> str:
    """
    Queries Groq's API using active production models with multi-key rotation and AI severity classification.
    """
    keys = get_api_keys()
    
    violations_summary = "None detected locally."
    if regex_violations:
        violations_summary = "\n".join([f"- {v['name']}: {v['risk']}" for v in regex_violations])

    user_content = f"""Analyze the following code snippet submitted by a builder.

Local Guardrail Scan Results:
{violations_summary}

Code Snippet:
{code_snippet}

Provide your response starting with a single status line formatted exactly as:
STATUS: [CLEAN | WARNING | HIGH_RISK | CRITICAL]

Followed strictly by these four headers:
### 1. Plain-Language Breakdown
### 2. Real-World Risk
### 3. Remediation Code
### 4. Takeaway Rule"""

    system_instruction = get_system_prompt()
    url = "https://api.groq.com/openai/v1/chat/completions"

    if keys:
        for key in keys:
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "openai/gpt-oss-120b",
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_content}
                ],
                "temperature": 0.3,
                "max_tokens": 1000
            }
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=12)
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    return f"STATUS: HIGH_RISK\n### 1. Plain-Language Breakdown\n**API ERROR ({response.status_code}):**\n`{response.text}`\n\n### 2. Real-World Risk\nThe Groq API rejected the payload.\n### 3. Remediation Code\nN/A\n### 4. Takeaway Rule\nCheck API endpoint formatting."
            except Exception as e:
                return f"STATUS: HIGH_RISK\n### 1. Plain-Language Breakdown\n**NETWORK ERROR:**\n`{str(e)}`\n\n### 2. Real-World Risk\nThe request timed out or failed to connect.\n### 3. Remediation Code\nN/A\n### 4. Takeaway Rule\nCheck Streamlit server connectivity."
    
    return 'STATUS: HIGH_RISK\n### 1. Plain-Language Breakdown\n**SECRETS ERROR:** No API keys were detected in the environment or Streamlit secrets.\n\n### 2. Real-World Risk\nStreamlit is not parsing your keys correctly.\n### 3. Remediation Code\nEnsure Secrets format is `GROQ_API_KEY = "gsk_..."`\n### 4. Takeaway Rule\nKeys must be configured properly in Streamlit dashboard settings.'