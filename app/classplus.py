import aiohttp
import base64
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Origin": "https://web.classplusapp.com",
    "Referer": "https://web.classplusapp.com/",
}

def encode_payload(payload: dict) -> str:
    return base64.b64encode(json.dumps(payload).encode()).decode()

async def get_batches(org_code: str):
    url_base = "https://api.classplusapp.com/v2/course/preview/search/"
    all_batches = []
    page = 1

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        while True:
            payload = {
                "orgCode": org_code,
                "page": page,
                "limit": 50
            }

            encoded = encode_payload(payload)
            url = url_base + encoded

            async with session.post(url) as resp:
                text = await resp.text()

                # ❌ If Classplus sends HTML or error page
                if "application/json" not in resp.headers.get("Content-Type", ""):
                    return {
                        "error": "Classplus blocked or invalid ORG code",
                        "status": resp.status,
                        "response": text[:500]
                    }

                data = json.loads(text)

                batches = data.get("data", [])
                if not batches:
                    break

                all_batches.extend(batches)
                page += 1

    return all_batches
