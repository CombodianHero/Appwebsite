import os
import json

OUTPUT_JSON = "output/json"

async def extract_batch(batch_id: str, batch_name: str):
    os.makedirs(OUTPUT_JSON, exist_ok=True)

    # MOCK STRUCTURE – plug your real extraction logic here
    data = {
        "batch_id": batch_id,
        "batch_name": batch_name,
        "folders": [
            {
                "name": "Videos",
                "videos": [
                    {
                        "title": "Lecture 1",
                        "url": "https://example.com/video.m3u8"
                    }
                ]
            },
            {
                "name": "PDFs",
                "pdfs": [
                    {
                        "title": "Notes",
                        "url": "https://example.com/file.pdf"
                    }
                ]
            }
        ]
    }

    path = f"{OUTPUT_JSON}/{batch_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return path
