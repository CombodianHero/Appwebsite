import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.classplus import get_batches
from app.extractor import extract_batch
from app.html_builder import build_html_from_json

# ✅ CREATE REQUIRED DIRECTORIES FIRST
os.makedirs("output/json", exist_ok=True)
os.makedirs("output/html", exist_ok=True)
os.makedirs("static", exist_ok=True)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/output", StaticFiles(directory="output"), name="output")


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/index.html", encoding="utf-8") as f:
        return f.read()


@app.post("/get-batches")
async def batches(request: Request):
    data = await request.json()
    org_code = data.get("org_code")

    if not org_code:
        return JSONResponse({"success": False, "error": "ORG code required"})

    return await get_batches(org_code)


@app.post("/extract-batch")
async def extract(request: Request):
    data = await request.json()
    batch_id = data.get("batch_id")
    batch_name = data.get("batch_name")

    json_path = await extract_batch(batch_id, batch_name)
    html_path = build_html_from_json(json_path)

    return {
        "success": True,
        "html_url": f"/{html_path}"
    }
