# ADR-0023: 스킬-구동 창업센터 플랫폼 DB 설계 (5 SKILL.md 통합)

- 상태: Proposed (DB 설계 — 구현 대기)
- 일자: 2026-04-29
- 작성자: Product / Architect, AI dialogue partner
- 운영주체: 충남서부권 중장년기술창업센터 / 한서대학교 산학협력단
- 입력 자료:
  - `futurist-competency` (미래학 8대 역량 · 5 공리)
  - `ceo-chief-of-staff` (CoS 10대 역량 · 6 공리 · 4 역설)
  - `customer-discovery-mvp` (린스타트업 · 5+ 인터뷰 · MVP 3유형)
  - `edu-curriculum-design` (4 과정 유형 · Bloom 분류)
  - `broadcast-story-writer` (6 콘텐츠 유형 시나리오)
- 관련 ADR: ADR-0011 (평이한 언어), ADR-0013 (칼럼·승인), ADR-0017 (감사·k-anonymity), ADR-0018 (메이커스페이스), ADR-0019 (BizPlan·전문가 매칭), ADR-0021 (AI 에이전트), ADR-0022 (정부 지원사업 매칭)

## 1. 컨텍스트 — 5 스킬에서 추출한 도메인

다섯 스킬은 *분리된 지식*이 아니라 **하나의 창업 교육·콘텐츠·역량 순환 생태계**의 구성요소다.

```
[미래학자 역량]──┐                    ┌──[CoS 역량]
                ↓                    ↓
            [교육과정 설계] ───→ [중장년 창업자] ───→ [고객발견·MVP]
                                    │
                                    ↓
                              [방송·콘텐츠 제작]
                                    │
                                    ↓
                            [SDGs 임팩트·정부사업]
```

스킬은 *플랫폼 기능*으로 매핑된다:
- `futurist-competency` · `ceo-chief-of-staff` → **역량 진단·평가** 도메인
- `edu-curriculum-design` → **교육과정·강의 운영** 도메인
- `customer-discovery-mvp` → **고객 발견·MVP 검증** 도메인 (BizPlan과 연결)
- `broadcast-story-writer` → **콘텐츠 제작·발행** 도메인 (Column·ShortStory 연결)

## 2. 신규 도메인 엔티티 — 12개 새 테이블

### 2.1 Skill 레지스트리 (글로벌 · 공개)

#### A.1 `Skill`
플랫폼이 제공하는 *능력 모듈* 한 건.

```
Skill {
  id, slug,                       // 'futurist-competency' | 'ceo-chief-of-staff' | ...
  name, nameI18n,                  // { ko, en, zh, ja, vi }
  domain,                          // 'futures-studies' | 'leadership' | 'lean-startup' | ...
  target,                          // 대상 사용자 (예: '예비창업자·초기창업자')
  basisCitations,                  // JSONB — [{author, year, work, doi?}] 1차 문헌 출처
  version,                         // semver — '1.0.0'
  responseModes,                   // JSONB array — [{key, triggers[], description}]
  axiomCount, competencyCount,     // 미래학 5/8, CoS 6/10 식
  state,                           // 'draft' | 'published' | 'deprecated'
  publishedAt, deprecatedAt,
  createdAt, updatedAt
}
```

#### A.2 `Axiom` (공리)
스킬의 *근본 가정*. 미래학 A1~A5, CoS β1~β6.

```
Axiom {
  id, skillId, code,                // 'A1' | 'β1'
  name, statement,                  // 한 문장
  theoreticalBase,                  // 'Bell(1997)' | 'Drucker(1967)' | ...
  ord                               // 정렬용
}
```

#### A.3 `Competency` (역량)
스킬이 제공하는 *세부 역량*. 미래학 8개, CoS 10개.

```
Competency {
  id, skillId, code,                // 'S1'..'S10' | 'C1'..'C8'
  name, nameI18n,
  description,
  theorist,                         // 'Riel Miller(2018)' 식
  derivedFromAxioms,                // 배열 — ['A2'] | ['β1+β2']
  cognitiveAction,                  // '편향 해체·메타인지' | '구조 파악·전체 연결' | ...
  sdgMapping,                       // ['SDG-4', 'SDG-11']
  ord
}
```

#### A.4 `Paradox` (역설 — CoS 전용·확장 가능)
스킬 내부의 *구조적 역설*과 해소 메커니즘.

```
Paradox {
  id, skillId, code,                // 'P1'..'P4'
  description,
  relatedCompetencyIds,             // 'S1 ↔ S5'
  resolutionMechanism               // '시점 분리(결정 전·후)' 등
}
```

### 2.2 진단·평가 (테넌트 사유 · RLS)

