import aiohttp
import json
import base64

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": "https://web.classplusapp.com",
    "Referer": "https://web.classplusapp.com/"
}

def encode(data):
    return base64.b64encode(json.dumps(data).encode()).decode()

async def get_batches(org_code: str):
    url_base = "https://api.classplusapp.com/v2/course/preview/search/"
    page = 1
    batches = []

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        while True:
            payload = {
                "orgCode": org_code,
                "page": page,
                "limit": 50
            }

            url = url_base + encode(payload)
            async with session.post(url) as r:
                text = await r.text()

                if "application/json" not in r.headers.get("Content-Type", ""):
                    return {"success": False, "error": "Classplus blocked or invalid ORG"}

                data = json.loads(text)
                items = data.get("data", [])

                if not items:
                    break

                batches.extend(items)
                page += 1

    return {"success": True, "batches": batches}
