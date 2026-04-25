# ADR-0006: Prisma를 ORM으로 채택한다 (RLS는 raw SQL 보강)

- 상태: Accepted
- 일자: 2026-04-25
- 작성자: Backend Lead
- 관련 문서: `docs/13-data-model.md`, `docs/15-security-design.md`, ADR-0002

## 컨텍스트
NestJS 백엔드에서 Postgres를 다룰 ORM이 필요하다. 후보는 Prisma, TypeORM, Drizzle, Kysely. 우리는 다음을 우선시한다:
- 모델·타입·마이그레이션이 단일 진실 소스
- 강한 TypeScript 타입 추론
- 마이그레이션 도구 성숙도
- RLS·복잡 SQL과의 공존

## 결정
**Prisma 7**을 채택한다. 단:
- 일반 CRUD는 Prisma Client 사용
- RLS·복잡 윈도우·CTE는 `$executeRaw` / `$queryRaw` 또는 `prisma migrate`의 SQL 마이그레이션
- 마이그레이션 파일은 항상 사람이 검토·편집 (자동 차이 + 손맛)
- 데이터소스 URL은 `prisma.config.ts`(Prisma 7 신 표준)에서 환경변수로 주입

## 근거
- 자동 생성 클라이언트로 타입 안전성 최고
- `prisma migrate`는 dev/staging/prod 일관 워크플로우
- raw SQL hatch가 충분히 열려 있어 RLS·집계 쿼리 가능
- 커뮤니티·문서·툴체인 풍부

## 결과
- (+) DX, 마이그레이션 워크플로우, 타입 안전성
- (-) Prisma Client는 RLS 컨텍스트(`SET LOCAL`) 자동 적용 X → 인터셉터로 명시 처리
- 위험: 대규모 join은 Prisma가 비효율 → raw SQL fallback 정책

## 대안
| 대안 | 장점 | 단점 | 기각 사유 |
|------|------|------|----------|
| Drizzle | 타입 추론 강함, SQL 친화 | 마이그레이션 도구 미성숙, 커뮤니티 작음 | 운영 안정성 |
| TypeORM | 데코레이터 친화 | 타입 약함, 마이그레이션 사고 사례 | 신뢰성 |
| Kysely | 쿼리빌더 강력 | 마이그레이션 도구 X, 모델 도구 X | 단독 부족 |

## 후속 액션
- [ ] Prisma 트랜잭션 헬퍼: `withTenant(tenantId, fn)`로 `SET LOCAL` 묶음
- [ ] 마이그레이션 린터: RLS 미적용 테이블 검출
- [ ] `prisma generate` CI 캐시
- [ ] 슬로우 쿼리 모니터링 (Prisma + Postgres `pg_stat_statements`)
