# 16. 인프라 & IaC (Infrastructure as Code)

## 1. 클라우드 토폴로지

### 1.1 리전·계정 분리
- **계정**:
  - `org-management` (AWS Organizations)
  - `prod-kr` (한국 운영)
  - `prod-eu` (EU 운영, 보조)
  - `staging`
  - `dev`
  - `security` (로그·감사 집중)
  - `shared-services` (CI/CD, 레지스트리)

- **리전**:
  - Primary: `ap-northeast-2` (서울)
  - Secondary: `eu-west-1` (아일랜드)
  - 옵션: `ap-northeast-1` (도쿄, 일본 고객)

### 1.2 VPC 설계
```
VPC 10.10.0.0/16
 ├─ Public Subnets ×3 AZ (10.10.0.0/24, .1.0/24, .2.0/24) — ALB, NAT, Bastion
 ├─ Private App Subnets ×3 AZ (10.10.10.0/24…)
 ├─ Private Data Subnets ×3 AZ (10.10.20.0/24…) — RDS, Redis, OpenSearch
 └─ VPC Endpoints — S3, ECR, Secrets Manager, KMS, CloudWatch
```

## 2. 핵심 서비스 매핑
| 컴포넌트 | AWS 서비스 |
|---------|-----------|
| Compute (App) | ECS Fargate (→ 향후 EKS) |
| Edge | CloudFront + AWS WAF + Shield |
| Load Balancer | ALB (앱), NLB (내부) |
| OLTP DB | RDS for PostgreSQL 16 (Multi-AZ) |
| Cache/Queue | ElastiCache Redis 7 |
| Search | OpenSearch Service |
| Analytics DB | ClickHouse (자체 호스팅 ECS Fargate, EBS gp3) |
| Object Store | S3 (Versioning + Object Lock) |
| Streaming | EventBridge + SQS |
| Secrets | Secrets Manager + KMS |
| DNS | Route 53 |
| CDN | CloudFront (KR + EU 엣지) |
| Email | SES |
| Monitoring | CloudWatch + 자체 OTel + Grafana |

## 3. Terraform 모듈 구조
```
infra/
├── modules/
│   ├── network/        # VPC, subnets, routing
│   ├── ecs-service/    # 표준 ECS 서비스
│   ├── rds-postgres/   # Multi-AZ Postgres
│   ├── redis/
│   ├── opensearch/
│   ├── s3-bucket/      # versioning, lock 옵션
│   ├── waf/
│   ├── kms-key/
│   └── observability/
├── envs/
│   ├── dev/
│   ├── staging/
│   └── prod-kr/
│   └── prod-eu/
└── shared/             # IAM, OIDC, organization-wide
```

- 모듈 SemVer 태그
- Atlantis로 PR 기반 plan/apply
- 정책 가드: OPA Conftest, tfsec, checkov

## 4. 컨테이너·이미지
- 베이스: `gcr.io/distroless/nodejs22-debian12`, `python:3.13-slim` (FastAPI는 distroless-python)
- 빌드: BuildKit 멀티스테이지
- 레지스트리: ECR (private, scan on push)
- 서명: cosign + Sigstore
- 이미지 태그: `git-sha` 불변 + 환경 alias

## 5. 시크릿·구성
- 환경별 분리: `parameter store` 비민감 + `secrets manager` 민감
- 자동 회전: DB 비밀 30일, API 키 90일
- IAM Roles for ECS Tasks, GitHub Actions OIDC (장기 키 0)

## 6. 환경 (Environments)
| 환경 | 목적 | 데이터 | 자동 적용 |
|------|------|--------|----------|
| dev | 개발 | 합성 | main → 자동 |
| staging | QA, 성능 | 익명화 prod 일부 | release-* → 자동 |
| prod-kr | 한국 운영 | 실데이터 | 승인 후 수동 |
| prod-eu | EU 운영 | 실데이터 | 승인 후 수동 |
| dr-eu | DR 워밍 | 복제 | 자동 |

## 7. 비용 가드레일 (FinOps)
- AWS Budgets + Anomaly Detection
- 태그 의무: `env`, `service`, `tenant_id` (해당 시), `owner`
- 단위 비용 대시보드: per tenant per month
- 미사용 리소스 자동 정리(주말 dev 종료 등)

## 8. 백업·복구
- RDS PITR 35일 + 일일 스냅샷 90일 보존
- S3 Versioning + Object Lock (보고서 발행본 immutable)
- 백업은 별도 계정 (security)
- 분기 복구 훈련 (전체 RDS, 1개 테넌트 데이터)

## 9. 네트워크 보안
- WAF 룰: OWASP CRS, geo-block, rate limit
- Shield Standard
- ACL/SG 최소 허용
- VPN/AWS Client VPN (운영 접근), Bastion 제거 (SSM Session Manager 사용)

## 10. 모니터링 & 알림
- CloudWatch Alarms (인프라)
- Grafana 대시보드 (앱 메트릭) — docs/19 참조
- 알림: PagerDuty (P1/P2), Slack (P3)

## 11. 비밀 회전 자동화
- Lambda + Secrets Manager 회전 함수
- 회전 후 통합 테스트 잡 트리거

## 12. 멀티 리전·DR
- Active-Passive (KR-prod ↔ EU-DR)
- DB: Cross-region read replica (RPO 5-15분)
- S3: Cross-Region Replication
- 페일오버 Runbook + 분기 훈련

## 13. 컴플라이언스 통제 매핑
- AWS Config: 정책 위반 자동 감지 (S3 public, MFA 미적용 등)
- CloudTrail: 모든 API 호출 (Org-wide), 7년 보존
- GuardDuty + Security Hub
- Inspector (이미지·EC2 취약점)

## 14. 환경 영향 (Sustainability)
- 저탄소 리전 우선 (서울·아일랜드는 평균 이상 청정)
- Graviton 인스턴스 우선 (전력당 성능)
- 야간/주말 dev 자동 정지
- AWS Customer Carbon Footprint Tool 활용

## 15. 운영 표준
- 변경 관리: PR + 리뷰 2명 + Atlantis plan 검토
- 비상 변경: break-glass 절차 (Security Lead 승인)
- Tagging 위반 시 자동 알림
- IaC 드리프트 감지 (Terraform Cloud / Atlantis 정기 plan)

## 16. 미래 진화
- ECS → EKS (사용자 워크로드 다양화)
- Cilium·Service Mesh (정교한 트래픽·정책)
- Karpenter (효율적 노드 스케일)
- 데이터 메시 + Iceberg (분석 확장 시)
