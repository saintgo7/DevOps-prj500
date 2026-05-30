# SDG 기반 SaaS 프로젝트 계획서

> 작성일: 2026-04-25
> 브랜치: `claude/sdg-saas-project-plan-ZZlFW`
> 목적: UN 지속가능발전목표(SDGs)를 핵심 가치로 하는 SaaS 제품을 기획·설계·운영하기 위한 21개 산출 문서의 구성과 일정 정의

---

## 1. 프로젝트 개요

### 1.1 비전
기업·기관·개인이 자신의 활동을 UN의 17개 지속가능발전목표(SDGs)에 매핑하고, 데이터를 측정·시각화·보고할 수 있도록 돕는 **SDG Impact SaaS 플랫폼**을 구축한다.

### 1.2 핵심 가치 제안 (Value Proposition)
- **측정 가능한 임팩트**: 활동/프로젝트를 17개 SDG 및 169개 세부목표에 자동 매핑
- **표준 보고서**: GRI, SASB, TCFD, ESRS 등 글로벌 표준에 맞춘 ESG/지속가능성 보고서 자동 생성
- **협업 워크플로우**: 부서·파트너·이해관계자 간 데이터 수집 및 검증 워크플로우
- **AI 기반 인사이트**: 활동 데이터로부터 SDG 기여도를 정량·정성 분석

### 1.3 타깃 고객
- 중견·대기업 ESG/지속가능성 담당 부서
- 비영리·국제개발 NGO
- 임팩트 투자사 및 액셀러레이터
- 공공기관·지방자치단체

### 1.4 비즈니스 모델
SaaS 구독(Tiered Pricing) + 컨설팅·인증 부가 서비스

---

## 2. 21개 산출 문서 구성

각 문서는 독립된 Markdown 파일로 `docs/` 디렉터리에 저장한다. 번호는 작성 순서이자 의존성 순서이다.

### Phase 1 — Discovery & Strategy (1~5)
| # | 문서명 | 파일 | 목적 |
|---|--------|------|------|
| 01 | 프로젝트 헌장 | `docs/01-project-charter.md` | 비전, 범위, 성공 기준, 이해관계자, 제약조건 |
| 02 | 시장·경쟁사 분석 | `docs/02-market-analysis.md` | TAM/SAM/SOM, 경쟁사(Worldfavor, Novata, Watershed 등) 비교 |
| 03 | SDG 매핑 프레임워크 | `docs/03-sdg-framework.md` | 17개 목표·169개 세부목표·232개 지표 데이터 모델 |
| 04 | 비즈니스 모델 캔버스 | `docs/04-business-model.md` | BMC, 수익모델, 가격정책 가설 |
| 05 | 리스크·규제 분석 | `docs/05-risk-compliance.md` | GDPR, K-ESG, EU CSRD, ISO 14064 등 |

### Phase 2 — Product Definition (6~10)
| # | 문서명 | 파일 | 목적 |
|---|--------|------|------|
| 06 | 사용자 페르소나 | `docs/06-personas.md` | 4~6개 핵심 페르소나, JTBD |
| 07 | 사용자 여정 지도 | `docs/07-user-journey.md` | 온보딩→데이터입력→리포트→공유 여정 |
| 08 | 기능 요구사항 명세 (FRD) | `docs/08-functional-requirements.md` | 모듈별 User Story, Acceptance Criteria |
| 09 | 비기능 요구사항 (NFR) | `docs/09-non-functional-requirements.md` | 성능, 가용성(99.9%), 보안, 접근성(WCAG 2.2 AA) |
| 10 | 정보 구조 & UX 가이드 | `docs/10-ux-design-system.md` | IA, 디자인 토큰, 컴포넌트 라이브러리 정책 |

### Phase 3 — Technical Architecture (11~16)
| # | 문서명 | 파일 | 목적 |
|---|--------|------|------|
| 11 | 시스템 아키텍처 | `docs/11-system-architecture.md` | C4 모델(Context/Container/Component) |
| 12 | 기술 스택 결정서 (ADR) | `docs/12-tech-stack.md` | Next.js, NestJS, PostgreSQL, Redis, AWS 등 선정 근거 |
| 13 | 데이터 모델 & ERD | `docs/13-data-model.md` | 엔터티, 관계, 인덱싱 전략, 다국어/멀티테넌시 |
| 14 | API 명세 (OpenAPI) | `docs/14-api-spec.md` | REST/GraphQL 엔드포인트, 인증, 버저닝 |
| 15 | 보안 설계 | `docs/15-security-design.md` | 위협 모델링(STRIDE), IAM, 암호화, 감사로그 |
| 16 | 인프라 & IaC | `docs/16-infrastructure.md` | Terraform 모듈, VPC, K8s/ECS, 멀티리전 전략 |

