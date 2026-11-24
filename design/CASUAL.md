# 캐주얼 디자인 가이드 (파란 하늘 버전)

Google Flow(Nano Banana 2.1)에서 고른 시안 "iPad chess game UI mockup"을 기준으로 만든 가이드예요.
그림 원본과 스타일 가이드 시트는 `design/flow/`에 있어요.

- `styleguide-a.webp`, `styleguide-b.webp`: 색 · 버튼 · 카드 · 글자 시트 (Flow가 그린 참고용)
- `avatars-*.webp`, `rewards-*.webp`, `mascot-*.webp`: 요소 묶음 원본 (a를 앱에 썼어요. 곰은 b)

## 느낌

- 아이용 캐주얼 게임 화면이에요. 바탕은 맑은 하늘색이고, 그 위에 크림색 패널이 떠 있어요.
- 모든 것이 둥글고 두툼해요. 패널과 버튼 아래에 '턱'(진한 아랫선)이 있어서 눌러 보고 싶게 생겼어요.
- 판이 주인공이에요. 민트와 크림 칸에 나무 테두리를 둘러요.
- 그림은 굵고 부드러운 외곽선, 볼터치, 반짝이가 있는 카툰 스타일이에요.

## 색 (index.html `:root`의 캐주얼 테마 블록)

| 이름 | 값 | 쓰는 곳 |
|---|---|---|
| 하늘 | `#85D1F2` | 화면 바탕 (`--paper`), 위쪽은 살짝 밝게 그라데이션 |
| 크림 | `#FDF3E1` | 패널·카드·버튼 바탕 (`--card`) |
| 판 크림 | `#FFF5DC` | 밝은 칸, 안쪽 칸 (`--light`, `--paper2`) |
| 민트 | `#7FC6A8` | 어두운 칸 (`--dark`) |
| 황갈 | `#C08F61` / 테두리 `#E6CFA9` / 턱 `#D8B98A` | 패널 테두리와 아랫선 (`--line`, `--ledge`) |
| 나무 | `#9E653A` / 진한 `#6B4222` | 판 테두리 (`--wood`, `--wood-d`) |
| 초록 | `#55A834` / 턱 `#3C7F22` | 주 버튼·지나온 길 (`--olive`, 가이드 원색 `#7DC354`은 흰 글자가 안 읽혀서 진하게) |
| 파랑 | `#3F8FD2` / 턱 `#2A6AA3` | 고른 탭·고른 칸 (`--blue`, 원색 `#56A2DF`) |
| 주황 | `#F29C38` | 보조 강조 (`--orange`) |
| 별 노랑 | `#FFD359` / 진한 `#D9961A` | 보상·보물상자·연속 일수 (`--amber`) |
| 남색 | `#2F3A53` | 글자 (`--ink`), 흐린 글자 `#59647D` |

글자 대비는 크림 위 4.5:1 이상을 지켜요. 하늘 바탕 위 글자는 `#33405B` 이상으로 진하게 써요.

## 모양

- 모서리: 패널 18px, 버튼·작은 칸 14px, 알약 모양은 끝까지 둥글게.
- 패널: 크림 바탕, 2px 황갈 테두리, 아래로 4px 턱 (`--sh`). 누르면 3px 내려가고 턱이 1px로 줄어요.
- 주 버튼: 초록 바탕, 흰 글자에 살짝 그림자, 안쪽 2px 흰 선, 아래 4px 진한 초록 턱.
- 고른 탭: 파랑 바탕, 흰 글자, 안쪽 흰 선, 진한 파랑 턱.
- 판: 10px 나무 테두리, 아래 7px 진한 나무 턱, 하늘빛 그림자.
- 글꼴: 제목·버튼·숫자는 Jua(둥근 손글씨 느낌), 본문은 기기 기본 둥근 글꼴.

## 요소 (앱에서 쓰는 그림)

| 파일 | 쓰는 곳 |
|---|---|
| `img/av/{lion,rabbit,bear,panda,fox,frog,tiger,penguin,unicorn,puppy,kitten,monkey}.png` | 프로필 얼굴 (이모지 대신). 순서는 `PROF_EMOJI`와 같아요 |
| `img/ui/bear-{wave,point,cheer,think}.png` | 길잡이 곰. 인사 · 다음 칸 가리키기 · 목표 완료 · 복습 권하기 |
| `img/ui/chest.png`, `chest-open.png` | 단원 끝 보물상자(닫힘 / 통과) |
| `img/ui/flame.png` | 연속 일수 (안 했으면 회색) |
| `img/ui/trophy.png`, `star.png`, `gift.png`, `medal.png`, `lock.png` | 아직 안 쓴 보상 그림 (배지·이벤트용으로 남겨 둠) |

새 묶음 그림을 오릴 때:

```bash
python3 tools/cut-sheet.py design/flow/<묶음>.webp img/ui 이름1,이름2,... 256
```

흰 바탕을 지우고, 가장자리 흰 테두리를 투명하게 바꾸고, 왼쪽 위부터 줄 순서대로 이름을 붙여요.

## 새 그림을 Flow에 부탁할 때

시안 이미지를 참고 이미지로 넣고, 아래 틀을 쓰면 같은 느낌으로 나와요.

> Using the attached image as the style reference, create … in exactly this cartoon style (thick soft outlines, glossy highlights, warm colors). Arrange in a tidy grid of N columns and M rows with wide even gaps, each the same size and centered in its cell. Plain flat pure white background, no text, no labels, no cast shadows.

- 묶음 그림은 칸 사이를 넓게 띄워야 잘 오려져요.
- 바탕은 순수한 흰색으로 해 주세요.
- 글자는 넣지 말아 주세요. 앱이 한국어로 따로 써요.
