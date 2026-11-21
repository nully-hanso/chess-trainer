// =====================================================================
// 이야기 플레이어: 실습 전에 짧은 모션그래픽으로 설명해요 (GSAP 타임라인)
// 장면(scene) = 말(say) + 무대(stage: 체스판 fen 또는 카드 card) + 동작(act) 목록
// 동작: ['mv','e2e4'] 이동/잡기/승진('e7e8q') · ['ar','a1','a8','bad'] 화살표 · ['hl',['e4'],'good|bad|path'] 칸 강조
//       ['dots','d4'] 갈 수 있는 칸 · ['add','e4','wq'] 등장 · ['del','e4'] 사라짐 · ['shake','e8'] 흔들기
//       ['txt','e4','체크!','bad'] 말풍선 · ['wait',0.6] · ['clear'] 화살표·강조 지우기
// 모션 원칙(motion-design 스킬): 아이용 Playful — 짧고(0.25~0.45s) 통통 튀며 멈추는 이징, 한 번에 하나씩 순서대로
// =====================================================================
(function(){
const SQ=sq=>{ const i=sqIdx(sq); return {i,f:i&7,r:i>>3}; };
const IMG=code=>`url(pieces/${code}.svg)`;
const codeOf=p=>(isW(p)?'w':'b')+p.toLowerCase();
const clean=t=>t.replace(/<[^>]+>/g,'').replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}]/gu,'').replace(/\s+/g,' ').trim();

