# 09. 비기능 요구사항 (NFR)

## 1. 성능 (Performance)
| 영역 | 지표 | 목표 |
|------|------|------|
| 페이지 로드 (LCP) | P75 | ≤ 2.5s |
| 인터랙션 (INP) | P75 | ≤ 200ms |
| Layout Shift (CLS) | P75 | ≤ 0.1 |
| API 응답 (read) | P95 | ≤ 300ms |
| API 응답 (write) | P95 | ≤ 800ms |
| AI 매핑 추천 | P95 | ≤ 5s |
| 보고서 생성 (단일 표준) | P95 | ≤ 90s |
| 데이터 임포트 (10K rows) | 평균 | ≤ 60s |

## 2. 가용성 (Availability)
| 티어 | SLA | 월 다운타임 |
|------|-----|------------|
| Starter | 99.0% | 7.3h |
| Growth | 99.5% | 3.6h |
| Enterprise | 99.9% | 43m |
| 계획 점검 | SLA 제외 | 월 2h |

- RTO: 1h, RPO: 15분 (Enterprise: RTO 30m, RPO 5m)
- 멀티 AZ 기본, 멀티 리전 액티브-패시브 (Enterprise)

## 3. 확장성 (Scalability)
- 동시 사용자 10,000+
- 단일 테넌트 활동 100만 건
- 단일 보고서 데이터 포인트 100만 건
- 월 AI 호출 1,000만+
- 자동 수평 확장 (HPA), DB 읽기 복제, 캐시(Redis)

## 4. 보안 (Security) — 자세한 내용 docs/15
- 전송: TLS 1.3, HSTS, mTLS 내부
- 저장: AES-256 + AWS KMS, 컬럼암호화 (PII)
- 인증: OIDC/SAML, MFA 강제(관리자), Passkey 지원
- 인가: RBAC + ABAC, RLS (DB 수준 테넌트 격리)
- 감사로그: 이벤트당 < 100ms 비차단 기록, 7년 보존
- 비밀: AWS Secrets Manager, 코드 내 비밀 0
- 정기 펜테스트 분기 1회

## 5. 접근성 (Accessibility)
- WCAG 2.2 AA 준수
- 키보드 전용 네비게이션 100%
- Screen Reader 호환 (VoiceOver, NVDA, JAWS)
- 명도 대비 4.5:1 (텍스트), 3:1 (UI)
- 자동 검사: axe-core CI 통합
- 사용자 검사: 분기당 1회 외부 a11y 감사

## 6. 국제화·현지화 (i18n/l10n)
- 1차 언어: 한국어, 영어, 일본어
- 확장: 중국어(간체), 스페인어, 프랑스어
- 통화·날짜·숫자 로케일별 포매팅 (ICU)
- RTL 미지원 (v1)
- 번역 워크플로우: Crowdin 또는 자체 + Claude 보조

## 7. 데이터 (Data)
- 백업: 일일 + 주간, 30일 보존, 분기 복구 훈련
- 보존: 활성 데이터 무제한, 비활성 7년 후 익명화
- 삭제: GDPR Right to Erasure, 30일 내 처리
- 데이터 위치: 한국(ap-northeast-2), EU(eu-west-1), 옵션 일본
- 백업 암호화 + 별도 계정 격리

## 8. 호환성 (Compatibility)
- 브라우저: Chrome/Edge 마지막 2버전, Safari 16+, Firefox 마지막 2버전
- 모바일: 반응형 (Tablet 우선, Phone 보조)
- 모바일 네이티브: v2 이후
- API 버저닝: SemVer, 주 버전 24개월 지원

## 9. 유지보수성 (Maintainability)
- 코드 리뷰: PR당 2명 이상 승인
- 정적 분석: ESLint, Ruff, mypy/tsc strict
- 테스트 커버리지: Unit 80%+, E2E 주요 흐름 100%
- 기술 부채: SonarQube Tech Debt Ratio < 5%
- 문서: 주요 모듈별 README, ADR 필수

## 10. 관측성 (Observability) — 자세한 내용 docs/19
- 로그: 구조화 JSON, 30일 보존, 검색 가능
- 메트릭: RED/USE 모델, 1초 단위
- 트레이싱: OpenTelemetry, 100% 샘플 (에러), 10% (정상)
- 알림: SLO 위반·이상 패턴 즉시 PagerDuty

## 11. 비용 (Cost / FinOps)
- 단위 비용 (per tenant per month) 추적
- AI 토큰 사용 가시화 (조직별, 사용자별)
- 비정상 사용 시 자동 알림·제한
- 월별 FinOps 리뷰

## 12. 컴플라이언스 (Compliance) — docs/05 참조
- GDPR, 한국 개인정보보호법, APPI
- ISMS-P, SOC 2 Type II (12개월 내)
- 접근성 (WCAG 2.2 AA, KS X OT 9241)

## 13. 사용성 (Usability)
- TTV (Time-to-First-Value) ≤ 7일
- 신규 사용자 온보딩 완료율 ≥ 80%
- SUS (System Usability Scale) ≥ 75
- 인앱 도움말, 가이디드 투어, 컨텍스트 도움말

## 14. 신뢰성 (Reliability of AI Outputs)
- 모든 AI 생성 결과에 신뢰도·인용 표기
- 환각 검출 휴리스틱 (값 검증, 매핑 일관성)
- 인간 검수 게이트 필수 (보고서 발행 전)
- AI 모델 변경 시 회귀 테스트 (라벨링 셋 1,000건+)

## 15. 환경 영향 (Sustainability of the SaaS itself)
- 탄소·전력 사용량 측정·보고 (자체 적용)
- 가능한 한 저탄소 리전 사용
- 효율적 모델 라우팅 (Sonnet vs Opus)
- 분기별 자체 SDG 보고서 공개

## 16. 검수 (Verification)
- 성능: k6/Locust 부하 테스트 (스테이징 분기)
- 보안: SAST/DAST/SCA CI, 분기 펜테스트
- 가용성: 카오스 엔지니어링 분기 1회
- a11y: axe + 스크린리더 수동 검사 분기
