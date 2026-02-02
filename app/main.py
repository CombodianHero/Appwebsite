from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.classplus import get_batches, extract_batch_content
from app.html_builder import build_html_from_json

import os, json

app = FastAPI()

os.makedirs("output/json", exist_ok=True)
os.makedirs("output/html", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/output", StaticFiles(directory="output"), name="output")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get-batches")
async def batches(org_code: str = Form(...)):
    return await get_batches(org_code)

@app.post("/extract")
async def extract(
    org_code: str = Form(...),
    batch_id: str = Form(...),
    batch_name: str = Form(...)
):
    data = await extract_batch_content(org_code, batch_id)

    json_path = f"output/json/{batch_name}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    html_index = build_html_from_json(batch_name, data)

    return {
        "json": f"/{json_path}",
        "html": html_index
    }