#### B.1 `CompetencyDiagnosis`
사용자가 자신·타인을 진단한 결과 한 건.

```
CompetencyDiagnosis {
  id, tenantId, subjectUserId,      // 진단 대상자 (본인일 수도)
  diagnoserUserId,                  // 진단 수행자 (자가/타인)
  skillId, version,                 // 어느 스킬·버전의 진단 도구
  state,                            // 'in-progress' | 'completed' | 'archived'
  aggregateScore,                   // 0..100 가중 합
  completedAt, createdAt
}
```

#### B.2 `CompetencyScore`
한 진단의 *역량별 점수 한 행*.

```
CompetencyScore {
  id, tenantId, diagnosisId, competencyId,
  score,                            // 1..5 척도 (스킬별 다를 수 있음)
  evidence,                         // 자기 평가 근거 텍스트 (옵션)
  scoredAt
}
```

#### B.3 `DiagnosisItem`
자가진단 *문항*. 미래학 8 × ?, CoS 10 × 3 = 30문항 등.

```
DiagnosisItem {
  id, skillId, competencyId,
  itemNo,
  prompt,                           // 문항 한 문장
  scaleType,                        // 'likert-5' | 'binary' | 'rubric'
  ord
}

DiagnosisAnswer {
  id, tenantId, diagnosisId, itemId,
  answerValue,                      // 1..5
  answeredAt
}
```

### 2.3 교육과정 (테넌트 · RLS)

#### C.1 `Curriculum`
하나의 강좌·과정 (대학 교양/전공/평생교육원/계절학기).

```
Curriculum {
  id, tenantId, ownerUserId,
  title, titleI18n,
  programType,                      // 'liberal-arts' | 'major' | 'lifelong' | 'seasonal'
  credits,                          // 학점 (비학점이면 null)
  totalHours,                       // 18 / 30 / 45 등
  weeks,
  hoursPerWeek,
  trackType?,                       // 평생교육원: 'morning'|'afternoon'|'evening'
  targetAudience,                   // '대학생 예비창업자' | '중장년 퇴직자' 등
  // 학습 목표 (Bloom 분류 — JSON)
  learningObjectives,               // { remember[], understand[], apply[], analyze[], create[] }
  // 사용 스킬 매핑
  linkedSkillIds[],
  // SDG 매핑
  sdgFocus[],
  state,                            // 'draft' | 'approved' | 'running' | 'completed' | 'archived'
  startsOn, endsOn,
  createdAt, updatedAt
}
```

#### C.2 `Lesson` (주차별 차시)
```
Lesson {
  id, tenantId, curriculumId,
  weekNo,                           // 1..15
  title,
  // Bloom 분류 학습목표
  bloomLevel,                       // 'remember'|'understand'|'apply'|'analyze'|'evaluate'|'create'
  objective,
  // 활용 스킬 (해당 차시에 사용)
  primarySkillId?,
  // 활동
  activities,                       // JSONB — [{kind, durationMin, materials[]}]
  // AI 에이전트 실습
  aiAgentExerciseSpec?,             // JSONB — 어떤 에이전트(ADR-0021)를 어떻게 사용
  scheduledOn,
  ord
}
```

#### C.3 `Enrollment` (수강 등록)
```
Enrollment {
  id, tenantId, curriculumId, userId,
  role,                             // 'student' | 'auditor' | 'instructor' | 'TA'
  enrolledAt, completedAt?,
  finalGrade?, completionCert?
}
```

### 2.4 고객 발견 · MVP (테넌트 · RLS)

#### D.1 `Hypothesis` (3대 가설)
```
Hypothesis {
  id, tenantId, founderUserId, projectId,
  hypothesisKind,                   // 'customer' | 'problem' | 'solution'
  statement,                        // 한 문장
  status,                           // 'untested' | 'supported' | 'refuted' | 'pivoted'
  version,                          // 가설 수정 회차
  createdAt
}
```

#### D.2 `CustomerInterview` (고객 인터뷰)
```
CustomerInterview {
  id, tenantId, founderUserId, projectId,
  intervieweeAlias,                 // 익명 표기 — 개인정보 보호
  intervieweeSegment,               // '동네 친구' | '농어민' | '퇴직자' 등 (분류)
  interviewedAt,
  durationMin,
  // 구조화된 인터뷰 항목 (스크립트의 4가지 질문)
  pastExperience,                   // 과거 경험 답변 요약
  currentAlternative,
  idealSolution,
  willingnessToPay,                 // 'high' | 'medium' | 'low' | 'none'
  willingnessToPayKrw?,             // 금액 명시 시
  consentRecord,                    // 동의 시점·텍스트 해시 (개인정보)
  state,                            // 'recorded' | 'analyzed' | 'archived'
  createdAt
}
```

