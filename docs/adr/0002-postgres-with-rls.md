# ADR-0002: PostgreSQL + RLS로 멀티테넌시 격리

- 상태: Accepted
- 일자: 2026-04-25
- 작성자: Data Lead
- 관련 문서: `docs/13-data-model.md`, `docs/15-security-design.md`

## 컨텍스트
멀티테넌시 SaaS의 데이터 격리 모델은 Silo / Bridge / Pool 중 선택한다. 운영 단순성과 비용을 고려하면 Pooled 모델이 유리하나, 격리 안전성이 필수다. 또한 ESG 데이터의 특성상 시계열·검색·JSONB가 모두 필요하다.

## 결정
**Postgres 16 단일 클러스터 + Pooled 스키마 + Row-Level Security**.
- 테이블별 `tenant_id NOT NULL`
- RLS 정책으로 `current_setting('app.tenant_id')` 강제
- API 미들웨어가 매 요청 `SET LOCAL app.tenant_id` 적용
- Enterprise 옵션: 테넌트별 KMS 키, 백업 분리

## 근거
- 운영 단순(단일 클러스터), 비용 효율
- RLS는 Postgres 1급 기능, 우회 불가능한 격리
- pgvector·BRIN·GIN 등 풍부한 인덱스
- RDS PITR·운영 성숙

## 결과
- (+) 격리 안전, 운영 단순, 백업·복구 간단
- (-) 한 클러스터 장애가 전체 영향 → Multi-AZ 필수
- 위험: RLS 미적용 테이블 누락 → 마이그레이션 린터로 가드

## 대안
| 대안 | 장점 | 단점 | 기각 사유 |
|------|------|------|----------|
| 테넌트별 DB | 강한 격리 | 운영·비용 폭증 | 테넌트 1,000+ 어려움 |
| 테넌트별 스키마 | 부분 격리 | 마이그레이션 N배 | 운영 복잡 |
| Mongo/Dynamo | 유연 | 트랜잭션·SQL 제약 | 보고서·집계 SQL이 적합 |

## 후속 액션
- [ ] RLS 정책 자동 검사 스크립트 (CI)
- [ ] 멀티테넌시 격리 통합 테스트 셋
- [ ] Enterprise CMK 옵션 설계
