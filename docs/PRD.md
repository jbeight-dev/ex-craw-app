# PRD: URL 기반 웹 크롤링 및 데이터 추출 도구

**문서 버전:** 1.2  
**작성일:** 2026-03-07  
**상태:** 진행 중 (In Progress)

---

## 1. 개요 (Overview)

### 1.1 배경

웹 상의 다양한 페이지에서 필요한 데이터를 수동으로 수집하는 작업은 반복적이고 비효율적이다. 이를 자동화하기 위해 URL을 입력받아 해당 페이지의 소스코드를 크롤링하고, 원하는 데이터를 구조적으로 추출하는 파이썬 도구를 개발한다.

### 1.2 목표

- URL을 입력하면 해당 웹 페이지의 HTML 소스를 수집한다.
- 수집된 소스에서 사용자가 정의한 규칙에 따라 데이터를 추출한다.
- 추출된 데이터를 구조화된 형식(JSON, CSV 등)으로 저장 또는 반환한다.

### 1.3 범위 (Scope)

| 항목 | 포함 여부 |
|------|----------|
| 단일 URL 크롤링 | ✅ |
| 다중 URL 배치 처리 | ✅ |
| JavaScript 렌더링 페이지 지원 | ✅ (선택적) |
| 로그인 인증 처리 | ❌ (v1 제외) |
| 분산 크롤링 | ❌ (v1 제외) |

---

## 2. 사용자 및 시나리오 (Users & Use Cases)

### 2.1 주요 사용자

- **데이터 분석가:** 특정 사이트에서 정기적으로 데이터를 수집해야 하는 사용자
- **개발자:** 크롤링 기능을 자신의 프로젝트에 통합하려는 사용자
- **리서처:** 웹에서 특정 키워드나 구조의 데이터를 추출하려는 사용자

### 2.2 핵심 시나리오

**시나리오 1 - 단일 페이지 데이터 추출**
> 사용자가 뉴스 기사 URL을 입력하면 제목, 본문, 날짜, 작성자를 추출하여 JSON으로 저장한다.

**시나리오 2 - 다중 URL 배치 처리**
> CSV 파일에 담긴 여러 URL을 순차적으로 크롤링하고, 각 페이지에서 동일한 규칙으로 데이터를 추출한다.

**시나리오 3 - 동적 페이지 처리**
> JavaScript로 렌더링되는 SPA 페이지에서도 데이터를 추출할 수 있어야 한다.

---

## 3. 기능 요구사항 (Functional Requirements)

### 3.1 입력 처리

| ID | 요구사항 | 우선순위 |
|----|---------|---------|
| F-01 | 단일 URL 문자열을 입력받아 크롤링을 수행한다 | 필수 |
| F-02 | URL 목록 파일(txt, csv)을 입력받아 배치 처리한다 | 필수 |
| F-03 | HTTP/HTTPS 프로토콜을 모두 지원한다 | 필수 |
| F-04 | User-Agent, 헤더, 쿠키 등 요청 옵션을 설정할 수 있다 | 권장 |
| F-05 | 요청 간 딜레이(Rate Limiting)를 설정할 수 있다 | 권장 |

### 3.2 크롤링 엔진

| ID | 요구사항 | 우선순위 |
|----|---------|---------|
| F-10 | `requests` 라이브러리를 사용하여 정적 HTML을 수집한다 | 필수 |
| F-11 | `Selenium` 또는 `Playwright`를 사용하여 JavaScript 렌더링 페이지를 지원한다 | 권장 |
| F-12 | HTTP 상태 코드에 따라 재시도 로직(Retry)을 수행한다 | 필수 |
| F-13 | 요청 타임아웃을 설정할 수 있다 | 필수 |
| F-14 | robots.txt를 파싱하여 크롤링 허용 여부를 확인한다 | 권장 |

### 3.3 데이터 추출

