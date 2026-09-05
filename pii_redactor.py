import re

def redact_pii(prompt: str) -> str:
    """
    Scans the incoming prompt for Personally Identifiable Information (PII)
    and replaces it with safe, generic tokens to prevent data leakage.
    """
    

email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

phone_pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'

ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'

scrubbed_prompt = re.sub(ssn_pattern, '[REDACTED_SSN]', prompt)
scrubbed_prompt = re.sub(email_pattern, '[REDACTED_EMAIL]', scrubbed_prompt)
scrubbed_prompt = re.sub(phone_pattern, '[REDACTED_PHONE]', scrubbed_prompt)

return scrubbed_prompt

if __name__ == "__main__":
    print("--- PII Redactor Test ---")
    test_prompt = "Can you summarize the account for john.doe@email.com? His SSN is 123-45-6789 and phone is 555-123-4567."
    
    print(f"RAW PROMPT: {test_prompt}")
    print(f"SAFE PROMPT: {redact_pii(test_prompt)}")