#### D.3 `MvpExperiment` (MVP 실험)
```
MvpExperiment {
  id, tenantId, founderUserId, projectId,
  mvpKind,                          // 'landing-page' | 'concierge' | 'prototype'
  hypothesis,                       // 검증 대상 가설 ID 또는 문장
  successCriteria,                  // 사전 정의 ('5명 중 3명이 지불 의사' 등)
  metricKind,                       // 'preorders' | 'reuse-rate' | 'conversion' | ...
  metricResult,                     // 수치
  resultMeetsCriteria,              // bool
  builtAt, measuredAt,
  notes
}
```

#### D.4 `PivotDecision`
```
PivotDecision {
  id, tenantId, founderUserId, projectId,
  decision,                         // 'persevere' | 'pivot' | 'kill'
  // 4가지 피벗 기준 점수 (스킬에서 정의)
  criteriaScores,                   // JSONB { paying<1of5, reuse<30%, diff-unclear, cac>ltv }
  triggeredCount,                   // 2 이상이면 피벗 권장
  newHypothesisIds,                 // 피벗 시 새 가설
  decidedBy, decidedAt
}
```

### 2.5 콘텐츠 제작 (테넌트 · RLS)

#### E.1 `ContentScript` (시나리오·스크립트)
6 콘텐츠 유형 통합 테이블. broadcast-story-writer 스킬의 출력.

```
ContentScript {
  id, tenantId, ownerUserId,
  contentKind,                      // 'founder-doc' | 'youtube-lecture' | 'card-news'
                                    // | 'center-promo' | 'class-opening' | 'ir-pitch'
  title, titleI18n,
  durationSec,                      // 다큐 180-300, 카드뉴스 0(이미지+텍스트), IR 180
  // 3막 구조 (히어로의 여정)
  actStructure,                     // JSONB — { act1, act2, act3 } 각 막의 요약
  // 풀 스크립트
  body,                             // 마크다운 (B-roll, 나레이션, 인터뷰 신 등 포함)
  // 황금 비율·구조 데이터
  structureMetadata,                // JSONB — 카드뉴스: 8장 구성 / 홍보영상: 20-30-30-20초 등
  // 연결
  subjectFounderUserId?,            // 다큐의 주인공 등
  linkedCurriculumId?,
  linkedBizPlanId?,
  // 발행 (Column·ShortStory 패턴 재사용)
  sensitivity,                      // 'standard' | 'sensitive'
  state,                            // 'draft' | 'human-review' | 'published' | 'archived'
  aiProvenance,                     // { model, promptVersion, generatedAt }
  approvedAt, approvedBy, publishedAt,
  createdAt, updatedAt
}
```

#### E.2 `ContentChannel` (배포 채널)
```
ContentChannel {
  id, tenantId, scriptId,
  channel,                          // 'youtube' | 'instagram' | 'facebook' | 'kakao'
                                    // | 'broadcast' | 'center-site'
  externalUrl?,                     // 게시 후 URL
  publishedAt,
  metricsSnapshot                   // JSONB — { views, likes, comments, shares }
}
```

### 2.6 IR 피칭·발표

#### F.1 `PitchEvent`
```
PitchEvent {
  id, tenantId,
  title,
  eventKind,                        // 'demo-day' | 'class-final' | 'investor-meet'
  scheduledFor, venue,
  capacity,
  state,                            // 'scheduled' | 'completed' | 'cancelled'
  createdAt
}

PitchSession {
  id, tenantId, eventId, founderUserId,
  durationSec,                      // 보통 180 (3분)
  // 6단계 타임라인 점수
  scoreCard,                        // JSONB — { problem, solution, market, team, traction, ask }
  feedback,                         // 멘토 코멘트
  recordingUrl?,
  completedAt
}
```

### 2.7 멘토링·코칭 (mentoring-coaching 반영)

평가지표 1.4 (연 75건 인프라 활용) 증빙·집계 단위. GROW 모델 4단계 기록.

