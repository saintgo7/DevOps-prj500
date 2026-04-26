# ADR-0018: SDG 실천가 자금 연결 (크라우드펀딩·임팩트투자) + 메이커스페이스 + 전 세계 구호·나눔 물품 매칭

- 상태: Accepted (MVP 구현 시작; 단계적 통합)
- 일자: 2026-04-26
- 작성자: Product / Architect, AI dialogue partner
- 관련 문서: ADR-0010 (피어 매칭), ADR-0012 (위클리 모니터링), ADR-0013 (승인), ADR-0016 (특허 전략·비영리), ADR-0017 (연구·도서·임팩트 검증)

## 컨텍스트

ADR-0017까지 본 플랫폼은 **발견 → 큐레이션 → 연구 → 도서 → 임팩트 검증**의 흐름을 갖추었다. 그러나 발견된 좋은 아이디어가 *실제로 실현되려면* 세 가지 자원이 필요하다:

1. **자금** — 지역·국가별 SDG 실천가가 제안서를 공개하면 기부·후원·임팩트 투자를 연결할 수 있어야 한다.
2. **도구** — 실천가가 필요한 웹·앱·모바일 도구를 *코드를 처음부터 짜지 않고* 만들 수 있어야 한다.
3. **물질** — 어느 지역에서 "이런 구호 물품·제품이 필요하다"고 알리면, 전 세계가 그 정보를 공유하고 제공자와 매칭될 수 있어야 한다.

세 영역의 공통 규범: **본 플랫폼은 절대 돈·물품의 *수탁자*가 되지 않는다.** 우리는 *조정 레이어(coordination layer)* 다. 결제·배송은 외부 파트너(스트라이프, 한정 토스, 우체국, NGO 물류 등)가 맡고, 본 플랫폼은 *발견·매칭·증빙·감사*를 책임진다.

## 결정

세 도메인 모두 "비영리 명시", "k-anonymity 기반 통계 공개", "사기 방지 검수 게이트", "공평성 가중(LDC 우선)" 의 4대 원리를 공유한다. 세 도메인 각각의 상세는 아래.

---

### A. 자금 연결 (Funding) — `apps/api/src/funding/`

#### 1. 도메인 모델

```
FundingProposal (1) ─── (N) FundingMilestone
       │
       ├── (N) FundingContribution
       └── (N) FundingReport
```

- `FundingProposal` — 제안서 한 건
  - 상태 머신: `draft → review → live → funding_locked → completed → reported` / `cancelled` / `refunded`
  - 자금 모델: `'all-or-nothing'` (목표 미달이면 환불) | `'keep-it-all'` (모인 만큼 사용)
  - 기여 유형 허용 셋: `'donation'` / `'impact-investment'` / `'in-kind'` 중 하나 이상
  - 비영리 의무: `noncommercialNotice = true` 필수 (DB CHECK)
  - 목표/마감: `softGoalMinor` (소프트 캡, 통화 minor unit), `hardGoalMinor` (도달 시 즉시 잠금), `currency`, `endsAt`
- `FundingMilestone` — 목표 단계 (escrow 개념)
  - 자금은 *마일스톤별로* 풀린다. 처음부터 한꺼번에 못 받음.
  - 마일스톤 검증: 증빙(영상·사진 해시·외부 URL) + 인간 검토자 2명 승인
- `FundingContribution` — 한 번의 후원
  - 익명성: `'public'` | `'pseudonymous'` | `'private'` (기본 private)
  - 외부 결제 ID는 보관, *카드/계좌 raw 데이터는 절대 보관 X*
  - 환불 가능 윈도우: 마일스톤 첫 풀림 전까지
- `FundingReport` — 사후 임팩트 보고
  - `ImpactStudy` (ADR-0017)와 선택적으로 연결 — 후원자가 자기 돈이 어떤 변화를 만들었는지 검증된 데이터로 본다.

#### 2. Hard rules (서비스 레이어)

1. `live` 상태로 전환은 admin 2-of-N 승인 + 비영리 명시 + 마일스톤 ≥ 1개 확인.
2. 한 번 `live`가 되면 본문(소개·예산·마일스톤) **수정 불가** — 정정은 `addendum` 레코드로만.
3. `keep-it-all` 모델은 LDC-우선 카테고리에서만 허용 (긴급 구호 성격일 때).
4. 환불은 *모든 미사용 잔액*만 가능 — 이미 풀린 마일스톤은 회수 불가.
5. 한 후원자의 단일 기여 상한 = `hardGoalMinor` 의 25% (단일 큰손이 의사결정 좌우 방지).
6. 본 플랫폼은 *수탁하지 않는다* — `paymentProviderRef`만 보관, 자금 흐름은 외부 결제사 webhook으로 추적.

