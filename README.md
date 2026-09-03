# VeriVibe 🛡️

VeriVibe is a Streamlit-based security application that provides automated code vulnerability scanning and intelligent mentorship. It combines deterministic local regex guardrails with high-speed, LLM-driven deep analysis to help developers understand and remediate security risks.

**🚀 Live Demo:** [Test VeriVibe Instantly](https://verivibe.streamlit.app)

## Key Features
* **Multi-Stage Security Scanning:** Fast local AST regex checks for immediate flaw detection.
* **AI-Powered Mentorship:** Deep context analysis using Groq (Llama 3) to break down vulnerabilities in plain language.
* **Instant Fallback Mechanism:** Guaranteed high-quality mentorship output even during network interruptions or API rate limits.
* **4-Pillar Educational Output:** Every scan returns a Plain-Language Breakdown, Real-World Risk assessment, Remediation Code, and a Takeaway Rule.

## Basic Structure
* `app.py`: Main Streamlit application and UI routing.
* `filter_ai.py`: Core AI logic, prompt formatting, API multi-key rotation, and instant fallback routing.
* `requirements.txt`: Python dependencies.
* `.env.example`: Template for environment variables (API keys).

## Local Setup
1. Clone the repository: `git clone https://github.com/Adsd06/VeriVibe.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory and add your API keys (see `.env.example`).
4. Run the application: `streamlit run app.py`