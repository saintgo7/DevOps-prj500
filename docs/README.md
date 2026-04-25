# SDG Impact Cloud — 문서 인덱스

이 디렉터리는 SDG SaaS 프로젝트의 21개 산출 문서를 포함합니다. 작성·의존성·읽는 순서는 번호 순입니다.

## 빠른 네비게이션

| 카테고리 | 문서 |
|---------|------|
| **What & Why** | [01 헌장](./01-project-charter.md) · [02 시장](./02-market-analysis.md) · [04 비즈니스](./04-business-model.md) · [20 GTM](./20-gtm-plan.md) · [21 임팩트·로드맵](./21-impact-roadmap.md) |
| **Domain** | [03 SDG 프레임워크](./03-sdg-framework.md) · [05 리스크·규제](./05-risk-compliance.md) |
| **User & Product** | [06 페르소나](./06-personas.md) · [07 여정](./07-user-journey.md) · [08 FRD](./08-functional-requirements.md) · [09 NFR](./09-non-functional-requirements.md) · [10 디자인 시스템](./10-ux-design-system.md) |
| **Architecture** | [11 시스템](./11-system-architecture.md) · [12 기술 스택](./12-tech-stack.md) · [13 데이터](./13-data-model.md) · [14 API](./14-api-spec.md) |
| **Security & Infra** | [15 보안](./15-security-design.md) · [16 인프라](./16-infrastructure.md) |
| **Delivery** | [17 DevOps](./17-devops-pipeline.md) · [18 테스트](./18-test-strategy.md) · [19 관측성](./19-observability.md) |

## 역할별 추천 읽기 순서

### Executive / Sponsor
01 → 02 → 04 → 21 → 20

### Product Owner / Manager
01 → 06 → 07 → 08 → 09 → 21

### Tech Lead / Architect
11 → 12 → 13 → 14 → 15 → 16

### Engineer (FE/BE)
10 → 12 → 13 → 14 → 17 → 18

### DevOps / SRE
16 → 17 → 19 → 15 → 11

### Security / Compliance
05 → 15 → 16 → 19

### QA
08 → 09 → 18 → 14

### Designer
06 → 07 → 10 → 09

### Sales / Marketing / CSM
01 → 04 → 06 → 20 → 21

## 문서 메타데이터

| # | 문서 | 책임자(Owner) | v1 검토 일자 | 다음 검토 |
|---|------|--------------|-------------|----------|
| 01 | 헌장 | Sponsor / PO | 2026-Q2 | 분기 |
| 02 | 시장 분석 | PO / Marketing | 2026-Q2 | 분기 |
| 03 | SDG 프레임워크 | Domain Expert | 2026-Q2 | 반기 |
| 04 | 비즈니스 모델 | PO / Finance | 2026-Q2 | 분기 |
| 05 | 리스크·규제 | Compliance Officer | 2026-Q2 | 분기 |
| 06 | 페르소나 | UX Lead | 2026-Q2 | 반기 |
| 07 | 사용자 여정 | UX Lead | 2026-Q2 | 반기 |
| 08 | FRD | PO | 2026-Q2 | 스프린트마다 |
| 09 | NFR | Tech Lead | 2026-Q2 | 분기 |
| 10 | 디자인 시스템 | Design Lead | 2026-Q2 | 월 |
| 11 | 시스템 아키텍처 | Architect | 2026-Q2 | 분기 |
| 12 | 기술 스택 (ADR) | Architect | 2026-Q2 | 변경 시 |
| 13 | 데이터 모델 | Data Lead | 2026-Q2 | 변경 시 |
| 14 | API 명세 | Backend Lead | 2026-Q2 | 변경 시 |
| 15 | 보안 설계 | Security Lead | 2026-Q2 | 분기 |
| 16 | 인프라·IaC | Platform Lead | 2026-Q2 | 분기 |
| 17 | DevOps·CI/CD | Platform Lead | 2026-Q2 | 분기 |
| 18 | 테스트 전략 | QA Lead | 2026-Q2 | 분기 |
| 19 | 관측성·SRE | SRE Lead | 2026-Q2 | 분기 |
| 20 | GTM | Sales / Marketing Lead | 2026-Q2 | 분기 |
| 21 | 임팩트·로드맵 | PO / CEO | 2026-Q2 | 분기 |

## ADR (아키텍처 결정 기록)

- [0001](./adr/0001-modular-monolith.md) Modular Monolith
- [0002](./adr/0002-postgres-with-rls.md) Postgres + RLS
- [0003](./adr/0003-claude-as-primary-llm.md) Claude를 1차 LLM
- [0004](./adr/0004-aws-as-cloud.md) AWS 1차 클라우드
- [0005](./adr/0005-otel-grafana-stack.md) OTel + Grafana 관측성
- [0006](./adr/0006-prisma-as-orm.md) Prisma ORM
- [0007](./adr/0007-observability-baseline.md) 관측성 베이스라인 (pino + Prom + structlog)
- [0008](./adr/0008-security-guardrails-baseline.md) 보안 가드레일 베이스라인

## 변경 절차
- 큰 변경: RFC PR + 도메인 책임자 승인
- 작은 보강: PR 1명 리뷰
- 변경 이력은 git log로 추적
- 큰 변경에는 `[BREAKING]` 또는 `[RFC]` PR 라벨

## 표기 약속
- 단위: SI 단위 우선, 통화는 USD 기준 (필요 시 KRW 병기)
- 일자: ISO 8601 (`YYYY-MM-DD`)
- 인용: UN 공식 자료는 출처 URL 명시
- 다국어 문구: `*_i18n` JSON 또는 본문에 `[ko]`, `[en]` 태그
