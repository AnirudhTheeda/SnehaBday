import json
import base64
import mimetypes
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="PUTTINA ROJU SUBHAKANSHALU",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

PROJECT_DIR = Path(__file__).parent
DATA_PATH = PROJECT_DIR / "birthday_data.json"

DEFAULT = {
    "name": "Srinivas",
    "sender": "Your best friend",
    "letter_greeting": "Dear You,",
    "letter_text": "Happy Birthday!\n\nI hope your day is filled with love, laughter, and all the little things that make you smile.\n\nThank you for being such a special person. I’m wishing you a beautiful year ahead, full of happiness and wonderful memories.\n\nWith love,",
    "letter_signoff": "Your best friend",
    "balloon_words": ["Sneha", "is", "THOPU", "XD"],
    "questions": []
}

try:
    saved = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    data = {**DEFAULT, **saved}
except (OSError, json.JSONDecodeError):
    data = DEFAULT.copy()

# Media is loaded only from the project folders. There are no upload controls
# on the webpage. Put your own files in photos/ and videos/ before running.
def load_local_media(folder_name, extensions, captions_key):
    folder = PROJECT_DIR / folder_name
    folder.mkdir(exist_ok=True)
    files = sorted(
        (p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in extensions),
        key=lambda p: p.name.lower()
    )
    captions = data.get(captions_key, [])
    items = []
    for index in range(5):
        if index < len(files):
            path = files[index]
            mime = mimetypes.guess_type(path.name)[0] or (
                "video/mp4" if folder_name == "videos" else "image/jpeg"
            )
            encoded = base64.b64encode(path.read_bytes()).decode("ascii")
            caption = captions[index].strip() if index < len(captions) and isinstance(captions[index], str) else ""
            if not caption:
                caption = path.stem.replace("_", " ").replace("-", " ")
            items.append({
                "data": f"data:{mime};base64,{encoded}",
                "caption": caption,
                "filename": path.name
            })
        else:
            items.append({"data": "", "caption": "", "filename": ""})
    return items

photo_items = load_local_media(
    "photos", {".jpg", ".jpeg", ".png", ".webp"}, "photo_captions"
)
video_items = load_local_media(
    "videos", {".mp4", ".webm", ".mov"}, "video_captions"
)

def js_string(value):
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")

html = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:ital,wght@0,500;0,600;1,500;1,600&display=swap" rel="stylesheet">
<style>
:root{--gold:#c49a43;--deep:#98702b;--ink:#66502b;--muted:#9b855d;--white:#fffdf6}
*{box-sizing:border-box}
html,body{margin:0;width:100%;min-height:100%;font-family:'DM Sans',sans-serif;color:var(--ink)}
body{overflow:hidden;background:linear-gradient(155deg,#fffef8 0%,#fff9e9 48%,#f5e7bd 100%)}
#app{height:100vh;min-height:570px;position:relative;overflow:hidden;background:
radial-gradient(ellipse at 20% 75%,rgba(236,207,135,.30),transparent 38%),
radial-gradient(ellipse at 80% 25%,rgba(255,246,211,.72),transparent 35%),
linear-gradient(160deg,#fffef8 0%,#fff9e9 42%,#f3e3b5 100%)}
.scene{position:absolute;inset:0;display:none;align-items:center;justify-content:center;text-align:center;padding:28px 18px 54px;opacity:0;transform:translateY(10px);transition:opacity .5s ease,transform .5s ease;overflow-y:auto}
.scene.active{display:flex;opacity:1;transform:translateY(0)}
.inner{width:min(780px,100%);position:relative;margin:auto}
.script{font-family:'Playfair Display',serif;font-style:italic;font-weight:500;color:#70582e}
h1{font:italic 500 clamp(2.35rem,5.6vw,3.65rem)/1.16 'Playfair Display',serif;margin:0 0 5px;color:#725729}
h2{font:italic 500 clamp(1.55rem,3.5vw,2.05rem)/1.3 'Playfair Display',serif;color:#94702f;margin:0 0 22px}
p{font-size:1.02rem;line-height:1.8}
button{font-family:'DM Sans',sans-serif;cursor:pointer}
.primary{border:0;background:var(--gold);color:#fff;border-radius:9px;padding:14px 30px;min-width:112px;font-size:1rem;box-shadow:0 5px 13px #c49a432b;transition:transform .2s,background .2s}
.primary:hover{background:#ae8334;transform:translateY(-2px)}
.secondary{border:1px solid #e5d9b8;background:#fffdf5;color:#725d37;border-radius:9px;padding:13px 28px;font-size:1rem}
.hearts{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.heart{position:absolute;color:#d6b76f;opacity:.55;font-size:16px;animation:drift 7s ease-in-out infinite}
.heart:nth-child(1){left:10%;top:18%;font-size:13px;animation-delay:-2s}.heart:nth-child(2){left:24%;top:32%;font-size:19px;animation-delay:-4s}.heart:nth-child(3){right:16%;top:20%;font-size:15px;animation-delay:-1s}.heart:nth-child(4){right:25%;top:43%;font-size:11px;animation-delay:-3s}.heart:nth-child(5){left:17%;bottom:22%;font-size:20px;animation-delay:-5s}.heart:nth-child(6){right:11%;bottom:24%;font-size:17px;animation-delay:-2s}.heart:nth-child(7){left:40%;top:12%;font-size:12px;animation-delay:-1s}.heart:nth-child(8){right:40%;bottom:13%;font-size:14px;animation-delay:-4s}
@keyframes drift{0%,100%{transform:translateY(0) rotate(-8deg)}50%{transform:translateY(-13px) rotate(8deg)}}
.birthday-art{position:relative;width:180px;height:160px;margin:8px auto 14px;display:flex;align-items:center;justify-content:center}
.birthday-art .bear{font-size:77px;filter:drop-shadow(0 4px 2px #00000010)}
.birthday-art .cake-mini{position:absolute;font-size:40px;bottom:7px;left:calc(50% - 21px)}
.bunting{font-size:20px;letter-spacing:3px;color:#b58b3b;margin-bottom:-8px}
.question{font:500 clamp(1.25rem,2.5vw,1.55rem) 'Playfair Display',serif;margin:20px 0 34px;color:#70552c;line-height:1.5}
.choice-row{display:flex;gap:18px;justify-content:center;flex-wrap:wrap;margin-top:22px}
#noBtn{position:relative;z-index:5;touch-action:none;user-select:none;-webkit-user-select:none;transition:transform .045s linear}
.balloons{display:grid;grid-template-columns:repeat(2,100px);column-gap:105px;row-gap:62px;justify-content:center;align-items:center;margin:42px auto 32px;width:max-content;padding:10px 20px 36px}
.balloon{width:68px;height:86px;border:0;border-radius:50% 50% 47% 47%;color:#fff;font-size:1rem;position:relative;box-shadow:inset -7px -7px 0 #0000000d,inset 7px 7px 0 #ffffff35;animation:float 2.6s ease-in-out infinite}
.balloon:after{content:"";position:absolute;left:50%;bottom:-11px;transform:translateX(-50%);border-left:5px solid transparent;border-right:5px solid transparent;border-top:9px solid currentColor;filter:brightness(.9)}
.balloon:before{content:"";position:absolute;left:50%;bottom:-33px;width:1px;height:23px;background:#b8a98c}
.balloon.popped{animation:pop .25s forwards;pointer-events:none}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes pop{to{transform:scale(1.7);opacity:0}}
.balloon-note{min-height:38px;margin:22px auto 0;font:italic 1.25rem 'Playfair Display',serif;color:#927035}
.cake{font-size:112px;line-height:1.4;filter:drop-shadow(0 8px 7px #ad8b481c);animation:float 3s ease-in-out infinite}
.cake-sub{font:italic 1rem 'Playfair Display',serif;color:#92713b;margin:0 0 24px}
.envelope{width:180px;height:116px;position:relative;margin:28px auto 24px;background:#ead9a9;border-radius:5px;box-shadow:0 13px 28px #a98a4b24;cursor:pointer;transition:transform .25s}
.envelope:hover{transform:translateY(-5px)}
.envelope:before{content:"";position:absolute;inset:0;background:#f6ebc9;clip-path:polygon(0 0,50% 57%,100% 0);border-radius:5px 5px 0 0}
.envelope:after{content:"";position:absolute;inset:0;background:#dfc68d;clip-path:polygon(0 100%,0 0,50% 55%,100% 0,100% 100%)}
.seal{position:absolute;z-index:2;left:calc(50% - 13px);top:50%;font-size:23px;transform:translateY(-15%);color:#a57a2d}
.letter-card{width:min(420px,94%);min-height:220px;background:#fffdf6;border:1px solid #e9dfc4;border-radius:5px;box-shadow:0 12px 30px #9f844326;margin:0 auto;padding:22px 23px;text-align:left;position:relative;animation:letterIn .65s ease both}
@keyframes letterIn{from{opacity:0;transform:translateY(20px) scale(.97)}to{opacity:1;transform:translateY(0) scale(1)}}
.letter-heart{position:absolute;right:12px;top:12px;background:#b78b3d;color:#fff;border-radius:50%;width:23px;height:23px;display:grid;place-items:center;font-size:12px}
.letter-card p{font:italic .9rem/1.8 'Playfair Display',serif;color:#6e6049;white-space:pre-line;margin:0}
.tiny-photo{position:absolute;right:12px;bottom:9px;font-size:19px}
.quiz-card{width:min(650px,94%);margin:0 auto;background:#fffdf0d9;border:1px solid #e9dfc4;border-radius:22px;padding:38px 34px;box-shadow:0 14px 36px #9f844320}
.quiz-number{font-size:.88rem;letter-spacing:.14em;text-transform:uppercase;color:#a3874f;margin-bottom:18px}
.quiz-question{font:500 clamp(1.6rem,3vw,2.1rem)/1.4 'Playfair Display',serif;color:#6d562e;margin-bottom:35px}
.quiz-options{display:flex;flex-direction:column;gap:20px;max-width:430px;margin:0 auto}
.quiz-option{border:1px solid #e6d9b8;background:#fffdf8;border-radius:13px;padding:16px 20px;font-size:1.12rem;color:#725d37;text-align:left;transition:.2s}
.quiz-option:hover{background:#fbf0d2;border-color:#c9a85f;transform:translateY(-2px)}
.quiz-feedback{min-height:32px;margin-top:22px;font-size:1.05rem;color:#98702b}
.memory-card{width:min(680px,94%);margin:0 auto;background:#fffdf0dc;border:1px solid #e9dfc4;border-radius:22px;padding:30px 28px;box-shadow:0 14px 36px #9f844320}
.slide-media{display:block;width:min(520px,100%);max-height:48vh;object-fit:contain;margin:10px auto 20px;border-radius:16px;background:#f2ead7;box-shadow:0 10px 28px #9f844320}
.slide-video{object-fit:contain}
.media-placeholder{width:min(520px,100%);height:260px;margin:10px auto 20px;border:2px dashed #d6c18c;border-radius:16px;background:#fff9e9;display:grid;place-items:center;color:#9b855d;padding:20px}
.memory-title{font:italic 500 clamp(1.65rem,3.5vw,2.3rem)/1.35 'Playfair Display',serif;color:#725729;margin:0 0 18px}
.memory-copy{font-size:1.08rem;line-height:1.8;color:#806d4b;max-width:560px;margin:0 auto 24px;white-space:pre-wrap}
.tiny{font-size:.9rem;color:#9b855d}
#back{position:absolute;top:18px;left:20px;border:0;background:transparent;color:#92713b;font-size:.85rem;display:none;z-index:10}
#back.show{display:block}
@media(max-width:620px){#app{min-height:540px}.scene{padding:48px 14px 40px}.balloons{grid-template-columns:repeat(2,72px);column-gap:65px;row-gap:48px;margin:32px auto 25px}.balloon{width:58px;height:74px}.quiz-card,.memory-card{padding:25px 17px}.quiz-question{margin-bottom:25px}.quiz-options{gap:14px}.quiz-option{font-size:1rem;padding:14px 16px}.slide-media{max-height:40vh}.media-placeholder{height:210px}}
</style>
</head>
<body>
<div id="app">
  <div class="hearts"><span class="heart">♥</span><span class="heart">♥</span><span class="heart">♥</span><span class="heart">♥</span><span class="heart">♥</span><span class="heart">♥</span><span class="heart">♥</span><span class="heart">♥</span></div>
  <button id="back" onclick="previous()">‹ Back</button>

  <section class="scene active" id="s0">
    <div class="inner">
      <h1>Happy Birthday,<br><span id="friendTitle">Srinivas</span></h1>
      <div class="bunting">✦ △ ▽ △ ▽ ✦</div>
      <div class="birthday-art"><span class="bear">🐻‍❄️</span><span class="cake-mini">🎂</span></div>
      <p class="question">Baaga excitement feel avthunnava?</p>
      <div class="choice-row">
        <button class="primary" onclick="showScene(1)">Yes</button>
        <button class="secondary" id="noBtn">No</button>
      </div>
    </div>
  </section>

  <div id="quizSlides"></div>

  <section class="scene" id="balloonScene">
    <div class="inner">
      <h2>Anni Budagalni pagalakottu</h2>
      <div class="balloon-note" id="balloonWords"></div>
      <div class="balloons" id="balloons"></div>
      <p class="tiny" id="balloonHint">Nee msg chudalani unte anni budagalni pagalakottu.</p>
      <div class="continue-wrap" id="balloonContinue" style="visibility:hidden"><button class="primary" onclick="next()">Continue →</button></div>
    </div>
  </section>

  <section class="scene" id="cakeScene">
    <div class="inner">
      <h2>Oka Chinna Bday Wish!!</h2>
      <div class="cake">🎂</div>
      <p class="cake-sub">Oka Chinna Korika Koruko! Peddadi ante nen wish purthicheyyalenu.</p>
      <button class="primary" onclick="next()">Nokki Saav →</button>
    </div>
  </section>

  <div id="photoSlides"></div>
  <div id="videoSlides"></div>

  <section class="scene" id="letterScene">
    <div class="inner">
      <h2>Oka Chinna Uttaram Neekosam!</h2>
      <div id="envelopeWrap" onclick="openLetter()">
        <div class="envelope"><span class="seal">♥</span></div>
        <p class="tiny">Ala kallappaginchi chudakunda, Uttaram Cover meeda nokku</p>
      </div>
      <div id="letterWrap" style="display:none">
        <div class="letter-card"><span class="letter-heart">♥</span><p id="letterText"></p><span class="tiny-photo">✨</span></div>
        <div class="continue-wrap"><button class="primary" onclick="next()">Continue →</button></div>
      </div>
    </div>
  </section>

  <section class="scene" id="finalScene">
    <div class="inner">
      <div class="letter-card" style="width:min(190px,80%);min-height:145px;text-align:center;padding:20px 12px;margin-bottom:16px;">
        <div style="font-size:3.3rem;line-height:1.3;">🐰 🧸</div>
        <div style="color:#a77c32;letter-spacing:.16em;font-size:.8rem;">♡ LOVE ♡</div>
      </div>
      <h2>Chaala Santhosham neekosam</h2>
      <p class="cake-sub" id="finalSignature">With love, your best friend</p>
      <button class="primary" onclick="replay()">↻ Replay</button>
      <p id="finalConfetti" style="font-size:1.5rem;min-height:30px"></p>
    </div>
  </section>
</div>
<script>
const DATA = __DATA__;
let current=0;
const sceneList=()=>Array.from(document.querySelectorAll('.scene'));
function showScene(n){
 const scenes=sceneList();
 scenes.forEach((s,i)=>{s.classList.remove('active');s.style.display=(i===n?'flex':'none');});
 current=Math.max(0,Math.min(n,scenes.length-1));
 requestAnimationFrame(()=>scenes[current].classList.add('active'));
 document.getElementById('back').classList.toggle('show',current>0);
}
function next(){showScene(Math.min(sceneList().length-1,current+1));}
function previous(){showScene(Math.max(0,current-1));}
function buildQuiz(){
 const host=document.getElementById('quizSlides');
 (DATA.questions||[]).forEach((q,i)=>{
  const section=document.createElement('section');section.className='scene';
  section.innerHTML='<div class="inner"><div class="quiz-card"><div class="quiz-number"></div><div class="quiz-question"></div><div class="quiz-options"></div><div class="quiz-feedback" aria-live="polite"></div></div></div>';
  section.querySelector('.quiz-number').textContent=`Question ${i+1} of ${DATA.questions.length}`;
  section.querySelector('.quiz-question').textContent=q.question||'';
  const options=section.querySelector('.quiz-options');
  (q.options||[]).forEach((option,j)=>{
   const button=document.createElement('button');button.className='quiz-option';button.textContent=option;
   button.addEventListener('click',()=>{
    const feedback=section.querySelector('.quiz-feedback');
    if(j===Number(q.correct_index)){feedback.textContent='That’s right! ♡';setTimeout(()=>showScene(current+1),650);}
    else{feedback.textContent='Not quite — try another answer!';}
   });
   options.appendChild(button);
  });
  host.appendChild(section);
 });
}
function makeMemorySlide(host, item, index, type){
 const section=document.createElement('section');section.className='scene';
 const inner=document.createElement('div');inner.className='inner';
 const card=document.createElement('div');card.className='memory-card';
 const number=document.createElement('div');number.className='quiz-number';
 number.textContent=(type==='photo'?'PHOTO MEMORY ':'VIDEO MEMORY ')+(index+1)+' OF 5';
 const title=document.createElement('h2');title.className='memory-title';
 title.textContent=type==='photo'?'A photo to remember':'A moment in motion';
 card.appendChild(number);card.appendChild(title);
 if(item && item.data){
  const media=document.createElement(type==='photo'?'img':'video');
  media.className='slide-media'+(type==='video'?' slide-video':'');
  media.src=item.data;
  if(type==='photo'){media.alt='Photo memory '+(index+1);}
  else{
   // Autoplay silently so browsers allow playback; loop continuously with no visible controls.
   media.autoplay=true;
   media.loop=true;
   media.muted=true;
   media.controls=false;
   media.playsInline=true;
   media.preload='auto';
   media.setAttribute('webkit-playsinline','');
   media.addEventListener('canplay',()=>{const playAttempt=media.play();if(playAttempt&&playAttempt.catch)playAttempt.catch(()=>{});});
   card.appendChild(media);
   const playAttempt=media.play();if(playAttempt&&playAttempt.catch)playAttempt.catch(()=>{});
  }
  if(type==='photo')card.appendChild(media);
 }else{
  const placeholder=document.createElement('div');placeholder.className='media-placeholder';
  placeholder.textContent=type==='photo'?'Photo '+(index+1)+' will appear here when added to the project folder':'Video '+(index+1)+' will appear here when added to the project folder';
  card.appendChild(placeholder);
 }
 const copy=document.createElement('p');copy.className='memory-copy';
 copy.textContent=(item && item.caption) || (type==='photo'?'Write what this memory is about in the photo caption box above.':'Add an optional description in the video caption box above.');
 card.appendChild(copy);
 const btn=document.createElement('button');btn.className='primary';btn.textContent=index===4?(type==='photo'?'Next: Videos →':'Continue →'):'Next →';
 btn.addEventListener('click',()=>next());card.appendChild(btn);
 inner.appendChild(card);section.appendChild(inner);host.appendChild(section);
}
function buildFiveSlides(){
 const photoHost=document.getElementById('photoSlides');
 const videoHost=document.getElementById('videoSlides');
 (DATA.photo_items||[]).forEach((item,i)=>makeMemorySlide(photoHost,item,i,'photo'));
 (DATA.video_items||[]).forEach((item,i)=>makeMemorySlide(videoHost,item,i,'video'));
}
buildQuiz();
buildFiveSlides();

function dodge(e){
 if(e&&e.cancelable)e.preventDefault();
 const b=document.getElementById('noBtn'),parent=b.parentElement;
 const p=parent.getBoundingClientRect(),r=b.getBoundingClientRect();
 const maxX=Math.max(0,(p.width-r.width)/2-8),maxY=65;
 let dx=(Math.random()>.5?1:-1)*(55+Math.random()*90);
 let dy=(Math.random()>.5?1:-1)*(25+Math.random()*45);
 if(e&&typeof e.clientX==='number'){dx=(r.left+r.width/2-e.clientX)>=0?Math.abs(dx):-Math.abs(dx);}
 dx=Math.max(-maxX,Math.min(maxX,dx));dy=Math.max(-maxY,Math.min(maxY,dy));
 b.style.transform=`translate(${dx}px,${dy}px)`;
}
const noButton=document.getElementById('noBtn');
noButton.addEventListener('pointerenter',dodge);
noButton.addEventListener('pointermove',dodge);
noButton.addEventListener('pointerdown',dodge);
noButton.addEventListener('touchstart',dodge,{passive:false});
noButton.addEventListener('click',e=>{e.preventDefault();dodge(e);});

document.getElementById('friendTitle').textContent=DATA.name||'Your Best Friend';
document.getElementById('finalSignature').textContent='With love, '+(DATA.sender||'your best friend');
const balloonWords=DATA.balloon_words||['You','are','so','loved'];
let popped=0;
function createBalloons(){
 const host=document.getElementById('balloons');host.innerHTML='';popped=0;
 document.getElementById('balloonWords').innerHTML='';
 document.getElementById('balloonHint').textContent='Tap each balloon to reveal your message.';
 document.getElementById('balloonContinue').style.visibility='hidden';
 balloonWords.slice(0,4).forEach((word,i)=>{
  const b=document.createElement('button');b.className='balloon';b.textContent='♡';
  b.style.background=['#b8d5c2','#c9c0df','#e8cf91','#d9b36b'][i];
  b.style.color=['#729b7f','#9384b6','#b18d43','#a98237'][i];
  b.style.animationDelay=(i*.25)+'s';
  b.addEventListener('click',()=>{
   if(b.classList.contains('popped'))return;
   b.classList.add('popped');b.textContent='';popped++;
   const revealed=document.createElement('span');revealed.textContent=word;revealed.style.margin='0 7px';
   document.getElementById('balloonWords').appendChild(revealed);
   if(popped===4){document.getElementById('balloonHint').textContent='You are so loved. ♡';document.getElementById('balloonContinue').style.visibility='visible';}
  });
  host.appendChild(b);
 });
}
createBalloons();
document.getElementById('letterText').textContent=(DATA.letter_greeting||'Dear You,')+'\n\n'+(DATA.letter_text||'Happy Birthday!')+'\n\n'+(DATA.letter_signoff||'Your best friend');
function openLetter(){document.getElementById('envelopeWrap').style.display='none';document.getElementById('letterWrap').style.display='block';}
function replay(){
 document.getElementById('letterWrap').style.display='none';
 document.getElementById('envelopeWrap').style.display='block';
 createBalloons();showScene(0);
}
</script>
</body>
</html>
"""

data["photo_items"] = photo_items
data["video_items"] = video_items
html = html.replace("__DATA__", js_string(data))
components.html(html, height=780, scrolling=False)
