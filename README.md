# 로드킬 프로토콜

차량이 주인공인 뱀서류 생존 게임입니다. 무기는 자동으로 쏘고, 플레이어는 가속·후진·핸들로 운전만 합니다. 좀비 대군을 들이받고, 무기 각성과 시너지로 쓸어버리며 목표 시간을 버티세요.

**플레이:** https://chlqudgnlsla-create.github.io/roadkill-protocol/

- 조작: ↑/W 가속 · ↓/S 브레이크·후진 · ←→/A D 핸들 · Space 드리프트 · Esc 일시정지 · M 소리
- 휴대폰: 화면 버튼으로 조작합니다. 가로 화면을 권장하며, 홈 화면에 추가하면 앱처럼 전체 화면으로 실행됩니다.
- 진행 상황(고철, 해금, 도감, 기록)은 브라우저에 저장됩니다.

## 구조

| 경로 | 내용 |
|---|---|
| `index.html` | 게임 전체 (HTML·CSS·JS 한 파일) |
| `assets/` | 차량·적·소품 스프라이트 (WebP) |
| `build.py` | `dist/`에 배포용 정적 사이트를 만듭니다 (문서 틀, 매니페스트, 아이콘) |
| `art/` | Qwen-Image 2.1로 에셋을 생성하고 후처리하는 스크립트, 아트 시안 |
| `docs/maps-plan.md` | 지역(맵) 설계 문서 |

## 로컬에서 실행

```sh
python3 build.py              # 아이콘까지 만들려면 Pillow가 필요합니다
python3 -m http.server -d dist 8000
```

`main`에 푸시하면 GitHub Actions가 빌드해서 GitHub Pages에 배포합니다.
