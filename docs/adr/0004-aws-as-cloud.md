# ADR-0004: AWS를 1차 클라우드로 채택한다

- 상태: Accepted
- 일자: 2026-04-25
- 작성자: Platform Lead
- 관련 문서: `docs/16-infrastructure.md`

## 컨텍스트
한국·EU 리전, 관리형 서비스 풍부, 보안 인증, 정부·대기업 검증, AI 다중 옵션이 필요하다.

## 결정
**AWS** — Primary `ap-northeast-2` (서울), Secondary `eu-west-1` (아일랜드), 옵션 `ap-northeast-1` (도쿄). IaC는 Terraform. 컴퓨트는 ECS Fargate (→ 향후 EKS).

## 근거
- 한국·EU·일본 리전 모두 보유, 데이터 위치 옵션 확보
- ISMS-P, SOC, ISO 27001 인증 가능 (AWS 컴플 매트릭스)
- Bedrock으로 Claude 보조 라우트 가능
- 풍부한 관리형 서비스(RDS, ElastiCache, OpenSearch)

## 결과
- (+) 빠른 출시, 운영 부담 완화
- (-) 벤더락 부분 존재 → IaC와 표준 OSS(Terraform·OTel)로 완화
- 위험: 비용 폭증 → FinOps 가드레일 (태깅·예산·Anomaly Detection)

## 대안
| 대안 | 장점 | 단점 | 기각 사유 |
|------|------|------|----------|
| GCP | BigQuery, AI 통합 | 한국 리전 제한 (특정 서비스), ISMS-P 사례 적음 | 한국 영업 영향 |
| Azure | 엔터프라이즈 호환 | AI 우리 스택과 적합도 낮음 | 도메인 적합 부족 |
| 멀티클라우드 | 협상력 | 운영 복잡·비용 | 초기 단계 부적합 |

## 후속 액션
- [ ] AWS Organizations + 계정 분리 (prod/staging/dev/security/shared)
- [ ] 비용·태깅 정책 자동 검증 (Conftest)
- [ ] 컴플 통제(Config·CloudTrail·GuardDuty) 베이스라인
