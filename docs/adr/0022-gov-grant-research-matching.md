# ADR-0022: 정부 지원사업 리서치·매칭·융합과제 준비 플랫폼 (백엔드 설계)

- 상태: Proposed (백엔드 설계 — 구현 대기)
- 일자: 2026-04-29
- 작성자: Product / Architect, AI dialogue partner
- 관련 문서: ADR-0012 (위클리 워치·수집), ADR-0013 (칼럼·승인·알림), ADR-0017 (감사·k-anonymity), ADR-0019 (BizPlan·6축 타당성·전문가 매칭), ADR-0021 (AI 에이전트 협력)

## 컨텍스트

대한민국 중앙정부·출연기관·부처별 지원사업은 *공고가 분산*되어 있고 *자격·요건·마감*이 제각각이라, 기업이 자기에게 맞는 사업을 찾고 *융합 과제*로 준비하기가 어렵다. 본 플랫폼은:

1. **수집·분석** — 부처·출연기관 공고를 실시간 수집, 카테고리(R&D·실증·사업화·IP·오픈이노베이션·투자연계)별로 구조화.
2. **자격 판정** — 기업 프로필 대비 *결정론적 자격 검사*(업종·규모·지역·마감·중복수혜).
3. **적합도 평가** — 6축 fit score로 *어느 사업이 가장 적합한지* 순위화.
4. **융합 과제 매칭** — 단독으로 어려운 과제는 *보완 기업과 컨소시엄* 후보를 추천.
5. **사업계획 정합 분석** — 기업 BizPlan(ADR-0019)을 공고 요건과 대조해 *기술 고도화·실증·인증* 준비 격차를 도출.
6. **알림** — 기업별 필터 구독 + 일일/주간 다이제스트(ADR-0013 패턴).

핵심 원칙 (기존 자산 그대로 상속):
- **공고 정보는 공개 자산** → `program_sources`·`grant_programs`는 글로벌(테넌트 무관, SDG 카탈로그 패턴).
- **기업 데이터는 사유 자산** → `company_profiles`·`grant_matches`·컨소시엄·알림은 RLS + FORCE.
- **자동 신청 금지** — 매칭·추천은 *제안*일 뿐, 신청은 인간이 직접.
- **출처 필수** — 모든 공고는 원문 공고 URL 보존 (ADR-0017 인용 체인).
- **개인·기업정보 보호** — 재무·인력 raw 데이터는 집계 공개 시 k-anonymity(ADR-0017).

## 결정 — 도메인 모델

### A. 글로벌 카탈로그 (공개, RLS 없음)

#### A.1 `ProgramSource` — 공고 출처 피드

```
ProgramSource {
  id, name,                    // '중소벤처기업부' | 'KIAT' | 'TIPA' | ...
  agencyType,                  // 'ministry' | 'funding-agency' | 'local-tp' | 'public-institute'
  url, feedUrl?,               // 공식 사이트 + RSS/API
  kind,                        // 'rss' | 'atom' | 'html' | 'api'
  region?,                     // 'national' | '서울' | '부산' | ...
  active, lastScannedAt, failureCount,
  createdAt
}
```

#### A.2 `GrantProgram` — 지원사업 공고 한 건

```
GrantProgram {
  id, sourceId,
  title, summary,
  // 카테고리 — 본 플랫폼 핵심 분류
  category,                    // 'rnd' | 'demonstration' | 'commercialization'
                               // | 'ip' | 'open-innovation' | 'investment-linked'
  // 자격 요건 (결정론 판정용 — 구조화)
  eligibility {
    enterpriseScales[],         // ['startup'|'small'|'medium'|'mid'|'large']
    ksicCodes[],                // 한국표준산업분류 (업종)
    maxYearsSinceFounding?,     // 창업 N년 이내 (예: 7)
    regions[],                  // 허용 지역 (빈 배열 = 전국)
    maxAnnualRevenueKrw?,       // 매출 상한
    minAnnualRevenueKrw?,
    requiresConsortium,         // 컨소시엄 필수 여부
    consortiumRoles[],          // ['lead','participant','academic','research']
    excludesPriorBeneficiary,   // 기수혜 제한
    techFields[],               // 공고 기술 분야 태그
  },
  // 사업 조건
  totalBudgetKrw?, perTaskBudgetKrw?,
  selfFundingRatio?,            // 자부담 비율 (예: 0.25)
  trlRange?,                    // [min, max] 요구 TRL
  needsDemonstration,          // 실증 포함 여부
  needsCertification,          // 인증 포함 여부
  // 일정
  announcedAt, opensAt, closesAt,
  sourceUrl,                    // 원문 공고 (필수)
  // 상태
  state,                        // 'open' | 'closing-soon' | 'closed' | 'archived'
  createdAt, updatedAt
}
```

