# california 실루엣 → 단정한(staunty풍) 표현으로 다시 칠하기
# 1) 1024px로 래스터화된 원본에서 외곽선/몸통/하이라이트를 색으로 구분
# 2) 굵은 외곽선을 약 1/3로: 몸통을 외곽선 쪽으로 넓히고, 바깥 실루엣을 조금 깎음
# 3) 새 팔레트로 칠하고 오른쪽으로 갈수록 살짝 어두워지는 부드러운 명암을 더함
import sys, os
import numpy as np
from PIL import Image, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
GROW = int(sys.argv[3]) if len(sys.argv) > 3 else 20
os.makedirs(OUT, exist_ok=True)
hexrgb = lambda h: np.array([int(h[i:i+2], 16) for i in (1, 3, 5)], float)
PAL = {
  'w': {'main': '#f4ecda', 'hi': '#fffdf6', 'line': '#3b2d21'},
  'b': {'main': '#3a2a22', 'hi': '#6a5240', 'line': '#0f0a08'},
}

def mask_img(m): return Image.fromarray((m*255).astype(np.uint8))
def arr(im): return np.array(im) > 127

for f in sorted(os.listdir(SRC)):
    if not f.endswith('.png'): continue
    c = f[0]; im = np.array(Image.open(os.path.join(SRC, f)).convert('RGBA')).astype(float)
    a = im[..., 3] > 127; lum = im[..., :3].mean(-1)
    if c == 'w': hi = a & (lum > 230); main = a & (lum > 150) & ~hi
    else:        hi = a & (lum > 102); main = a & (lum > 45) & ~hi
    line = a & ~hi & ~main
    # 몸통·하이라이트를 외곽선 안쪽으로 넓히기(2px씩 반복해서 가까운 쪽 색을 따라가게)
    for _ in range(GROW // 2):
        hd = arr(mask_img(hi).filter(ImageFilter.MaxFilter(5)))
        md = arr(mask_img(main).filter(ImageFilter.MaxFilter(5)))
        nh = line & hd; nm = line & md & ~nh
        hi |= nh; main |= nm; line &= ~(nh | nm)
    # 바깥 실루엣을 GROW만큼 깎아 바깥 외곽선도 가늘게
    sil = arr(mask_img(a).filter(ImageFilter.MinFilter(2*GROW+1)))
    # 부드러운 명암: 기물 폭 기준 왼쪽 밝고 오른쪽 살짝 어둡게
    ys, xs = np.nonzero(sil); x0, x1 = xs.min(), xs.max()
    gx = np.clip((np.arange(im.shape[1]) - x0) / max(1, x1 - x0), 0, 1)
    shade = 1 - 0.13 * (gx ** 1.6)
    out = np.zeros((*a.shape, 4))
    P = {k: hexrgb(v) for k, v in PAL[c].items()}
    for m, col in ((main, P['main']), (hi, P['hi']), (line, P['line'])):
        out[m, :3] = col
    body = main | hi
    out[body, :3] *= shade[None, :].repeat(a.shape[0], 0)[body][:, None]
    out[..., 3] = sil * 255
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), 'RGBA')
    img.resize((256, 256), Image.LANCZOS).save(os.path.join(OUT, f[0] + f[1].lower() + '.png'))
    print('ok', f)

# 12개 모두 같은 비율로 키우기: 전체를 감싸는 상자 하나로 똑같이 잘라 상대 크기는 그대로
ims = {f: Image.open(os.path.join(OUT, f)) for f in os.listdir(OUT) if f.endswith('.png')}
bbs = [im.getbbox() for im in ims.values()]
x0 = min(b[0] for b in bbs); y0 = min(b[1] for b in bbs); x1 = max(b[2] for b in bbs); y1 = max(b[3] for b in bbs)
side = max(x1 - x0, y1 - y0); cx = (x0 + x1) / 2
box = (int(cx - side/2), y1 - side, int(cx + side/2), y1)
for f, im in ims.items():
    c = im.crop(box); S = 256; m = int(S * .05)
    can = Image.new('RGBA', (S, S)); can.paste(c.resize((S - 2*m, S - 2*m), Image.LANCZOS), (m, m + int(S*.01)))
    can.save(os.path.join(OUT, f))
print('crop', box)
