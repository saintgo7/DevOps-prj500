# ADR-0019: AI 사업계획서·정책·공약·ODA 작성 + 다학제 타당성 검토 + 전문가 역량 매칭

- 상태: Accepted (MVP 구현 시작; 단계적 통합)
- 일자: 2026-04-26
- 작성자: Product / Architect, AI dialogue partner
- 관련 문서: ADR-0011 (발견·평이한 언어), ADR-0012 (위클리 모니터링), ADR-0013 (승인), ADR-0016 (특허), ADR-0017 (연구·임팩트), ADR-0018 (자금·메이커·필요)

## 컨텍스트

ADR-0018까지의 흐름: **발견 → 큐레이션 → 연구 → 도서 → 임팩트 검증 → 자금·도구·물품 매칭**. 그러나 *제안서를 잘 쓰는 능력*과 *그 제안서를 검토할 전문가를 만나는 능력*은 LDC 실천가·연구자·정책 입안자에게 가장 큰 진입 장벽이다.

이번 라운드는 세 가지 능력을 하나의 흐름으로 묶는다:

1. **AI 보조 BizPlan 작성** — 본 플랫폼에 누적된 *실시간 데이터*(특허 ADR-0016, 위클리 발견 ADR-0012, 큐레이션 칼럼 ADR-0013, 게재 논문 ADR-0017)를 근거로 SDG 관련 사업계획서·정책 제안·공약·투자 유치 자료·ODA 제안·사업 실행 계획·사업 관리 문서를 작성한다. 모든 인용은 우리 플랫폼의 1차 자료에 닿는다.
2. **다학제 타당성 검토 (Feasibility)** — 작성된 안을 영향·재무·기술·법·윤리·임팩트 6축으로 점수화, 결정론적 가드와 인간 전문가 검토를 결합.
3. **전문가 역량 매칭 (ExpertMatching)** — 같은 도메인·언어·LDC 가중을 갖는 전문가 풀에서 *연락처 마스킹된 상태로* 추천하고, 양측 명시 동의 시점에 비로소 연결.

세 영역의 공통 규범:
- **AI는 인용 없이 단정하지 않는다** — 모든 생성은 plat-source ID(WatchItem / Column / PatentInsight / Manuscript)로 추적 가능.
- **인간 검토 게이트** — `ready_for_use`로 가기 전 인간 ≥ 1명 (ODA·정책 트랙은 ≥ 2명) 승인.
- **사생활 보호** — 전문가 식별 정보는 양측 동의 전 마스킹.
- **공평성 가중** — LDC 영향이 큰 안은 우선 검토.

## 결정

### A. AI BizPlan 작성 (`apps/api/src/bizplan/`)

#### 1. 도메인 모델

```
BizPlan (1) ─── (N) BizPlanSection ─── (N) BizPlanSourceRef
                       │
                       └── (1) BizPlanFeasibility   (1:1, 한 시점의 결과물)
```

- `BizPlan` — 하나의 작성 안
  - 트랙: `'business'` (사업계획) | `'policy'` (정책 제안) | `'pledge'` (공약) | `'investment'` (투자 유치) | `'oda'` (ODA 제안) | `'execution'` (사업 실행) | `'management'` (사업 관리)
  - 상태: `'drafting' → 'ai_drafted' → 'human_review' → 'revising' → 'ready_for_use' → 'archived'`
  - 비영리 의무: `noncommercialNotice = true` 필수 (DB CHECK)
  - SDG 포커스, 지역(LDC 가중), 기간, 대상 청중
- `BizPlanSection` — 섹션 한 개
  - 종류: `'executive_summary'` | `'problem_statement'` | `'solution'` | `'theory_of_change'` | `'beneficiaries'` | `'budget'` | `'timeline'` | `'risk'` | `'monitoring'` | `'sustainability'` | `'partners'`
  - 콘텐츠: 다국어 (`bodyI18n`)
  - AI provenance: `model`, `promptVersion`, `draftedAt`, `tokensIn`, `tokensOut`
- `BizPlanSourceRef` — 인용 한 건
  - 정확히 한 source: `WatchItem` / `Column` / `PatentInsight` / `ResearchManuscript` / `externalDoi` / `externalUrl` (DB CHECK + 서비스 가드, ADR-0017 패턴 재사용)
- `BizPlanFeasibility` — 한 시점의 타당성 스냅샷

