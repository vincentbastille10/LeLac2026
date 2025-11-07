#!/usr/bin/env python3
import os, re, html, hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(ROOT, "template.html")
OUTPUT = os.path.join(ROOT, "index.html")

def load_access():
    # Multiple emails supported (comma or spaces). Password hashed.
    emails = ["vincentbastille100@gmail.com"]
    pw = "lac26"
    af = os.path.join(ROOT, "access.txt")
    if os.path.isfile(af):
        with open(af, "r", encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if not line or line.startswith("#"): continue
                if line.lower().startswith("email="):
                    raw=line.split("=",1)[1]
                    emails=[e.strip() for e in re.split(r"[,\s]+", raw) if e.strip()]
                elif line.lower().startswith("password="):
                    pw=line.split("=",1)[1].strip() or pw
    return emails, hashlib.sha256(pw.encode("utf-8")).hexdigest()

def sort_key(name: str):
    m = re.match(r'^(\d+)[-_ ]?', name)
    num = int(m.group(1)) if m else 9999
    return (num, name.lower())

def label_from(name: str):
    base = os.path.splitext(name)[0]
    base = re.sub(r'^\d+[-_ ]*', '', base)           # drop numeric prefix
    base = re.sub(r'^le[-_ ]lac[-_ ]*', '', base, flags=re.I)  # drop "le-lac-"
    base = base.replace('_',' ').replace('-',' ').strip()
    return base.capitalize()

def read_text(path: str):
    try:
        with open(path,"r",encoding="utf-8") as f: return f.read()
    except UnicodeDecodeError:
        with open(path,"r",encoding="latin-1") as f: return f.read()

def root_sections():
    files=[f for f in os.listdir(ROOT) if os.path.isfile(os.path.join(ROOT,f))]
    txts=[f for f in files if f.lower().endswith(".txt") and f not in {"index.html","template.html","build.py","vercel.json","access.txt","README.md"}]
    if not txts:
        return "<p style='opacity:.7'>Aucun fichier .txt détecté à la racine.</p>"
    sections=[]
    for f in sorted(txts,key=sort_key):
        raw = read_text(os.path.join(ROOT,f))
        # Support raw HTML in .txt (like your mise en scène); if it looks like HTML block, keep as is.
        looks_html = ("<details" in raw) or ("<p>" in raw) or ("<summary>" in raw)
        body = raw if looks_html else f"<pre>{html.escape(raw, quote=False)}</pre>"
        sections.append(f"<details><summary>{label_from(f)}</summary><div class='body'>{body}</div></details>")
    return "<details class='grp'><summary>Dossier — sections</summary><div class='sub'>" + "\n".join(sections) + "</div></details>"

def attachments():
    files=[f for f in os.listdir(ROOT) if os.path.isfile(os.path.join(ROOT,f))]
    atts=[f for f in files if os.path.splitext(f)[1].lower() in (".pdf",".xlsx",".csv")]
    if not atts: return ""
    links=[f"<li><a href='{html.escape(f)}' target='_blank' rel='noopener'>{label_from(f)}</a></li>" for f in sorted(atts,key=str.lower)]
    return "<details class='grp'><summary>Pièces jointes</summary><div class='sub'><div class='body'><ul>" + "\n".join(links) + "</ul></div></div></details>"

def main():
    emails, pwhash = load_access()
    with open(TEMPLATE,"r",encoding="utf-8") as f: tpl=f.read()
    emails_js = "[" + ",".join([f"'{e}'" for e in emails]) + "]"
    tpl = tpl.replace("/* @@ACCESS_CONFIG */", f"const ALLOWED_EMAILS={emails_js}; const PASS_HASH='{pwhash}';")
    html_out = "\n".join([root_sections(), attachments()])
    out = tpl.replace("<!-- @@INJECT_GROUPS_HERE -->", html_out)
    with open(OUTPUT,"w",encoding="utf-8") as f: f.write(out)
    print("[OK] Généré:", OUTPUT)

if __name__=="__main__":
    main()
