// story.js의 이야기 대사로 녹음 대본(voice/script.txt)을 만들어요.  사용: node tools/voice-script.js
const fs=require('fs'), path=require('path');
const src=fs.readFileSync(path.join(__dirname,'..','story.js'),'utf8');
const body=src.slice(src.indexOf('const START='),src.indexOf('\n};\n',src.indexOf('const STORIES='))+3);
const STORIES=new Function(body+';return STORIES;')();
const clean=t=>t.replace(/<[^>]+>/g,'').replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}]/gu,'').replace(/\s+/g,' ').trim();
let out=`체스 첫걸음 — 녹음 대본\n\n`+
`· 장면마다 녹음 파일 하나씩. 파일 이름은 [ ] 안의 이름 그대로 (예: intro-01.m4a)\n`+
`· 다 녹음하면 chess-trainer/voice/ 폴더에 넣으면 이야기에서 자동으로 재생돼요\n\n`;
let n=0;
for(const [id,st] of Object.entries(STORIES)){
  out+=`━━━━━━━━━━━━━━━━━━━━\n${clean(st.title)}\n━━━━━━━━━━━━━━━━━━━━\n\n`;
  st.scenes.forEach((sc,i)=>{ n++;
    out+=`[${id}-${String(i+1).padStart(2,'0')}]\n${clean(sc.say)}\n`;
    if(sc.card&&sc.card.items) out+=sc.card.items.map(([,t,d])=>`  · ${clean(t)}: ${clean(d)}`).join('\n')+'\n';
    out+='\n'; });
}
fs.writeFileSync(path.join(__dirname,'..','voice','script.txt'),out);
console.log('scenes',n);