#### 3. 사기·악용 방지

- `FundingFlag` — 누구나 신고 가능 (사유 ≥ 30자).
- super-admin은 `live` 단계 제안서를 즉시 일시정지 가능 (사유 영구 보존, ADR-0016 패턴 재사용).
- 일시정지 동안 신규 후원 차단, 기존 후원자는 환불 옵션 활성화.

---

### B. SDG 실천가용 메이커스페이스 (Maker) — `apps/api/src/maker/`

"실천가가 코드를 처음부터 안 짜고도 자기에게 필요한 도구를 만든다."

#### 1. 도메인 모델

```
MakerTemplate ─── (N) MakerProject ─── (N) MakerArtifact
                          │
                          └── (N) MakerContributor
```

- `MakerTemplate` — 플랫폼 큐레이션된 시작 템플릿
  - 종류: `'static-site'` | `'next-app'` | `'pwa'` | `'mobile-rn'` | `'data-dashboard'` | `'sms-bot'` | `'whatsapp-bot'`
  - 모든 템플릿이 기본 탑재: i18n (13 locale), 멀티테넌시 RLS, plain-language UI 기본값, 윤리 톤 라이브러리, 해로운 콘텐츠 가드
  - `licenseSpdx` — 'MIT' | 'Apache-2.0' | 'CC-BY-NC-SA-4.0' 등
  - 활성 상태 + 제거(retire) 기능
- `MakerProject` — 한 사용자/팀의 프로젝트
  - `templateId` — 시작 템플릿
  - 상태 머신: `'scaffolding' → 'building' → 'review' → 'live' → 'archived'`
  - `targetRegions` — LDC 가중 적용
  - 비영리 의무: `noncommercialNotice = true` (`live` 전환 게이트)
- `MakerContributor` — 공동 빌더
- `MakerArtifact` — 빌드 산출물
  - `kind`: `'repo'` (Git URL) | `'bundle'` (S3 ref) | `'preview'` (URL)
  - `contentHash` — 위변조 검증
  - 자동 생성된 산출물에는 *항상* "AI-assisted, content standard v{n}, ethics tones library" 워터마크 메타데이터 포함

#### 2. Hard rules

1. `live` 전환 전, 자동 검사: 라이선스 spdx 필수, README plain-language 점수 ≥ 60, 모든 폼/페이지에 *최소 영어 + 1개 LDC 언어* 포함.
2. 사용자가 만든 앱이 본 플랫폼 API와 통신할 경우, 본 플랫폼의 *비영리 게이트와 동의 텍스트*를 그대로 노출해야 한다 (라이선스 조건).
3. AI 보조로 생성된 코드 라인은 `aiProvenance` 메타에 모델·프롬프트 버전 기록.
4. 사용자가 자기 앱을 partner 앱으로 제출하면 ADR-0013 partner approval 흐름을 그대로 탄다.

---

### C. 구호·나눔 물품 매칭 (Needs / Offers / Match) — `apps/api/src/needs/`

"어느 지역에서 무엇이 필요하다고 알리면 전 세계가 보고, 줄 수 있는 사람과 매칭된다."

#### 1. 도메인 모델

```
NeedRequest (1) ◀──── NeedMatch ────▶ (1) OfferListing
                            │
                            └── (1) NeedFulfillment
```

- `NeedRequest` — 한 건의 필요 요청
  - 카테고리: `'relief'` (긴급 구호) | `'supplies'` (소모품) | `'equipment'` (설비) | `'knowledge'` (지식·전문가) | `'volunteers'` (자원봉사)
  - 정량: `quantity`, `unit`, `urgency` (`'critical'` | `'high'` | `'normal'` | `'low'`), `neededBy` (마감)
  - 위치: `region` (ISO-3166), `subregion` (선택, 평문)
  - 상태: `'draft'` → `'published'` → `'matching'` → `'fulfilled'` → `'closed'` / `'cancelled'` / `'expired'`
  - 신원 검증 수준: `'verified'` (NGO 인증·정부 발급 등) | `'community-vouched'` (다른 NGO 보증) | `'unverified'`
- `OfferListing` — 한 건의 제공 가능
  - `NeedRequest`와 같은 모양
  - `availableUntil` (제공 가능 기한)
