# california 기물 SVG → 편집하기 쉬운 SVG로 변환 (앱도 이 파일을 그대로 써요)
# - 도형으로 그려진 굵은 외곽선(검은 고리 path)을 지우고, 몸통 도형에 '선(stroke)'으로 외곽선을 그려요
# - 몸통은 왼쪽이 밝고 오른쪽이 살짝 어두운 그라데이션(staunty풍), 하이라이트는 밝은 색
# - 색·선 굵기를 도형마다 속성(fill/stroke/stroke-width)으로 직접 써서 피그마·일러스트레이터에서 바로 편집돼요
# - id에 기물 이름을 붙여(wk-g, wk-a…) 여러 기물을 한 파일에 모아도 겹치지 않아요
# 사용: python3 tools/pieces-svg.py <california svg 폴더> <출력 폴더>
import re, sys, os

LINE_W = 10          # 원본 외곽선 굵기(30)의 1/3
PAL = {
    'w': dict(main='#f4ecda', main2='#d9ccae', hi='#fffdf6', line='#3b2d21'),
    'b': dict(main='#4a372d', main2='#2c2019', hi='#6a5240', line='#0f0a08'),
}
BODY = {'#ccc', '#cccccc', '#4d4d4d'}
HI = {'#fff', '#ffffff', 'gray', '#808080', '#f2f2f2', '#999', '#b3b3b3', '#666'}

def convert(s, c, code):
    p = PAL[c]
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    body = s[s.index('>', s.index('<svg')) + 1: s.rindex('</svg>')]
    defs = ''.join(re.findall(r'<defs>(.*?)</defs>', body, re.S))
    body = re.sub(r'<defs>.*?</defs>', '', body, flags=re.S)
    clips = re.findall(r'<clipPath.*?</clipPath>', body, re.S)
    for cp in clips: body = body.replace(cp, '')
    defs += ''.join(clips)
    gid = f'{code}-g'
    J = f'stroke="{p["line"]}" stroke-width="{LINE_W}" stroke-linejoin="round" stroke-linecap="round"'
    ATTR = {'body': f'fill="url(#{gid})" {J}', 'hi': f'fill="{p["hi"]}"', 'ln': f'fill="none" {J}',
            'hiln': f'fill="{p["hi"]}" {J}', 'detail': f'fill="{p["line"]}"'}
    out, prev = [], None
    for m in re.finditer(r'<g[^>]*>|</g>|<path[^>]*/>|<path[^>]*>\s*</path>', body):
        t = m.group(0)
        if not t.startswith('<path'): out.append(t); continue
        fill = re.search(r'fill="([^"]+)"', t); fill = fill.group(1).lower() if fill else '#000'
        bare = re.sub(r'\s(fill|stroke|stroke-width|stroke-linejoin|stroke-linecap|stroke-miterlimit)="[^"]*"', '', t)
        if 'stroke-width' in t:                      # 원래 선으로 그린 부분(구슬·십자가 등): 선만 가늘게
            kind = 'ln' if fill == 'none' else 'hiln' if fill in HI else 'body'
        elif fill == '#000' and prev in BODY | HI:   # 몸통 바로 뒤의 검은 고리 = 도형 외곽선 → 지우고 선으로 대신
            prev = None; continue
        elif fill in BODY: kind = 'body'
        elif fill in HI: kind = 'hi'
        else: kind = 'detail'
        out.append(bare.replace('<path', f'<path {ATTR[kind]}', 1))
        prev = None if 'stroke-width' in t else fill
    inner = ''.join(out)
    for i in set(re.findall(r'id="([^"]+)"', defs)):
        rp = lambda x: x.replace(f'id="{i}"', f'id="{code}-{i}"').replace(f'url(#{i})', f'url(#{code}-{i})').replace(f'href="#{i}"', f'href="#{code}-{i}"')
        defs, inner = rp(defs), rp(inner)
    grad = (f'<linearGradient id="{gid}" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{p["main"]}"/>'
            f'<stop offset=".55" stop-color="{p["main"]}"/><stop offset="1" stop-color="{p["main2"]}"/></linearGradient>')
    return vb, f'<defs>{grad}{defs}</defs>', inner

if __name__ == '__main__':
    SRC, OUT = sys.argv[1], sys.argv[2]
    os.makedirs(OUT, exist_ok=True)
    for f in sorted(os.listdir(SRC)):
        if not f.endswith('.svg'): continue
        code = f[0] + f[1].lower()
        vb, defs, inner = convert(open(os.path.join(SRC, f)).read(), f[0], code)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="{vb}" width="100" height="100">'
               f'{defs}<g id="{code}">{inner}</g></svg>\n')
        open(os.path.join(OUT, code + '.svg'), 'w').write(svg)
        print('ok', code)
