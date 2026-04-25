# ADR-0001: Modular Monolith를 출발점으로 채택한다

- 상태: Accepted
- 일자: 2026-04-25
- 작성자: Architect
- 관련 문서: `docs/11-system-architecture.md`, `docs/12-tech-stack.md`

## 컨텍스트
초기 팀 규모는 6-10명, MVP 12개월 일정이다. 마이크로서비스의 운영 오버헤드(배포·네트워크·관측성)가 제품 가치 검증보다 먼저 와선 안 된다. 동시에, 도메인 경계가 분명한 영역은 미리 모듈로 분리해 향후 추출(extract)을 쉽게 하고 싶다.

## 결정
NestJS 기반 **Modular Monolith**로 시작한다. 다음 영역만 별도 컨테이너로 분리한다:
- `apps/web` (Next.js — UI/BFF)
- `apps/api` (NestJS — 핵심 도메인 모놀리스)
- `apps/ai` (FastAPI — AI Gateway, 프롬프트·평가 진화 빠름)
- `apps/worker` (Node — 비동기 잡)

도메인은 NestJS 모듈 경계로 분리하되, 이벤트는 외부 메시지 버스(EventBridge + SQS)로 발행해 미래의 분리에 대비한다.

## 근거
- 운영 단순(단일 배포·관측), 대신 모듈 경계로 향후 분리 옵션 보존
- AI 영역은 Python 생태계 + 빠른 변화율 → 별도
- 비동기 워커는 자원 격리가 중요해 별도

## 결과
- (+) 출시 속도, 디버깅 용이, 비용 효율
- (-) 잘못된 모듈 경계는 결합도 증가 위험
- 위험: 모듈 경계 침범 → ESLint 룰(import 제한)로 가드. 통합 테스트로 도메인 이벤트 계약 검증.

## 대안
| 대안 | 장점 | 단점 | 기각 사유 |
|------|------|------|----------|
| Microservices | 독립 배포, 스케일 | 운영 비용↑, 분산 장애 | 팀 규모·일정에 비해 과함 |
| 단일 컨테이너 (AI 포함) | 단순 | Python·Node 혼재 어색 | AI 변화율·도구 차이로 분리 |

## 후속 액션
- [ ] NestJS 모듈 경계 ESLint 룰 설정
- [ ] 도메인 이벤트 계약(Outbox + EventBridge) 베이스라인 ADR
- [ ] 분리 트리거 기준 정의 (모듈 트래픽·팀 규모·배포 빈도)