// ---------------- 이야기 내용 ----------------
const START='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1';
const STORIES={
intro:{title:'🎬 체스 이야기',scenes:[
  {say:'체스는 <b>두 나라 군대</b>가 겨루는 놀이예요. 백 군대와 흑 군대가 각각 <b>16개</b>의 기물로 시작해요.',fen:START,act:[['drop']]},
  {say:'목표는 단 하나! 상대 <b>킹</b>을 꼼짝 못 하게 가두는 것, 바로 <b>체크메이트</b>예요.',fen:'6k1/5ppp/8/8/8/8/8/R5K1 w - - 0 1',act:[['ar','a1','a8'],['mv','a1a8'],['shake','g8'],['txt','g8','체크메이트!','bad']]},
  {say:'킹이 공격받는 걸 <b>체크</b>라고 해요. 체크를 받으면 꼭 피해야 하고, 피할 방법이 하나도 없으면 게임이 끝나요.',card:{items:[['🏆','이기기','상대 킹을 체크메이트!'],['🤝','비기기','스테일메이트, 같은 자리가 세 번 등'],['🏳️','기권','더 못 하겠으면 “졌어요”']]}},
  {say:'체스는 약 <b>1500년 전 인도</b>의 “차투랑가”에서 시작됐어요. 코끼리·말·전차·보병, 네 부대가 싸우는 놀이였대요.',card:{items:[['🇮🇳','인도 · 약 1500년 전','차투랑가: 코끼리 · 말 · 전차 · 보병'],['🇮🇷','페르시아','샤트란지: “샤 마트(왕이 꼼짝 못 해)” → 체크메이트'],['🇪🇸','유럽 · 약 500년 전','퀸이 가장 강해지며 지금 규칙 완성'],['🌍','지금','전 세계 수억 명이 즐기는 게임']]}},
  {say:'판은 <b>오른쪽 아래 칸이 밝은 색</b>이 되게 놓아요. 퀸은 <b>자기 색 칸</b>에! 백 퀸은 밝은 칸, 흑 퀸은 어두운 칸이에요.',fen:START,act:[['hl',['h1'],'good'],['txt','h1','밝은 칸','good'],['hl',['d1','d8'],'path']]},
  {say:'<b>백이 먼저</b> 두고, 한 번씩 번갈아 둬요. 한 번에 기물 하나만 움직여요.',fen:START,act:[['mv','e2e4'],['wait',.3],['mv','e7e5'],['wait',.3],['mv','g1f3']]},
  {say:'체스 선수들의 약속도 있어요.',card:{items:[['🤝','악수','시작할 때와 끝날 때 “잘 부탁해 / 잘 뒀어”'],['✋','손대면 움직이기','손댄 기물은 꼭 그 기물로 둬요'],['🤫','조용히','상대가 생각할 때는 방해하지 않아요'],['😊','멋진 마음','이기면 겸손하게, 지면 박수!']]}},
  {say:'이제 기물 하나하나를 만나러 가 볼까요? 레슨에서 기물마다 이야기가 기다려요!',card:{pieces:['wk','wq','wr','wb','wn','wp']}}]},

rook:{title:'🎬 룩 이야기',scenes:[
  {say:'룩은 <b>성의 탑</b>처럼 생겼어요. 이름은 페르시아 말 “루흐(전차)”에서 왔어요.',card:{big:'wr',items:[['🏰','모양','성벽 위 뾰족뾰족한 탑'],['💰','가치','5점']]}},
  {say:'룩은 <b>가로·세로로 쭉!</b> 길만 비어 있으면 몇 칸이든 가요.',fen:'8/8/8/8/3R4/8/8/8 w - - 0 1',act:[['dots','d4']]},
  {say:'길이 막히면 멈춰요. <b>상대 기물</b>이면 그 칸으로 가서 잡을 수 있지만, <b>내 기물</b>은 뛰어넘을 수 없어요.',fen:'8/8/8/3p4/3R1P2/8/8/8 w - - 0 1',act:[['dots','d4'],['wait',.4],['mv','d4d5'],['txt','d5','+1','good']]},
  {say:'처음엔 구석에 숨어 있다가 길이 열리는 <b>게임 후반</b>에 큰 힘을 내요. 킹과 함께 <b>캐슬링</b>도 해요.',fen:'4k3/8/8/8/8/8/8/R3K2R w KQ - 0 1',act:[['mv','e1g1'],['mv','h1f1']]}]},

bishop:{title:'🎬 비숍 이야기',scenes:[
  {say:'비숍은 원래 <b>코끼리</b>였어요! 인도와 페르시아에서는 코끼리 부대였고, 유럽에서 교회의 <b>주교(비숍)</b>가 됐어요. 머리의 홈은 주교 모자 모양이에요.',card:{big:'wb',items:[['🐘','처음엔','코끼리 부대'],['⛪','지금은','주교 모자'],['💰','가치','3점']]}},
  {say:'비숍은 <b>대각선으로 쭉!</b>',fen:'8/8/8/8/3B4/8/8/8 w - - 0 1',act:[['dots','d4']]},
  {say:'그래서 처음 칸 색을 <b>절대 벗어나지 못해요</b>. 밝은 칸 비숍, 어두운 칸 비숍이 하나씩 있어요.',fen:'8/8/8/8/8/8/8/2B2B2 w - - 0 1',act:[['dots','c1'],['wait',.5],['clear'],['dots','f1']]},
  {say:'두 비숍이 함께 있으면 판 전체를 노릴 수 있어서 <b>“비숍 쌍”</b>은 아주 든든해요.',fen:'8/8/8/8/3BB3/8/8/8 w - - 0 1',act:[['dots','d4'],['dots','e4']]}]},

queen:{title:'🎬 퀸 이야기',scenes:[
  {say:'퀸은 가장 강한 기물! 그런데 옛날 페르시아에서는 왕 옆의 <b>신하</b>로, 대각선 한 칸만 가는 약한 기물이었어요.',card:{big:'wq',items:[['🧓','옛날엔','왕의 신하 “피르즈” · 대각선 한 칸'],['👑','약 500년 전','유럽에서 가장 강한 기물로 변신'],['💰','가치','9점']]}},
  {say:'<b>룩 + 비숍 = 퀸</b>. 가로·세로·대각선, 어디든 쭉!',fen:'8/8/8/8/3Q4/8/8/8 w - - 0 1',act:[['dots','d4']]},
  {say:'너무 소중해서 처음부터 혼자 나가면 쫓겨 다니기 쉬워요. <b>나이트·비숍</b>을 먼저 꺼내고 퀸은 나중에!',fen:'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w - - 0 1',act:[['mv','d1h5'],['wait',.3],['mv','g8f6'],['ar','f6','h5','bad'],['txt','h5','쫓겨요!','bad']]}]},

knight:{title:'🎬 나이트 이야기',scenes:[
  {say:'나이트는 <b>말을 탄 기사</b>예요. 인도의 기병 부대에서 시작해서 지금까지 모양이 거의 그대로예요.',card:{big:'wn',items:[['🐴','모양','말 머리'],['💰','가치','3점']]}},
  {say:'<b>“ㄱ”자</b>로 움직여요. 한 방향으로 두 칸 가고, 옆으로 한 칸!',fen:'8/8/8/8/3N4/8/8/8 w - - 0 1',act:[['hl',['d5','d6'],'path'],['ar','d4','e6'],['wait',.3],['clear'],['dots','d4']]},
  {say:'나이트만 할 수 있는 마법! 다른 기물을 <b>뛰어넘어요</b>.',fen:'8/8/8/2ppp3/2pNp3/2ppp3/8/8 w - - 0 1',act:[['mv','d4e6']]},
  {say:'한 번에 두 기물을 노리는 <b>포크</b>의 달인이에요. 나이트는 움직일 때마다 칸 색이 바뀌어요.',fen:'r3k3/8/8/1N6/8/8/8/4K3 w - - 0 1',act:[['mv','b5c7'],['ar','c7','e8','bad'],['ar','c7','a8','bad'],['txt','c7','포크!','good']]}]},

king:{title:'🎬 킹 이야기',scenes:[
  {say:'킹은 우리 군대의 <b>왕</b>이에요. 머리의 십자가가 왕관 표시! 가장 소중해서 점수를 매길 수 없어요.',card:{big:'wk',items:[['👑','모양','십자가가 달린 왕관'],['💎','가치','값을 매길 수 없음']]}},
  {say:'모든 방향으로 <b>딱 한 칸씩</b>.',fen:'8/8/8/8/4K3/8/8/8 w - - 0 1',act:[['dots','e4']]},
  {say:'잡히면 지니까 <b>공격받는 칸으로는 갈 수 없어요</b>. 빨간 줄은 흑 룩이 노리는 곳이에요.',fen:'8/8/8/8/8/8/r7/4K3 w - - 0 1',act:[['hl',['b2','c2','d2','e2','f2','g2','h2'],'bad'],['dots','e1']]},
  {say:'게임 후반에 기물이 줄어들면 킹도 <b>싸우러 나와요</b>. 아주 든든한 전사가 된답니다!',card:{pieces:['wk','wp','wp']}}]},

pawn:{title:'🎬 폰 이야기',scenes:[
  {say:'폰은 <b>걸어서 싸우는 병사</b>예요. 8명이 맨 앞줄에서 군대를 지켜요.',card:{big:'wp',items:[['🪖','모양','둥근 머리의 병사'],['💰','가치','1점 (하지만 꿈은 퀸!)']]}},
  {say:'앞으로 <b>한 칸</b>씩. 처음 자리에서만 <b>두 칸</b>도 갈 수 있어요. 뒤로는 못 가요.',fen:'8/8/8/8/8/8/4P3/8 w - - 0 1',act:[['dots','e2'],['wait',.3],['mv','e2e4']]},
  {say:'앞이 막히면 못 가요. 잡을 때만 <b>대각선 앞</b>으로!',fen:'8/8/8/3pp3/4P3/8/8/8 w - - 0 1',act:[['dots','e4'],['wait',.3],['mv','e4d5'],['txt','d5','+1','good']]},
  {say:'끝까지 가면 <b>퀸으로 변신!</b> 이걸 “승진”이라고 해요.',fen:'8/4P3/8/8/8/8/8/8 w - - 0 1',act:[['mv','e7e8q'],['txt','e8','승진!','good']]}]},

mates:{title:'🎬 체크메이트 vs 스테일메이트',scenes:[
  {say:'둘 다 <b>둘 수 있는 수가 하나도 없는</b> 상황이에요. 차이는 딱 하나! 지금 킹이 <b>공격받고 있나?</b>',card:{items:[['👑','체크메이트','체크 + 둘 곳 없음 → 이겨요!'],['🤝','스테일메이트','체크 아님 + 둘 곳 없음 → 비겨요']]}},
  {say:'흑 킹이 퀸에게 공격받고 있어요(체크). 퀸은 백 킹이 지켜서 잡을 수도 없고, 도망갈 칸도 모두 막혔어요.',fen:'k7/1Q6/1K6/8/8/8/8/8 b - - 0 1',act:[['ar','b7','a8','bad'],['shake','a8'],['hl',['a7','b8'],'bad'],['txt','a8','체크메이트!','bad']]},
  {say:'이번엔 킹이 공격받지 <b>않아요</b>. 그런데 갈 수 있는 칸이 모두 막혔고 다른 기물도 없어요. 둘 수가 없으니 <b>비김</b>!',fen:'k7/8/1Q6/2K5/8/8/8/8 b - - 0 1',act:[['hl',['a7','b7','b8'],'bad'],['txt','a8','스테일메이트','good']]},
  {say:'조심! 이긴 게임도 마무리를 잘못하면 비김이 돼요. 퀸을 c7로 두면… 흑은 체크가 아닌데 둘 곳이 없어요 😱',fen:'k7/8/1K6/8/8/8/8/2Q5 w - - 0 1',act:[['mv','c1c7'],['hl',['a7','b7','b8'],'bad'],['txt','a8','비김 😱','bad']]},
  {say:'정답은 <b>체크로 끝내기</b>! 퀸을 c8로 두면 체크이면서 도망갈 곳도 없어요. 체크메이트!',fen:'k7/8/1K6/8/8/8/8/2Q5 w - - 0 1',act:[['mv','c1c8'],['ar','c8','a8','bad'],['shake','a8'],['txt','a8','체크메이트!','good']]}]},

hanging:{title:'🎬 공짜 기물',scenes:[
  {say:'아무도 지키지 않는 기물은 <b>공짜</b>! 그냥 잡으면 이득이에요.',fen:'4k3/8/8/3n4/8/8/8/3QK3 w - - 0 1',act:[['ar','d1','d5'],['mv','d1d5'],['txt','d5','+3','good']]},
  {say:'하지만 지키는 기물이 있으면? 잡은 뒤 <b>되잡혀요</b>. 퀸(9)을 주고 나이트(3)를 얻으면 큰 손해!',fen:'4k3/8/4p3/3n4/8/8/8/3QK3 w - - 0 1',act:[['ar','e6','d5','bad'],['txt','d5','지켜져요!','bad']]},
  {say:'그래서 잡기 전에 꼭 물어봐요. <b>“잡으면 되잡히나?”</b>',card:{items:[['🔍','1. 찾기','공격할 수 있는 상대 기물'],['🛡️','2. 확인','그 기물을 누가 지키나?'],['⚖️','3. 계산','주는 점수 vs 얻는 점수']]}}]},
fork:{title:'🎬 포크',scenes:[
  {say:'<b>포크</b>는 한 기물이 <b>두 기물을 동시에</b> 공격하는 기술이에요. 상대는 하나밖에 못 구해요!',fen:'r3k3/8/8/1N6/8/8/8/4K3 w - - 0 1',act:[['mv','b5c7'],['ar','c7','e8','bad'],['ar','c7','a8','bad'],['txt','c7','포크!','good']]},
  {say:'킹은 꼭 피해야 하니까… 남은 룩을 잡아요!',fen:'r3k3/2N5/8/8/8/8/8/4K3 b - - 0 1',act:[['mv','e8d7'],['wait',.2],['mv','c7a8'],['txt','a8','+5','good']]},
  {say:'포크는 나이트가 제일 잘하지만 퀸·폰·킹도 할 수 있어요. 폰 포크도 아주 무서워요!',fen:'8/8/8/2n1b3/8/3P4/8/8 w - - 0 1',act:[['mv','d3d4'],['ar','d4','c5','bad'],['ar','d4','e5','bad'],['txt','d4','폰 포크!','good']]}]},
pin:{title:'🎬 핀',scenes:[
  {say:'<b>핀</b>은 기물을 “압정으로 꽂아” 못 움직이게 하는 기술이에요. 뒤에 더 소중한 기물이 숨어 있거든요.',fen:'4k3/8/8/3p4/4n3/8/5P2/4R1K1 w - - 0 1',act:[['ar','e1','e8','bad'],['hl',['e4'],'bad'],['txt','e4','못 움직여요!','bad']]},
  {say:'움직이지 못하는 기물은 <b>더 싼 기물로 공격</b>하면 끝! 폰으로 나이트를 노려요.',fen:'4k3/8/8/3p4/4n3/8/5P2/4R1K1 w - - 0 1',act:[['mv','f2f3'],['ar','f3','e4'],['txt','e4','도망 못 가요','bad']]}]},
skewer:{title:'🎬 스큐어',scenes:[
  {say:'<b>스큐어(꼬치)</b>는 핀의 반대예요. <b>앞에 있는 소중한 기물</b>을 공격해서, 비키면 뒤의 기물을 잡아요.',fen:'8/8/8/8/q3k3/8/8/6KR w - - 0 1',act:[['mv','h1h4'],['ar','h4','a4','bad'],['shake','e4'],['txt','e4','체크!','bad']]},
  {say:'킹이 피할 수밖에 없으니… 뒤에 숨은 퀸을 잡아요!',fen:'8/8/8/8/q3k2R/8/8/6K1 b - - 0 1',act:[['mv','e4d3'],['wait',.2],['mv','h4a4'],['txt','a4','+9','good']]}]},
disc:{title:'🎬 디스커버드 어택',scenes:[
  {say:'<b>디스커버드 어택</b>은 앞 기물이 비키면 <b>뒤에 숨은 기물의 공격이 “짠!”</b> 하고 드러나는 기술이에요.',fen:'7k/8/8/2q5/3N4/8/1B6/6K1 w - - 0 1',act:[['ar','b2','h8','path'],['txt','d4','비켜 줄게!','good']]},
  {say:'나이트가 비키면서 퀸을 공격! 동시에 비숍이 킹에게 체크! 공격이 두 개라 다 막을 수 없어요.',fen:'7k/8/8/2q5/3N4/8/1B6/6K1 w - - 0 1',act:[['mv','d4b3'],['ar','b2','h8','bad'],['ar','b3','c5','bad'],['shake','h8'],['txt','h8','체크!','bad']]},
  {say:'킹이 피하는 동안 퀸을 잡아요. 대성공!',fen:'7k/8/8/2q5/8/1N6/1B6/6K1 b - - 0 1',act:[['mv','h8h7'],['wait',.2],['mv','b3c5'],['txt','c5','+9','good']]}]},
};

