# lichess 퍼즐 DB(CC0)에서 패턴별 문제를 골라 patterns.txt로 저장해요.
#   내려받기: https://database.lichess.org/lichess_db_puzzle.csv.zst (약 310MB, 저장소에는 넣지 않아요)
#   실행: python3 tools/patterns-pick.py <내려받은 .csv.zst> > patterns.txt   (zstandard 모듈 필요)
# 고르는 기준: 아이 수준(점수 400~1700), 많이 풀리고(300번 이상) 평가가 좋은(인기 85 이상) 문제,
# 메이트 패턴은 1수·2수 메이트만, 전술은 내 수 4개 이하. 점수 구간마다 고르게 뽑아서 쉬운 것부터 어려운 것까지.
import csv, io, sys, math
import zstandard

# (패턴 키, 퍼즐 태그, 메이트인가)
PATTERNS = [
    ('backRankMate', 1), ('smotheredMate', 1), ('hookMate', 1), ('anastasiaMate', 1), ('arabianMate', 1),
    ('cornerMate', 1), ('bodenMate', 1), ('doubleBishopMate', 1), ('dovetailMate', 1), ('epauletteMate', 1),
    ('hangingPiece', 0), ('fork', 0), ('pin', 0), ('skewer', 0), ('discoveredAttack', 0), ('doubleCheck', 0),
    ('trappedPiece', 0), ('capturingDefender', 0),
    ('deflection', 0), ('attraction', 0), ('intermezzo', 0), ('xRayAttack', 0), ('clearance', 0),
    ('interference', 0), ('quietMove', 0), ('defensiveMove', 0), ('underPromotion', 0),
    ('promotion', 0), ('pawnEndgame', 0), ('rookEndgame', 0),
]
PER = 36
BUCKETS = [(400, 700), (700, 900), (900, 1100), (1100, 1300), (1300, 1500), (1500, 1700)]
cand = {k: [] for k, _ in PATTERNS}
with open(sys.argv[1], 'rb') as fh:
    text = io.TextIOWrapper(zstandard.ZstdDecompressor().stream_reader(fh), encoding='utf-8')
    for row in csv.DictReader(text):
        r, rd, pop, plays = int(row['Rating']), int(row['RatingDeviation']), int(row['Popularity']), int(row['NbPlays'])
        if not (400 <= r < 1700) or rd > 90 or pop < 85 or plays < 300: continue
        th = set(row['Themes'].split()); mv = row['Moves'].split()
        for k, mate in PATTERNS:
            if k not in th: continue
            if mate and not ({'mateIn1', 'mateIn2'} & th): continue
            if not mate and len(mv) > 8: continue
            n = 1 if 'mateIn1' in th else 2 if 'mateIn2' in th else 0
            cand[k].append((pop * math.log(plays), row['PuzzleId'], row['FEN'], row['Moves'], r, n))
used = set(); out = []
for k, mate in sorted(PATTERNS, key=lambda p: len(cand[p[0]])):   # 드문 패턴부터 골라야 겹칠 때 손해가 적어요
    pick = []
    for lo, hi in BUCKETS:
        b = sorted((c for c in cand[k] if lo <= c[4] < hi and c[1] not in used), reverse=True)
        pick += b[:PER // len(BUCKETS)]
    if len(pick) < PER:   # 어떤 구간이 비면 남은 좋은 문제로 채우기
        rest = sorted((c for c in cand[k] if c[1] not in used and c not in pick), reverse=True)
        pick += rest[:PER - len(pick)]
    for c in pick: used.add(c[1])
    print(f'{k}: 후보 {len(cand[k])} · 고름 {len(pick)}', file=sys.stderr)
    out += [(k, c) for c in sorted(pick, key=lambda c: c[4])]
order = [k for k, _ in PATTERNS]
for k, c in sorted(out, key=lambda x: (order.index(x[0]), x[1][4])):
    _, pid, fen, moves, r, n = c
    print(f'{k}|{pid}|{" ".join(fen.split()[:4])}|{moves}|{r}|{n}')
