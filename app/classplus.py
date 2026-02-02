import aiohttp, re

HEADERS = {
    "api-version": "35",
    "user-agent": "Mobile-Android",
    "region": "IN",
    "content-type": "application/json"
}

async def get_org_hash(session, org):
    html = await (await session.get(f"https://{org}.courses.store")).text()
    m = re.search(r'"hash":"(.*?)"', html)
    return m.group(1) if m else None

async def get_batches(org):
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        org_hash = await get_org_hash(session, org)
        if not org_hash:
            return []

        all_batches = []
        page = 1

        while True:
            payload = {
                "query": "",
                "page": page,
                "limit": 20,
                "filters": {},
                "sort": {"createdAt": -1}
            }

            url = f"https://api.classplusapp.com/v2/course/preview/search/{org_hash}"
            res = await (await session.post(url, json=payload)).json()

            courses = res.get("data", {}).get("coursesData", [])
            if not courses:
                break

            all_batches.extend(courses)
            page += 1

        # remove duplicates
        unique = {}
        for b in all_batches:
            unique[b["id"]] = b

        return list(unique.values())

async def extract_batch_content(org, batch_id):
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        info = await (await session.get(
            "https://api.classplusapp.com/v2/course/preview/org/info",
            params={"courseId": batch_id}
        )).json()

        token = info["data"]["hash"]

        res = await (await session.get(
            f"https://api.classplusapp.com/v2/course/preview/content/list/{token}"
        )).json()

    tree = {"folders": {}}

    for item in res["data"]:
        folder = item.get("folderName") or "ROOT"
        tree["folders"].setdefault(folder, {"videos": [], "pdfs": []})

        url = item.get("url")
        if not url:
            continue

        entry = {"title": item["name"], "url": url}

        if url.endswith(".pdf"):
            tree["folders"][folder]["pdfs"].append(entry)
        else:
            tree["folders"][folder]["videos"].append(entry)

    return tree
