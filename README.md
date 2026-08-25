# news-automation

줍줍 데일리 뉴스 카드뉴스 자동화 저장소.

매일 아침 6시(KST) 클라우드 예약 에이전트가 이 저장소를 clone해서:
1. 오늘의 주요 뉴스 TOP 9를 검색·선정
2. `-습니다`체 기사 본문 + 태그 5개(라벨 없이 본문 바로 뒤에 #뉴스 #이슈 포함 해시태그로) + 카드뉴스 헤드라인 작성 → `articles/YYYY-MM-DD.md`
3. `assets/stock/`에 미리 번들된 저작권 프리(CC0/CC-BY/CC-BY-SA/Public Domain) 이미지 중 이슈별로 가장 적합한 것을 선택 (클라우드 샌드박스가 외부 이미지 사이트 접근을 차단하므로 실시간 다운로드는 하지 않음)
4. `scripts/make_card.py`로 1080x1350 PNG 카드뉴스 9장 생성 → `output/YYYY-MM-DD/card_01.png` ~ `card_09.png`
5. 결과물을 이 저장소에 commit & push

## 폴더 구조
- `assets/jubjub_logo.png` — 줍줍 로고
- `assets/fonts/` — Noto Sans KR (OFL 라이선스, 상업적 사용 무료)
- `assets/stock/` — 번들된 저작권 프리 스톡 이미지 라이브러리 (카테고리별 1장, `stock_attribution.md`에 출처/라이선스 명시). 클라우드 에이전트가 매일 이 중에서 주제에 맞는 이미지를 골라 사용
- `scripts/make_card.py` — 카드 이미지 생성 스크립트
- `articles/` — 날짜별 기사 원고
- `output/` — 날짜별 카드뉴스 PNG

## 로컬 실행
```
pip install -r requirements.txt
python scripts/make_card.py --photo path/to/photo.jpg --headline "헤드라인 1줄\n헤드라인 2줄" --out output/card_01.png
```
