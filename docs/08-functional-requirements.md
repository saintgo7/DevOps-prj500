# 08. 기능 요구사항 명세 (FRD)

## 1. 모듈 개요
| 모듈 | 설명 | 우선순위 (MVP) |
|------|------|--------------|
| M1. Identity & Tenant | 인증, 조직, 사용자, RBAC | Must |
| M2. SDG Catalog | UN 17/169/232 카탈로그 | Must |
| M3. Activity & Metric | 활동·지표 CRUD, 매핑 | Must |
| M4. Data Collection | 워크플로우, 폼, 임포트 | Must |
| M5. AI Mapping | Claude 기반 추천·검증 | Must |
| M6. Report Builder | GRI/TCFD/ESRS 자동 생성 | Must |
| M7. Crosswalk Engine | 표준 간 매핑 | Should |
| M8. Audit & Evidence | 근거 추적, 감사로그 | Must |
| M9. Integrations | API, ERP/HR/회계 연동 | Should |
| M10. Analytics & Dashboard | 임팩트 대시보드 | Should |
| M11. Notifications | 알림·태스크 | Must |
| M12. Admin & Billing | 결제, 사용량, 관리 | Must |

---

## 2. Epic & User Stories

### Epic E1. Identity & Tenant
- **US-1.1**: 사용자로서, 이메일·비밀번호로 가입한다.
  - AC: 이메일 검증, 약관 동의, 비밀번호 정책(12자+ 복잡도)
- **US-1.2**: 사용자로서, SSO(Google, Microsoft)로 로그인한다.
- **US-1.3**: 관리자로서, SAML SSO를 설정한다. (Enterprise)
- **US-1.4**: 관리자로서, 사용자에게 역할(Admin/Reviewer/Contributor/Viewer)을 부여한다.
- **US-1.5**: 사용자로서, MFA(TOTP)를 활성화한다.

### Epic E2. SDG Catalog
- **US-2.1**: 사용자로서, 17개 SDG·169 Target·232 Indicator를 검색·필터링한다.
- **US-2.2**: 사용자로서, Indicator 상세(설명, 단위, 산정 방법, Tier)를 본다.
- **US-2.3**: 관리자로서, 조직 커스텀 메트릭을 만든다 (UN 카탈로그와 매핑).

### Epic E3. Activity & Metric
- **US-3.1**: 사용자로서, 활동(프로젝트·사업)을 등록하고 SDG에 매핑한다.
- **US-3.2**: 사용자로서, 활동에 시계열 데이터 포인트를 입력한다.
- **US-3.3**: 사용자로서, 데이터 포인트에 Evidence(파일, URL, 노트)를 첨부한다.
- **US-3.4**: 사용자로서, 활동을 부서·지역·세그먼트로 분류한다.

### Epic E4. Data Collection
- **US-4.1**: 관리자로서, 데이터 수집 캠페인을 만들어 부서별 담당자에게 폼을 발송한다.
- **US-4.2**: 담당자로서, 폼을 작성하거나 엑셀을 업로드한다.
- **US-4.3**: 시스템은 단위·범위·완전성 검증 규칙을 적용한다.
- **US-4.4**: 검토자로서, 제출된 데이터를 승인/반려/코멘트한다.

### Epic E5. AI Mapping (Claude)
- **US-5.1**: 사용자로서, 활동 설명을 입력하면 SDG/Target 후보 3개를 신뢰도와 함께 받는다.
- **US-5.2**: 사용자로서, AI 답변에 첨부된 인용(Citations)을 확인한다.
- **US-5.3**: 사용자로서, AI 추천을 수락/수정/거부하면 모델 학습 신호로 기록된다.
- **US-5.4**: 사용자로서, 문서(PDF) 업로드 시 자동 추출·매핑을 받는다.
- **NFR**: 추천 P95 < 5초, 정확도 F1 ≥ 0.85

### Epic E6. Report Builder
- **US-6.1**: 사용자로서, 보고 표준(GRI / SASB / TCFD / ESRS / K-ESG)을 선택하고 기간·범위를 정한다.
- **US-6.2**: 시스템은 Claude로 표준별 항목 초안을 생성한다 (각 단락에 데이터 인용 포함).
- **US-6.3**: 사용자로서, 단락별 코멘트·재생성·수정 후 승인 워크플로우로 보낸다.
- **US-6.4**: 시스템은 PDF, HTML, iXBRL(ESRS) 출력을 지원한다.
- **US-6.5**: 사용자로서, 보고서 버전 이력을 추적한다.

### Epic E7. Crosswalk Engine
- **US-7.1**: 시스템은 GRI ↔ SDG ↔ ESRS 매핑 테이블을 제공한다.
- **US-7.2**: 사용자로서, 한 데이터 포인트가 여러 표준에 어떻게 사용되는지 본다.

### Epic E8. Audit & Evidence
- **US-8.1**: 모든 변경(생성/수정/삭제)은 감사로그에 기록된다 (Who/What/When/Why).
- **US-8.2**: 외부 감사인으로서, 읽기 전용 권한으로 Evidence와 데이터 흐름을 검토한다.
- **US-8.3**: 시스템은 데이터 lineage를 시각화한다 (Source → Metric → Report).

### Epic E9. Integrations
- **US-9.1**: REST/GraphQL API로 데이터 read/write
- **US-9.2**: 사전 통합: SAP, Workday, NetSuite, Google Sheets, Salesforce
- **US-9.3**: Webhook으로 이벤트 발신

### Epic E10. Analytics & Dashboard
- **US-10.1**: 임원 대시보드: 17 SDG 점수, 핵심 KPI 트렌드
- **US-10.2**: Drill-down: Goal → Target → Indicator → Activity
- **US-10.3**: 동종업계 벤치마크 (익명 집계)

### Epic E11. Notifications
- **US-11.1**: 인앱·이메일 알림 (멘션, 승인 요청, 만기)
- **US-11.2**: Slack/Teams 채널 통합

### Epic E12. Admin & Billing
- **US-12.1**: 관리자로서, 플랜 변경·결제 수단 관리
- **US-12.2**: 사용량(저장, AI 호출) 대시보드

---

## 3. 비기능 인터페이스
- 모든 변경 액션은 i18n 키 + 감사 메시지 표준화
- API 응답 형식 RFC 7807 (Problem Details for HTTP)

## 4. 우선순위 (MoSCoW 요약)
- **Must**: M1, M2, M3, M4, M5 (기본), M6 (GRI/TCFD/K-ESG), M8, M11, M12
- **Should**: M5 (문서 업로드 추출), M6 (ESRS), M7, M10
- **Could**: M9 (사전 통합 5개), 산업 벤치마크
- **Won't (v1)**: 블록체인 검증, 탄소거래, 모바일 네이티브 앱

## 5. Definition of Done
- AC 모두 통과
- 단위 테스트 80%+, E2E 핵심 시나리오 그린
- a11y 자동 검사 (axe) 위반 0
- i18n 키 누락 0
- 보안 스캔 (Snyk) High 0
- 성능 예산 (Core Web Vitals) 통과
- PR 2명 리뷰 + 도메인 전문가 1명 (해당 시)
