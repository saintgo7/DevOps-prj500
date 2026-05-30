# 19. 관측성 & SRE (Observability)

## 1. 관측성 3축
| 신호 | 도구 | 보존 |
|------|------|------|
| Logs | Loki + 구조화 JSON | 30일 hot, 1년 cold(S3) |
| Metrics | Prometheus → Grafana Cloud / Mimir | 13개월 |
| Traces | Tempo (OTel) | 30일 |

- **표준**: OpenTelemetry SDK + Auto-instrumentation
- **Collector**: ADOT (AWS Distro)

## 2. 로깅 표준
- 모든 로그 JSON, 필수 필드:
  - `ts`, `level`, `service`, `env`, `request_id`, `trace_id`, `tenant_id`, `user_id`, `event`, `message`, `extra`
- PII 마스킹 (이메일·전화 자동)
- 로그 레벨: error / warn / info / debug
- prod 기본 info, 임시 debug는 30분 자동 만료

## 3. 메트릭 모델
### 3.1 RED (요청 단위)
- **R**ate, **E**rrors, **D**uration — 모든 HTTP/RPC 엔드포인트

### 3.2 USE (자원 단위)
- **U**tilization, **S**aturation, **E**rrors — CPU, 메모리, DB connections, queue depth

### 3.3 비즈니스 메트릭
- 활성 사용자, 활동 생성 수, 보고서 발행 수
- AI: 호출 수, 토큰, 캐시 hit, 평균 latency, 비용

## 4. 분산 추적
- traceId 전파: HTTP headers, SQS 메시지 attributes, BullMQ 작업
- 100% 샘플 (에러), 10% 샘플 (정상), AI 호출 100%
- 핵심 span 속성: tenant.id, user.id, ai.model, ai.tokens.in/out, ai.cache_hit

## 5. SLO (Service Level Objectives)
| 서비스 | 지표 | SLO (30d) |
|--------|------|-----------|
| Web/API | 가용성 | 99.9% |
| Web | LCP P75 | ≤ 2.5s |
| API read | P95 latency | ≤ 300ms |
| API write | P95 latency | ≤ 800ms |
| AI mapping | P95 latency | ≤ 5s |
| Report gen | P95 | ≤ 90s |
| 백그라운드 잡 성공률 | 24h | ≥ 99% |

- 에러 예산 소진율 ≥ 2x → 릴리스 동결, RCA

## 6. 알림 (Alerting)
| 우선순위 | 예시 | 통보 |
|---------|------|------|
| P1 | 가용성 < 99%, 데이터 손실, 보안 침해 | PagerDuty + 전화 |
| P2 | SLO 위반, 일부 기능 장애 | PagerDuty 일근시간 |
| P3 | 비SLO 이상, 성능 저하 | Slack |
| P4 | 정보 | 이메일 |

- 알림 피로 방지: 중복 그룹핑, 5분 deduplication

## 7. 대시보드
| 이름 | 목적 |
|------|------|
| Service Health | RED + 가용성 + 에러율 |
| Latency Heatmap | P50/P95/P99 |
| AI Operations | 모델별 토큰·비용·정확도 |
| Tenant Insights | 테넌트별 사용량·비용 |
| Database | 쿼리 P95, 연결, 잠금 |
| Queue/Worker | 깊이, 처리율, 실패 |
| Frontend (RUM) | Core Web Vitals |
| Business KPI | 활성, 보고서, NPS |

## 8. RUM (Real User Monitoring)
- Sentry Performance + Web Vitals
- 사용자별 세션 재현 (개인정보 마스킹)
- 에러 추적 → 릴리스/소스맵 매핑

## 9. 인시던트 관리
- 등급: P1/P2/P3
- 절차: detection → triage → containment → comms → recovery → postmortem
- 통신: 상태 페이지 (statuspage.io), Slack #incidents
- Postmortem: 24h 내, blameless 템플릿
- 액션 아이템 추적: 30일 내 완료

## 10. 온콜 (On-call)
- Primary + Secondary, 일주일 단위
- 보상: 평일 일근, 주말 추가 수당 (정책)
- 핸드오프 미팅 매주 월 09:00
- 온콜 부담 KPI: 야간 호출 < 2회/주

## 11. Runbook
- 모든 알림에 Runbook 링크 (필수)
- 표준 섹션: 증상, 가능 원인, 진단 명령, 완화, 에스컬레이션
- 분기별 Runbook 검토

## 12. 카오스·게임데이
- 분기 1회 게임데이 (시나리오 무지 상태)
- 결과 → Runbook 보강 + 알림 임계치 조정

## 13. 비용·FinOps
- 비용 대시보드 (서비스/테넌트/팀별)
- AI 비용 알림 (테넌트별 초과)
- 미사용 리소스 자동 알림 (월간)

## 14. SRE 메트릭
- DORA + 다음:
  - SLO 준수율
  - 에러 예산 소진율
  - Postmortem 액션 완료율
  - MTTD, MTTR

## 15. 사용자 영향 측정
- 특정 인시던트가 영향 준 테넌트·사용자 수 자동 산출
- SLA 위반 시 자동 크레딧 계산

## 16. 거버넌스
- 분기 SRE 리뷰: SLO 조정, 알림 정리, 도구 정합
- 신규 서비스 출시 전 Production Readiness Review (PRR)

## 17. 도구 구성
- **OTel Collector**: Sidecar 또는 DaemonSet
- **Grafana**: 자체 호스팅 (cost) 또는 Cloud (속도)
- **Sentry**: 자체 호스팅 옵션 검토
- **PagerDuty**: 외부, 통합 핵심
- **Slack**: 통신, ChatOps

## 18. 사용자 의사소통
- 상태 페이지: 실시간 영향 표시
- 사후 통보: P1·P2 인시던트 24h 내 메일
- 분기별 가용성 리포트 (Enterprise)