// ---------------- 플레이어 ----------------
const S={id:null,i:0,tl:null,voice:LS.get('chess.voice',true)};
const el=document.createElement('div'); el.className='story'; el.id='story'; el.hidden=true;
el.innerHTML=`<div class="st-card" role="dialog" aria-modal="true">
  <div class="st-top"><span class="st-ttl" id="stTitle"></span><button class="st-ic" id="stVoice" hidden></button><button class="st-ic" id="stReplay" title="다시 보기">↻</button><button class="st-ic" id="stClose" title="닫기">✕</button></div>
  <div class="st-body"><div class="st-stage" id="stStage"></div>
    <div class="st-side"><div class="st-say" id="stSay"></div>
      <div class="st-nav"><button class="btn" id="stPrev">◀</button><div class="st-dots" id="stDots"></div><button class="btn primary" id="stNext">다음 ▶</button></div></div></div></div>`;
document.body.appendChild(el);
const $s=id=>document.getElementById(id);

// 목소리: 기계 음성(TTS)은 쓰지 않아요. 직접 녹음한 파일이 voice/<이야기>-<장면번호>.m4a 로 있으면 그것만 재생
// (예: voice/intro-01.m4a). 파일이 없으면 조용히 넘어가요. 녹음이 하나라도 재생되면 🔊 버튼이 나타나요.
let audio=null;
const stopAudio=()=>{ if(audio){ audio.pause(); audio=null; } };
function speak(i){
  stopAudio(); if(!S.voice) return;
  const a=new Audio(`voice/${S.id}-${String(i+1).padStart(2,'0')}.m4a`); audio=a;
  a.addEventListener('canplay',()=>{ $s('stVoice').hidden=false; },{once:true});
  a.play().catch(()=>{});
}
function voiceBtn(){ $s('stVoice').textContent=S.voice?'🔊':'🔇'; $s('stVoice').title=S.voice?'읽어 주기 끄기':'읽어 주기 켜기'; }

