# 18. 테스트 전략 (Test Strategy)

## 1. 테스트 피라미드
```
            ┌────────────┐
            │   E2E (5%) │   Playwright, 핵심 흐름
            └────────────┘
          ┌──────────────────┐
          │ Integration (15%)│ Testcontainers, Pact
          └──────────────────┘
        ┌────────────────────────┐
        │     Unit (80%)         │ Vitest, pytest
        └────────────────────────┘
```

## 2. 단위 테스트 (Unit)
- **도구**: Vitest (TS), pytest (Python)
- **범위**: 순수 함수, 도메인 로직, 컴포넌트 (RTL)
- **커버리지 목표**: 80%+
- **DOUBLE 기본**: 외부 I/O 모킹, 시간/UUID 결정적
- **속도**: 전체 단위 5분 이내

## 3. 통합 테스트
- **도구**: Testcontainers (Postgres, Redis, OpenSearch)
- **범위**: Repository, Service, API 컨트롤러, 외부 통합 어댑터
- **AI 통합**: Anthropic SDK 모킹 + 골든 응답 셋
- **데이터**: 픽스처 빌더 (Factory) + 스냅샷

## 4. 계약 테스트 (Contract)
- **도구**: Pact (FE-BE), OpenAPI Schemathesis (외부 API)
- **흐름**:
  1. FE가 컨슈머 컨트랙트 발행
  2. BE 빌드에서 검증
  3. Provider 변경 시 호환성 자동 확인

## 5. E2E 테스트
- **도구**: Playwright (Chromium, WebKit, Firefox)
- **시나리오** (필수):
  - 가입 → 온보딩 → 첫 활동 입력
  - 활동 매핑 (AI 제안 → 수락)
  - 캠페인 생성 → 데이터 수집 → 검수
  - 보고서 생성 (GRI) → 발행
  - SSO 로그인, MFA
  - 데이터 임포트 (CSV)
- **환경**: Staging, 일일 자동 + PR 시 smoke 5개
- **안정화**: Auto-wait, retry 1회, flake quarantine

## 6. 시각 회귀 (Visual Regression)
- **도구**: Chromatic + Storybook
- **범위**: 디자인 시스템 컴포넌트 + 핵심 페이지
- **임계치**: > 0.1% 픽셀 차이 시 리뷰

## 7. 성능 테스트
- **도구**: k6 (HTTP), Locust (대안)
- **시나리오**:
  - 정상 부하: 100 RPS, 30분
  - 피크: 500 RPS, 10분
  - 지속: 50 RPS, 4시간
- **임계치 (P95)**: API < 800ms, DB < 200ms, 에러율 < 0.5%
- **빈도**: 분기 + 릴리스 후 1회

## 8. 부하·확장 테스트
- 데이터: 100만 활동, 1억 데이터 포인트, 1만 동시 사용자
- 분기별 1회, 결과 캐파시티 플랜에 반영

## 9. 카오스 엔지니어링
- **도구**: AWS Fault Injection Service
- **시나리오**: 단일 AZ 장애, RDS 페일오버, Redis 장애, 네트워크 지연
- **빈도**: 분기 1회, staging
- **목표**: SLO 영향 < 5분

## 10. 보안 테스트
- SAST/DAST/SCA: docs/15 참조
- 분기 외부 펜테스트
- 인증·세션·RBAC 회귀 테스트 자동화

## 11. 접근성 (a11y)
- **자동**: axe-core (CI), Lighthouse a11y
- **수동**: 스크린리더 (VoiceOver, NVDA) 분기 1회
- **임계치**: 자동 검사 위반 0

## 12. 다국어 검증
- i18n 키 누락 검사 (CI)
- 의사 번역(Pseudo-localization)으로 UI 깨짐 검증
- 언어별 기능 시각 검증

## 13. AI 평가 (Evaluation)
- **데이터셋**: SDG 매핑 1,000건 (도메인 전문가 라벨링)
- **메트릭**: Precision, Recall, F1, MRR (top-3)
- **회귀 테스트**: 프롬프트·모델 변경 시 자동
- **수용 기준**: F1 ≥ 0.85, MRR ≥ 0.80
- **휴먼 평가**: 분기 100건 더블블라인드, Likert 1-5

## 14. AI 안전성 테스트
- Prompt Injection 회귀 (50건 시나리오)
- PII 마스킹 검증
- 시스템 명령 노출 검사
- 환각 검출 (값/인용 불일치)

## 15. 데이터 검증
- 마이그레이션: forward + rollback dry-run
- 백업/복구: 분기 훈련, 데이터 무결성 비교
- ETL: 소스-타겟 row count + 체크섬

## 16. 테스트 데이터 관리
- 합성 데이터 생성기 (Faker + 도메인 룰)
- 익명화: 결정론적 해싱 + 형식 보존
- 민감 데이터는 dev/local에서 사용 금지

## 17. 사용성 테스트 (UX)
- 5명 사용자 / 분기 (페르소나별)
- 태스크 성공률, 시간, SUS 점수
- 결과는 백로그 우선순위에 반영

## 18. 회귀 테스트 자동화
- 모든 버그 수정 시 회귀 테스트 추가 (정책)
- 회귀 셋 분기 리뷰, 가치 낮은 테스트 제거

## 19. 테스트 환경
- 로컬: Docker Compose
- CI: GitHub Actions runners
- E2E: 격리된 staging 테넌트
- 데이터: 매 실행 초기화 또는 분리 schema

## 20. 메트릭 & 리포팅
- 커버리지 리포트 (Codecov)
- E2E 안정성 (flake rate < 1%)
- 테스트 시간 (CI < 12분)
- 회귀 결함 비율 (분기당 < 5건)
