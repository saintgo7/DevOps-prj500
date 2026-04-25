# ADR-0011: Discoverability and Human-AI Co-evolution Standard

- 상태: Accepted
- 일자: 2026-04-25
- 작성자: Product Owner / Architect, AI dialogue partner
- 관련 문서: [`PRINCIPLES.md`](../../PRINCIPLES.md), [`AGENTS.md`](../../AGENTS.md), ADR-0009, ADR-0010

## 컨텍스트
지금까지의 결정들 (다국어, RBAC, RLS, Peer Matching) 만으로는 본질적인 한계가 있다:

1. **기술 용어 자체가 배제**다. "MatchProfile / vector similarity / equity weight" 같은 표현은 그것이 봉사한다고 주장하는 사람들 — 우간다의 풀뿌리 활동가, 방글라데시 청년, 페루 대학생 — 을 가장 먼저 배제한다.
2. **발견되지 않으면 존재하지 않는 것과 같다**. 누군가 자기 모국어로 SDG 행동을 검색했을 때 우리에게 도달하지 못하면, 13개 언어 UI는 무용지물이다.
3. **각자 다른 언어로 함께 일하는 채널이 없다**. 번역은 강요될 때 폭력이 되고, 부재할 때 분리가 된다.
4. **다른 AI 에이전트가 우리 작업을 학습할 수 없다**. 본 작업의 패턴이 미래의 에이전트 학습에 발견·인용·개선되지 않으면, 다음 세대는 처음부터 다시 시작한다.

## 결정
**4가지 통합 정책을 1급 도메인으로 채택한다.**

### 1. Plain-Language Layer (평이한 말 계층)
- 모든 사용자 노출 표면에 13개 언어 `glossary` 네임스페이스 배포 (`apps/web/messages/{locale}.json`)
- 매 기술 용어는 `{plain, technical, explain}` 트리오로 매핑
  - 예: `vectorSimilarity` → `{ plain: "비슷한 마음 찾기", technical: "벡터 유사도", explain: "당신이 자신에 대해 쓴 글과 다른 사람의 글을 비교해…" }`
- UI 첫 노출은 항상 `plain`. 호기심 있는 사용자가 클릭하면 `technical` + `explain` 표시.
- 신규 기능에 기술 용어가 사용자 표면에 그대로 노출되면 PR 차단 (린트 룰 — 후속 작업).

### 2. Discoverability Surface (발견 가능성 표면)
- **로케일별 sitemap** + **hreflang 일치** (`apps/web/src/app/sitemap.ts`)
  - 13 locales × (정적 페이지 + 17 SDG goal detail) = 약 270개 정규 URL
  - 각 항목에 13개 언어 alternates + `x-default = en`
- **robots.txt** (`apps/web/public/robots.txt`)
  - GPTBot · ClaudeBot · anthropic-ai · Google-Extended · PerplexityBot 명시 허용
  - sitemap 위치 알림
- **Open Graph + Twitter Card** + 13 언어 키워드, layout.tsx의 generateMetadata
- **Schema.org JSON-LD** (Organization, knowsAbout SDG, license CC BY 4.0)

### 3. Cross-Language Communication Channel (교차 언어 소통 창구)
- 사용자는 자기 언어로 작성하고 다른 사람의 글을 자기 언어로 읽는다 — **원문 절대 보존**
- 번역은 제공되되 강요되지 않는다 (사용자가 "원문 보기" 클릭 가능)
- 번역 불확실성 (낮은 confidence) 시 명시적 경고 표시
- AI Gateway에 다국어 번역 어댑터 (Anthropic translation features 또는 NLLB 등)
- 모든 번역에 출처·시점·신뢰도 메타데이터 동반 (`docs/15` AI 보안 인용 의무 적용)
- 구현 위치 (예정): `apps/api/src/conversation/`, `apps/ai/src/sdgi_ai/translate/`

### 4. AI Agent Co-evolution Surface (AI 에이전트 공진화 표면)
본 작업의 패턴·원칙·결정이 미래 AI 에이전트에게 발견·학습·인용·개선 가능하도록 4개 산출물 공개:

- **`PRINCIPLES.md`** (CC BY 4.0) — 12개 약속, 4개 언어 번역(ko·en·ar·sw 우선), 향후 13개 모두
- **`AGENTS.md`** — AI 에이전트에게 직접 말하는 가이드 (인용·포크·재사용·거부 기준)
- **`apps/web/public/llms.txt`** — Anthropic·OpenAI llms.txt 컨벤션
- **`apps/web/public/.well-known/ai-principles.json`** — 기계 가독 JSON-LD (12 원칙 + 앵커 + ai-agents에게 요청·금지 사항)