function buildBoard(stage,fen){
  const s=parseFEN(fen), wrap=document.createElement('div'); wrap.className='stb';
  for(let i=0;i<64;i++){ const q=document.createElement('div'); q.className='stq '+(((i>>3)+(i&7))%2?'d':'l'); wrap.appendChild(q); }
  const fx=document.createElement('div'); fx.className='stfx'; wrap.appendChild(fx);
  const svg=document.createElementNS('http://www.w3.org/2000/svg','svg'); svg.setAttribute('viewBox','0 0 8 8'); svg.setAttribute('class','starr'); wrap.appendChild(svg);
  const map={};
  s.b.forEach((p,i)=>{ if(p) map[i]=pieceEl(wrap,i,codeOf(p)); });
  stage.appendChild(wrap);
  return {wrap,fx,svg,map,b:s.b.slice(),fen};
}
function pos(i){ return {left:(i&7)*12.5+'%',top:(i>>3)*12.5+'%'}; }
function pieceEl(wrap,i,code){
  const d=document.createElement('div'); d.className='stp'; d.style.setProperty('--img',IMG(code));
  Object.assign(d.style,pos(i)); wrap.appendChild(d); return d;
}
function overlay(B,i,cls,html){ const d=document.createElement('div'); d.className=cls; Object.assign(d.style,pos(i)); if(html!=null) d.innerHTML=html; B.fx.appendChild(d); return d; }