| ID | 요구사항 | 우선순위 |
|----|---------|---------|
| F-20 | CSS 셀렉터 기반으로 HTML 요소를 추출한다 | 필수 |
| F-21 | XPath 기반으로 HTML 요소를 추출한다 | 권장 |
| F-22 | 정규표현식(Regex)을 사용하여 텍스트 패턴을 추출한다 | 권장 |
| F-23 | 메타 태그(og:title, description 등)를 자동 추출한다 | 권장 |
| F-24 | 이미지, 링크 URL 목록을 추출한다 | 권장 |
| F-25 | 추출 필드를 설정 파일(YAML/JSON)로 정의할 수 있다 | 권장 |

### 3.4 출력 및 저장

| ID | 요구사항 | 우선순위 |
|----|---------|---------|
| F-30 | 추출 결과를 JSON 형식으로 저장한다 (processed 디렉토리) | 필수 |
| F-31 | 추출 결과를 CSV 형식으로 저장한다 | 필수 |
| F-32 | 원본 HTML 소스를 파일로 저장한다 (raw 디렉토리) | 필수 |
| F-33 | 표준 출력(stdout)으로 결과를 출력할 수 있다 | 권장 |

---

## 4. 비기능 요구사항 (Non-Functional Requirements)

### 4.1 성능

- 단일 URL 응답 처리 시간: **5초 이내** (네트워크 지연 제외 기준)
- 배치 처리 시 병렬 요청 수: **최대 5개 동시 요청** (기본값: 1)

### 4.2 안정성

- 네트워크 오류 및 HTTP 4xx/5xx 에러 발생 시 자동 재시도 (**최대 3회**)
- 특정 URL 실패 시 전체 작업이 중단되지 않고 오류를 기록 후 계속 진행

### 4.3 확장성

- 추출 규칙을 외부 설정 파일로 분리하여 코드 수정 없이 커스터마이징 가능
- 모듈 구조로 설계하여 크롤링 엔진, 파서, 저장소 컴포넌트를 독립적으로 교체 가능

### 4.4 보안 및 준법

- 과도한 요청으로 인한 서버 부하를 방지하기 위해 Rate Limiting 기본 적용
- robots.txt 준수 여부를 설정으로 제어 가능

---

## 5. 시스템 아키텍처 (System Architecture)

```
┌─────────────────────────────────────────────────┐
│                   CLI / API 인터페이스            │
└───────────────────────┬─────────────────────────┘
                        │ URL(s) + 설정
                        ▼
┌─────────────────────────────────────────────────┐
│                   Crawler 엔진                   │
│  ┌────────────────┐   ┌──────────────────────┐  │
│  │ Static Crawler │   │  Dynamic Crawler      │  │
│  │ (requests)     │   │  (Selenium/Playwright)│  │
│  └────────┬───────┘   └──────────┬───────────┘  │
└───────────┼──────────────────────┼──────────────┘
            │        HTML Source   │
            ▼                      ▼
┌─────────────────────────────────────────────────┐
│                   Parser 모듈                    │
│   CSS Selector / XPath / Regex / Meta Tags      │
└───────────────────────┬─────────────────────────┘
                        │ Structured Data
                        ▼
┌─────────────────────────────────────────────────┐
│                  Storage 모듈                    │
│          JSON / CSV / Raw HTML 저장              │
└─────────────────────────────────────────────────┘
```

---

## 6. 기술 스택 (Tech Stack)

| 구분 | 라이브러리 | 용도 |
|------|----------|------|
| HTTP 요청 | `requests`, `httpx` | 정적 페이지 크롤링 |
| HTML 파싱 | `BeautifulSoup4`, `lxml` | HTML 구조 파싱 |
| 동적 렌더링 | `Playwright` (권장) 또는 `Selenium` | JS 렌더링 페이지 처리 |
| 설정 관리 | `PyYAML`, `python-dotenv` | 설정 파일 파싱 |
| CLI | `argparse` 또는 `click` | 커맨드라인 인터페이스 |
| 데이터 저장 | `pandas`, 내장 `json`/`csv` | 데이터 출력 포맷 |
| 로깅 | `logging` (내장) | 실행 로그 관리 |

---

## 7. 프로젝트 구조 (Project Structure)