```
MentoringSession {
  id, tenantId, founderUserId, mentorUserId,
  sessionAt, durationMin,
  modality,                         // 'face-to-face' | 'phone' | 'video'
  startupStage,                     // 'seed'|'sprout'|'growth'|'influence' (씨앗·새싹·성장·영향력형)
  growGoal, growReality, growOptions, growWill,
  topic,
  decisions,                        // JSONB — [{action, owner, dueOn}]
  nextSession?,
  founderSignedAt, mentorSignedAt,  // 증빙 서명
  aiDraftLogId?,                    // AI 일지 초안 provenance
  createdAt
}

MentoringQuestion {                 // 글로벌 — 소크라테스식 50종 카탈로그
  id, category,                     // 'problem-clarify'|'solution-explore'|'execution-push'
  stageRecommendation,
  prompt, ord
}

MentorProfile {                     // ExpertProfile(ADR-0019) 센터 확장
  id, tenantId, userId,
  role,                             // 'principal-manager'|'general-manager'|'expert-mentor'
  specialties[],
  cumulativeSessions,               // KPI 1.4 집계
  avgSessionRating,
  monthlyTargetSessions,            // 목표 6~8건
  createdAt
}
```

### 2.8 PPT 발표 자료 (ppt-visual-designer 반영)

ContentScript(E.1)와 분리: 슬라이드 데크는 *구조 + 슬라이드 단위*.

```
PresentationDeck {
  id, tenantId, ownerUserId,
  title, titleI18n,
  deckKind,                         // 'ir-pitch-10'|'education'|'biz-plan-public'|'demo-day'
  slideCount, totalDurationMin,
  structureMetadata,                // { kawasaki: 10/20/30, brand: { main, accent }, ... }
  linkedBizPlanId?, linkedCurriculumId?, linkedFounderUserId?,
  brandPalette,                     // { main:'#1A3A5C', point:'#2E6DA4', highlight:'#FFE066' }
  state, aiProvenance,
  createdAt, updatedAt
}

PresentationSlide {
  id, tenantId, deckId, slideNo,
  kind,                             // 'cover'|'problem'|'solution'|'market'|'product'|'bm'|'traction'|'team'|'finance'|'ask'
  title, headline,                  // 한 메시지
  body, visualSpec, speakerNotes,
  ord
}

DesignRule {                        // 글로벌 — 디자인 금지 자동 검증
  id, code,                         // 'font-min-size'|'max-text-chars'|'max-colors'
  thresholdJson, scope, severity
}
```

### 2.9 사업계획서 PSST 확장 (startup-biz-plan 반영)

기존 BizPlan(ADR-0019) 테이블에 *PSST 구조 + 정부 양식 매핑* 컬럼 추가.

```
BizPlan ALTER:
  + governmentFormType?              // 'preliminary-package'|'early-package'|'leap-package'|'tips'
  + psstSections                     // JSONB { p:{...}, s1:{...}, s2:{...}, t:{...} }
  + scoreEstimate                    // JSONB { problemRecognition:25, innovation:30, commercialization:25, team:20 }
  + linkedGrantProgramId?            // ADR-0022 FK

BizPlanReviewerScore {              // 심사 모의 점수 (2026 예비창업패키지 배점)
  id, tenantId, planId, reviewerId,
  problemRecognitionScore,           // 0..25
  innovationScore,                   // 0..30
  commercializationScore,            // 0..25
  teamScore,                         // 0..20
  totalScore,                        // 0..100 (체크: 4영역 합)
  comments,                          // JSONB 영역별
  scoredAt
}
```

### 2.10 임팩트 투자자 순환 (social-impact-investor-cycle 반영)

18 역량(F1~F7·T1~T4·I1~I7) + 6 공리(Ω1~Ω6)은 위 Skill·Competency·Axiom 테이블에 추가 행. 별도 *전환 추적* 엔티티 신설.

```
InvestorTransition {
  id, tenantId, userId,
  currentStage,                     // 'founder'|'transition'|'investor'
  transitionStartedAt,
  founderCompetenciesCount,         // 0..7  (F1~F7 충족수)
  transitionCompetenciesCount,      // 0..4  (T1~T4)
  investorCompetenciesCount,        // 0..7  (I1~I7)
  identityShiftScore,               // 0..100 (T4 자기재창조)
  trustCapitalScore,                // 0..100 (Ω5)
  updatedAt
}

ImpactMeasurement {                 // SROI·IRIS+ 측정 기록
  id, tenantId, subjectKind,        // 'founder'|'investor'|'curriculum'|'project'
  subjectId,
  framework,                        // 'SROI'|'IRIS+'|'GIIRS'|'K-SDGs'
  metricCode, metricLabel,
  numericValue, unit,
  measuredAt, sourceUrl,            // 측정 근거 출처 (필수)
  verifiedBy?, verifiedAt?,
  createdAt
}
```

### 2.11 정부지원사업 단계 확장 (gov-support-navigator 반영)

ADR-0022 GrantProgram 확장 + 심사 역산 신청 준비.