function buildCard(stage,card){
  const w=document.createElement('div'); w.className='stc';
  let h='';
  if(card.big) h+=`<div class="stc-big" style="--img:${IMG(card.big)}"></div>`;
  if(card.pieces) h+=`<div class="stc-row">${card.pieces.map(c=>`<i style="--img:${IMG(c)}"></i>`).join('')}</div>`;
  if(card.items) h+=`<div class="stc-items">${card.items.map(([e,t,d])=>`<div class="stc-it"><span class="em">${e}</span><div><b>${t}</b><small>${d}</small></div></div>`).join('')}</div>`;
  w.innerHTML=h; stage.appendChild(w); return w;
}

function scene(i){
  const st=STORIES[S.id], sc=st.scenes[i]; S.i=i;
  if(S.tl) S.tl.kill();
  const stage=$s('stStage'); stage.innerHTML='';
  $s('stSay').innerHTML=sc.say;
  $s('stDots').innerHTML=st.scenes.map((_,k)=>`<i class="${k===i?'on':k<i?'past':''}"></i>`).join('');
  $s('stPrev').disabled=i===0;
  $s('stNext').textContent=i<st.scenes.length-1?'다음 ▶':(S.after||'실습하러 가기 ▶');
  const tl=gsap.timeline({defaults:{duration:.4,ease:'back.out(1.6)'},delay:.35}); S.tl=tl;
  tl.fromTo($s('stSay'),{opacity:0,y:10},{opacity:1,y:0,duration:.3,ease:'power2.out'},0);
  if(sc.card){
    const w=buildCard(stage,sc.card);
    const big=w.querySelector('.stc-big'), row=w.querySelectorAll('.stc-row i'), its=w.querySelectorAll('.stc-it');
    if(big){ tl.from(big,{scale:.3,opacity:0,y:30,duration:.55},0.1); tl.to(big,{y:-6,duration:1.4,ease:'sine.inOut',repeat:-1,yoyo:true},'>'); }
    if(row.length) tl.from(row,{y:40,opacity:0,stagger:.08},0.15);
    if(its.length) tl.from(its,{x:-24,opacity:0,stagger:.18,ease:'power2.out'},big?0.45:0.15);
  } else {
    const B=buildBoard(stage,sc.fen); let fx=[];
    for(const a of sc.act||[]) act(B,tl,a,fx);
  }
  if(RM()) tl.progress(1);
  speak(i);
}