### B. 테넌트 사유 자산 (RLS + FORCE)

#### B.1 `CompanyProfile` — 기업 프로필

```
CompanyProfile {
  id, tenantId, ownerId,
  name,
  enterpriseScale,             // 'startup'|'small'|'medium'|'mid'|'large'
  ksicCodes[],                 // 업종 (복수 가능)
  foundedOn,                   // 설립일
  region,
  annualRevenueKrw?,
  headcount?,
  techFields[],                // 보유 기술 분야
  ownedIp { patents, trademarks, ... },  // 보유 IP 요약
  trl?,                        // 대표 기술 성숙도
  hasDemonstrationCapacity,    // 실증 인프라 보유
  certifications[],            // 보유 인증 (ISO, KC, GMP 등)
  priorGrants[],               // 기수혜 이력 (중복수혜 판정용)
  selfFundingCapacityKrw?,     // 자부담 가능 한도
  linkedBizPlanId?,            // ADR-0019 BizPlan 연결
  createdAt, updatedAt
}
```

#### B.2 `GrantMatch` — 기업 ↔ 공고 적합도

```
GrantMatch {
  id, tenantId, companyId, programId,
  eligibilityPassed,           // 결정론 자격 검사 결과 (bool)
  eligibilityReasons[],        // 통과/탈락 사유 (사람이 읽는 문장)
  fitScore,                    // 6축 가중 종합 (0..100)
  axisScores {                 // 각 축 0..100 + 근거
    tech, commercialization, consortium, demonstration, funding
  },
  convergenceOpportunity,      // 융합 과제 가능성 (bool + 사유)
  recommendation,              // 'apply-solo' | 'apply-consortium' | 'prepare-first' | 'skip'
  gapAnalysis[],               // 준비 격차 (기술 고도화·실증·인증)
  state,                       // 'suggested' | 'reviewing' | 'preparing' | 'applied' | 'dropped'
  computedAt
}
```

#### B.3 `ConsortiumProposal` + `ConsortiumMember` — 융합 과제 컨소시엄

```
ConsortiumProposal {
  id, tenantId, programId, leadCompanyId,
  theme,                       // 융합 주제
  convergenceFields[],         // 결합되는 기술 분야들
  state,                       // 'draft' | 'inviting' | 'formed' | 'submitted' | 'dropped'
  createdBy, createdAt
}
ConsortiumMember {
  id, tenantId, proposalId, companyId,
  role,                        // 'lead' | 'participant' | 'academic' | 'research'
  contribution,                // 담당 기술·역할
  acceptedAt?,
}
```

#### B.4 `GrantAlert` — 알림 구독

```
GrantAlert {
  id, tenantId, companyId,
  filter {                     // 구독 조건
    categories[], ksicCodes[], regions[],
    minFitScore?,              // 이 점수 이상만 알림
    onlyEligible,              // 자격 통과만
  },
  channel,                     // 'inapp' | 'email' | 'digest'
  digestFrequency?,            // 'daily' | 'weekly'
  active, lastNotifiedAt, createdAt
}
```

### C. DB CHECK 제약 (방어선)

- `grant_programs.category IN ('rnd','demonstration','commercialization','ip','open-innovation','investment-linked')`
- `grant_programs.state IN ('open','closing-soon','closed','archived')`
- `company_profiles.enterprise_scale IN ('startup','small','medium','mid','large')`
- `grant_matches.fit_score BETWEEN 0 AND 100`
- `grant_matches.recommendation IN ('apply-solo','apply-consortium','prepare-first','skip')`
- `consortium_members.role IN ('lead','participant','academic','research')`
- 컨소시엄 1개당 `role='lead'` 정확히 1개 (서비스 레이어 + 부분 유니크 인덱스)
- 모든 테넌트 테이블 RLS + FORCE / 글로벌 카탈로그(`program_sources`,`grant_programs`)는 RLS 없음

## 결정 — 적합도 스코어링 (순수 모듈, `grants/scoring.ts`)

ADR-0019 feasibility scoring과 동일 철학: *결정론 + 가중 + 가드*. AI 없이 설명 가능해야 함.

### 1. 자격 검사 (Eligibility gate — pass/fail, AI 아님)

`checkEligibility(program, company) → { eligible, reasons[] }`. 하나라도 위반이면 `eligible=false`.

