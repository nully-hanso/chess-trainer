# 피그마·일러스트레이터에서 만지기 좋은 디자인 파일 만들기
#   design/board.svg        빈 체스판(칸 색·테두리·좌표)
#   design/chess-set.svg    체스판 + 시작 배치(기물마다 이름 붙은 그룹)
#   design/pieces-sheet.svg 기물 12개를 크게 모은 시트
# 기물 모양은 design/pieces-svg/*.svg(선 외곽선 버전)를 그대로 옮겨 넣어요.
import os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); D = os.path.join(ROOT, 'design')
LIGHT, DARK, BORDER, COORD_L, COORD_D = '#e2c98f', '#6f9440', '#557330', '#5e7d33', '#f3e6c2'
FIT = 1.087   # 앱과 같은 크기: 기물 그림을 칸의 108.7%로 가운데 맞춤
NAMES = {'k': '킹', 'q': '퀸', 'r': '룩', 'b': '비숍', 'n': '나이트', 'p': '폰'}

def piece(code):
    s = open(os.path.join(D, 'pieces-svg', code + '.svg')).read()
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    defs = re.search(r'<defs>(.*?)</defs>', s, re.S).group(1)
    inner = re.search(r'<g id="[^"]+">(.*)</g></svg>', s, re.S).group(1)
    return vb, defs, inner

def place(code, X, Y, S, label=None):
    (x, y, w, h), _, inner = piece(code)
    s = S * FIT / max(w, h); tx = X + S / 2 - (x + w / 2) * s; ty = Y + S / 2 - (y + h / 2) * s
    name = ('백 ' if code[0] == 'w' else '흑 ') + NAMES[code[1]] + (f' {label}' if label else '')
    return f'<g id="{name}" transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">{inner}</g>'

def all_defs(codes):
    return ''.join(piece(c)[1] for c in sorted(set(codes)))

def board(S=100, B=10, coords=True):
    out = [f'<rect id="테두리" x="0" y="0" width="{8*S+2*B}" height="{8*S+2*B}" rx="16" fill="{BORDER}"/>', '<g id="칸">']
    for r in range(8):
        for f in range(8):
            out.append(f'<rect id="{"abcdefgh"[f]}{8-r}" x="{B+f*S}" y="{B+r*S}" width="{S}" height="{S}" fill="{LIGHT if (r+f)%2==0 else DARK}"/>')
    out.append('</g>')
    if coords:
        out.append('<g id="좌표" font-family="sans-serif" font-size="13" font-weight="800">')
        for r in range(8):
            out.append(f'<text x="{B+4}" y="{B+r*S+15}" fill="{COORD_L if r%2==0 else COORD_D}">{8-r}</text>')
        for f in range(8):
            out.append(f'<text x="{B+f*S+S-12}" y="{B+8*S-5}" fill="{COORD_L if f%2==1 else COORD_D}">{"abcdefgh"[f]}</text>')
        out.append('</g>')
    return ''.join(out)

def svg(w, h, body, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<defs>{defs}</defs>{body}</svg>\n')

S, B = 100, 10
open(os.path.join(D, 'board.svg'), 'w').write(svg(8*S+2*B, 8*S+2*B, board(S, B)))

START = ['rnbqkbnr', 'pppppppp', '', '', '', '', 'PPPPPPPP', 'RNBQKBNR']
pcs, codes = [], []
for r, row in enumerate(START):
    for f, ch in enumerate(row):
        code = ('w' if ch.isupper() else 'b') + ch.lower(); codes.append(code)
        pcs.append(place(code, B + f*S, B + r*S, S, label='abcdefgh'[f] + str(8-r)))
open(os.path.join(D, 'chess-set.svg'), 'w').write(svg(8*S+2*B, 8*S+2*B, board(S, B) + '<g id="기물">' + ''.join(pcs) + '</g>', all_defs(codes)))

T = 200; order = 'kqbnrp'; body = []; codes = []
for row, c in enumerate('wb'):
    for i, t in enumerate(order):
        x, y = i*T, row*T; codes.append(c+t)
        body.append(f'<rect x="{x}" y="{y}" width="{T}" height="{T}" fill="{LIGHT if (i+row)%2==0 else DARK}"/>')
        body.append(place(c+t, x, y, T))
open(os.path.join(D, 'pieces-sheet.svg'), 'w').write(svg(6*T, 2*T, ''.join(body), all_defs(codes)))
print('ok')