```
web-crawler/
├── crawler/
│   ├── __init__.py
│   ├── manager.py         # 크롤링 파이프라인 관리 (오케스트레이션)
│   ├── static.py          # requests 기반 정적 크롤러
│   ├── dynamic.py         # Playwright 기반 동적 크롤러
│   └── retry.py           # 재시도 로직
├── parser/
│   ├── __init__.py
│   ├── css_parser.py      # CSS 셀렉터 파서
│   ├── xpath_parser.py    # XPath 파서
│   └── meta_parser.py     # 메타 태그 파서
├── storage/
│   ├── __init__.py
│   ├── json_writer.py
│   ├── csv_writer.py
│   └── raw_html_writer.py # 원본 HTML 파일 저장
├── utils/
│   ├── __init__.py
│   ├── config.py          # 설정 로드 및 CLI 인자 파싱
│   └── helpers.py         # URL 파싱 등 범용 유틸리티
├── config/
│   └── rules.yaml         # 추출 규칙 정의 파일
├── output/                # 크롤링 결과물 디렉토리
│   ├── raw/               # 원본 데이터 그대로 보존 (html)
│   └── processed/         # 정제된 텍스트 결과물 (json, csv)
├── main.py                # 진입점 (CLI)
├── requirements.txt
└── README.md
```

---

## 8. 설정 파일 예시 (Configuration)

```yaml
# config/rules.yaml
target:
  url: "https://example.com/news"
  render_js: false
  delay_seconds: 1
  timeout: 10
  retry_count: 3

extract:
  title:
    selector: "h1.article-title"
    type: css
  date:
    selector: "//span[@class='date']"
    type: xpath
  body:
    selector: "div.content p"
    type: css
    multiple: true

output:
  format: json
  path: "./output/result.json"
  save_html: false
```

---

## 9. CLI 사용 예시 (Usage)

```bash
# 단일 URL 크롤링
python main.py --url "https://example.com" --config config/rules.yaml

# 다중 URL 배치 처리
python main.py --url-file urls.txt --config config/rules.yaml --output csv

# 동적 페이지 처리 (JS 렌더링)
python main.py --url "https://spa-example.com" --render-js --delay 2

# 결과를 stdout으로 출력
python main.py --url "https://example.com" --config config/rules.yaml --stdout
```

---

## 10. 오류 처리 (Error Handling)

| 오류 유형 | 처리 방식 |
|----------|---------|
| 네트워크 연결 실패 | 최대 3회 재시도 후 오류 로그 기록 및 다음 URL로 진행 |
| HTTP 4xx (클라이언트 오류) | 재시도 없이 즉시 오류 기록 |
| HTTP 5xx (서버 오류) | 최대 3회 재시도 |
| 타임아웃 | 재시도 후 실패 시 건너뜀 |
| 파싱 오류 (셀렉터 불일치) | 해당 필드를 `null`로 기록, 전체 실패 아님 |
| robots.txt 차단 | 크롤링 중단 및 경고 로그 기록 |

---

## 11. 마일스톤 (Milestones)

| 단계 | 내용 | 목표 시점 |
|------|------|---------|
| M1 | 정적 크롤러 + CSS 파서 + JSON/HTML 분리 저장 | ✅ 완료 |
| M2 | XPath 파서 + CSV 저장 + CLI 인터페이스 완성 | ✅ 완료 |
| M3 | 동적 크롤러(Playwright) 통합 + 배치 처리 | ✅ 완료 |
| M4 | 설정 파일 기반 추출 규칙 + 오류 처리 강화 | Week 4 |
| M5 | 테스트 작성 + 문서화 + 코드 리뷰 | Week 5 |

---

## 12. 미해결 사항 (Open Questions)

- [ ] 로그인이 필요한 페이지 지원은 v2에서 다룰 것인지 확인 필요
- [ ] 추출 결과를 DB(SQLite, PostgreSQL 등)에 저장하는 기능 포함 여부
- [ ] 비동기(`asyncio` + `httpx`) 방식 vs 멀티스레딩 중 병렬 처리 전략 결정 필요
- [ ] 클라우드 환경(Lambda, Cloud Run) 배포 고려 여부

---

*본 문서는 개발 진행에 따라 지속적으로 업데이트됩니다.*