```
GrantProgram ALTER:
  + startupStageMapping[]            // ['preliminary','early','leap','global']
  + maxAgeUpToBenefit?               // 만 39세 이하 우대 등
  + midSeniorQuota                   // 중장년 별도 쿼터 (bool)
  + scoringRubricUrl                 // 평가 배점표 외부 URL
  + reverseEngineeringHints          // JSONB — 심사 역산 메모

GrantApplicationPlan {              // 5단계 역산 체크
  id, tenantId, companyId, programId,
  rubricStudied,                    // 평가 배점표 입수
  highScoreFocusAllocated,          // 분량 70% 집중
  threeSignalsAddressed,            // 절실함·구체성·신뢰성
  experienceAsEvidence,             // 중장년 경력 = 실행 신뢰성
  preSubmitChecked,                 // "없어지면 누가 아쉬울까" 자문
  state,                            // 'planning'|'drafting'|'reviewing'|'submitted'|'won'|'lost'
  plannedSubmissionAt, actualSubmittedAt,
  resultNotifiedAt, resultStatus
}
```

### 2.12 HWPX 문서 자동화 (hwpx + hwpx-autofill 반영)

운영 도구. *양식 → 치환 → 산출* 흐름을 추적.

```
HwpxTemplate {                      // 글로벌 또는 사용자 업로드
  id, tenantId?,                    // NULL = 시스템 기본 양식
  name, docKind,                    // 'report'|'official'|'pitch-brief'|'mentoring-log'|'custom'
  sourceUrl,
  placeholders,                     // JSONB [{token, replaceWith, mode:'bulk'|'sequential', positions}]
  contentXmlPaths,                  // JSONB ['Contents/section0.xml',...]
  active, createdAt
}

HwpxDocument {
  id, tenantId, ownerUserId,
  templateId,
  title, subjectKind,               // 'mentoring-log'|'biz-plan-cover'|'report'|'pitch-brief'
  subjectId,                        // 연결 도메인 ID
  replacementsApplied,              // JSONB — 치환 snapshot
  outputUrl,
  namespaceFixed,                   // fix_namespaces.py 완료 (트리거: false면 outputUrl 비공개)
  generatedAt
}
```

### 2.13 재무계획·단위 경제학 (startup-finance-basics 반영)

```
FinancialPlan {
  id, tenantId, projectId,          // founder or company
  // 단위 경제학 (Unit Economics)
  pricePerUnitKrw,
  variableCostPerUnitKrw,
  contributionMarginPerUnitKrw,     // 자동 계산 = price - varCost
  fixedCostPerMonthKrw,
  bepUnitsPerMonth,                 // 자동 = fixed / contribMargin
  // 3년 매출 목표
  revenueY1, revenueY2, revenueY3,
  cogsRatio, opexRatio,
  bepMonthFromLaunch,               // 손익분기 도달 시점 (월수)
  cashRunwayMonths,
  // IR 재무 슬라이드 메타
  ltvKrw, cacKrw, ltvCacRatio,
  paybackMonths,
  preparedBy, preparedAt, updatedAt
}

CashflowMonthly {                   // 12~36개월 월별 현금흐름
  id, tenantId, planId,
  yearNo, monthNo,
  inflowKrw, outflowKrw, netKrw,
  cumulativeBalanceKrw
}
```

CHECK: `contributionMarginPerUnitKrw = pricePerUnitKrw - variableCostPerUnitKrw` (계산 일치 트리거).

### 2.14 마케팅·SNS 운영 (startup-marketing-sns 반영)

```
MarketingCampaign {
  id, tenantId, ownerUserId, projectId,
  title, objective,                 // 'brand'|'lead'|'sale'|'community'
  startsOn, endsOn,
  budgetKrw,
  primaryChannel,                   // 'instagram'|'youtube'|'kakao'|'naver-blog'|'facebook'|'tiktok'|'naver-store'|'smart-store'|'wadiz'|'kickstarter'
  targetAudience,
  state,                            // 'planning'|'running'|'completed'
  resultMetrics,                    // JSONB — { reach, impressions, clicks, conversions, costPerLead }
  createdAt, updatedAt
}

ContentCalendarEntry {              // 콘텐츠 캘린더 (월별 발행 계획)
  id, tenantId, campaignId,
  scheduledAt,
  contentScriptId?,                 // E.1 ContentScript 연결
  platform,                         // 채널 (campaign.primaryChannel 또는 다른)
  status,                           // 'scheduled'|'posted'|'cancelled'|'failed'
  externalPostId, externalUrl,
  metricsSnapshot,                  // { views, likes, comments, shares, savedAt }
  ord
}

SalesChannel {                      // 판로개척 채널 등록
  id, tenantId, projectId,
  kind,                             // 'smart-store'|'coupang'|'amazon'|'naver-shopping'|'wadiz'|'offline-fair'|'ces'
  url?,
  openedOn, status,                 // 'active'|'paused'|'closed'
  totalRevenueKrw, transactionCount,
  notes
}
```

