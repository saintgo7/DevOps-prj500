# 11. 시스템 아키텍처 (System Architecture)

## 1. 아키텍처 스타일
- **Pattern**: Modular Monolith → Service-oriented (성장 시 분리)
- **Hosting**: AWS, Multi-AZ, Multi-region (KR-primary, EU-secondary)
- **Tenancy**: Pooled DB + Row-Level Security + Per-tenant 암호화 키
- **Deployment**: Container (ECS Fargate → 추후 EKS), Blue/Green

## 2. C4 — Level 1: System Context
```
[ESG 담당자]──┐
[부서 사용자]──┤
[CFO/IR]──────┼──HTTPS──>[ SDG Impact Cloud ]<──Webhook/API──[ERP/HR/회계]
[NGO PM]──────┤                                            
[감사인]──────┘                ▲
                                ├── Anthropic API (Claude)
                                ├── AWS S3/RDS/KMS
                                ├── Email (SES) / Slack / Teams
                                └── Crowdin (i18n)
```

## 3. C4 — Level 2: Container

### 3.1 컨테이너 구성
| 컨테이너 | 기술 | 역할 |
|---------|------|------|
| Web App | Next.js 15 (SSR + RSC) | UI, BFF |
| API Service | NestJS 11 (Node 22) | 도메인 API, 비즈니스 로직 |
| Worker | BullMQ + Node | 비동기 작업 (AI, 보고서, 임포트) |
| AI Gateway | FastAPI (Python 3.13) | Claude 호출 추상화, 프롬프트 관리 |
| Reporting Engine | Node + Headless Chromium | PDF/HTML/iXBRL 생성 |
| OLTP DB | PostgreSQL 16 + RLS | 운영 데이터 |
| Cache | Redis 7 | 세션, 큐, 캐시 |
| Search | OpenSearch | 활동·지표 검색 |
| Analytics DB | ClickHouse | 시계열·대시보드 |
| Object Store | S3 | Evidence, 보고서, 백업 |
| Message Bus | EventBridge + SQS | 도메인 이벤트 |

### 3.2 트래픽 흐름
1. CDN (CloudFront) → ALB → Next.js (SSR) → BFF
2. BFF → NestJS API (mTLS 내부)
3. API → DB (RLS), Redis (캐시·세션)
4. AI 작업 → SQS → Worker → AI Gateway → Claude
5. 보고서 → Worker → Reporting Engine → S3
6. 통합 → API Gateway → 파트너 시스템

## 4. C4 — Level 3: Component (Identity 모듈 예시)
```
NestJS API
 ├─ AuthController
 │   └─ AuthService → SessionRepository (Redis)
 ├─ UserController
 │   └─ UserService → UserRepository (Postgres)
 ├─ TenantContextMiddleware (RLS GUC 설정)
 ├─ RbacGuard
 └─ AuditInterceptor → Audit Pub (EventBridge)
```

## 5. 핵심 도메인 분리 (Bounded Contexts)
1. **Identity & Tenant** — 사용자, 조직, 역할
2. **Catalog** — UN SDG 카탈로그, Crosswalk
3. **Activity** — 활동, 지표, 데이터 포인트
4. **Collection** — 캠페인, 폼, 검증
5. **AI** — 매핑·요약·생성 추상화
6. **Reporting** — 표준 템플릿, 빌더, 출력
7. **Analytics** — 대시보드, 벤치마크
8. **Audit** — 이벤트 소싱·감사로그
9. **Billing** — 플랜, 결제, 사용량

각 컨텍스트는 모듈 경계를 가지며 도메인 이벤트로만 소통한다.

## 6. 동기 vs 비동기
| 액션 | 모드 | 이유 |
|------|------|------|
| CRUD | 동기 | 즉시 응답 |
| AI 매핑 추천 | 동기 (5s 이내) | UX 중요 |
| 문서 추출(PDF) | 비동기 | 시간 변동 |
| 보고서 생성 | 비동기 + 진행률 | 60-90초 |
| 데이터 임포트 | 비동기 | 대용량 |
| 알림 | 비동기 | 비차단 |

## 7. 데이터 일관성
- **Transactional**: 단일 도메인 내 — Postgres ACID
- **Cross-domain**: Outbox 패턴 + EventBridge
- **Eventual**: Analytics, Search 인덱스
- **Saga**: 보고서 생성 (입력 잠금→AI→검수→출력)

## 8. 멀티테넌시
- 모든 테이블 `tenant_id` + RLS 정책
- 데이터베이스 GUC `app.tenant_id` 미들웨어로 설정
- 파일 S3 prefix `tenants/{tenantId}/`
- 테넌트별 KMS 키 (Enterprise) — 추가 비용 옵션

## 9. AI 통합 패턴
- **Gateway 패턴**: 모든 AI 호출은 AI Gateway 경유
- **모델 라우팅**: 작업·테넌트별 모델 매핑
  - 매핑 추천: `claude-sonnet-4-6`
  - 보고서 초안: `claude-opus-4-7`
  - 단순 요약: `claude-haiku-4-5-20251001`
- **Prompt Caching**: 시스템 프롬프트 + SDG 카탈로그 캐시 (1h)
- **Tool Use**: 데이터 조회·계산·인용 도구 등록
- **Fallback**: Anthropic 직접 → AWS Bedrock Claude

## 10. 보안 아키텍처 (요약, docs/15 상세)
- 네트워크: VPC, Private Subnet, NAT, WAF, Shield
- 비밀: AWS Secrets Manager, IAM Roles for Service Accounts
- 인증: OIDC, SAML, MFA, Passkey
- 인가: RBAC + ABAC (조직·부서·역할)

## 11. 관측성 (요약, docs/19 상세)
- OpenTelemetry SDK → Collector → Tempo/Loki/Prometheus → Grafana
- 분산 추적 traceId 전파 (HTTP, SQS, BullMQ)
- AI 호출 메타데이터 추적 (모델, 토큰, latency)

## 12. 배포 아키텍처
- 환경: dev / staging / prod
- 리전: KR (ap-northeast-2) 주, EU (eu-west-1) 보조
- CI/CD: GitHub Actions → ECR → ECS Fargate
- 전략: Blue/Green, 카나리 (Enterprise 트래픽 5% → 100%)

## 13. 비기능 매핑
| NFR | 아키텍처 결정 |
|-----|--------------|
| 99.9% 가용성 | Multi-AZ ECS, RDS Multi-AZ, ALB |
| 데이터 위치 | 리전 분리 배포, S3 리전 격리 |
| AI 환각 방지 | Tool Use + Citations + 인간 게이트 |
| 멀티테넌시 격리 | RLS + 테넌트별 KMS |
| 100만 시계열 | ClickHouse 컬럼 저장 |

## 14. 향후 진화
- 모놀리스 → 도메인별 분리 (AI Gateway 우선)
- ECS → EKS (사용자 워크로드 다양화 시점)
- ClickHouse 자체 호스팅 → ClickHouse Cloud
- 데이터 메시 (도메인별 데이터 제품)

## 15. 트레이드오프 결정 (ADR 요약)
- ADR-001: Modular Monolith 채택 (분리 비용 < 단일 배포 이익)
- ADR-002: Postgres + RLS (테넌트 격리, 운영 단순)
- ADR-003: AI Gateway 분리 (Python 생태계, 프롬프트 진화 빠름)
- ADR-004: 별도 ClickHouse (시계열 분석)
- 자세한 사항 docs/12 참조
