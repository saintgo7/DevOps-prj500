# ADR-0007: 관측성 베이스라인 (pino + Prometheus + structlog)

- 상태: Accepted
- 일자: 2026-04-25
- 작성자: SRE Lead
- 관련 문서: `docs/19-observability.md`, ADR-0005

## 컨텍스트
ADR-0005에서 OTel + Grafana 스택 채택을 결정했다. 그러나 OTel SDK 풀 통합은 운영 환경 (Tempo/Loki/Prometheus) 구축이 선행되어야 한다. 그 사이에 즉시 가치를 줄 베이스라인이 필요하다.

## 결정
- **로깅**: 모든 서비스 구조화 JSON
  - Node (api/worker): `pino` + `nestjs-pino` (api), 비밀 redact, 표준 필드 (`service`, `env`, `request_id`, `tenant_id`, `trace_id` placeholder)
  - Python (ai): `structlog` + JSONRenderer + contextvars
- **요청 ID**: 모든 서비스가 `X-Request-Id` 헤더를 받아 검증·생성하고 응답 헤더에 echo
- **메트릭**: Prometheus 호환 `/metrics` (api: `prom-client`, ai: `prometheus-client` 차후)
  - 기본 process 메트릭 + HTTP duration histogram
- **헬스/레디**: `/v1/health` (liveness, no DB), `/v1/ready` (DB ping)
- **OTel SDK**: 추후 동일 인터페이스로 추가 (pino → otel pino-transport, prom → OTel exporter)

## 근거
- 즉시 운영 가능한 최소 셋
- 표준 OSS 의존, 벤더 락 없음
- 향후 OTel SDK 도입 시 코드 변경 최소화 (구조화 로그·request_id는 그대로 활용)

## 결과
- (+) 디버깅·인시던트 분석 가능, Prometheus scrape 즉시 가능
- (-) 분산 추적 미적용 (단일 서비스 단위 로그/메트릭만)
- 위험: 라벨 카디널리티 폭증 → 경로 라벨에 raw path 사용 시 주의 (`/users/:id` 형태로 정규화)

## 후속 액션
- [ ] OTel SDK 통합 (Node `@opentelemetry/sdk-node`, Python `opentelemetry-instrumentation-fastapi`)
- [ ] 분산 추적 traceId 전파 (HTTP header, BullMQ job data, Anthropic 호출)
- [ ] Grafana 대시보드 시드 (Service Health, AI Ops, Tenant Insights)
