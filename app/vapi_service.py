import os
import httpx

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")
VAPI_PHONE_NUMBER_ID = os.getenv("VAPI_PHONE_NUMBER_ID")

async def trigger_call(*, phone: str, message: str):
    payload = {
        "assistantId": VAPI_ASSISTANT_ID,
        "phoneNumberId": VAPI_PHONE_NUMBER_ID,
        "customer": {"number": phone},
        "assistantOverrides": {
            "variableValues": {
                "message": message
            }
        }
    }

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            "https://api.vapi.ai/call",
            json=payload,
            headers={
                "Authorization": f"Bearer {VAPI_API_KEY}",
                "Content-Type": "application/json",
            },
        )
        r.raise_for_status()
        return r.json()