#### 2. Hard rules

1. **인용 없이 사실 단정 금지** — AI 보조로 생성된 모든 섹션은 `BizPlanSourceRef`가 ≥ 1개 (`executive_summary` 제외)
2. **트랙별 길이 제한** — `pledge`는 평이한 언어 우선, 한 섹션 ≤ 200 단어
3. **트랙별 검수자 수** — `oda` / `policy` 트랙은 인간 검토자 ≥ 2명 (한 명은 SDG 도메인 전문가)
4. **자기 인용 ≤ 20%** (ADR-0017 citation rule 재사용)
5. **트랙 전환 한 방향만** — 한 번 정한 트랙은 변경 불가; 새 트랙은 새 BizPlan으로

#### 3. AI 작성 흐름

```
사용자 입력(SDG, 지역, 트랙, 기간)
  → 플랫폼 인용 후보 자동 수집 (WatchItem · Column · PatentInsight · Manuscript)
  → Claude 호출 (PII 마스킹 후, 인용 ID 동봉)
  → 섹션별 초안 + 각 섹션의 인용 ID 회신
  → 인용 ID 검증 (실재 + 현재 published/approved 상태)
  → 검증 통과 시 'ai_drafted'로 저장
```

PII 마스킹은 ADR-0015 패턴을 재사용; AI 출력은 항상 *우리 1차 자료를 인용*하도록 system prompt에 강제.

### B. 다학제 타당성 검토 (`apps/api/src/feasibility/`)

#### 1. 6축 평가

| 축 | 의미 | 평가 방법 |
|----|------|-----------|
| `impact` | SDG 임팩트 잠재력 | 영향 인구 × 지속성 × LDC 우선순위 |
| `financial` | 재무적 지속가능성 | 예산 일관성 + 수익·자금 구조 + 마일스톤 비중 |
| `technical` | 기술적 실현 가능성 | 의존 기술의 TRL + 운영 필요 인프라 |
| `legal` | 법·규제 적합성 | 비영리 의무 + 데이터 보호 + 지적재산 사용 |
| `ethical` | 윤리적 위험 | 해로운 콘텐츠 가드 + 비대상 피해 가능성 |
| `evidence` | 증거 강도 | 인용 출처 다양성 + 출처 신뢰도 분포 |

각 축 0–100, 결정론적 룰 + (선택) 인간 보정. 가중 평균이 본 안의 `feasibilityScore`. **score < 40인 축이 하나라도 있으면 `ready_for_use` 차단**.

#### 2. 결정론적 가드 (서비스 레이어)

- **인용 0건 → evidence = 0**
- **인용 모두 자기 도메인(같은 SDG) → evidence ≤ 50** (시야 협소)
- **예산 합계 ≠ 마일스톤 합계 → financial ≤ 30**
- **비영리 명시 false → legal = 0** (즉시 fail)
- **해로운 콘텐츠 가드 fail → ethical = 0**
- **TRL ≤ 2 + 18개월 내 deployment → technical ≤ 40**

#### 3. 인간 검토자

- 각 축은 도메인 전문가가 보정 가능. 보정 사유는 영구 보존.
- ODA·policy 트랙은 보정 없는 결정론 점수만으로 ready_for_use 불가 — 인간 보정 필수.

### C. 전문가 역량 매칭 (`apps/api/src/experts/`)

#### 1. 도메인 모델

```
ExpertProfile  ─────────  ExpertCredential  (어떻게 검증됐는지)
       │
       └── ExpertMatch ─── BizPlan (또는 ImpactStudy / FundingProposal / 등)
```

- `ExpertProfile` — 한 명의 전문가
  - 도메인: SDG-1..SDG-17 + post-SDG 카테고리 멀티 태깅
  - 언어: 13 locale 멀티 태깅 (`workingLocales`)
  - 지역 경험: ISO-3166 멀티 (`fieldRegions`) — LDC 경험에 가중치
  - 가용성: `'open'` | `'busy'` | `'closed'`
  - 시간 단가는 *기록하지 않음* (비영리 + 사용자 사생활 우선)
  - 프로필 공개 수준: `'public'` (검색 노출) | `'platform-only'` (매칭에만 노출) | `'private'` (오너 동의 후 매칭) — 기본 `platform-only`