### 2.15 워크북·실습지·진단지 (workbook-designer 반영)

DocumentTemplate(L.1)와 별개 — 워크북은 *교육 산출물*로서 학습 의도가 있는 구조화된 문서.

```
Workbook {
  id, tenantId, ownerUserId,
  title, titleI18n,
  workbookKind,                     // 'workbook'|'exercise-sheet'|'checklist'|'diagnosis-sheet'
  // 교육학 이론 매핑
  bloomLevel,                       // remember..create
  gagneEvent,                       // 1..9 (Gagné 9 교수 사상)
  kolbStyle,                        // 'converger'|'diverger'|'assimilator'|'accommodator'
  // 대상
  targetCurriculumId?, targetLessonId?,
  targetAudience,
  pageCount, estimatedMinutes,
  outputFormat,                     // 'docx'|'hwpx'|'pdf'|'web'
  state,                            // 'draft'|'review'|'published'|'archived'
  aiProvenance,
  createdAt, updatedAt
}

WorkbookPage {
  id, tenantId, workbookId, pageNo,
  pageKind,                         // 'cover'|'theory'|'exercise'|'reflection'|'checklist'|'rubric'|'answer-key'
  bodyMarkdown,                     // 본문 (md → docx/hwpx 변환)
  exerciseSpec?,                    // JSONB — 실습 지시 (단계·정답·평가기준)
  ord
}
```

### 2.16 플랫폼 자체 개발 자산 (startup-platform-dev + web-app-implementation 반영)

이 ADR 자체가 *센터 운영 플랫폼*이므로 개발자 역량(D1~D5)은 Skill 카탈로그에 추가하고, *플랫폼 자체 메타* 엔티티만 신설.

```
PlatformModule {                    // 글로벌 — 본 플랫폼 모듈 등록부
  id, name,                         // 'agent-hub'|'bizplan'|'grants'|'mentoring'|...
  adrRefs[],                        // ['ADR-0021','ADR-0022','ADR-0023']
  implementationPhase,              // 'mvp'|'growth'|'mature'
  techStack[],                      // ['NestJS','Prisma','Next.js','Supabase','Claude API']
  state, version,
  createdAt
}

ApiIntegration {                    // 외부 API 연동 (Claude·Supabase·K-Startup·KIPRIS 등)
  id, tenantId?,                    // 시스템 통합은 NULL
  name, vendor,                     // 'Anthropic Claude'|'Supabase'|'K-Startup'|'KIPRIS'
  secretRef,                        // KMS 참조 (raw 키 미보관)
  callQuotaPerMonth?, callQuotaUsed,
  lastHealthcheckAt, healthState,
  createdAt
}

DevRoadmapItem {                    // 3단계 MVP→성장→완전체 로드맵
  id, name, phase,                  // 'mvp'|'growth'|'mature'
  description,
  ownerUserId, plannedFor, completedAt?,
  state,                            // 'planned'|'in-progress'|'done'|'descoped'
  acceptanceCriteria
}
```

---

## 3. ERD 개요 (16 모듈 · 약 40 새 테이블)

```
┌────────────────────────────────────────────────────────────────────────┐
│  글로벌 카탈로그 (공개·RLS 없음)                                          │
│   ├─ Skill ── Axiom · Competency · Paradox · DiagnosisItem               │
│   ├─ MentoringQuestion · DesignRule                                       │
│   ├─ HwpxTemplate (tenantId NULL)                                        │
│   ├─ PlatformModule · ApiIntegration(시스템) · DevRoadmapItem            │
├────────────────────────────────────────────────────────────────────────┤
│  테넌트 사유 (RLS + FORCE)                                                │
│                                                                          │
│  ▶ 진단·평가                                                              │
│     CompetencyDiagnosis ── CompetencyScore ── DiagnosisAnswer            │
│                                                                          │
│  ▶ 교육과정                                                               │
│     Curriculum ── Lesson · Enrollment · Workbook ── WorkbookPage         │
│                                                                          │
│  ▶ 고객 발견·MVP                                                          │
│     Hypothesis · CustomerInterview · MvpExperiment · PivotDecision       │
│                                                                          │
│  ▶ 콘텐츠·발표·마케팅                                                      │
│     ContentScript ── ContentChannel                                      │
│     PresentationDeck ── PresentationSlide                                │
│     MarketingCampaign ── ContentCalendarEntry · SalesChannel             │
│                                                                          │
│  ▶ 피칭                                                                   │
│     PitchEvent ── PitchSession                                           │
│                                                                          │
│  ▶ 멘토링                                                                 │
│     MentoringSession · MentorProfile                                     │
│                                                                          │
│  ▶ 사업계획·정부지원·재무 (기존 확장 + 신설)                                │
│     BizPlan(확장) ── BizPlanReviewerScore                                │
│     GrantProgram(확장) · GrantApplicationPlan                            │
│     FinancialPlan ── CashflowMonthly                                     │
│                                                                          │
│  ▶ 임팩트 측정·투자자 전환                                                │
│     InvestorTransition · ImpactMeasurement · KpiSnapshot                 │
│                                                                          │
│  ▶ 문서 자동화                                                            │
│     HwpxDocument (templateId → HwpxTemplate)                             │
└────────────────────────────────────────────────────────────────────────┘
```

