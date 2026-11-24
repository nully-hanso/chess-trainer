// 체스 엔진 검사: index.html의 엔진 부분만 꺼내서 표준 perft 국면 5개로 수 생성이 정확한지 확인해요.
// perft = 몇 수 뒤까지 둘 수 있는 모든 수의 개수. 캐슬링·앙파상·승진·핀이 하나라도 틀리면 숫자가 달라져요.
// 사용: node tools/test-engine.js        (전부 맞으면 끝에 "모두 통과", 아니면 종료 코드 1)
const fs = require('fs'), path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const a = html.indexOf('/*ENGINE*/'), b = html.indexOf('/*DATA*/');
if (a < 0 || b < a) { console.error('index.html에서 /*ENGINE*/ … /*DATA*/ 표시를 못 찾았어요'); process.exit(1); }
const E = new Function(html.slice(a, b) + '\nreturn {parseFEN,legal,make,inCheck,posKey,insufficient,botChoose,botScores,kpkProbe};')();

function perft(s, d) { if (d === 0) return 1; let n = 0; for (const m of E.legal(s)) n += perft(E.make(s, m), d - 1); return n; }
const PERFT = [
  ['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', [20, 400, 8902, 197281]],
  ['r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1', [48, 2039, 97862]],
  ['8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1', [14, 191, 2812, 43238]],
  ['r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1', [6, 264, 9467]],
  ['rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8', [44, 1486, 62379]],
];
let fail = 0;
const check = (ok, name, info = '') => { console.log((ok ? 'OK   ' : 'FAIL ') + name + (info ? '  ' + info : '')); if (!ok) fail++; };
for (const [fen, exp] of PERFT) {
  const s = E.parseFEN(fen), got = exp.map((_, i) => perft(s, i + 1));
  check(got.join() === exp.join(), 'perft ' + fen.split(' ')[0].slice(0, 24), got.join(',') + (got.join() === exp.join() ? '' : ' | 기대 ' + exp.join(',')));
}
// 무승부 규칙
const ins = f => E.insufficient(E.parseFEN(f + ' w - - 0 1'));
check(ins('8/8/4k3/8/8/3K4/8/8'), '킹 대 킹 → 기물 부족');
check(ins('8/8/4k3/8/8/3K4/5N2/8'), '킹+나이트 대 킹 → 기물 부족');
check(ins('8/8/4k3/2b5/8/3K4/5B2/8'), '같은 색 칸 비숍끼리 → 기물 부족');
check(!ins('8/8/4k3/3b4/8/3K4/5B2/8'), '다른 색 칸 비숍끼리 → 계속');
check(!ins('8/8/4k3/8/8/3K4/4NN2/8'), '나이트 둘 → 계속(메이트 가능한 자리가 있어요)');
check(!ins('8/8/4k3/8/8/3K4/4P3/8'), '폰이 있으면 → 계속');
// 같은 자리 판정: 잡을 수 없는 앙파상 칸은 무시
const k1 = E.posKey(E.parseFEN('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'));
const k2 = E.posKey(E.parseFEN('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1'));
check(k1 === k2, '잡을 수 없는 앙파상 칸은 같은 자리로 봐요');
const k3 = E.posKey(E.parseFEN('rnbqkbnr/ppp1pppp/8/8/3pP3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'));
const k4 = E.posKey(E.parseFEN('rnbqkbnr/ppp1pppp/8/8/3pP3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1'));
check(k3 !== k4, '앙파상을 할 수 있으면 다른 자리로 봐요');
// 봇: 1수 메이트를 놓치지 않아요
const m = E.botChoose(E.parseFEN('6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1'), 1600);
const after = E.make(E.parseFEN('6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1'), m);
check(E.legal(after).length === 0 && E.inCheck(after, 'b'), '봇이 1수 메이트(Ra8#)를 찾아요');
// 킹+폰 대 킹 정답표: 잘 알려진 결과
const kp = f => { const r = E.kpkProbe(E.parseFEN(f)); return r ? (r.win ? 'W' : 'D') : '-'; };
for (const [f, exp, name] of [
  ['4k3/8/4K3/4P3/8/8/8/8 w - - 0 1', 'W', '6번째 줄 킹이 폰 앞 (백 차례)'],
  ['4k3/8/4K3/4P3/8/8/8/8 b - - 0 1', 'W', '6번째 줄 킹이 폰 앞 (흑 차례)'],
  ['8/8/8/3k4/8/3K4/3P4/8 w - - 0 1', 'D', '마주 보기: 백 차례면 비김'],
  ['8/8/8/3k4/8/3K4/3P4/8 b - - 0 1', 'W', '마주 보기: 흑 차례면 백 승'],
  ['k7/8/1K6/P7/8/8/8/8 w - - 0 1', 'D', '가장자리 폰, 흑 킹이 구석'],
  ['8/8/8/8/4p3/4k3/8/4K3 b - - 0 1', 'W', '흑 폰도 뒤집어서 계산'],
]) check(kp(f) === exp, 'KPK ' + name, kp(f));
console.log(fail ? `\n${fail}개 실패` : '\n모두 통과');
process.exit(fail ? 1 : 0);
