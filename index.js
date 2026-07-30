// 🌙 Cloudflare Worker Translator
// کپی کن، paste کن، تمام! 🚀

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // API endpoint for translation
    if (url.pathname === '/api/translate' && request.method === 'POST') {
      const body = await request.text();
      const params = new URLSearchParams(body);
      const text = params.get('text');
      const source = params.get('source') || 'auto';
      const target = params.get('target') || 'fa';
      
      const result = await translate(text, source, target);
      return new Response(JSON.stringify(result), {
        headers: { 
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }
    
    // Serve the HTML page
    return new Response(HTML_PAGE, {
      headers: { 'Content-Type': 'text/html; charset=utf-8' }
    });
  }
};

// Translation via Google Translate (free)
async function translate(text, source, target) {
  try {
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${source}&tl=${target}&dt=t&q=${encodeURIComponent(text)}`;
    const r = await fetch(url);
    const data = await r.json();
    if (data && data[0]) {
      return {
        translated: data[0][0][0],
        backend: 'Google'
      };
    }
  } catch (e) {}
  
  return { translated: '❌ Translation failed', backend: 'Error' };
}

// Full HTML/CSS/JS in one string - Dark Theme!
const HTML_PAGE = `<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>🌙 Dark Translator</title>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0a0a1a;--card:#12122a;--border:#1f1f3a;--accent:#a855f7;--accent2:#6366f1;--text:#f1f5f9;--dim:#5a5a7a;--success:#22c55e;--error:#ef4444}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
body::before{content:'';position:fixed;inset:0;background:radial-gradient(ellipse 80% 50% at 20% 0%,rgba(168,85,247,.15) 0%,transparent 50%),radial-gradient(ellipse 60% 40% at 80% 100%,rgba(99,102,241,.1) 0%,transparent 50%);z-index:-1}
.container{max-width:1200px;margin:0 auto;padding:20px}
header{display:flex;align-items:center;justify-content:space-between;padding:16px 24px;margin-bottom:24px;background:rgba(18,18,42,.9);backdrop-filter:blur(20px);border:1px solid var(--border);border-radius:20px;position:relative;overflow:hidden}
header::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--accent),var(--accent2),var(--accent));animation:shine 3s linear infinite}
@keyframes shine{0%{transform:translateX(-100%)}100%{transform:translateX(100%)}}
.logo{display:flex;align-items:center;gap:12px;font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.main{display:flex;flex-direction:column;gap:20px}
.lang-row{display:flex;gap:12px;align-items:center}
select{flex:1;padding:14px 16px;background:var(--card);border:1px solid var(--border);border-radius:14px;color:var(--text);font-size:1rem;font-family:inherit;cursor:pointer;appearance:none}
select:focus{outline:none;border-color:var(--accent)}
.swap-btn{width:52px;height:52px;border-radius:14px;background:var(--card);border:1px solid var(--border);color:var(--accent);font-size:1.4rem;cursor:pointer;flex-shrink:0;transition:all .3s}
.swap-btn:hover{background:var(--accent);color:var(--bg);transform:rotate(180deg)}
textarea{width:100%;height:250px;padding:20px;background:var(--card);border:1px solid var(--border);border-radius:16px;color:var(--text);font-family:'Vazirmatn',monospace;font-size:1rem;line-height:1.8;resize:vertical}
textarea:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px rgba(168,85,247,.15)}
textarea::placeholder{color:var(--dim)}
.trans-btn{width:100%;padding:16px;background:linear-gradient(135deg,var(--accent),var(--accent2));border:none;border-radius:14px;color:#fff;font-size:1.1rem;font-weight:700;font-family:inherit;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;transition:all .3s;position:relative;overflow:hidden}
.trans-btn::before{content:'';position:absolute;top:0;left:-100%;right:-100%;bottom:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.2),transparent);animation:shimmer 2s infinite}
@keyframes shimmer{0%{left:-100%}100%{left:100%}}
.trans-btn:hover{transform:translateY(-2px);box-shadow:0 12px 40px rgba(168,85,247,.4)}
.trans-btn:active{transform:scale(.98)}
.trans-btn.loading .btn-text{display:none}
.trans-btn .spinner{display:none;width:20px;height:20px;border:2px solid rgba(255,255,255,.3);border-top-color:#fff;border-radius:50%;animation:spin .8s linear infinite}
.trans-btn.loading .spinner{display:block}
@keyframes spin{to{transform:rotate(360deg)}}
.actions{display:flex;gap:12px;flex-wrap:wrap}
.act-btn{flex:1;min-width:120px;padding:14px;background:var(--card);border:1px solid var(--border);border-radius:14px;color:var(--text);font-size:.9rem;font-weight:600;font-family:inherit;cursor:pointer;transition:all .2s}
.act-btn:hover{background:var(--border);transform:translateY(-2px)}
.toast{position:fixed;bottom:30px;left:50%;transform:translateX(-50%) translateY(100px);background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;padding:14px 28px;border-radius:14px;font-weight:600;z-index:1000;opacity:0;transition:all .4s cubic-bezier(.34,1.56,.64,1)}
.toast.show{transform:translateX(-50%) translateY(0);opacity:1}
.char-count{text-align:left;font-size:.75rem;color:var(--dim);margin-top:8px}
.result-box{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:20px;min-height:150px;white-space:pre-wrap;line-height:1.8;font-size:1.05rem}
.result-box.empty{color:var(--dim);font-style:italic}
.result-box .backend-badge{display:inline-block;font-size:.7rem;padding:2px 10px;border-radius:100px;background:rgba(34,197,94,.15);color:var(--success);margin-top:8px}
footer{text-align:center;padding:20px;color:var(--dim);font-size:.8rem}
footer a{color:var(--accent);text-decoration:none}
@media(max-width:640px){.container{padding:12px}.lang-row{flex-direction:column}.swap-btn{width:100%;transform:rotate(90deg)}.swap-btn:hover{transform:rotate(270deg) scale(1.1)}}
</style>
</head>
<body>
<div class="container">
  <header>
    <div class="logo"><span>🌙</span><span>Translator</span></div>
    <div style="color:var(--dim);font-size:.8rem">Powered by Cloudflare ⚡</div>
  </header>
  
  <div class="main">
    <div class="lang-row">
      <select id="src">
        <option value="auto" selected>🔍 تشخیص خودکار</option>
        <option value="fa">🇮🇷 فارسی</option>
        <option value="en">🇺🇸 English</option>
        <option value="ar">🇸🇦 العربية</option>
        <option value="tr">🇹🇷 Türkçe</option>
        <option value="de">🇩🇪 Deutsch</option>
        <option value="fr">🇫🇷 Français</option>
        <option value="es">🇪🇸 Español</option>
        <option value="ru">🇷🇺 Русский</option>
        <option value="zh">🇨🇳 中文</option>
        <option value="ja">🇯🇵 日本語</option>
        <option value="ko">🇰🇷 한국어</option>
        <option value="it">🇮🇹 Italiano</option>
        <option value="pt">🇵🇹 Português</option>
        <option value="hi">🇮🇳 हिन्दी</option>
        <option value="nl">🇳🇱 Nederlands</option>
        <option value="pl">🇵🇱 Polski</option>
        <option value="sv">🇸🇪 Svenska</option>
      </select>
      <button class="swap-btn" onclick="swap()">⇄</button>
      <select id="tgt">
        <option value="fa">🇮🇷 فارسی</option>
        <option value="en" selected>🇺🇸 English</option>
        <option value="ar">🇸🇦 العربية</option>
        <option value="tr">🇹🇷 Türkçe</option>
        <option value="de">🇩🇪 Deutsch</option>
        <option value="fr">🇫🇷 Français</option>
        <option value="es">🇪🇸 Español</option>
        <option value="ru">🇷🇺 Русский</option>
        <option value="zh">🇨🇳 中文</option>
        <option value="ja">🇯🇵 日本語</option>
        <option value="ko">🇰🇷 한국어</option>
        <option value="it">🇮🇹 Italiano</option>
        <option value="pt">🇵🇹 Português</option>
        <option value="hi">🇮🇳 हिन्दी</option>
        <option value="nl">🇳🇱 Nederlands</option>
        <option value="pl">🇵🇱 Polski</option>
        <option value="sv">🇸🇪 Svenska</option>
      </select>
    </div>
    
    <div style="position:relative">
      <textarea id="input" placeholder="اینجا تایپ کن یا پیست کن... (Ctrl+Enter)" oninput="updateCount()"></textarea>
      <div class="char-count" id="count">0 کاراکتر</div>
    </div>
    
    <button class="trans-btn" id="transBtn" onclick="translate()">
      <span class="btn-text"><span>🚀</span> ترجمه کن</span>
      <div class="spinner"></div>
    </button>
    
    <div class="result-box empty" id="result">ترجمه اینجا نشون داده میشه...</div>
    
    <div class="actions">
      <button class="act-btn" onclick="copyResult()">📋 کپی ترجمه</button>
      <button class="act-btn" onclick="clearAll()">🗑️ پاک کردن</button>
    </div>
  </div>
  
  <footer>Suilt with ❤️ by Abolfazl | <a href="#">🌙 Dark Translator</a></footer>
</div>

<div class="toast" id="toast"></div>

<script>
let debounce;
const src=document.getElementById('src'),tgt=document.getElementById('tgt'),
input=document.getElementById('input'),result=document.getElementById('result'),
count=document.getElementById('count'),btn=document.getElementById('transBtn'),toast=document.getElementById('toast');

src.value=localStorage.getItem('srcLang')||'auto';
tgt.value=localStorage.getItem('tgtLang')||'fa';
src.onchange=()=>localStorage.setItem('srcLang',src.value);
tgt.onchange=()=>localStorage.setItem('tgtLang',tgt.value);

input.onkeydown=e=>{if(e.ctrlKey&&e.key==='Enter'){e.preventDefault();translate()}};
input.oninput=()=>{clearTimeout(debounce);debounce=setTimeout(()=>{if(input.value.trim().length>2)translate()},800)};

function updateCount(){count.textContent=input.value.length.toLocaleString()+' کاراکتر'}

function swap(){
if(src.value==='auto')return showToast('نمیشه با auto جابه‌جا کرد 😅','info');
const s=src.value,t=tgt.value;
src.value=t;tgt.value=s;
if(input.value.trim()&&result.textContent&&!result.classList.contains('empty')){
const tmp=input.value;input.value=result.textContent;result.textContent=tmp;updateCount();translate()
}}

async function translate(){
const text=input.value.trim();
if(!text){showToast('یه متن بنویس 😅','info');input.focus();return}
btn.classList.add('loading');
try{
const r=await fetch('/api/translate',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},
body:new URLSearchParams({text,source:src.value,target:tgt.value})});
const d=await r.json();
result.textContent=d.translated;
result.classList.remove('empty');
result.innerHTML=d.translated+'<div class="backend-badge">'+d.backend+'</div>';
showToast('ترجمه شد ✨')
}catch(e){showToast('خطا در ترجمه ❌','error')}
btn.classList.remove('loading')
}

function copyResult(){
const t=result.textContent.trim();
if(!t)return;
navigator.clipboard.writeText(t).then(()=>showToast('کپی شد ✅')).catch(()=>showToast('کپی نشد 😅','error'))
}

function clearAll(){input.value='';result.textContent='ترجمه اینجا نشون داده میشه...';result.classList.add('empty');count.textContent='0 کاراکتر';input.focus()}

function showToast(msg,type=''){
toast.textContent=msg;
toast.className='toast show';
setTimeout(()=>toast.className='toast',3000)
}

input.focus();
</script>
</body>
</html>`;
