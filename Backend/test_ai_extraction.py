from app.services.ai_service import extract_policy_evidence_with_ai

result = extract_policy_evidence_with_ai(
    "Google Maps collects precise location information for directions and nearby search.",
    "Google Maps",
)

print("AI EXTRACTION RESULT:")
print(result)