- `ExpertCredential` — 검증 출처
  - 종류: `'orcid'` | `'linkedin'` | `'official_org'` | `'community-vouched'` | `'self-reported'`
  - `verifiedBy` (admin / partner) + `verifiedAt`
  - 'verified' 등급은 self-reported로 절대 부여 불가 (DB CHECK)
- `ExpertMatch` — 한 건의 매칭
  - `subjectKind`: `'bizplan'` | `'impact_study'` | `'funding_proposal'` | `'maker_project'` | `'need_request'`
  - `subjectId`
  - 상태: `'suggested' → 'invited' → 'accepted' → 'engaged' → 'completed'` / `'declined'` / `'cancelled'`
  - 양측 동의 전 contact 마스킹 (ADR-0018 NeedMatch 패턴 재사용)
  - 매칭 알고리즘: 도메인 일치도(40%) + 언어 일치도(20%) + 지역 경험(20%) + LDC 가중(10%) + 가용성(10%)

#### 2. Hard rules

1. **자동 메시지 발송 금지** — 매칭은 *제안*, 양측이 명시 동의 후에만 연락.
2. **연락처 마스킹** — 이메일·전화는 양측 `accepted` 전 응답에 미포함.
3. **Verified 등급 자가 부여 금지** — `verifierId`/`verifiedAt`이 NULL이면 'verified' 저장 불가 (DB CHECK).
4. **편향 방지** — LDC 출신 전문가 부족 영역에서는 모집 알림(super-admin only).
5. **opt-out 즉시** — 사용자가 `closed`로 바꾸면 그 시점 이후 모든 신규 매칭 제안에서 제외.

### D. AI Provenance (모든 AI 보조 결과 공통)

- 모든 BizPlan / Feasibility 보정 / Expert 매칭 추천에는 AI 사용 시 `aiProvenance = { model, promptVersion, generatedAt, tokensIn, tokensOut }` 강제 기록.
- 사용 모델은 `claude-opus-4-7` / `claude-sonnet-4-6` 등 정확한 ID. 사용자에게 항상 *AI-assisted* 배지 노출.

## 데이터 모델 — 새 테이블 9개

BizPlan: `biz_plans` / `biz_plan_sections` / `biz_plan_source_refs` / `biz_plan_feasibility`
Feasibility: `feasibility_axis_scores` / `feasibility_reviews`
Expert: `expert_profiles` / `expert_credentials` / `expert_matches`

핵심 DB CHECK:
- `biz_plans.noncommercial_notice = true`
- `biz_plans.track ∈ {business, policy, pledge, investment, oda, execution, management}`
- `biz_plan_source_refs` 정확히 하나의 source (ADR-0017 패턴)
- `feasibility_axis_scores.score BETWEEN 0 AND 100`
- `expert_credentials.kind = 'verified'` 일 때 `verified_by IS NOT NULL AND verified_at IS NOT NULL`
- `expert_matches.subject_kind ∈ {bizplan, impact_study, funding_proposal, maker_project, need_request}`

모든 테이블 RLS + FORCE.

## 보안·거버넌스 핵심 규칙

1. **AI는 인용 없이 단정하지 않는다** — `BizPlanSourceRef` ≥ 1 (executive_summary 제외).
2. **트랙별 검수자 수** — ODA · policy 트랙은 ≥ 2명, 그중 ≥ 1명 SDG 도메인 전문가.
3. **타당성 6축 모두 ≥ 40** 이어야 `ready_for_use` 가능.
4. **연락처 마스킹** — 양측 accepted 전 마스킹.
5. **모든 매칭은 제안일 뿐** — 자동 발송 금지.
6. **Verified 등급은 외부 발급기관·관리자만 부여**.

## 13 locale 메시지 namespace

`bizplan.*`, `feasibility.*`, `expert.*` 추가. ko / en / zh 풀 번역; ar / es / fr / sw 네이티브; bn / hi / id / ja / pt / ru 영어 fallback + `_translationNeeded`.

## Out of scope (다음 ADR)

- Claude API 실제 호출 통합 (현재는 service interface + 결정론 검증만)
- ORCID OAuth 통합 (현재는 ID 입력 + 관리자 검증)
- 매칭 알고리즘 ML 튜닝 (현재는 가중 합계)
- 전문가 시간 단가 / 결제 — 본 플랫폼 범위 밖 (당사자 간)
- 매칭 결과 ImpactStudy 자동 등록
