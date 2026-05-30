# 17. DevOps & CI/CD 파이프라인

## 1. 브랜치 전략 (Trunk-based + 짧은 수명 브랜치)
- `main` — 항상 배포 가능
- `feat/*`, `fix/*`, `chore/*` — 1-3일 수명
- PR 머지 = squash, 1차 리뷰어 + 코드 오너
- 릴리스 태그 `v{major}.{minor}.{patch}` SemVer

## 2. 환경 매핑
| 환경 | 트리거 | 배포 방식 | 데이터 |
|------|--------|----------|--------|
| dev | `main` push | Auto, 5분 | 합성 |
| staging | tag `staging-*` | Auto, 승인 1명 | 익명화 prod |
| prod-kr | tag `v*` | 승인 2명, 카나리 | 실 |
| prod-eu | prod-kr 후 1h | 자동 | 실 |

## 3. CI 파이프라인 (PR)
```yaml
# 단계
1. checkout + setup (캐시 적극)
2. lint (ESLint, Ruff, Prettier check)
3. typecheck (tsc, mypy)
4. unit tests (Vitest, pytest) 병렬
5. build (Next.js, NestJS, FastAPI)
6. SAST (Semgrep, CodeQL)
7. SCA (Snyk, Trivy)
8. 컨테이너 빌드 + scan + sign
9. 통합 테스트 (Testcontainers, Pact)
10. E2E smoke (Playwright)
11. 변경 영향 분석 (DB 마이그레이션 dry-run)
12. PR 코멘트로 결과 요약
```

- 평균 소요: 12분 목표 (캐시·병렬 최적화)
- 실패 시 머지 불가 (필수 체크)

## 4. CD 파이프라인 (Merge → main)
```yaml
1. 컨테이너 태그 push (git-sha)
2. dev 자동 배포 (Terraform + ECS)
3. 스모크 테스트 (synthetic)
4. 자동 OK 시 staging 후보 등록
5. 매일 18:00 staging 자동 승격 (또는 수동 tag)
6. staging 부하·E2E 통과 시 prod 후보
```

## 5. 프로덕션 배포 (Blue/Green + Canary)
1. Green 환경에 새 태스크 배포
2. Health check + 1% 카나리 (CodeDeploy)
3. 5분 관찰 (RED 메트릭, 에러율)
4. 단계 25% → 50% → 100%
5. 5분 안정 → Blue 종료
6. 실패 신호 시 자동 롤백 (90초)

## 6. 데이터베이스 마이그레이션
- Expand → Migrate → Contract 3단계
- 온라인 마이그레이션 (zero downtime)
- 마이그레이션 PR은 코드 변경과 분리, DBA 리뷰 필수
- 백오프 잡 (Backfill) 별도 배포

## 7. AI 프롬프트·모델 변경
- 프롬프트 변경 = 코드 변경, 버전 태그(`prompt_v23`)
- 평가 셋(1,000건) 자동 회귀 테스트
- 회귀 점수 기준 미달 시 머지 차단
- 모델 변경(예: Sonnet 4.5 → 4.6) RFC 필수

## 8. 릴리스 캐던스
- **dev**: 하루 5-20회 (작은 PR)
- **staging**: 하루 1-2회
- **prod**: 주 1-2회 (수, 화요일)
- **긴급**: 핫픽스 브랜치 → 빠른 트랙 (스킵 staging은 예외 승인)

## 9. 기능 플래그
- LaunchDarkly 또는 자체 (Postgres + Redis 캐시)
- 모든 큰 기능은 플래그로 점진 출시
- 테넌트·사용자·% 기반 타겟팅
- 정리 의무: 90일 후 미사용 플래그 제거

## 10. 자동화 도구
- **Renovate** — 의존성 업데이트 자동 PR
- **Atlantis** — Terraform plan/apply
- **Sentry Releases** — 에러 추적, 릴리스 매핑
- **CodeDeploy** — Blue/Green
- **Bytebase** 또는 자체 — DB 마이그레이션 게이트

## 11. 환경 변수·구성 관리
- 12-Factor: ENV로 주입
- IaC가 SSM Parameter Store / Secrets Manager 채움
- 코드에서 직접 접근 금지 (Config Service 통과)

## 12. 인시던트 대응 (배포 사고)
- 자동 롤백 (RED 메트릭 알림 시)
- 수동 롤백 절차 (`scripts/rollback.sh`)
- 사고 발생 시 Postmortem 24h 내 작성

## 13. CI 보안
- GitHub OIDC → AWS IAM (단기 토큰)
- Self-hosted runners (민감 빌드)
- 비밀 마스킹, 빌드 로그 보관 90일
- Approval gates (production)

## 14. 빌드 캐시·최적화
- Turborepo (모노레포)
- Docker Buildx 캐시 (registry)
- pnpm store 캐시
- 결과물 dependency cache → 평균 빌드 시간 50% 감소

## 15. 코드 오너십
- `CODEOWNERS` 파일
- 도메인별 팀 (Identity, Reporting, AI 등)
- 보안·인프라 PR은 Security/Platform 팀 필수 리뷰

## 16. 변경 추적
- 모든 PR에 변경 영향(테넌트·사용자·SLA) 표기
- 릴리스 노트 자동 생성 (Conventional Commits → CHANGELOG)
- 사용자 노출은 in-app changelog

## 17. 메트릭
- DORA 지표:
  - Deployment Frequency: 일일+
  - Lead Time for Changes: < 24h
  - Change Failure Rate: < 15%
  - MTTR: < 1h
- CI 통과율 95%+
- PR 머지 시간 P50 < 1일

## 18. 도구 비용·라이선스
- 분기 도구 리뷰 (사용률·ROI)
- OSS 우선, SaaS는 ROI 입증 필수
