# ADR-0017: Multidisciplinary research authoring (Nature / SSCI level) + accessible book authoring + privacy-preserving SDG-impact verification

- 상태: Accepted (MVP 구현 시작; 단계적 통합)
- 일자: 2026-04-26
- 작성자: Product / Architect, AI dialogue partner
- 관련 문서: [`PRINCIPLES.md`](../../PRINCIPLES.md), [`CONTENT_STANDARD.md`](../../CONTENT_STANDARD.md), ADR-0012 (위클리 모니터링), ADR-0013 (칼럼·승인), ADR-0014 (연구 제안), ADR-0016 (특허 전략)

## 컨텍스트

이번 라운드는 본 플랫폼이 수집해 온 모든 정보를 — 위클리 발견(ADR-0012), 큐레이션 칼럼(ADR-0013), 연구 제안(ADR-0014), 특허 전략(ADR-0016) — **세 개의 새 출구**로 흘려보낸다:

1. **연구 (Research)** — 저발전 국가의 지역·국가별 SDG 실천가에게 다학제간 통찰을 전달하기 위해 *Nature 수준*의 1차 연구 논문, *SSCI 수준*의 사회과학 논문을 본 플랫폼 안에서 공동 집필·동료심사·게재한다.
2. **도서 (Book)** — 게재된 논문과 기존 칼럼·카드뉴스를 **재사용**하여 누구나 쉽게 읽을 수 있는 도서로 엮는다 — 과학을 일상의 언어로 옮기는 것이 본 플랫폼의 의무이기 때문이다.
3. **임팩트 검증 (Impact verification)** — 본 플랫폼의 콘텐츠를 구독·좋아요한 사람들의 **사생활을 절대 침해하지 않는 범위에서 그들의 명시적 승인**을 받고, 우리가 만든 영향이 지역·국가·SDG 항목별로 달성되고 있는지를 객관적·과학적으로 검증한다. 결과는 공유·확산을 극대화한다.

세 영역의 공통 원리: **Citation chain은 깨지지 않는다.** 어느 출구든 맨 끝의 인용으로 거슬러 올라가면 우리 플랫폼의 큐레이션된 1차 자료(또는 외부 1차 자료)에 닿는다. 자기 표절·가짜 인용·복제는 차단한다.

## 결정

### A. 연구 집필 (Research authoring)

#### 1. Manuscript 상태 머신

```
        submitToInternalReview          requestExternalReview
draft ─────────────────────────▶ internal_review ─────────────────────▶ external_peer_review
   ▲                                  │                                       │
   │                                  ▼                                       ▼
   └──── revise ◀──── revise_requested ─────────────────────────── revise_requested
                                       │                                       │
                                       ▼                                       ▼
                                   accepted ──────publish──────▶ published (DOI optional)
                                       │
                                       ▼
                                   withdrawn (any state, with reason)
```

상태는 append-only. 게재된(`published`) 논문은 **수정 대신 erratum**만 허용한다. 인용 체인은 게재 시점 기준으로 freeze된다.

#### 2. Co-author / contribution roles (CRediT taxonomy)

- ORCID 필수(있으면). 없으면 `contact_email` + `affiliation` 필수.
- CRediT 14개 역할 중 골라서 기록 (Conceptualization, Methodology, Software, ...). UI는 한국어/영어 plain-language로 안내.
- 공평성 weight: 저발전국 소속 공동저자 1명 이상 — 시스템이 추천하지만 강제하지 않음(편집자 메모로 남음).

#### 3. Manuscript citations — 인용 체인 검증

본 플랫폼의 어떤 논문도 다음을 만족해야 한다:
- 인용된 모든 `Column` / `WatchItem` / `PatentInsight` / `ResearchManuscript`가 *현재 published 또는 approved 상태*.
- 외부 논문 인용은 DOI 또는 영구 URL 필수.
- 자기 인용 비율 ≤ 20% (편집자가 사유 입력 시 초과 허용).
- 인용 체인은 게재 시점에 **freeze**되어 audit log로 보관.

#### 4. Plain-language abstract

논문은 **반드시** 두 종류의 요약을 가진다:
- `scientificAbstract` — 학술 표준 (250 단어 이내, 영어 기본 + primaryLocale)
- `plainLanguageSummary` — 누구나 읽을 수 있는 5문단 이내 요약 (13개 locale 모두 — 적어도 영어 + primaryLocale + 영향 지역 LDC locale 1개 이상)

