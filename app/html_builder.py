import json
import os

OUTPUT_HTML = "output/html"

def build_html_from_json(json_path):
    os.makedirs(OUTPUT_HTML, exist_ok=True)

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{data['batch_name']}</title>
<link rel="stylesheet" href="/static/css/style.css">
</head>
<body>

<h1>{data['batch_name']}</h1>

<input type="text" id="search" placeholder="Search..." onkeyup="search()">

<div id="content">
"""

    for folder in data["folders"]:
        html += f"""
<button class="collapsible">{folder['name']}</button>
<div class="folder">
"""

        for v in folder.get("videos", []):
            html += f"""
<div>
<a href="https://cpplayer.onrender.com/?url={v['url']}" target="_blank">
▶ {v['title']}
</a>
</div>
"""

        for p in folder.get("pdfs", []):
            html += f"""
<div>
<a href="{p['url']}" target="_blank">📄 {p['title']}</a>
</div>
"""

        html += "</div>"

    html += """
</div>

<script>
document.querySelectorAll(".collapsible").forEach(btn=>{
  btn.onclick = () => btn.nextElementSibling.classList.toggle("show");
});

function search(){
  let q=document.getElementById("search").value.toLowerCase();
  document.querySelectorAll("#content div").forEach(d=>{
    d.style.display=d.innerText.toLowerCase().includes(q)?"":"none";
  });
}
</script>

</body>
</html>
"""

    out = f"{OUTPUT_HTML}/{data['batch_id']}.html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)

    return out
