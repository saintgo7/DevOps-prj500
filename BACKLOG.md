# 실행 백로그 (Sprint 0 / Sprint 1)

> 목적: 21개 문서가 작성된 현 시점부터 MVP 개발 시작까지의 즉시 실행 가능한 작업 목록.
> 갱신: PR로 변경, Owner 명시.

## Sprint 0 — Foundation (2주)
**목표**: 모노레포 스캐폴딩 + 인프라 베이스 + CI/CD 골격

### S0-01. 모노레포 부트스트랩 [Platform]
- pnpm + Turborepo, `apps/`, `packages/`, `infra/` 구조
- `apps/web` (Next.js 15), `apps/api` (NestJS 11), `apps/ai` (FastAPI)
- `packages/types`, `packages/ui`, `packages/sdk`
- AC: `pnpm i && pnpm build` 그린

### S0-02. TypeScript / Python 도구 정렬
- tsconfig strict, eslint + prettier (또는 Biome)
- Ruff + mypy 설정
- pre-commit 훅 (commitlint, lint-staged)

### S0-03. Docker Compose (로컬)
- Postgres 16, Redis 7, OpenSearch, MinIO(S3 모방), MailHog
- `make dev` 한 번에 기동
- AC: 로컬 헬스체크 모두 OK

### S0-04. CI 골격 [Platform]
- GitHub Actions: lint / typecheck / build / unit / SAST(Semgrep) / SCA(Trivy)
- 캐시(Turbo, pnpm store), PR 코멘트 결과 요약
- AC: 평균 CI 시간 < 12분

### S0-05. Terraform 베이스 [Platform]
- `infra/modules/network`, `infra/envs/dev` 골격
- AWS Organizations·OIDC for GH Actions
- dev VPC 한 개 배포 가능
- AC: `terraform plan` 깨끗, `apply` 시 dev VPC 생성

### S0-06. ADR 디렉터리 + 첫 ADR 5개
- `docs/adr/0001-modular-monolith.md` ~ `0005-claude-as-primary-llm.md`
- 템플릿: Context / Decision / Consequences / Alternatives
- Owner: Architect

### S0-07. CODEOWNERS + 보안 베이스라인
- `.github/CODEOWNERS`, `SECURITY.md`
- secret 스캔 (TruffleHog)
- Dependabot/Renovate 활성

### S0-08. 디자인 시스템 시드
- `packages/ui` shadcn/ui + Tailwind tokens
- Storybook 1차 (Button, Input, SDGBadge, ConfidenceBar)
- a11y 자동 검사 (axe)

---

## Sprint 1 — Identity & Catalog 기반 (2주)
**목표**: 인증·테넌시 작동 + SDG 카탈로그 검색 가능

### S1-01. 데이터 모델 v1 (Prisma)
- `tenants`, `users`, `roles`, `memberships`, RLS 정책
- 카탈로그 스키마 `catalog.sdg_goals/targets/indicators`
- 마이그레이션 + 시드 (UN 232 지표)
- 관련 문서: `docs/13`

### S1-02. 인증 (Auth.js)
- 이메일·비밀번호, Google OIDC
- Argon2id, MFA(TOTP)
- 세션 쿠키 + Refresh
- AC: 가입·로그인·로그아웃 E2E 통과

### S1-03. 테넌트 컨텍스트 미들웨어
- 모든 API 요청에 `SET LOCAL app.tenant_id`
- 멀티테넌시 격리 통합 테스트 (cross-tenant read 거부)
- AC: 격리 테스트 그린

### S1-04. RBAC (Casbin 또는 OPA)
- admin / reviewer / contributor / viewer / auditor
- 정책 평가 단일 진입점, 감사 이벤트 발행

### S1-05. SDG 카탈로그 API (read-only)
- `GET /v1/catalog/goals`, `/targets`, `/indicators`
- 검색 (Postgres FTS), 다국어 응답
- AC: OpenAPI 문서 자동 생성, P95 < 200ms

### S1-06. Web — 카탈로그 브라우저 UI
- 17 Goals 그리드 → Targets → Indicator 상세
- 필터·검색, 다국어 토글
- AC: a11y 위반 0, Storybook 등록

### S1-07. 감사로그 v1
- `audit_events` 테이블, append-only
- API 미들웨어로 자동 기록
- 관리자 화면에서 조회 (간단)

### S1-08. 관측성 베이스
- OTel 트레이스·로그·메트릭 → 로컬 Tempo/Loki/Prometheus (Compose)
- 핵심 대시보드 1개 (Service Health)

### S1-09. 보안 가드레일
- WAF 룰셋(개발), 비밀 회전 자동화 베이스
- 펜테스트용 자체 점검 체크리스트

### S1-10. 문서 동기화
- 코드 변경에 따라 `docs/13`, `docs/14` 업데이트
- ADR 추가 (필요 시)

---

## Sprint 2 (예고) — Activity & AI Mapping
- 활동 CRUD, SDG 매핑(수동·AI)
- AI Gateway: Claude Sonnet 4.6 + 인용
- 평가 데이터셋 100건 베이스라인

## Sprint 3 (예고) — Data Collection & Reports v1
- 캠페인·폼·검수 워크플로우
- GRI/TCFD 보고서 빌더 (AI 초안)

---

## 백로그 (우선순위 미정)
- E2E 테스트 인프라 (Playwright + 격리 테넌트)
- Webhook 발송, REST/GraphQL 분리
- ESRS 보고서 모듈
- ClickHouse 분석 파이프라인
- 모바일 반응형 다듬기
- SCIM 2.0 (Enterprise)
- 일본어·일본 SSBJ 모듈

## 정의 (Definitions)
- **DoR (Definition of Ready)**: AC 명확, 디자인 또는 와이어프레임 첨부, 종속성 해결
- **DoD (Definition of Done)**: AC 통과 + 단위 80%+ + 통합/E2E 그린 + a11y 통과 + 문서 업데이트 + PR 리뷰 2명

## 우선순위 (MoSCoW)
- Must: S0-01 ~ S0-05, S1-01 ~ S1-05
- Should: S0-06 ~ S0-08, S1-06 ~ S1-08
- Could: S1-09 ~ S1-10
- Won't (이번 분기): 모바일 네이티브, 블록체인 검증

## 메트릭
- 스프린트 속도(Velocity) 추적
- 리드타임(아이디어→배포)
- 결함 누설률
- 백로그 노화도
