# 15. 보안 설계 (Security Design)

## 1. 보안 원칙
1. Defense in Depth — 다중 계층
2. Least Privilege — 최소 권한
3. Secure by Default — 기본 안전
4. Zero Trust — 어떤 요청도 신뢰하지 않음
5. Encrypt Everything — 암호화 필수
6. Auditable — 모든 행위 추적 가능

## 2. 위협 모델링 (STRIDE)

| 위협 | 벡터 예시 | 대응 |
|------|----------|------|
| **S**poofing | 세션 탈취, SSO 우회 | TLS 1.3, MFA, 토큰 짧게, 디바이스 핑거프린트 |
| **T**ampering | API 페이로드·파일 변조 | 입력 검증, JSON Schema, 파일 sha256, 서명 |
| **R**epudiation | 행위 부인 | 감사로그 (불변, 7년), 결재선 |
| **I**nformation Disclosure | 멀티테넌시 누수 | RLS, 통합 테스트, 펜테스트 |
| **D**enial of Service | 대용량 입력, AI 폭주 | Rate limit, WAF, AI 토큰 한도, 비용 알림 |
| **E**levation of Privilege | RBAC 우회 | 정책 단일 평가지점(PEP), 정기 감사 |

## 3. 네트워크 보안
- VPC private subnet 기본, public 최소
- AWS WAF (OWASP Top 10 룰셋, geo-block 옵션)
- Shield Standard (Advanced 검토)
- Internal mTLS (서비스 간), AWS Certificate Manager
- Egress 제한: 외부 도메인 화이트리스트 (Anthropic, AWS, S3)

## 4. 인증
- 비밀번호: Argon2id, 12자 이상, 누출 비밀번호 차단 (HIBP)
- MFA: TOTP, WebAuthn(Passkey), SMS 미사용
- SSO: OIDC, SAML 2.0 (Enterprise), SCIM 2.0 사용자 동기화
- 세션: HttpOnly + Secure + SameSite=Lax 쿠키, 15분 idle, 8h max

## 5. 인가 (RBAC + ABAC)
- 역할: admin, reviewer, contributor, viewer, auditor
- 속성: 조직, 부서, 데이터 분류
- 정책 평가: OPA(Rego) 또는 Casbin — 단일 진입점
- 모든 리소스 접근 정책 평가 + 감사 기록
- 4-eyes: 보고서 발행은 두 명 승인 필수 (정책)

## 6. 데이터 보호
- **저장**: 디스크 AES-256 (EBS, RDS), 컬럼 암호화 (PII, AES-GCM + KMS)
- **전송**: TLS 1.3, HSTS, 내부 mTLS
- **키 관리**: AWS KMS, 자동 회전 1년, 테넌트별 CMK (Enterprise)
- **백업**: 암호화 + 별도 계정 + immutable (S3 Object Lock)
- **클라이언트 측**: 민감 입력은 IndexedDB 미저장, 메모리만

## 7. 비밀 관리
- AWS Secrets Manager + 자동 회전
- 코드 내 비밀 0 (TruffleHog CI)
- ENV는 IaC 산출, GitHub Secrets는 OIDC로 단기 토큰만
- `.env` 파일 git 무시, pre-commit 훅

## 8. 입력·출력 검증
- 입력: Zod/Pydantic 스키마, 화이트리스트
- 출력: HTML 이스케이프, CSP 엄격 (`default-src 'self'`)
- 파일 업로드: MIME 검증, 안티바이러스(ClamAV), 별도 도메인 제공

## 9. AI 보안 (Specific)
- **Prompt Injection 방어**:
  - 시스템 프롬프트 분리, 사용자 입력 명확 구분
  - Tool Use 결과만 신뢰
  - 출력에서 명령 실행성 감지(우리 시스템 명령어 패턴)
- **민감 데이터**: PII 마스킹 후 호출
- **모델 출력**: 신뢰도·인용 표기, 인간 검수 필수
- **로그 보관**: 12개월, 분석은 익명화 후
- **Bedrock 옵션**: AWS 내부 데이터 처리

## 10. 감사로그 (Auditing)
- 모든 변경(create/update/delete) 기록
- 인증 이벤트, 권한 변경, 데이터 접근 (Sensitive)
- 불변(append-only), 7년 보존, 외부 SIEM 송출 (S3 + Athena)
- 검색 도구: 관리자/Auditor 전용

## 11. 취약점 관리
- SAST: Semgrep, GitHub CodeQL
- DAST: OWASP ZAP 야간
- SCA: Snyk + Dependabot
- 컨테이너: Trivy, Distroless 베이스
- 정기 펜테스트: 분기 (외부 1회/년 + 자체 분기)
- 버그 바운티 (HackerOne) — 출시 6개월 후

## 12. 인시던트 대응 (IR)
- IR 플레이북: detection / triage / containment / eradication / recovery / lessons
- 24/7 온콜 (출시 후), PagerDuty
- 통보 시한: GDPR 72h, 한국 24h
- 고객 통보 템플릿, 외부 PR 협력
- 분기별 IR 훈련 (table-top)

## 13. 비즈니스 연속성 (BCP/DR)
- RTO 1h / RPO 15m (Enterprise: 30m / 5m)
- DR 사이트: EU 리전 stand-by
- 분기 DR 훈련, 전체 페일오버 연 1회

## 14. 컴플라이언스 매핑 (요약)
| 통제 | SOC 2 | ISO 27001 | ISMS-P |
|------|-------|----------|--------|
| 접근 제어 | CC6 | A.9 | 2.5 |
| 암호화 | CC6 | A.10 | 2.7 |
| 변경관리 | CC8 | A.12.1 | 2.9 |
| 모니터링 | CC7 | A.12.4 | 2.10 |
| IR | CC7 | A.16 | 2.11 |

## 15. 보안 운영 메트릭
- 평균 패치 시간 (MTTP): Critical 24h, High 7d, Medium 30d
- 펜테스트 발견 사항 SLA: Critical 24h, High 7d
- 보안 인시던트 (P1) 분기 0건 목표
- 비밀 누출 사고 0건

## 16. 책임 (RACI)
- Security Lead: A (보안 전체)
- DPO: A (데이터 보호)
- Tech Lead: R (구현)
- 모든 직원: R (보안 교육 분기 1회)
- 외부 감사인: C (펜테스트, 인증)

## 17. 보안 교육
- 신규 입사 4시간 보안 오리엔테이션
- 분기 피싱 시뮬레이션
- 연간 OWASP Top 10·AI 보안 워크숍

## 18. 폐기·반환
- 서비스 종료 시 90일 데이터 반환 기간
- 종료 후 30일 내 안전 삭제 (NIST 800-88)
- 삭제 증명서 발급
