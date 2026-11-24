# Flow에서 만든 그림 묶음(흰 바탕)을 하나씩 오려서 투명 PNG로 저장해요.
#   python3 tools/cut-sheet.py <묶음 그림> <저장 폴더> <이름1,이름2,...> [긴 변 픽셀]
# 이름은 왼쪽 위부터 오른쪽으로, 줄 순서대로. 작은 반짝이는 가까운 큰 그림에 붙여요.
import sys, os
import numpy as np
from PIL import Image
from collections import deque

src, out, names = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
size = int(sys.argv[4]) if len(sys.argv) > 4 else 256
os.makedirs(out, exist_ok=True)
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32)
H, W, _ = im.shape

# 1) 테두리에서 이어진 밝은 바탕 찾기
light = (255 - im.min(axis=2))          # 0 = 하얀색
near = light < 70                        # 바탕 후보(살짝 회색까지)
bg = np.zeros((H, W), bool); q = deque()
for x in range(W):
    for y in (0, H - 1):
        if near[y, x] and not bg[y, x]: bg[y, x] = True; q.append((y, x))
for y in range(H):
    for x in (0, W - 1):
        if near[y, x] and not bg[y, x]: bg[y, x] = True; q.append((y, x))
while q:
    y, x = q.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < H and 0 <= nx < W and near[ny, nx] and not bg[ny, nx]:
            bg[ny, nx] = True; q.append((ny, nx))

# 2) 투명도: 바탕 쪽 픽셀은 하얀 정도만큼 투명하게(가장자리 흰 테두리 없애기)
a = np.ones((H, W), np.float32)
a[bg] = np.clip((light[bg] - 12) / 58, 0, 1)
rgb = im.copy()
m = (a > 0) & (a < 1)
rgb[m] = np.clip((im[m] - (1 - a[m, None]) * 255) / a[m, None], 0, 255)

# 3) 덩어리 나누기(작게 줄여서 빠르게)
s = 4; h2, w2 = H // s, W // s
fg = (a[:h2 * s, :w2 * s].reshape(h2, s, w2, s).max(axis=(1, 3)) > 0.5)
lab = np.zeros((h2, w2), int); n = 0; boxes = []
for y in range(h2):
    for x in range(w2):
        if fg[y, x] and not lab[y, x]:
            n += 1; lab[y, x] = n; q = deque([(y, x)]); y0 = y1 = y; x0 = x1 = x; c = 0
            while q:
                cy, cx = q.popleft(); c += 1
                y0, y1, x0, x1 = min(y0, cy), max(y1, cy), min(x0, cx), max(x1, cx)
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h2 and 0 <= nx < w2 and fg[ny, nx] and not lab[ny, nx]:
                            lab[ny, nx] = n; q.append((ny, nx))
            boxes.append([x0 * s, y0 * s, (x1 + 1) * s, (y1 + 1) * s, c])
big = sorted([b for b in boxes if b[4] > 600], key=lambda b: -b[4])[:len(names)]
small = [b for b in boxes if b not in big]
for b in small:  # 반짝이 같은 작은 조각은 가장 가까운 큰 그림에 합쳐요
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    t = min(big, key=lambda B: max(0, B[0] - cx, cx - B[2]) + max(0, B[1] - cy, cy - B[3]))
    if max(0, t[0] - cx, cx - t[2]) + max(0, t[1] - cy, cy - t[3]) < 60:
        t[0], t[1], t[2], t[3] = min(t[0], b[0]), min(t[1], b[1]), max(t[2], b[2]), max(t[3], b[3])
rowh = np.median([b[3] - b[1] for b in big])
big.sort(key=lambda b: (round(((b[1] + b[3]) / 2) / rowh), (b[0] + b[2]) / 2))
assert len(big) == len(names), f'{len(big)}개를 찾았어요(이름 {len(names)}개)'
rgba = np.dstack([rgb, a * 255]).astype(np.uint8)
for nm, (x0, y0, x1, y1, _) in zip(names, big):
    p = 6; x0, y0, x1, y1 = max(0, x0 - p), max(0, y0 - p), min(W, x1 + p), min(H, y1 + p)
    piece = Image.fromarray(rgba[y0:y1, x0:x1], 'RGBA')
    piece.thumbnail((size, size), Image.LANCZOS)
    piece.save(os.path.join(out, nm + '.png'), optimize=True)
    print(nm, piece.size)
