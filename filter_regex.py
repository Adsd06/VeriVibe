import os
import json
import re

RULES_FILE = os.path.join(os.path.dirname(__file__), 'References', 'guardrail_rules.json')

FALLBACK_RULES = [
    {
        "id": "RULE_001",
        "name": "Hardcoded Secret / API Key",
        "pattern": "(sk_live|api_key|password|secret|bearer)\\s*[:=]\\s*['\"][a-zA-Z0-9-_]{16,}['\"]",
        "risk": "Exposed credentials in source code allow unauthorized access and security breaches."
    },
    {
        "id": "RULE_002",
        "name": "SQL Injection Vulnerability",
        "pattern": "execute\\s*\\(\\s*['\"].*\\+\\s*.*['\"]\\s*\\)",
        "risk": "Direct string concatenation in database queries enables malicious database manipulation."
    },
    {
        "id": "RULE_003",
        "name": "Dangerous Shell Execution",
        "pattern": "os\\.system\\s*\\(|subprocess\\.call\\s*\\(.*shell\\s*=\\s*True",
        "risk": "Executing shell commands with unvalidated input can lead to remote code execution."
    }
]

def load_rules():
    """Load regex rules from References/guardrail_rules.json safely with fallbacks."""
    if os.path.exists(RULES_FILE):
        try:
            with open(RULES_FILE, 'r', encoding='utf-8') as f:
                rules = json.load(f)
                if isinstance(rules, list) and len(rules) > 0:
                    return rules
        except Exception:
            pass
    return FALLBACK_RULES

def scan_code(code_text: str) -> list:
    """
    Scans code text against defined guardrail rules locally with zero network latency.
    Returns a list of matched violation objects.
    """
    if not code_text or not isinstance(code_text, str):
        return []

    rules = load_rules()
    violations = []
    
    for rule in rules:
        pattern = rule.get("pattern", "")
        if pattern:
            try:
                if re.search(pattern, code_text, flags=re.IGNORECASE):
                    violations.append({
                        "id": rule.get("id", "RULE_UNKNOWN"),
                        "name": rule.get("name", "Security Warning"),
                        "risk": rule.get("risk", "A potential security risk was detected in this block.")
                    })
            except re.error:
                continue
                
    return violations