도서(B) 작업은 이 plain-language summary를 가져다 쓴다 — 같은 정보를 두 번 작성하지 않는다.

### B. 도서 집필 (Book authoring) — 재사용 우선

#### 1. BookProject + BookChapter

```
BookProject (1) ─── (N) BookChapter
```

**핵심 제약**: 각 `BookChapter`는 다음 중 **정확히 하나**의 source를 가진다:
- `sourceColumnId` — 기존 큐레이션 칼럼을 그대로 활용 (ADR-0013)
- `sourceManuscriptId` — 게재된 논문의 plain-language summary를 활용 (이 ADR §A)
- `sourceShortStoryId` — 카드뉴스/숏폼 캡션을 활용 (ADR-0015)
- `sourceWatchItemDigestId` — 위클리 다이제스트 모음(ADR-0012)
- `sourceCustom` — 위 어디에도 해당 안 되는 *순수 신규* 챕터 (편집자 사유 필수)

이렇게 하면 **이미 인간이 승인한 콘텐츠**만 도서에 들어간다. 책 한 권을 새로 쓰는 인지 부담이 *재구성* 작업으로 줄어든다.

#### 2. License & royalty

- 기본 라이선스: CC BY-NC-SA 4.0 (비영리 + 동일 조건 변경 허락)
- 인쇄 출판은 별도 partner agreement (이 ADR 범위 밖)
- 모든 챕터는 끝부분에 `attribution` 블록 — 어느 칼럼/논문/숏폼에서 왔는지를 자동 생성

#### 3. 13개 locale plain-language pass

모든 도서는 출간 전에:
- 영어 + 한국어는 **무조건** 있어야 한다 (한국어 default 정책)
- LDC 대상 도서면 해당 LDC 1차 언어 1개 이상 (예: 사하라이남 영향이면 sw or fr; 방글라데시 영향이면 bn)
- 평이한 언어 검사기는 ADR-0011/0014의 공통 모듈 사용 (Plain Language Score ≥ 60)

### C. 임팩트 검증 (Privacy-preserving impact verification)

#### 1. Consent first — opt-in only

**우리는 "구독·좋아요 = 동의" 라고 가정하지 않는다.** 우리 콘텐츠를 구독·좋아요한 사람도, 임팩트 연구에 기여하기 위해서는 **별도의 명시적 opt-in**이 필요하다.

```
ImpactConsentRecord {
  id, tenantId, userId,
  scope: { sdgFocus[], regions[], topicTags[] },   // 연구 범위
  level: 'aggregate-only' | 'longitudinal',         // aggregate-only이면 시계열 추적 불가
  expiresAt,                                        // 기본 12개월
  revokedAt,                                        // 언제든 철회 가능
  consentVersion,                                    // 동의 텍스트 버전
  agreedClauseHash                                   // 사용자가 본 정확한 텍스트 SHA256
}
```

해지 즉시 — 그 사용자의 기여는 다음 집계 사이클부터 제외된다. 기존 출판물은 timestamped audit가 남고, 그 출판물 아래에 *"Some contributors have since revoked consent; see audit log"* 표시.

#### 2. K-anonymity floor — 절대 깨지지 않는 바닥

`ImpactObservation`은 항상 **최소 cohort 크기 k=10** 이상을 충족해야 release된다. 이는:

- DB CHECK 제약: `CHECK (cohort_size >= 10)` — false면 INSERT/UPDATE 자체 실패
- 서비스 레이어 가드: `requireKAnonymity(observation)` — UI/API 출력 직전 재확인
- `ImpactStudy.publish()` 호출 시 — study에 속한 모든 observation을 다시 검사하여, k 미만 그룹이 하나라도 있으면 publish 실패

k=10은 floor — 민감 주제(`sensitiveTopic=true`)는 k=25로 자동 상향. 추후 differential privacy 노이즈는 별도 ADR로 검토.

#### 3. Aggregate boundary

- 개인 단위 데이터는 **DB 안에서도 ImpactObservation에 저장하지 않는다** — `ImpactConsentRecord` (개인) 와 `ImpactObservation` (집계) 사이에 *boundary view*가 있어, 집계 boundary를 통과한 결과만 observation에 INSERT된다.
- 집계 함수는 deterministic SQL aggregate — 모델 추론은 boundary 안 쪽에서만 호출.
- 구독·좋아요 raw event 자체는 별도 *raw_engagements* 테이블 (RLS + 30일 retention) — 집계 후 자동 삭제, 90일 이상 보관 금지.