### Phase 4 — Delivery & Operations (17~21)
| # | 문서명 | 파일 | 목적 |
|---|--------|------|------|
| 17 | DevOps & CI/CD | `docs/17-devops-pipeline.md` | GitHub Actions, 환경 분리, 릴리스 전략 |
| 18 | 테스트 전략 | `docs/18-test-strategy.md` | 단위/통합/E2E, 커버리지 목표, 테스트 데이터 |
| 19 | 관측성 & SRE | `docs/19-observability.md` | 로깅, 메트릭, 트레이싱, SLO, 인시던트 대응 |
| 20 | Go-to-Market 플랜 | `docs/20-gtm-plan.md` | 가격, 채널, 파트너, KPI |
| 21 | 임팩트 측정 & 로드맵 | `docs/21-impact-roadmap.md` | OKR, 분기별 마일스톤, SDG 기여도 자체 측정 |

---

## 3. 일정 (12주 가정)

| 주차 | 마일스톤 | 산출물 |
|------|----------|--------|
| W1   | Kickoff & Discovery 시작 | 01, 02 |
| W2   | SDG/규제 도메인 정리 | 03, 05 |
| W3   | 비즈니스 모델 확정 | 04 |
| W4   | 사용자/UX 정의 | 06, 07 |
| W5   | 요구사항 베이스라인 | 08, 09 |
| W6   | 디자인 시스템 초안 | 10 |
| W7   | 아키텍처 합의 | 11, 12 |
| W8   | 데이터/API 설계 | 13, 14 |
| W9   | 보안/인프라 설계 | 15, 16 |
| W10  | 파이프라인·테스트 전략 | 17, 18 |
| W11  | 운영·관측성 | 19 |
| W12  | GTM·로드맵 확정 → 릴리스 게이트 | 20, 21 |

---

## 4. 역할 및 책임 (RACI 요약)
- **Product Owner**: 1, 4, 6, 7, 8, 20, 21
- **Tech Lead/Architect**: 11, 12, 13, 14, 15, 16
- **UX Lead**: 7, 10
- **DevOps/SRE**: 16, 17, 19
- **QA Lead**: 18
- **Compliance/Legal**: 5, 15
- **Domain Expert (Sustainability)**: 3, 21

---

## 5. 권장 기술 스택 (가설)
- **Frontend**: Next.js 15, React 19, Tailwind, shadcn/ui, i18next
- **Backend**: NestJS (Node 22) 또는 FastAPI (Python 3.13)
- **Data**: PostgreSQL 16, Redis 7, ClickHouse(분석), S3
- **AI**: Claude API (Opus 4.7 / Sonnet 4.6) — 보고서 초안, SDG 매핑 추론, 임팩트 요약
- **Infra**: AWS (EKS/RDS/CloudFront), Terraform, GitHub Actions
- **Observability**: OpenTelemetry, Grafana, Loki, Tempo, Sentry

---

## 6. SDG 정렬 (자체 적용)
본 SaaS 자체가 다음 SDG에 직접 기여한다.
- **SDG 9** (산업·혁신·인프라): 디지털 인프라 통한 지속가능성 데이터 표준화
- **SDG 12** (지속가능한 소비·생산): 기업의 책임있는 생산 데이터 가시화
- **SDG 13** (기후 행동): 탄소·기후 KPI 측정 지원
- **SDG 17** (파트너십): 다중 이해관계자 협업 워크플로우 제공

---

## 7. 성공 지표 (Definition of Success)
- 21개 문서 100% 작성·리뷰 완료
- 각 문서는 최소 1명 도메인 리뷰어 승인
- 아키텍처·보안 문서는 위협 모델링 워크숍 통과
- 12주 종료 시 MVP 백로그(우선순위화된 Epic 30개 이상) 도출
- 파일럿 고객 3개사 LOI 확보

---

## 8. 다음 액션
1. 본 계획서 리뷰 및 승인
2. `docs/` 디렉터리 생성 및 21개 문서 템플릿 스캐폴딩
3. Phase 1(문서 01~05) 작성 착수
4. 주간 리뷰 미팅(매주 금요일) 운영

---

## 9. 활용 Skill / 도구
- `/init` — 프로젝트 CLAUDE.md 초기화로 컨텍스트 자동 로딩
- `/review` — 문서 PR 리뷰 자동화
- `/security-review` — 보안 설계 문서(15) 검증
- `/simplify` — 요구사항·아키텍처 문서 가독성 개선
- `claude-api` skill — AI 매핑/요약 기능 프로토타이핑
- `loop` skill — 정기 진행상황 점검 자동화
