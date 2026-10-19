# Taewan Cho — Personal website

소개, 연구, 회사, 개인 프로젝트, 개인적인 글을 모으는 GitHub Pages 사이트입니다.
방문자에게 제공하는 파일은 정적 HTML/CSS/JavaScript이며, 별도의 애플리케이션 서버나 데이터베이스가 필요하지 않습니다.

## 로컬 미리보기

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build.py
.venv/bin/python -m http.server 4318 --bind 127.0.0.1
```

브라우저에서 <http://127.0.0.1:4318/>을 엽니다. 파일 수정 후 빌드하고 새로고침하면 됩니다.
위 명령은 GitHub에 커밋하거나 푸시하지 않습니다.

## 구성

| 주소 | 내용 | 수정할 곳 |
| --- | --- | --- |
| `/` | 소개, 대표 연구, 회사, 대표 프로젝트, 최근 글 3개 | `templates/home.html`, `content/profile.json` |
| `/research/` | 전체 논문, 연구 관심사, 특허 | `content/publications.json`, `content/profile.json`, `templates/patents.html` |
| `/company/` | Plaid Labs 소개, 구축 영역, 제품, 온디바이스 적용 흐름, 사례, 회사 문의 | `content/company.json`, `templates/company.html` |
| `/project/` | 개인 프로젝트와 공개한 도구 | `content/projects.json` |
| `/blog/` | 공개 글의 최신순 목록 | `content/posts/*.md` |
| `/blog/글-이름/` | 개별 글 | 같은 Markdown 파일 |
| `/feed.xml` | 공개 글 RSS | 빌드 시 자동 생성 |

`templates/base.html`은 모든 페이지의 공통 머리말·메뉴·바닥글입니다.
`styles.css`에서 글꼴, 색상, 여백, 모바일 화면을 조정합니다.
생성된 `index.html`, `research/index.html`, `company/index.html`, `project/index.html`, `blog/` HTML은 직접 수정하지 않습니다.
빌드가 해당 파일을 다시 생성합니다. 원본 콘텐츠와 생성 파일을 함께 관리합니다.

## 언어와 연락처

- 기본 진입 언어는 영어입니다. 기존 주소(`/`, `/research/` 등)는 영어이며, `/ko/`, `/ko/research/` 등은 한국어입니다.
- 오른쪽 위 EN / KO 버튼은 현재 페이지와 앵커를 유지하며 언어를 전환합니다. 내부 링크도 선택한 언어를 유지합니다. 메뉴 이름은 두 언어에서 About / Research / Company / Project / Blog로 통일합니다.
- 공통 UI 문구는 `content/site-copy.json`의 `en`/`ko`에서 관리합니다. 두 언어의 키를 맞춰야 합니다.
- 연구 소개와 관심사는 `content/profile.json`의 `bio`/`bio_ko`, `interests`/`interests_ko`를 사용합니다.
- 논문 제목·저자·학회명은 원문을 유지하며, 요약은 `summary`/`summary_ko`로 나눕니다.
- 오픈소스 설명은 `description`/`detail`이 한국어, `description_en`/`detail_en`이 영어입니다. 분류는 `kind`/`kind_ko`입니다.
- 블로그는 EN / KO에 맞춰 준비된 언어판의 제목·소개·본문을 표시합니다. 번역본이 없으면 원문을 표시하며, 자동 번역하지 않습니다. RSS에는 원문 링크로 글이 한 번씩만 들어갑니다.
- 연구 연락처는 `email`(`taewan2002@kaist.ac.kr`), 회사 문의는 `company_email`(`technoking@plaid.ai.kr`)입니다. 모두 복사할 수 있는 일반 텍스트로 표시합니다.

영문과 한국어 페이지는 같은 템플릿에서 함께 생성됩니다. `ko/`의 HTML도 직접 수정하지 않습니다.

## 글 추가하기

1. `content/posts/_template.md`를 `content/posts/my-first-post.md`로 복사합니다.
2. 제목, 날짜, 소개, 언어와 본문을 작성합니다. 파일명은 영문 소문자·숫자·하이픈으로 정하고, 공개 이후에는 주소 유지를 위해 바꾸지 않습니다.
3. 초안은 `draft: true`로 둡니다. 로컬에서 보려면 `.venv/bin/python scripts/build.py --drafts`를 실행합니다.
4. 공개할 준비가 되면 `draft: false`로 바꾸고 일반 빌드를 실행합니다.

```yaml
---
title: "내가 쓰고 싶은 이야기"
date: "2026-10-18"
summary: "목록과 공유 미리보기에 표시할 짧은 소개입니다."
lang: ko
draft: true
---
```

한국어(`ko`)와 영어(`en`) 글을 지원합니다. Markdown의 제목·인용·목록·표·코드·이미지를 사용할 수 있습니다.
번역본은 `content/posts/en/my-first-post.md`처럼 언어 폴더 아래에 원문과 같은 파일명으로 저장합니다.
번역본에도 제목·소개·본문과 front matter를 작성하며, `lang`은 폴더 언어와 일치해야 합니다.
날짜와 `draft`는 원문과 동일하게 유지합니다. 두 파일은 하나의 글로 묶이며, `/blog/my-first-post/`와 `/ko/blog/my-first-post/`에서 각각 준비된 언어판을 보여줍니다.
번역된 페이지는 각 언어 URL을 canonical로 사용하고, 실제 존재하는 언어판끼리 hreflang으로 연결합니다.
이미지는 `assets/blog/` 아래에 넣고 `![설명](/assets/blog/example.png)`로 연결합니다.
본문의 raw HTML은 실행하지 않습니다. 카테고리는 아직 강제하지 않습니다.

일반 빌드는 초안과 한국 시간 기준 미래 날짜의 글을 목록·본문·RSS에서 제외합니다.
`--drafts`로 본 글에는 초안 표시와 `noindex`가 붙으며 RSS에 들어가지 않습니다.
이후 일반 빌드를 실행하면 남아 있던 초안 HTML도 제거합니다.
미래 날짜가 되어도 자동 예약 발행되지는 않으며 다시 빌드해야 합니다.

**중요:** `noindex`는 비공개 기능이 아닙니다. GitHub 저장소 자체가 공개라면 Markdown 원본도 공개됩니다.
개인 초안은 공개 저장소 밖에 보관하고, 업로드 전에는 반드시 일반 빌드를 실행하세요.

## 연구와 오픈소스 추가하기

- 논문은 `content/publications.json`에 항목을 추가합니다. 목록은 JSON의 순서를 유지합니다.
- 홈의 대표 논문은 `content/profile.json`의 `selected_papers`에서 ID로 선택합니다.
- 공개 도구는 `content/projects.json`에 이름, 설명, 이미지, GitHub 주소를 추가합니다.
- 회사 내용은 `content/company.json`에서 영어·한국어를 함께 관리합니다. `sources`는 공식 홈페이지의 근거 링크이며, `source_checked`는 내용을 마지막으로 대조한 날짜입니다. `source_document`에는 제작자가 제공한 회사 리플릿의 버전을 기록합니다. 사례는 회사가 공개한 프로젝트를 요약하며 개인 단독 실적으로 표기하지 않습니다.
- 이미지의 출처는 `ASSET-SOURCES.md`, 논문 날짜의 기준은 `PUBLICATION-DATES.md`에 기록합니다.

기존 논문 10편의 저자·순서·날짜·원문 링크와 특허 정보를 유지했습니다.
기존 홈페이지의 개별 논문·특허 해시 링크는 이동한 Research 페이지로 연결합니다.
이전 로컬 시안의 `/open-source/`는 언어와 앵커를 유지하면서 `/project/`로 이동합니다.

## 확인과 배포

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build.py
git diff --check
```

빌드 결과는 GitHub Pages의 `main` 브랜치 루트에서 서비스합니다.
`.nojekyll`을 유지합니다. Python 의존성은 작성·빌드할 때만 필요합니다.
발행할 글과 번역본을 함께 `draft: false`로 바꾸고, 위의 일반 빌드로 생성한 파일을 원본과 함께 커밋합니다.
`main`에 푸시하면 GitHub Pages가 정적 파일을 배포합니다. `--drafts`로 생성한 미리보기는 배포하지 않습니다.

## 디자인 참고

기존 논문 목록의 출발점은 [Jon Barron의 홈페이지](https://jonbarron.info/)입니다.
소개·연구·개인적인 글을 한 도메인에서 분리하는 구성은 [Giseop Kim의 홈페이지](https://gisbi-kim.github.io/)를 참고했습니다.
코드와 레이아웃은 이 사이트에 맞게 직접 작성했습니다.

현재 디자인은 흑백 중심의 색상, 큰 산세리프 제목, 얇은 구분선과 넓은 여백을 사용합니다.
[SpaceX](https://www.spacex.com/), [Tesla](https://www.tesla.com/), [Palantir](https://www.palantir.com/)의 공식 사이트에서 시각적 원칙을 참고했으며 해당 사이트의 코드나 이미지는 사용하지 않았습니다.
Company의 첫 화면은 회사 소개에 집중한 텍스트 구성이고, 제품은 별도 섹션에서 설명합니다.
좁은 화면에서는 메뉴와 언어 전환을 두 줄로 배치하고, 제품·연구 목록은 한 열로 전환합니다.