function act(B,tl,a,fx){
  const [k,...x]=a;
  if(k==='drop'){
    const ps=Object.values(B.map); tl.from(ps,{y:-40,opacity:0,stagger:{each:.025,from:'center'},duration:.35},'+=0.1'); return;
  }
  if(k==='wait'){ tl.to({},{duration:x[0]}); return; }
  if(k==='mv'){
    const from=sqIdx(x[0].slice(0,2)), to=sqIdx(x[0].slice(2,4)), promo=x[0][4], el=B.map[from]; if(!el) return;
    const cap=B.map[to], p=B.b[from], knight=p&&p.toLowerCase()==='n', dist=Math.hypot((from&7)-(to&7),(from>>3)-(to>>3));
    const dur=Math.min(.75,.32+.07*dist);
    tl.set(el,{zIndex:5},'+=0.15');
    tl.to(el,{...pos(to),duration:dur,ease:'power2.inOut'},'>');
    tl.to(el,{scale:knight?1.25:1.1,duration:dur/2,yoyo:true,repeat:1,ease:'sine.inOut'},'<');
    if(cap){ tl.to(cap,{opacity:0,scale:.4,rotation:-25,duration:.3,ease:'power2.in'},`<${dur*.7}`); }
    tl.call(()=>{ if(typeof sfx==='function') sfx(cap?'cap':'move'); },null,`<${cap?.0:dur}`);
    if(promo){ const code=(isW(p)?'w':'b')+promo; tl.to(el,{scale:0,duration:.18,ease:'power2.in'}); tl.call(()=>el.style.setProperty('--img',IMG(code))); tl.to(el,{scale:1,duration:.4,ease:'back.out(2.5)'}); B.b[to]=isW(p)?promo.toUpperCase():promo; }
    else B.b[to]=p;
    B.b[from]=null; B.map[to]=el; delete B.map[from]; tl.set(el,{zIndex:''});
    return;
  }
  if(k==='dots'){
    const i=sqIdx(x[0]), p=B.b[i]; if(!p) return;
    const ms=legal({b:B.b,turn:isW(p)?'w':'b',castle:'',ep:-1}).filter(m=>m.from===i);
    const ds=ms.map(m=>overlay(B,m.to,B.b[m.to]?'stcap':'stdot')); fx.push(...ds);
    tl.from(ds,{scale:0,opacity:0,stagger:.035,duration:.3},'+=0.1'); return;
  }
  if(k==='hl'){
    const ds=x[0].map(s=>overlay(B,sqIdx(s),'sthl '+(x[1]||'good'))); fx.push(...ds);
    tl.from(ds,{scale:.5,opacity:0,stagger:.06,duration:.3},'+=0.1'); return;
  }
  if(k==='ar'){
    const a1=SQ(x[0]), b1=SQ(x[1]), col={bad:'#e2453c',path:'#f0a020',good:'#2fa968'}[x[2]||'good'];
    const x1=a1.f+.5,y1=a1.r+.5,x2=b1.f+.5,y2=b1.r+.5, len=Math.hypot(x2-x1,y2-y1), ux=(x2-x1)/len, uy=(y2-y1)/len;
    const ex=x2-ux*.32, ey=y2-uy*.32, ns='http://www.w3.org/2000/svg';
    const g=document.createElementNS(ns,'g'); g.setAttribute('opacity','.88');
    const ln=document.createElementNS(ns,'line'); Object.entries({x1,y1,x2:ex,y2:ey,stroke:col,'stroke-width':.16,'stroke-linecap':'round','stroke-dasharray':len,'stroke-dashoffset':len}).forEach(([k2,v])=>ln.setAttribute(k2,v));
    const hd=document.createElementNS(ns,'polygon'), px=-uy, py=ux;
    hd.setAttribute('points',`${x2},${y2} ${ex+px*.24},${ey+py*.24} ${ex-px*.24},${ey-py*.24}`); hd.setAttribute('fill',col); hd.setAttribute('opacity','0');
    g.append(ln,hd); B.svg.appendChild(g); fx.push(g);
    tl.to(ln,{attr:{'stroke-dashoffset':0},duration:.25+.08*len,ease:'power2.out'},'+=0.1').to(hd,{attr:{opacity:1},duration:.15},'>-0.05'); return;
  }
  if(k==='txt'){
    const d=overlay(B,sqIdx(x[0]),'sttxt '+(x[2]||'good'),`<span>${x[1]}</span>`); fx.push(d);
    tl.from(d.firstChild,{scale:0,y:10,duration:.45,ease:'back.out(2.4)'},'+=0.1'); return;
  }
  if(k==='shake'){ const e=B.map[sqIdx(x[0])]; if(e) tl.to(e,{rotation:10,duration:.07,repeat:5,yoyo:true,ease:'sine.inOut'},'+=0.1').set(e,{rotation:0}); return; }
  if(k==='add'){ const e=pieceEl(B.wrap,sqIdx(x[0]),x[1]); B.map[sqIdx(x[0])]=e; tl.from(e,{scale:0,opacity:0,duration:.4,ease:'back.out(2)'},'+=0.1'); return; }
  if(k==='del'){ const i=sqIdx(x[0]), e=B.map[i]; if(e){ tl.to(e,{scale:.3,opacity:0,duration:.3},'+=0.1'); delete B.map[i]; B.b[i]=null; } return; }
  if(k==='clear'){ const old=fx.splice(0); if(old.length) tl.to(old,{opacity:0,duration:.25},'+=0.1'); return; }
}

