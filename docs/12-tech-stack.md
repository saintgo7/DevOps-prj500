# 12. 기술 스택 결정서 (Tech Stack ADRs)

## 0. 결정 요약

| 영역 | 선택 | 대안 | 결정 |
|------|------|------|------|
| Frontend | Next.js 15 + React 19 + TS | Remix, SvelteKit | ADR-101 |
| 스타일 | Tailwind 4 + shadcn/ui | MUI, Chakra | ADR-102 |
| Backend | NestJS 11 (Node 22) | Express, FastAPI | ADR-103 |
| AI Gateway | FastAPI (Python 3.13) | Node 단일화 | ADR-104 |
| OLTP DB | PostgreSQL 16 | MySQL, Aurora | ADR-105 |
| Cache/Queue | Redis 7 + BullMQ | Kafka, SQS only | ADR-106 |
| Search | OpenSearch | Elasticsearch, Meilisearch | ADR-107 |
| Analytics DB | ClickHouse | Snowflake, Redshift | ADR-108 |
| Cloud | AWS | GCP, Azure | ADR-109 |
| IaC | Terraform | Pulumi, CDK | ADR-110 |
| CI/CD | GitHub Actions | CircleCI, Buildkite | ADR-111 |
| AI Provider | Anthropic Claude | OpenAI, Bedrock primary | ADR-112 |
| Observability | OTel + Grafana stack | Datadog | ADR-113 |
| Auth | Auth.js + WorkOS (SSO) | Auth0 | ADR-114 |

---

## ADR-101. Frontend = Next.js 15 + React 19
- **Context**: SSR/SEO, RSC로 성능, 풀스택 라우팅, 광범위 생태계
- **Decision**: Next.js 15 App Router, React 19, TypeScript strict
- **Consequences**:
  - (+) 성능, DX, RSC로 컴포넌트 단위 데이터 패칭
  - (-) Vercel 의존 인식 — 우리는 자체 호스팅
- **Alternatives**: Remix(러닝커브), SvelteKit(생태계 작음)

## ADR-102. Tailwind 4 + shadcn/ui
- 유틸리티 우선 + Radix 기반 접근성 컴포넌트로 디자인 토큰 통제
- 컴포넌트 소스 소유 (벤더락 회피)
- 다크 모드·디자인 토큰 자동 동기화

## ADR-103. Backend API = NestJS 11
- **Decision**: NestJS, Node 22, TypeScript
- **Why**: 모듈러 모놀리스에 적합, 데코레이터·DI, 강한 컨벤션
- **Why not Express**: 컨벤션 부족, 대규모 팀에서 일관성 떨어짐
- **Why not FastAPI(여기서)**: 도메인 BFF·웹앱과의 타입 공유 (TS/zod)

## ADR-104. AI Gateway = FastAPI (Python)
- **Decision**: AI 영역만 Python — 빠른 프롬프트·평가·Tool 진화
- **Why**: Anthropic SDK Python의 빠른 기능 도입(예: 캐싱, Citations), pandas/scikit 등 평가 도구
- **Trade-off**: 다중 언어 운영 비용 — 단일 도메인으로 한정해 영향 최소화

## ADR-105. OLTP = PostgreSQL 16
- RLS, JSONB, 풍부한 인덱스(BRIN, GIN), 통계 확장
- pgvector로 임베딩 (AI 매핑 보조)
- 백업·PITR (RDS), 운영 성숙

## ADR-106. Redis + BullMQ
- 캐시 + 잡 큐 단일 인프라로 단순화
- BullMQ: 작업 우선순위, 재시도, rate limit, 재예약
- 향후 Kafka는 도메인 이벤트 규모 커지면 검토

## ADR-107. OpenSearch
- AWS 매니지드, 카탈로그·활동 검색 한국어 nori 분석기
- Elastic 라이선스 변경 영향 회피

## ADR-108. ClickHouse (Analytics)
- 컬럼 기반, 수억 행 시계열 집계 빠름
- 임팩트 대시보드 P95 < 1s 가능
- Postgres와 분리해 OLTP 부담 격리

## ADR-109. AWS
- 한국·EU 리전, ISMS-P 인증 가능, 관리형 서비스 풍부
- 정부·대기업 검증된 실적
- AI 다중 옵션 (Bedrock 통한 Claude 옵션도 확보)

## ADR-110. Terraform + Atlantis
- 다중 클라우드 가능성 대비 Terraform
- 모듈화, 정책(OPA)으로 가드레일

## ADR-111. GitHub Actions
- 레포 통합·생태계 풍부
- Self-hosted runners (보안 빌드, 비용 최적화)

## ADR-112. Anthropic Claude
- **선택**: Claude Opus 4.7 (보고서·복합 추론), Sonnet 4.6 (매핑), Haiku 4.5 (요약)
- **이유**:
  - 긴 컨텍스트(SDG 카탈로그 + 사용자 데이터) 처리 우수
  - 도구 사용·인용·캐싱 일등급 지원
  - 안전성·정렬 평판
- **위험 완화**: AWS Bedrock Claude를 보조 라우트로 가용성 확보
- **Prompt Caching**: 시스템 프롬프트·SDG 카탈로그 1시간 TTL → 비용 ~80% 절감 기대

## ADR-113. OTel + Grafana Stack
- 표준 OpenTelemetry, 벤더 락 회피
- Tempo(트레이스), Loki(로그), Prometheus(메트릭), Grafana(시각화)
- Datadog 대비 비용 1/3 수준

## ADR-114. Auth.js + WorkOS (Enterprise SSO)
- 자체 OIDC + Auth.js 통합
- WorkOS로 SAML/OIDC SSO·SCIM 빠르게 (Enterprise 영업 가속)

---

## 라이브러리 표준
- **검증**: Zod (FE/BE 공유 스키마)
- **ORM**: Prisma (Postgres) — 단순, 마이그레이션 우수
- **Form**: React Hook Form
- **Charts**: Recharts + visx (커스텀)
- **Tables**: TanStack Table v8
- **Editor**: Tiptap (보고서 단락 편집)
- **i18n**: next-intl
- **Date**: date-fns (treeshake)
- **Test**: Vitest, Playwright, Pact (계약 테스트)
- **Lint/Format**: ESLint, Prettier, Biome 검토 중

## 운영 표준
- Node 22 LTS, Python 3.13
- TypeScript strict + `noUncheckedIndexedAccess`
- Python: Ruff + mypy strict
- 컨테이너: Distroless 베이스
- Image scanning: Trivy

## 의존성 정책
- 메이저 버전 업그레이드 RFC 필요
- 라이선스: MIT/Apache/BSD 허용, GPL 회피
- SCA: Snyk 또는 GitHub Dependabot

## 폐기·교체 트리거
- 라이브러리 1년 미유지 → 대체
- AI 모델 정확도 회귀 → 다른 모델 라우팅
- 데이터베이스 스케일 한계 → 샤딩/Citus 검토
