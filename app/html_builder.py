import os

BASE = "output/html"

def build_html_from_json(batch, data):
    os.makedirs(BASE, exist_ok=True)

    index_links = []

    for folder, items in data["folders"].items():
        fname = f"{folder}.html".replace(" ", "_")
        path = f"{BASE}/{fname}"

        videos = "".join(
            f"<li onclick=\"play('{v['url']}')\">{v['title']}</li>"
            for v in items["videos"]
        )
        pdfs = "".join(
            f"<li onclick=\"pdf('{p['url']}')\">{p['title']}</li>"
            for p in items["pdfs"]
        )

        html = f"""
<!DOCTYPE html>
<html>
<head>
<title>{folder}</title>
<link rel="stylesheet" href="/static/css/style.css">
</head>
<body>

<h2>{folder}</h2>

<div class="layout">
<aside>
<h3>Videos</h3><ul>{videos}</ul>
<h3>PDFs</h3><ul>{pdfs}</ul>
</aside>

<main>
<iframe id="v"></iframe>
<iframe id="p"></iframe>
</main>
</div>

<script>
function play(u) {{
 document.getElementById('v').src =
  'https://cpplayer.onrender.com/?url=' + encodeURIComponent(u);
 document.getElementById('p').src='';
}}
function pdf(u) {{
 document.getElementById('p').src=u;
 document.getElementById('v').src='';
}}
</script>

</body>
</html>
"""
        open(path, "w", encoding="utf-8").write(html)
        index_links.append(f"<li><a href='/output/html/{fname}'>{folder}</a></li>")

    index = f"""
<html>
<body>
<h1>{batch}</h1>
<ul>{''.join(index_links)}</ul>
</body>
</html>
"""
    main_path = f"{BASE}/{batch}.html"
    open(main_path, "w").write(index)

    return f"/output/html/{batch}.html"