| 검사 | 규칙 |
|------|------|
| 기업 규모 | `company.enterpriseScale ∈ program.eligibility.enterpriseScales` |
| 업종 | `company.ksicCodes ∩ program.eligibility.ksicCodes ≠ ∅` (공고에 업종 제한 있을 때) |
| 창업 연차 | `maxYearsSinceFounding` 있으면 `(now - foundedOn) ≤ N년` |
| 지역 | `program.regions` 비었으면 전국 허용, 아니면 `company.region ∈ regions` |
| 매출 상·하한 | `company.annualRevenueKrw` 가 `[min,max]` 범위 |
| 중복 수혜 | `excludesPriorBeneficiary` 이고 `company.priorGrants`에 동일 사업 있으면 탈락 |
| 마감 | `program.state ∈ ('open','closing-soon')` 이고 `closesAt > now` |

모든 사유는 *사람이 읽는 한국어 문장*으로 누적 (예: "창업 9년차 — 7년 이내 요건 초과").

### 2. 6축 적합도 (Fit score — 각 0..100, 가중 평균)

자격 통과(`eligible=true`)한 공고만 점수화. 자격 미통과 = `fitScore=0`.

| 축 | 가중 | 평가 |
|----|------|------|
| `eligibility` (게이트) | — | false면 전체 0 |
| `tech` | 0.30 | `company.techFields ∩ program.techFields` 중첩도 + 동일 카테고리 보너스 |
| `commercialization` | 0.20 | 매출·인력·TRL — `category='commercialization'`일수록 가중 |
| `consortium` | 0.15 | `requiresConsortium`이면 *보유 파트너·산학연 네트워크* 충족도, 아니면 중립 70 |
| `demonstration` | 0.15 | `needsDemonstration`이면 `hasDemonstrationCapacity` + 인증 이력 |
| `funding` | 0.20 | `selfFundingRatio × perTaskBudget` ≤ `company.selfFundingCapacity` 여부 |

결정론 가드 (ADR-0019 패턴 — *덧셈 보너스가 구조적 cap을 못 이김*):
- 자부담 능력 부족 → `funding ≤ 30`
- `needsDemonstration` 인데 실증 인프라 없음 → `demonstration ≤ 40`
- `requiresConsortium` 인데 파트너 0 → `consortium ≤ 35`
- 기술 분야 교집합 0 → `tech ≤ 25`
- TRL이 공고 요구 범위 밖 → `tech` 추가 -15

### 3. 추천·격차 분석

- `fitScore ≥ 70` + 단독 가능 → `recommendation='apply-solo'`
- `fitScore ≥ 55` + `requiresConsortium` 또는 융합 기회 → `apply-consortium`
- `40 ≤ fitScore < 55` → `prepare-first` (+ `gapAnalysis`: 어떤 축이 낮은지)
- `fitScore < 40` 또는 자격 미통과 → `skip`

`gapAnalysis`는 *어느 축을 어떻게 올려야 하는가*를 문장으로 (예: "실증 인프라 부재 — 테스트베드 협약 또는 리빙랩 참여로 보완 필요").

### 4. 융합 과제 기회 탐지

`detectConvergence(program, company, candidatePartners[]) → { opportunity, theme, fields[] }`:
- 공고 `techFields` 중 *기업이 못 채우는 분야*를 *다른 기업이 채울 수 있으면* 융합 후보.
- 같은 테넌트 내 또는 (동의된) 외부 기업 풀에서 보완 파트너 추천 (ExpertMatch 패턴 재사용, 연락처 마스킹).

## 결정 — API 엔드포인트 (백엔드 표면)

`@Controller('grants')` · JWT + RBAC.

### 공개 카탈로그 (읽기)

| 메서드 | 경로 | 권한 | 설명 |
|--------|------|------|------|
| GET | `/grants/programs` | 인증 | 공고 목록 (카테고리·지역·마감 필터) |
| GET | `/grants/programs/:id` | 인증 | 공고 상세 |
| GET | `/grants/sources` | admin | 출처 피드 목록 |

### 기업 프로필

| 메서드 | 경로 | 권한 | 설명 |
|--------|------|------|------|
| POST | `/grants/companies` | admin/reviewer/contributor | 기업 프로필 생성 |
| PATCH | `/grants/companies/:id` | 〃 | 수정 |
| GET | `/grants/companies/:id` | 〃 | 조회 |

### 매칭·분석