- `NeedMatch` — 매칭 한 건
  - 상태: `'suggested'` (시스템·인간 추천) → `'contacted'` (양측이 연락 시작) → `'accepted'` → `'shipped'` → `'delivered'` / `'cancelled'`
  - 양측이 `accepted` 하기 전에는 *상대방 연락처가 노출되지 않는다* — 플랫폼 내부 보안 채널만 사용
- `NeedFulfillment` — 최종 증빙
  - 배송 추적 ID, 사진·영상 해시, 양측 서명(electronic signature: timestamp + agreedClauseHash)

#### 2. Hard rules — 사생활·신뢰

1. 요청자/제공자의 개인 연락처는 양측 `accepted` 상태 전까지 *서버에서도 마스킹된 상태로만 조회 가능*. accept 시점에 *amgaster pattern*으로 양측에 동시 노출.
2. 위치는 기본 `region` (국가 코드). subregion 평문 노출 동의는 별도 토글.
3. 신원 검증 수준은 상대방에게 *언제나* 표시 — 'verified' 배지를 가짜로 표기 못 하도록 발급자(`verifiedBy`)와 발급 시점(`verifiedAt`) 기록.
4. 사기 방지: 누구나 `NeedFlag` 신고 가능, super-admin은 즉시 listing 일시정지 권한.
5. LDC 가중: `urgency='critical'` + LDC region은 검색·피드에서 자동 상단.

#### 3. 정책: "절대 자동 발신하지 않는다"

본 플랫폼은 매칭을 *제안*할 뿐, 양측 사용자가 명시적으로 `contacted` 버튼을 누르기 전에는 어떤 메시지도 발송하지 않는다 (ADR-0012, ADR-0014와 동일 원칙).

---

## 데이터 모델 — 새 테이블 13개

자금: `funding_proposals` / `funding_milestones` / `funding_contributions` / `funding_reports` / `funding_flags`
메이커: `maker_templates` / `maker_projects` / `maker_contributors` / `maker_artifacts`
필요·제공: `need_requests` / `offer_listings` / `need_matches` / `need_fulfillments`

모든 테이블 RLS + tenant_id::text = current_setting('app.tenant_id', true). 단, `maker_templates`만 platform-level (tenant_id NULL 허용).

핵심 DB CHECK:
- `funding_proposals.noncommercial_notice = true`
- `funding_proposals.soft_goal_minor <= hard_goal_minor`
- `funding_contributions.amount_minor > 0`
- `need_requests.quantity > 0`
- `need_matches`의 `request_id` 와 `offer_id` 는 같은 카테고리여야 함 (FK + CHECK)

## 보안·거버넌스 핵심 규칙

1. **본 플랫폼은 자금·물품 수탁자가 아니다** — 외부 결제·물류 파트너 ID만 보관. PCI-DSS scope 회피.
2. **모든 funding `live` 전환은 2-of-N admin 승인** (ADR-0013 패턴 재사용).
3. **모든 needs `accepted` 전에는 연락처 마스킹** — 서버 응답 자체에서 빠짐.
4. **모든 maker `live` 전환은 라이선스 + 평이한 README + 다국어 검사 통과 필수.**
5. **세 도메인 모두 super-admin 즉시 일시정지권** (ADR-0016 revoke 패턴 재사용).
6. **공평성 가중**: 모든 검색·피드에서 LDC region에 +30% 우선순위 (ADR-0011/0014 동일).
7. **k-anonymity 통계**: funding/needs 공개 통계는 cohort ≥ 10 미만이면 suppressed (ADR-0017 재사용).

## 13 locale 메시지 namespace

`funding.*`, `maker.*`, `needs.*` 추가. ko / en / zh 풀 번역; ar / es / fr / sw 네이티브 번역; 나머지(bn / hi / id / ja / pt / ru) 영어 fallback + `_translationNeeded`.

## Out of scope (다음 ADR)

- 실제 결제사 통합 (Stripe Connect, Toss Payments, Razorpay 등)
- 실제 물류사 통합 (DHL Open Tracker, 우체국, NGO logistics platform)
- 메이커 템플릿 자동 빌드 파이프라인 (Worker 기반 — 별도 ADR)
- 임팩트 투자 ROI 트래킹 — funding completion → ImpactStudy 자동 연결
- 신원 검증 외부 발급기관(eIDAS, KYC partner) 연동
- 모바일 푸시·SMS 알림 (현재는 in-app + email만)