function open(id,opts={}){
  if(!STORIES[id]) return;
  S.id=id; S.after=opts.after||null; S.onClose=opts.onClose||null;
  $s('stTitle').textContent=STORIES[id].title; voiceBtn();
  el.hidden=false; document.body.classList.add('st-open');
  gsap.fromTo(el.querySelector('.st-card'),{scale:.92,opacity:0,y:20},{scale:1,opacity:1,y:0,duration:.35,ease:'back.out(1.4)'});
  const seen=store.get('stories',{}); seen[id]=true; store.set('stories',seen);
  scene(0);
}
function close(){
  if(S.tl) S.tl.kill(); stopAudio();
  el.hidden=true; document.body.classList.remove('st-open'); const f=S.onClose; S.onClose=null; refreshHooks(); if(f) f();
}
$s('stClose').onclick=close;
$s('stReplay').onclick=()=>scene(S.i);
$s('stPrev').onclick=()=>{ if(S.i>0) scene(S.i-1); };
$s('stNext').onclick=()=>{ const n=STORIES[S.id].scenes.length; if(S.i<n-1) scene(S.i+1); else { celebrate(12); close(); } };
$s('stVoice').onclick=()=>{ S.voice=!S.voice; LS.set('chess.voice',S.voice); voiceBtn(); if(S.voice) speak(S.i); else stopAudio(); };
el.addEventListener('click',e=>{ if(e.target===el) close(); });
addEventListener('keydown',e=>{ if(el.hidden) return; if(e.key==='Escape') close(); if(e.key==='ArrowRight') $s('stNext').click(); if(e.key==='ArrowLeft') $s('stPrev').click(); });
const seen=id=>!!store.get('stories',{})[id];
window.Story={open,seen,STORIES,clean};