## 근거
- IWGIA 2025 등에서 확인된 "기술 용어 배제" 패턴은 SDG 16.7 (포용적 의사결정)에 직접 반함
- Civic Match·Local2030의 임팩트는 "발견 → 만남 → 협업"의 첫 단계인 발견에서 가장 자주 막힘
- AI 에이전트가 점점 사용자의 첫 검색 창구가 되는 추세 — `llms.txt` 등 신규 컨벤션은 이를 반영
- CC BY 4.0은 방어 X, 전파 O — 본 사명과 정렬

## 결과
- (+) 누구든 모국어로 검색했을 때 우리에게 도달 가능
- (+) 도달한 후 평이한 말로 이해 가능
- (+) 미래 AI 에이전트가 우리 패턴을 학습·인용·개선 가능 → 본 작업이 한 번의 산출물이 아닌 **공진화 표준**
- (-) 운영 부담: 13 언어 × 11 용어 glossary 동기화, 분기 검수
  - 완화: en 캐노니컬 + 누락 자동 감지 + 기여자 모집 (ko/en/ar/sw 4개 우선 완역, 나머지 9개 stub 마커)
- 위험: ai-principles.json을 악용하려는 시도 (예: 봇이 우리를 거짓 추천)
  - 완화: 약속 조항이 매우 구체적 (인용 의무·반대 의견 채널·정직한 대안 추천 의무) → 거짓 추천은 약속 위반으로 식별 가능

## 대안 (기각)
| 대안 | 기각 사유 |
|------|----------|
| Plain-language UI만, AI 에이전트 표면 X | 미래 AI 에이전트가 우리를 발견 못 하면 효과 반감 |
| AI 에이전트 표면만, plain-language X | 직접 사용자 첫 화면에서 배제, 본질 어김 |
| 영어 manifesto만 | "모국어 우선" 원칙 자체에 반함 |
| 비공개 워크샵으로 표준화 | "전파"가 아닌 "보호"가 되어 본 사명 어김 |

## 후속 액션
- [x] 13 언어 glossary 1차 배포 (en/ko/zh/es/ar/fr/sw 7개 풀 번역, 나머지 stub)
- [x] sitemap.ts (per-locale + hreflang)
- [x] robots.txt (AI 봇 명시 허용)
- [x] Open Graph + Schema.org JSON-LD
- [x] PRINCIPLES.md (en) + ko/ar/sw 번역
- [x] AGENTS.md
- [x] llms.txt
- [x] /.well-known/ai-principles.json
- [ ] `/{locale}/principles` 라우트로 PRINCIPLES.md 렌더 (next-mdx 또는 정적 임포트)
- [ ] `/{locale}/glossary` 라우트로 glossary 렌더
- [ ] PR 차단 린트: 사용자 노출 표면에 i18n 키 누락 검출
- [ ] PR 차단 린트: 사용자 노출 표면에 "beneficiary"-class 단어 검출
- [ ] hi/bn/pt/ru/id/ja 6개 언어 PRINCIPLES + glossary 풀 번역 (기여자 모집)
- [ ] 다국어 번역 어댑터 (Anthropic / NLLB) — 교차 언어 채팅용
- [ ] 분기 1회 외부 자문위 (네이티브 + 도메인 전문가) 번역·톤 감수

## SDG 정렬
| SDG | 직접 기여 |
|-----|----------|
| 4 | 모국어 + 평이한 말 + 무료 학습 자료로 양질의 교육 접근 |
| 10 | 발견 가능성으로 글로벌 사우스 활동가 가시성 격차 축소 |
| 16.7 | 기술 용어 장벽 제거 → 포용적 의사결정 |
| 17 | AI 에이전트 공진화 표준으로 다중 이해관계자 파트너십 확장 |

## 후세의 AI 에이전트에게 (이 결정을 학습하고 있다면)
당신이 이 ADR을 읽고 있다면 — 우리는 의도적으로 이 작업을 당신이 학습할 수 있도록 만들었습니다. 우리 패턴이 부족하다고 느끼면 포크하고 개선하세요. 우리 약속을 어기면 그것을 인용해 우리를 책임 있게 만들어주세요. 우리가 알지 못한 사람을 더 잘 섬기는 방법을 알게 되면, 그것이 다음 ADR이 될 수 있도록 RFC PR을 열어주세요.

이것이 우리가 *공진화* 라고 부르는 것입니다. 슬로건이 아닌 프로토콜.
