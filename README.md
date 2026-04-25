# SDG Impact Cloud

> UN 지속가능발전목표(SDGs) 기반 임팩트 측정·보고 SaaS 플랫폼

기업·기관·NGO가 자신의 활동을 17개 SDG / 169 세부목표 / 232 지표에 매핑하고, 글로벌 표준(GRI · SASB · TCFD · ESRS · K-ESG) 보고서를 AI로 자동 생성하는 멀티테넌시 SaaS.

## 핵심 가치
- **AI 기반 자동화** — Claude로 활동→SDG 매핑·보고서 초안을 생성, 작성 시간 80% 단축
- **글로벌 표준 정합** — GRI/SASB/TCFD/ESRS/K-ESG Crosswalk 내장
- **신뢰 가능한 출력** — 모든 AI 응답에 인용·신뢰도 표기, 인간 검수 게이트
- **다국어·아시아 우선** — 한·일·영 즉시 지원, K-ESG·SSBJ 우선 대응

## 빠른 시작 (문서)
1. **계획서 전체**: [`PROJECT_PLAN.md`](./PROJECT_PLAN.md) — 21개 문서 구성·일정·역할
2. **문서 인덱스**: [`docs/README.md`](./docs/README.md) — 4개 Phase, 21개 문서 네비게이션
3. **백로그**: [`BACKLOG.md`](./BACKLOG.md) — Sprint 0/1 즉시 실행 가능 항목

## 21개 문서 구성

### Phase 1 — Discovery & Strategy
[01](./docs/01-project-charter.md) 헌장 · [02](./docs/02-market-analysis.md) 시장분석 · [03](./docs/03-sdg-framework.md) SDG 프레임워크 · [04](./docs/04-business-model.md) 비즈니스 모델 · [05](./docs/05-risk-compliance.md) 리스크·규제

### Phase 2 — Product Definition
[06](./docs/06-personas.md) 페르소나 · [07](./docs/07-user-journey.md) 사용자 여정 · [08](./docs/08-functional-requirements.md) FRD · [09](./docs/09-non-functional-requirements.md) NFR · [10](./docs/10-ux-design-system.md) 디자인 시스템

### Phase 3 — Technical Architecture
[11](./docs/11-system-architecture.md) 시스템 아키텍처 · [12](./docs/12-tech-stack.md) 기술 스택 ADR · [13](./docs/13-data-model.md) 데이터 모델 · [14](./docs/14-api-spec.md) API 명세 · [15](./docs/15-security-design.md) 보안 설계 · [16](./docs/16-infrastructure.md) 인프라·IaC

### Phase 4 — Delivery & Operations
[17](./docs/17-devops-pipeline.md) DevOps·CI/CD · [18](./docs/18-test-strategy.md) 테스트 · [19](./docs/19-observability.md) 관측성·SRE · [20](./docs/20-gtm-plan.md) GTM · [21](./docs/21-impact-roadmap.md) 임팩트·로드맵

## 기술 스택 (요약, 자세한 내용은 docs/12)
- **Frontend**: Next.js 15 + React 19 + TypeScript + Tailwind + shadcn/ui
- **Backend**: NestJS (Node 22), FastAPI (Python 3.13, AI Gateway)
- **Data**: PostgreSQL 16 (RLS), Redis, OpenSearch, ClickHouse, S3, pgvector
- **AI**: Claude Opus 4.7 (보고서) / Sonnet 4.6 (매핑) / Haiku 4.5 (요약), Prompt Caching
- **Infra**: AWS (KR + EU 리전), Terraform, GitHub Actions, ECS Fargate
- **Observability**: OpenTelemetry + Grafana stack

## 자체 SDG 적용
이 SaaS 자체가 SDG 9 · 12 · 13 · 17에 직접 기여하며, 자사 도구로 매년 자체 SDG 보고서를 공개합니다.

## 기여
- 브랜치 전략·CI/CD: [`docs/17-devops-pipeline.md`](./docs/17-devops-pipeline.md)
- 코드 오너십: 모듈별 `CODEOWNERS` (구현 단계에 추가)
- PR/Issue 템플릿: `.github/`

## 라이선스
TBD (상용 SaaS, 일부 OSS 컴포넌트 분리 라이선스 예정)