#### 4. Study lifecycle

```
ImpactStudy: draft → enrolling → analysing → review → published → retired
```

- `draft`에서는 scope/조건만 정의
- `enrolling`에서 `ImpactConsentRecord`를 모집 (UI: "이 연구에 기여하시겠어요?")
- `analysing`에서 raw_engagements (RLS) → ImpactObservation aggregate로 boundary 통과
- `review`에서 *최소 2명의 인간 reviewer* (한 명은 도메인 SDG 전문가) approve 필요
- `published` 시점에 obs들이 freeze되며 외부 공유 가능
- `retired` 후에는 모든 raw 결합이 영구 삭제 (집계만 남음)

#### 5. Sharing maximisation under privacy

게재된 study는 다음 채널로 자동 노출 (사용자 동의 외에 새로운 동의 없이):
- Public Atom feed (CC BY 4.0) — ADR-0013과 동일 인프라
- 다국어 카드뉴스/숏폼으로 자동 변환 — ADR-0015 파이프라인 재사용
- 파트너 webhook (HMAC-SHA256) — ADR-0013

확산은 **집계 결과만**. 개인 contribution은 어디에도 노출되지 않는다.

## 코드 구조 — MVP

```
apps/api/src/
├── research/
│   ├── manuscripts.service.ts        # state machine + citation freeze
│   ├── manuscripts.controller.ts     # /research/manuscripts ...
│   ├── citations.ts                  # citation chain validator (pure)
│   ├── citations.spec.ts
│   └── research.module.ts
├── books/
│   ├── books.service.ts              # BookProject + BookChapter; reuses sources
│   ├── books.controller.ts
│   └── books.module.ts
└── impact/
    ├── consent.service.ts            # opt-in / revoke / scope match
    ├── k-anonymity.ts                # pure: enforces k=10 / k=25 floor
    ├── k-anonymity.spec.ts
    ├── studies.service.ts            # study lifecycle + observation publish gate
    ├── studies.controller.ts
    └── impact.module.ts
```

## 데이터 모델 (요약 — 자세한 마이그레이션은 `20260426300000_research_books_impact/`)

새 테이블 11개:
- `research_manuscripts` (RLS, state CHECK)
- `manuscript_coauthors`
- `manuscript_citations` (composite source ref)
- `book_projects` (RLS)
- `book_chapters` (정확히 하나의 source — DB CHECK)
- `impact_consent_records` (RLS, expires_at + revoked_at)
- `raw_engagements` (RLS, 30일 retention 인덱스)
- `impact_studies` (RLS, state CHECK)
- `impact_observations` (k-anonymity floor CHECK, foreign key to study)
- `impact_study_reviews` (2-of-N approval ledger)
- `impact_disclosures` (어느 study가 어느 partner에 어떤 시점에 공유됐는지)

## 보안 / 거버넌스 핵심 규칙

1. **Manuscript citation freeze는 게재 시점에 audit_event를 만든다** — 누구도 게재 후 인용을 변경할 수 없다.
2. **Book chapter는 source가 정확히 하나여야 한다** — `CHECK ((source_column_id IS NOT NULL)::int + (source_manuscript_id IS NOT NULL)::int + (source_short_story_id IS NOT NULL)::int + (source_watch_digest_id IS NOT NULL)::int + (source_custom IS NOT NULL)::int = 1)`.
3. **Impact observation k-floor는 DB CHECK + 서비스 가드 둘 다** — 두 곳에서 막힌다.
4. **Consent expiry는 default 12개월** — 만료된 record로는 새 study에 enroll 불가.
5. **Revoke는 cascade하지 않는다** — 이미 published된 study는 그대로지만, 다음 cycle부터 제외 + audit 표시.
6. **Plain-language summary는 manuscript publish 전 *필수*** — 영어 + primaryLocale 둘 다.

## 13 locale 메시지 namespace

`research.*`, `book.*`, `impact.*` 추가. 한국어/영어/중국어 풀 번역; 나머지 locale은 `_translationNeeded` 플래그 + 영문 fallback (ADR-0011 패턴).

## Out of scope (다음 ADR)

- Real ORCID OAuth integration (지금은 ORCID 입력 필드만)
- Differential privacy (epsilon noise) — 지금은 k-anonymity만
- DOI minter integration — 지금은 internal DOI placeholder
- 인쇄 출판 royalty pipeline
- Subscriber-side dashboard ("어떤 study에 내가 기여하고 있나?") — UI 다음 라운드
