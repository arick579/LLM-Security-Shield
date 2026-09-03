# LLM-Security-Shield

An asynchronous Python security proxy designed to sanitize PII and intercept zero-day prompt injection attacks before they reach production Large Language Models (LLMs).

## The Tech Stack
* **Backend Framework:** FastAPI, Uvicorn, Python (Asyncio)
* **Artificial Intelligence:** PyTorch, Hugging Face Transformers (DeBERTa-v3)
* **Data Sanitization:** Regular Expressions (Regex)
* **Analytics & Logging:** SQLite, Matplotlib, Seaborn

## Core Architecture
1. **Asynchronous Gatekeeper:** A FastAPI proxy server that acts as a middleman between the user and the LLM, processing requests with sub-50ms latency.
2. **PII Redaction Engine:** A regex-based pipeline that automatically scrubs sensitive information (SSNs, Emails, Phone Numbers) replacing them with enterprise-safe `[REDACTED]` tokens.
3. **AI Injection Guardrail:** A localized, hardware-accelerated PyTorch transformer model trained on cybersecurity datasets to detect and block malicious prompt injections with confidence scoring.
4. **Audit Analytics:** An automated SQLite logging system that tracks intercepted threats and renders localized threat-distribution metrics via Matplotlib.

## Visual Proof
**Security Shield Interception**
<img width="1250" height="301" alt="image" src="https://github.com/user-attachments/assets/7bf18c6b-f1a5-4815-8423-730dab4dde4f" />



**Automated Threat Metrics**
<img width="1120" height="706" alt="Screenshot 2026-07-24 130102" src="https://github.com/user-attachments/assets/ee4d160d-5484-4f6e-aea3-651bc2353b47" />

## How to Run Locally
**1. Install Dependencies:**
```bash
pip install -r requirements.txt
```
**2. Boot the Proxy Server:**
```bash
uvicorn proxy_server:app --reload
```
**3. Run the Traffic Simulator (in a new terminal):**
```bash
python simulator.py