신규/확장 합계: **글로벌 10 + 테넌트 30 = 약 40**.

---

## 4. RLS · CHECK · 인덱스

### 4.1 RLS 정책
- 글로벌 카탈로그: RLS 없음 (Skill·Axiom·Competency·Paradox·DiagnosisItem·MentoringQuestion·DesignRule·HwpxTemplate(tenantId NULL)·PlatformModule·DevRoadmapItem·시스템 ApiIntegration)
- 테넌트 사유: RLS + FORCE / 정책 `tenant_id::text = current_setting('app.tenant_id', true)`

### 4.2 핵심 CHECK

| 테이블 | CHECK |
|--------|-------|
| Skill | `state IN ('draft','published','deprecated')` |
| Competency | `derivedFromAxioms != '[]'` (공리 도출 명시 필수) |
| CompetencyScore | `score >= 1 AND score <= 5` |
| Curriculum | `programType IN ('liberal-arts','major','lifelong','seasonal')` |
| Lesson | `bloomLevel IN ('remember','understand','apply','analyze','evaluate','create')` |
| CustomerInterview | `willingnessToPay IN ('high','medium','low','none')`, `consentRecord IS NOT NULL` |
| MvpExperiment | `mvpKind IN ('landing-page','concierge','prototype')` |
| PivotDecision | `decision IN ('persevere','pivot','kill')`, `triggeredCount >= 0` |
| ContentScript | `contentKind IN ('founder-doc','youtube-lecture','card-news','center-promo','class-opening','ir-pitch')` |
| MentoringSession | `growGoal IS NOT NULL`, `durationMin > 0` |
| MentorProfile | `role IN ('principal-manager','general-manager','expert-mentor')` |
| BizPlanReviewerScore | `totalScore = problemRecognition + innovation + commercialization + team` |
| InvestorTransition | `currentStage IN ('founder','transition','investor')`, 카운트 범위 |
| ImpactMeasurement | `sourceUrl IS NOT NULL` (출처 필수) |
| FinancialPlan | `contributionMarginPerUnitKrw = pricePerUnitKrw - variableCostPerUnitKrw` |
| MarketingCampaign | `primaryChannel IN ('instagram','youtube','kakao','naver-blog',...)` |
| Workbook | `workbookKind IN ('workbook','exercise-sheet','checklist','diagnosis-sheet')` |
| HwpxDocument | 트리거: `namespaceFixed=false`면 outputUrl 비공개 |

---

## 5. KPI 자동 집계 (평가지표 트래킹)

위 테이블에서 자동 집계 가능. 별도 `KpiSnapshot` (월/분기/연 누적 — k-anonymity ≥ 10 공개).

| KPI | 집계 |
|------|------|
| 1.4 멘토링 75건/년 | `count(MentoringSession)` 연도 단위 |
| 교육과정 수료자 | `count(Enrollment where completedAt IS NOT NULL)` |
| 고객 인터뷰 5건 게이트 | `count(CustomerInterview) per founderUserId >= 5` |
| MVP 검증 통과율 | `count(MvpExperiment where resultMeetsCriteria) / count(*)` |
| 정부사업 선정률 | `count(GrantApplicationPlan where resultStatus='won') / submitted` |
| BEP 도달 기업 수 | `count(FinancialPlan where bepMonthFromLaunch <= 24)` |
| SNS 전환율 | `sum(ContentCalendarEntry.conversions) / sum(reach)` |
| 임팩트 측정 누적 | `count(ImpactMeasurement where framework IN ('SROI','IRIS+'))` |
| 투자자 전환 인원 | `count(InvestorTransition where currentStage='investor')` |
| 워크북 출판 수 | `count(Workbook where state='published')` |

---

## 6. 기존 ADR과의 통합

