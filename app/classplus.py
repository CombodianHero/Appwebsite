import aiohttp, re

HEADERS = {
    "api-version": "35",
    "user-agent": "Mobile-Android",
    "region": "IN"
}

async def get_batches(org):
    async with aiohttp.ClientSession(headers=HEADERS) as s:
        html = await (await s.get(f"https://{org}.courses.store")).text()
        token = re.search(r'"hash":"(.*?)"', html).group(1)

        res = await (await s.get(
            f"https://api.classplusapp.com/v2/course/preview/similar/{token}"
        )).json()

        return res["data"]["coursesData"]

async def extract_batch_content(org, batch_id, batch_name):
    async with aiohttp.ClientSession(headers=HEADERS) as s:
        info = await (await s.get(
            "https://api.classplusapp.com/v2/course/preview/org/info",
            params={"courseId": batch_id}
        )).json()

        token = info["data"]["hash"]

        content = await (await s.get(
            f"https://api.classplusapp.com/v2/course/preview/content/list/{token}"
        )).json()

    tree = {"Batch": batch_name, "folders": {}}

    for c in content["data"]:
        folder = c.get("folderName", "ROOT")
        tree["folders"].setdefault(folder, {"videos": [], "pdfs": []})

        url = c.get("url", "")
        if not url:
            continue

        item = {"title": c["name"], "url": url}

        if url.endswith(".pdf"):
            tree["folders"][folder]["pdfs"].append(item)
        else:
            tree["folders"][folder]["videos"].append(item)

    return tree
