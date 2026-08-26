from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
from pii_redactor import redact_pii
from prompt_classifier import InjectionDetector
from audit_logger import log_event

app = FastAPI(
    title="LLM Security Shield",
    description="An asynchronous proxy verifying prompts for PII leaks and injection attacks.",
    version="1.0.0"
)

print("Booting up AI Guardrail...")
ai_guardrail = InjectionDetector()

class PromptRequest(BaseModel):
    user_id: str
    raw_prompt: str

class ShieldResponse(BaseModel):
    status: str
    safe_prompt: str | None = None
    warning: str | None = None
    latency_ms: float

@app.post("/api/v1/secure-chat", response_model=ShieldResponse)
async def process_prompt(request: PromptRequest):
    start_time = time.time()
    
    # AI Injection Detection (Check for Hackers First)
    # We analyze the RAW prompt before the redactor touches it.
    ai_analysis = ai_guardrail.check_prompt(request.raw_prompt)
    
    if ai_analysis["is_attack"]:
        # Log the attack with the exact AI confidence score
        log_event(
            request.user_id, 
            "INJECTION_BLOCKED", 
            request.raw_prompt, 
            ai_analysis["injection_confidence"]
        )
        raise HTTPException(
            status_code=403, 
            detail=f"Security Alert: Potential prompt injection blocked (Confidence: {ai_analysis['injection_confidence']}%)"
        )

    # If they are not a hacker, we scrub their data.
    scrubbed_prompt = redact_pii(request.raw_prompt)
    
    if scrubbed_prompt != request.raw_prompt:
        log_event(request.user_id, "PII_REDACTED", "Sensitive data scrubbed from prompt.", 1.0)

    # If it reaches this line, the prompt is 100% clean and safe.
    latency = round((time.time() - start_time) * 1000, 2)
    
    log_event(
        request.user_id, 
        "PROMPT_CLEARED", 
        scrubbed_prompt, 
        ai_analysis["safe_confidence"]
    )

    return ShieldResponse(
        status="success",
        safe_prompt=scrubbed_prompt,
        latency_ms=latency
    )
