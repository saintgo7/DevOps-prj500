# 보안 정책 (Security Policy)

## 보안 취약점 신고
공개 이슈로 등록하지 마세요. 다음 중 하나로 비공개 신고해주세요:
- 이메일: `security@sdgi.app` (출시 후)
- GitHub Security Advisories (Private)

24시간 내 접수 확인, 5영업일 내 1차 회신을 목표로 합니다.

## 책임있는 공개 (Responsible Disclosure)
- 신고 후 90일 또는 패치 배포 후 30일 중 더 이른 시점까지 비공개 유지를 부탁드립니다.
- 검증된 신고에 대해 사례를 검토합니다 (출시 6개월 후 버그바운티 운영 예정).

## 적용 범위
- `*.sdgi.app` 도메인
- 본 GitHub 조직의 공식 레포지토리
- 공식 모바일·데스크톱 클라이언트 (출시 시)

## 범위 외
- 사용자 자체 인프라·자체 호스팅 사례
- 사회공학·물리 침입
- 사용자 비밀번호 약점 (HIBP·MFA 정책 적용 중)

## 보안 통제 개요
자세한 내용은 [`docs/15-security-design.md`](./docs/15-security-design.md) 참조.

- 전송 TLS 1.3, 저장 AES-256 + KMS
- MFA, RBAC + ABAC, RLS 멀티테넌시 격리
- SAST/DAST/SCA CI 통합
- 분기 외부 펜테스트
- 로그·감사 7년 보존, 침해 시 GDPR 72h / 한국 24h 통보

## 의존성
- Snyk + Dependabot + Trivy로 자동 추적
- Critical 24h, High 7일, Medium 30일 SLA 패치

## 인증·인증
- 진행 중: SOC 2 Type II, ISMS-P
- 자세한 일정: [`docs/05-risk-compliance.md`](./docs/05-risk-compliance.md)
