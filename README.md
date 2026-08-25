# news-automation

줍줍 데일리 뉴스 카드뉴스 자동화 저장소.

매일 아침 6시(KST) 클라우드 예약 에이전트가 이 저장소를 clone해서:
1. 오늘의 주요 뉴스 TOP 9를 검색·선정
2. `-습니다`체 기사 + 태그 5개(#뉴스 #이슈 포함) + 카드뉴스 헤드라인 작성 → `articles/YYYY-MM-DD.md`
3. 이슈별 저작권 프리(CC0/CC-BY/CC-BY-SA/Public Domain) 이미지를 위키미디어 커먼즈에서 검색·다운로드
4. `scripts/make_card.py`로 1080x1350 PNG 카드뉴스 9장 생성 → `output/YYYY-MM-DD/card_01.png` ~ `card_09.png`
5. 결과물을 이 저장소에 commit & push

## 폴더 구조
- `assets/jubjub_logo.png` — 줍줍 로고
- `assets/fonts/` — Noto Sans KR (OFL 라이선스, 상업적 사용 무료)
- `scripts/make_card.py` — 카드 이미지 생성 스크립트
- `articles/` — 날짜별 기사 원고
- `output/` — 날짜별 카드뉴스 PNG

## 로컬 실행
```
pip install -r requirements.txt
python scripts/make_card.py --photo path/to/photo.jpg --headline "헤드라인 1줄\n헤드라인 2줄" --out output/card_01.png
```
