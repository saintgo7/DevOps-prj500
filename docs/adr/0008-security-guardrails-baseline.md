# ADR-0008: 보안 가드레일 베이스라인 (Helmet + Throttler + Secret 스캐너)

- 상태: Accepted
- 일자: 2026-04-25
- 작성자: Security Lead
- 관련 문서: `docs/15-security-design.md`, `docs/14-api-spec.md` §8

## 컨텍스트
docs/15에 정의된 보안 통제는 인증/암호화/감사로그 등 굵직한 항목 위주이다. 일상적인 가드레일 (보안 헤더, 레이트 리밋, 비밀 노출 방지)을 베이스라인으로 즉시 적용해야 한다.

## 결정
- **HTTP 보안 헤더**: `helmet` 미들웨어 적용 (api). dev에선 CSP off, prod에선 helmet 기본 CSP. CORS는 명시적 origin allowlist + credentials.
- **레이트 리밋**: `@nestjs/throttler` 전역 ThrottlerGuard
  - short: 1초당 20 요청
  - long: 1분당 300 요청
  - `/v1/health`, `/v1/ready`, `/metrics`는 `@SkipThrottle()`
  - 추후 docs/14 §8의 티어별(Starter/Growth/Enterprise) 한도는 Throttler scope로 분기
- **입력 검증**: `ValidationPipe` 전역 (whitelist + forbidNonWhitelisted) — 알려지지 않은 필드 거부
- **쿠키**: HttpOnly + SameSite=Lax + Secure(prod)
- **비밀 스캐너**: `scripts/security-check.sh` 로컬 + Gitleaks(CI)
- **Helmet 옵션**:
  - `crossOriginResourcePolicy: cross-origin` — 다국어 정적 자산 호환
  - 기본 활성화: `xFrameOptions=DENY`, `xContentTypeOptions=nosniff`, `referrerPolicy=strict-origin-when-cross-origin`, HSTS

## 근거
- OWASP Top 10 즉시 대응 (Injection, Broken Access, Security Misconfig)
- 레이트 리밋으로 부르트포스·DoS 1차 방어
- 입력 화이트리스트로 over-posting 방지

## 결과
- (+) 베이스라인 보안, 신뢰성
- (-) 헤더/리밋 세부 튜닝은 부하 테스트 후 조정 필요
- 위험: WebSocket·SSE 도입 시 throttler 정책 별도 설계 필요

## 후속 액션
- [ ] 인증 사용자 티어별 레이트 리밋 (Starter 5 RPS, Growth 20, Enterprise 100+)
- [ ] CSRF 토큰 (cookie+state for non-API consumers)
- [ ] WAF 룰셋 (CloudFront WAF) — 인프라 단계
- [ ] 정기 침투 테스트 일정화
- [ ] HSTS preload 등록 (커스텀 도메인 확정 후)