| 메서드 | 경로 | 권한 | 설명 |
|--------|------|------|------|
| POST | `/grants/companies/:id/match` | admin/reviewer | 전체 공개 공고 대비 적합도 일괄 계산 → `GrantMatch[]` 생성 |
| GET | `/grants/companies/:id/matches` | 〃 | 적합도 순 매칭 목록 (fitScore desc) |
| GET | `/grants/matches/:id` | 〃 | 매칭 상세 (축별 점수 + 격차 분석) |
| POST | `/grants/matches/:id/transition` | 〃 | 상태 전이 (suggested→reviewing→preparing→applied / dropped) |
| POST | `/grants/companies/:id/gap-analysis` | 〃 | BizPlan(ADR-0019) 대조 → 기술 고도화·실증·인증 격차 |

### 융합 컨소시엄

| 메서드 | 경로 | 권한 | 설명 |
|--------|------|------|------|
| POST | `/grants/consortiums` | admin/reviewer | 컨소시엄 제안 생성 (lead + program) |
| POST | `/grants/consortiums/:id/members` | 〃 | 멤버 추가 (role 지정) |
| POST | `/grants/consortiums/:id/transition` | 〃 | 상태 전이 |
| GET | `/grants/programs/:id/convergence` | 〃 | 융합 후보 파트너 추천 (연락처 마스킹) |

### 알림

| 메서드 | 경로 | 권한 | 설명 |
|--------|------|------|------|
| POST | `/grants/alerts` | 인증 | 알림 구독 생성 (필터) |
| DELETE | `/grants/alerts/:id` | 인증 | 구독 해지 |
| GET | `/grants/alerts/:id/preview` | 인증 | 현재 필터로 매칭되는 공고 미리보기 |

## 가드·거버넌스 핵심 규칙

| 영역 | 규칙 |
|------|------|
| 자격 판정 | 결정론 — false positive 0. 사유는 한국어 문장으로 누적 |
| 적합도 | 6축 가중 + 구조적 cap (덧셈 보너스가 cap 못 이김) |
| 자동 신청 금지 | 매칭·추천은 제안만. 신청은 인간이 직접 |
| 출처 | 모든 공고 `sourceUrl` 필수 (없으면 등록 차단) |
| 격리 | 기업 데이터 RLS + FORCE / 공고 카탈로그는 공개 |
| 연락처 마스킹 | 융합 파트너 추천 시 양측 동의 전 연락처 미노출 (ADR-0019 ExpertMatch 패턴) |
| 집계 공개 | 기업 재무·인력 집계는 k-anonymity ≥ 10 (ADR-0017) |
| 감사 | 매칭 계산·상태 전이·컨소시엄 구성 audit_events 기록 (ADR-0007) |

## 기존 모듈과의 연결

- **수집**: `ProgramSource` → Worker가 RSS/HTML/API 스캔 (ADR-0012 WatchSource 어댑터 재사용).
- **사업계획 분석**: `CompanyProfile.linkedBizPlanId` → BizPlan(ADR-0019) 6축 타당성 결과를 격차 분석 입력으로.
- **파트너 매칭**: 융합 후보 추천은 ExpertMatch 스코어링(ADR-0019) 재사용 — 도메인·지역·가용성.
- **알림**: 다이제스트는 Column 발행·Atom 피드·partner webhook(ADR-0013) 재사용.
- **AI 보조**: 공고 요약·격차 분석 초안은 AI 보조 가능 — *인용 없이 단정 금지* + provenance 기록(ADR-0019).

## 데이터 모델 — 새 테이블 7개

글로벌: `program_sources` · `grant_programs`
테넌트(RLS+FORCE): `company_profiles` · `grant_matches` · `consortium_proposals` · `consortium_members` · `grant_alerts`

## 구현 범위 (다음 단계 — 사용자 승인 후)

1. Prisma 스키마 + 마이그레이션 (RLS + CHECK + 인덱스)
2. 순수 모듈: `eligibility.ts` + `fit-scoring.ts` + `convergence.ts` (+ 각 spec)
3. 서비스: `grants.service.ts` (프로그램·기업·매칭·컨소시엄·알림) + spec
4. 컨트롤러 + 모듈 + app.module 등록
5. 13 locale 메시지 (`grants.*`)
6. 파이프라인(lint·typecheck·test·build) + 커밋·푸시

## Out of scope (별도 ADR)

- 실제 부처·기관 RSS/API 어댑터 (현재는 인터페이스만)
- e-나라도움·범부처통합연구지원시스템(IRIS) 연동
- 자동 신청서 작성 (현재는 격차 분석까지만)
- 기업 신용·재무 외부 데이터 연동 (NICE·KED)