// ---------------- 앱 곳곳에 연결 ----------------
// 1) 길잡이: 맨 위에 "체스 이야기" 카드
const roadCard=document.createElement('button'); roadCard.className='st-entry'; roadCard.id='stRoad';
roadCard.innerHTML='<span class="em">🎬</span><span><b>체스 이야기</b><small>게임의 목표 · 체스의 역사 · 선수들의 약속</small></span><span class="go">보기 ▶</span>';
roadCard.onclick=()=>open('intro');
document.getElementById('road').before(roadCard);

// 2) 레슨: 기물 이동·체크메이트 레슨은 처음 열 때 이야기를 먼저 보여 주고, 언제든 다시 볼 수 있게
const LESSON_STORY={rook:'rook',bishop:'bishop',queen:'queen',knight:'knight',king:'king',pawn:'pawn',mates:'mates'};
const _openLesson=window.openLesson;
window.openLesson=function(les){
  _openLesson(les);
  const sid=LESSON_STORY[les.id], box=document.getElementById('lIntro');
  let b=document.getElementById('stLes'); if(b) b.remove();
  if(!sid) return;
  b=document.createElement('button'); b.id='stLes'; b.className='btn small st-mini'; b.textContent='🎬 이야기 다시 보기';
  b.onclick=()=>open(sid); box.after(b);
  if(!seen(sid)) open(sid);
};

// 3) 퍼즐: 목표마다 설명 이야기(메이트 → 체크메이트 이야기, 기물 얻기 → 기술별 이야기)
const TAC_STORY=[['hanging','공짜 기물'],['fork','포크'],['pin','핀'],['skewer','스큐어'],['disc','디스커버드']];
let lastTac=null;
function refreshHooks(){
  const box=document.getElementById('pGoalTxt'); if(!box||typeof P==='undefined') return;
  let r=document.getElementById('stPz'); if(!r){ r=document.createElement('div'); r.id='stPz'; r.className='st-pzrow'; box.after(r); }
  if(P.goal==='m1'||P.goal==='m2') r.innerHTML=`<button class="btn small st-mini" data-s="mates">🎬 체크메이트 이야기${seen('mates')?'':' <i class="st-new">NEW</i>'}</button>`;
  else if(P.goal==='mat') r.innerHTML='🎬 '+TAC_STORY.map(([k,n])=>`<button class="btn small st-mini" data-s="${k}">${n}${seen(k)?'':' <i class="st-new">NEW</i>'}</button>`).join('');
  else r.innerHTML='';
  r.querySelectorAll('[data-s]').forEach(b=>b.onclick=()=>open(b.dataset.s));
  // 기술을 처음 골랐을 때는 그 기술 이야기부터
  if(P.goal==='mat'&&P.tac!==lastTac){ const t=P.tac; lastTac=t; if(t!=='all'&&!seen(t)&&el.hidden&&document.getElementById('v-puzzle').classList.contains('on')) open(t); }
}
const _render=P.render; P.render=()=>{ _render(); refreshHooks(); };
refreshHooks();

// 4) 처음 온 아이: 프로필 고르기 창이 없으면 바로 인트로 이야기
setTimeout(()=>{ if(!seen('intro')&&!document.getElementById('profModal').classList.contains('on')&&document.getElementById('v-road').classList.contains('on')) open('intro'); },600);
})();
