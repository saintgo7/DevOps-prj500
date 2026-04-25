# ADR-0005: 관측성은 OpenTelemetry + Grafana 스택으로 표준화

- 상태: Accepted
- 일자: 2026-04-25
- 작성자: SRE Lead
- 관련 문서: `docs/19-observability.md`

## 컨텍스트
모든 서비스(웹·API·AI·워커)에서 일관된 로그·메트릭·트레이스가 필요하고, 벤더 락은 피하고 싶다. 비용 통제도 중요하다.

## 결정
- **계측**: OpenTelemetry SDK + 자동 계측, ADOT Collector
- **저장**:
  - 트레이스: Tempo
  - 로그: Loki (구조화 JSON)
  - 메트릭: Prometheus (장기 보존은 Mimir)
- **시각화/알림**: Grafana, Alertmanager → PagerDuty
- **에러**: Sentry (RUM·릴리스 매핑 강점)

## 근거
- OTel 표준 → 스토리지 교체 가능 (벤더락 회피)
- Grafana 스택은 OSS·자체 호스팅 가능, 비용 효율 (Datadog 대비 1/3 추정)
- Sentry는 RUM·소스맵에서 우수

## 결과
- (+) 비용·이식성·일관성
- (-) 자체 호스팅 운영 부담 → 초기에는 Grafana Cloud 무료 티어로 시작 가능
- 위험: 대용량 로그 비용 → 인덱스 정책·샘플링·라벨 카디널리티 가드

## 대안
| 대안 | 장점 | 단점 | 기각 사유 |
|------|------|------|----------|
| Datadog | 통합·UX 우수 | 비용 큼 | 초기 ROI 낮음 |
| New Relic | 통합 | OTel 호환 부분적, 가격 | 동일 |
| 자체 ELK | 친숙 | Elastic 라이선스 변경, 운영 부담 | 부담 큼 |

## 후속 액션
- [ ] OTel Collector 베이스 + 자동 계측 적용
- [ ] 표준 라벨 정의 (`tenant_id`, `request_id`, `trace_id`)
- [ ] 카디널리티 알림 (라벨 폭증 방지)
- [ ] Grafana 대시보드 시드 (Service Health, AI Ops)
