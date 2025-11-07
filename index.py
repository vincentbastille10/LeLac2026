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

# --- Bloc de protection par mot de passe (cookies persistants) ---
password_gate = """
<style>
  #pw-overlay{
    position:fixed;inset:0;display:flex;align-items:center;justify-content:center;
    background:rgba(3,6,10,0.92);z-index:9999;color:#fff;font-family:Inter,system-ui,sans-serif;
  }
  #pw-box{width:min(520px,92vw);border-radius:12px;padding:28px;
    background:linear-gradient(180deg,rgba(255,255,255,0.03),rgba(255,255,255,0.02));
    box-shadow:0 10px 30px rgba(0,0,0,0.6);text-align:center;}
  #pw-box h2{margin:0 0 8px;font-size:20px;letter-spacing:0.2px;}
  #pw-box p{margin:0 0 18px;color:#bfc9d6;font-size:13px}
  #pw-input{width:100%;padding:12px 14px;border-radius:8px;border:1px solid rgba(255,255,255,0.06);
    background:transparent;color:#fff;font-size:15px;box-sizing:border-box}
  #pw-submit{margin-top:12px;padding:10px 16px;border-radius:8px;border:0;
    background:#1f6feb;color:#fff;font-weight:600;cursor:pointer}
  #pw-error{color:#ff7b7b;font-size:13px;margin-top:10px;display:none}
</style>

<div id="pw-overlay" aria-hidden="false">
  <div id="pw-box" role="dialog" aria-modal="true" aria-label="Accès protégé">
    <h2>Accès protégé — Dossier LE LAC</h2>
    <p>Entrez le mot de passe pour ouvrir le dossier.</p>
    <input id="pw-input" type="password" placeholder="Mot de passe" autofocus autocomplete="current-password" />
    <button id="pw-submit">Ouvrir</button>
    <div id="pw-error">Mot de passe incorrect.</div>
    <p style="margin-top:12px;font-size:12px;color:#9aa6b8">Contact : vincentbastille — accès collaborateur</p>
  </div>
</div>

<script>
(function(){
  const CORRECT = "lac26";
  const COOKIE_NAME = "le-lac-unlocked";
  const COOKIE_DAYS = 365;

  const overlay = document.getElementById("pw-overlay");
  const input = document.getElementById("pw-input");
  const btn = document.getElementById("pw-submit");
  const err = document.getElementById("pw-error");
  const box = document.getElementById("pw-box");

  function setCookie(name,value,days){
    const d = new Date();
    d.setTime(d.getTime() + (days*24*60*60*1000));
    document.cookie = name + "=" + encodeURIComponent(value) + ";expires=" + d.toUTCString() + ";path=/";
  }
  function getCookie(name){
    const v = document.cookie.match('(^|;)\\\\s*' + name + '\\\\s*=\\\\s*([^;]+)');
    return v ? decodeURIComponent(v.pop()) : null;
  }
  function unlock(){
    overlay.style.transition = "opacity .25s ease";
    overlay.style.opacity = "0";
    setTimeout(()=>overlay.remove(),260);
    setCookie(COOKIE_NAME,"1",COOKIE_DAYS);
  }
  if(getCookie(COOKIE_NAME)==="1"){ overlay.remove(); return; }

  btn.addEventListener("click", tryPass);
  input.addEventListener("keydown",(e)=>{ if(e.key==="Enter") tryPass(); });
  function tryPass(){
    err.style.display="none";
    const val = (input.value||"").trim();
    if(val===CORRECT){ unlock(); }
    else{
      err.style.display="block";
      input.value=""; input.focus();
      box.animate([{transform:"translateX(-6px)"},{transform:"translateX(6px)"},{transform:"translateX(0)"}],{duration:220});
    }
  }
})();
</script>
"""

# --- Génération du fichier HTML final ---
with open("index.html", "w", encoding="utf-8") as f:
    f.write(f"<!doctype html><html lang='fr'><meta charset='utf-8'>"
            f"<body style='background:#0b0d12;color:white;font-family:sans-serif;padding:20px'>"
            f"{password_gate}{html_content}</body></html>")

print("[OK] index.html régénéré avec protection par mot de passe (cookie persistant).")
