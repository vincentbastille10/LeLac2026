import os, html

# cherche tous les .txt du dossier public/
txts = sorted([f for f in os.listdir("public") if f.endswith(".txt")])

html_content = "<h1>LE LAC — Dossier</h1>"
for f in txts:
    with open(os.path.join("public", f), encoding="utf-8", errors="ignore") as fh:
        content = html.escape(fh.read())
    html_content += f"""
    <details style='margin:8px 0;padding:10px;border:1px solid #333;border-radius:10px;'>
      <summary style='cursor:pointer;font-weight:bold;color:#4ea4ff'>{f}</summary>
      <pre style='white-space:pre-wrap'>{content}</pre>
    </details>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(f"<!doctype html><html lang='fr'><meta charset='utf-8'><body style='background:#0b0d12;color:white;font-family:sans-serif;padding:20px'>{html_content}</body></html>")

print("[OK] index.html régénéré.")