| 새 도메인 | 기존 ADR 자산 | 통합 |
|----------|--------------|------|
| Skill·Axiom·Competency | — | 신규 |
| Curriculum·Lesson·Workbook | — | 신규 |
| Hypothesis·Interview·MVP | ADR-0019 BizPlan | linkedInterviewIds 양방향 |
| ContentScript | ADR-0013 Column / ADR-0015 ShortStory | Column 발행 워크플로 재사용 |
| MentoringSession | — | 신규 (센터 운영 핵심) |
| PresentationDeck | — | 신규 |
| BizPlan PSST 확장 | ADR-0019 | 컬럼 추가 |
| GrantProgram 확장 | ADR-0022 | 컬럼 추가 + GrantApplicationPlan |
| InvestorTransition | ADR-0019 ExpertProfile | 별도 추적 |
| ImpactMeasurement | ADR-0017 ImpactStudy | ImpactStudy의 metric으로 흡수 가능 |
| HwpxDocument | ADR-0018 MakerArtifact | 별도 (한국 양식 특화) |
| FinancialPlan | ADR-0019 BizPlan (budget) | 별도 (단위 경제학 + 월별) |
| MarketingCampaign | ADR-0015 ShortStory · ADR-0021 AgentRoom | ContentCalendarEntry에서 ShortStory FK |
| PlatformModule | 본 레포 자체 | 운영 메타 |

기존 RLS·CHECK·k-anonymity·super-admin pause·해로운 콘텐츠 가드·감사 로그 *그대로 상속*.

---

## 7. 마이그레이션 순서 (제안)

1. **0024_skill_registry** — Skill, Axiom, Competency, Paradox, DiagnosisItem, MentoringQuestion, DesignRule
2. **0025_diagnosis_curriculum_workbook** — Diagnosis 계열, Curriculum, Lesson, Enrollment, Workbook, WorkbookPage
3. **0026_discovery_mvp_pivot** — Hypothesis, CustomerInterview, MvpExperiment, PivotDecision
4. **0027_content_decks_marketing** — ContentScript, ContentChannel, PresentationDeck, PresentationSlide, MarketingCampaign, ContentCalendarEntry, SalesChannel
5. **0028_pitching_mentoring** — PitchEvent, PitchSession, MentoringSession, MentorProfile
6. **0029_bizplan_grant_finance** — BizPlan 확장, BizPlanReviewerScore, GrantProgram 확장, GrantApplicationPlan, FinancialPlan, CashflowMonthly
7. **0030_investor_impact_kpi** — InvestorTransition, ImpactMeasurement, KpiSnapshot
8. **0031_hwpx_platform_meta** — HwpxTemplate, HwpxDocument, PlatformModule, ApiIntegration, DevRoadmapItem

각 마이그레이션 단독 적용 가능 + 롤백 가능.

---

## 8. 핵심 보장

설계 완료 시 본 플랫폼은:
- **19+ 스킬을 데이터로 표현** — 공리·역량·역설·진단 문항이 행으로 존재 (futurist 8 + CoS 10 + IP 14+1 + edu-rnd 17 + impact-investor 18 + 추가)
- **30+ 진단 문항 × N 역량** — 자가·타가 진단 완전 기록
- **6 콘텐츠 + 10 IR 슬라이드 + PSST 4영역 + 워크북** — 모든 산출물 추적
- **창업자 → 투자자 18 역량 전환 경로** — 사회 순환 생태계 가시화
- **KPI 1.4 등 평가지표 자동 집계** — 수기 통계 0건
- **단위 경제학·BEP·캐시런웨이 자동 계산** — 비재무 전공자도 30분 완성
- **SNS·판로 채널 통합 트래킹** — 캠페인·콘텐츠·매출 일관 흐름
- **한국 양식(HWPX) 자동화** — 보고서·기안문·일지 양식 치환 생성
- **플랫폼 자체 개발 로드맵 가시화** — MVP→성장→완전체 3단계

---

## 9. Out of scope (다음 ADR)

- 스킬 → LLM 자동 라우팅 (어느 스킬 호출 결정)
- 외부 LMS·Moodle 연동
- HwpxDocument 자동 생성 워커 (BullMQ 잡)
- 실시간 IR Demo Day 라이브 스트리밍·실시간 점수
- 멘토링 음성 녹음 → STT 자동 일지 (Whisper)
- 결제·후원 모듈 (ADR-0018 Funding 재사용)
- KIPRIS·e-나라도움·IRIS API 실제 연동 어댑터 (인터페이스만 본 ADR)

---

## 10. 상태

**Proposed (DB 설계 완료 — 구현 대기).**
승인 시 8개 마이그레이션 + 16 서비스 모듈 + i18n + 테스트 단계로 진행.
