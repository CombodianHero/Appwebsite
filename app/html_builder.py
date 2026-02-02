import os

BASE = "output/html"

def build_html_from_json(batch, data):
    os.makedirs(BASE, exist_ok=True)
    links = []

    for folder, items in data["folders"].items():
        fname = folder.replace(" ", "_") + ".html"
        path = f"{BASE}/{fname}"

        videos = "".join(
            f"<li onclick=\"play('{v['url']}')\">🎬 {v['title']}</li>"
            for v in items["videos"]
        )
        pdfs = "".join(
            f"<li onclick=\"pdf('{p['url']}')\">📄 {p['title']}</li>"
            for p in items["pdfs"]
        )

        html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{folder}</title>
<link rel="stylesheet" href="/static/css/style.css">
</head>
<body>

<h2>{folder}</h2>

<div class="layout">
  <aside>
    <button class="collapsible">🎬 Videos</button>
    <div class="content">
      <ul>{videos}</ul>
    </div>

    <button class="collapsible">📄 PDFs</button>
    <div class="content">
      <ul>{pdfs}</ul>
    </div>
  </aside>

  <main>
    <iframe id="v"></iframe>
    <iframe id="p"></iframe>
  </main>
</div>

<script>
function play(u) {{
  document.getElementById("v").src =
    "https://cpplayer.onrender.com/?url=" + encodeURIComponent(u);
  document.getElementById("p").src = "";
}}

function pdf(u) {{
  document.getElementById("p").src = u;
  document.getElementById("v").src = "";
}}

document.querySelectorAll(".collapsible").forEach(function(btn) {{
  btn.addEventListener("click", function() {{
    btn.nextElementSibling.classList.toggle("show");
  }});
}});
</script>

</body>
</html>
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

        links.append(f"<li><a href='/output/html/{fname}'>{folder}</a></li>")

    index_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{batch}</title>
<link rel="stylesheet" href="/static/css/style.css">
</head>
<body>

<h1>{batch}</h1>
<ul>
  {''.join(links)}
</ul>

</body>
</html>
"""
    index_path = f"{BASE}/{batch}.html"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)

    return f"/output/html/{batch}.html"
