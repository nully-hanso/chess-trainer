// story.js의 이야기 대사로 녹음 대본(voice/script.txt)을 만들고,
// voice/ 폴더에 있는 녹음 파일(*.m4a) 목록을 voice/index.json에 적어요(앱은 목록에 있는 파일만 재생해요).
// 사용: node tools/voice-script.js   ← 녹음 파일을 넣거나 뺄 때마다 다시 실행
const fs=require('fs'), path=require('path');
const src=fs.readFileSync(path.join(__dirname,'..','story.js'),'utf8');
const body=src.slice(src.indexOf('const START='),src.indexOf('\n};\n',src.indexOf('const STORIES='))+3);
const STORIES=new Function(body+';return STORIES;')();
const clean=t=>t.replace(/<[^>]+>/g,'').replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}]/gu,'').replace(/\s+/g,' ').trim();
let out=`체스 첫걸음 — 녹음 대본\n\n`+
`· 장면마다 녹음 파일 하나씩. 파일 이름은 [ ] 안의 이름 그대로 (예: intro-01.m4a)\n`+
`· 녹음 파일을 chess-trainer/voice/ 폴더에 넣고 node tools/voice-script.js 를 한 번 실행하면 이야기에서 재생돼요\n\n`;
let n=0;
for(const [id,st] of Object.entries(STORIES)){
  out+=`━━━━━━━━━━━━━━━━━━━━\n${clean(st.title)}\n━━━━━━━━━━━━━━━━━━━━\n\n`;
  st.scenes.forEach((sc,i)=>{ n++;
    out+=`[${id}-${String(i+1).padStart(2,'0')}]\n${clean(sc.say)}\n`;
    if(sc.card&&sc.card.items) out+=sc.card.items.map(([,t,d])=>`  · ${clean(t)}: ${clean(d)}`).join('\n')+'\n';
    out+='\n'; });
}
fs.writeFileSync(path.join(__dirname,'..','voice','script.txt'),out);
const VD=path.join(__dirname,'..','voice');
const rec=fs.readdirSync(VD).filter(f=>f.endsWith('.m4a')).map(f=>f.slice(0,-4)).sort();
fs.writeFileSync(path.join(VD,'index.json'),JSON.stringify(rec)+'\n');
console.log('scenes',n,'· 녹음',rec.length);
