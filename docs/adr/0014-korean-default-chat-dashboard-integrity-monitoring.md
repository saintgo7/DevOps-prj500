# ADR-0014: Korean default + country-aware locale + real-time chat + SDG dashboard + 100% content integrity + admin-only monitoring

- 상태: Accepted (MVP 구현 시작; 일부 항목은 단계적 구현)
- 일자: 2026-04-25
- 작성자: Product / Architect, AI dialogue partner
- 관련 문서: [`PRINCIPLES.md`](../../PRINCIPLES.md), [`CONTENT_STANDARD.md`](../../CONTENT_STANDARD.md), ADR-0009 (언어 정책), ADR-0011 (발견·평이한 말), ADR-0012 (워치), ADR-0013 (칼럼·승인·파트너)

## 컨텍스트
플랫폼이 본격적으로 일상에 들어가면 다음 7개 결정이 동시에 필요해진다:

1. **메인 언어를 한국어로** — 운영 본거지가 한국임을 반영, 단 외국인 접속자는 그들의 언어로
2. **국가별 자동 언어 제공** — 접속 국가 IP 기반으로 자동 매핑, 사용자가 수동 변경 가능
3. **실시간 채팅** — 각자 모국어로 입력하지만 상대는 자기 언어로 읽음. 원문 보존, 자동 번역
4. **SDG 시각 카테고리 대시보드** — 17 Goals + 169 Targets + Post-SDGs 미래 의제까지 시각적으로 분류
5. **100% 컨텐츠 정합성 검증** — 외부 자료(연구·논문·기사·SNS)는 *반드시* 자동 검증을 통과해야만 노출
6. **세션 분리** — 외부 큐레이션 vs 본 플랫폼 자체 발행. 한 화면에 섞이지 않음
7. **승인된 관리자만의 모니터링 채널** — 새 연구·프로젝트 기획·전문가 협력 제안의 종합 감독

## 결정

### 1. 한국어 기본 + 국가→언어 자동 매핑

- `apps/web/src/i18n/routing.ts` 의 `defaultLocale` 을 `en` → **`ko`** 로 전환
- 국가 코드(ISO-3166 alpha-2)를 우선 언어로 매핑하는 `countryToLocale()` 헬퍼 추가
  - 한국 KR → `ko`, 일본 JP → `ja`, 중국 CN/TW/HK → `zh`, 사우디아라비아·이집트 등 22개국 → `ar`, 사하라이남 14개 LDC (BJ, BF, ML, NE, ...) → `fr`, 케냐·탄자니아·우간다 → `sw`, 인도 → `hi`, 방글라데시 → `bn`, 라틴아메리카 21개국 → `es`, 브라질·앙골라·모잠비크 → `pt`, 러시아·CIS → `ru`, 인도네시아 → `id`
  - 매핑되지 않은 국가는 영어 (en) — 명시적 fallback
- 우선순위: 사용자 명시 선택(쿠키) > URL 로케일 > IP 국가 매핑 > Accept-Language > 기본 ko
- ADR-0009 의 "사용자가 ko/ja/zh 등을 원하면 영어로 강제 다운그레이드 금지" 불변 규칙은 그대로 유지

### 2. 실시간 채팅 + 양방향 자동 번역

도메인 모델:
- `Conversation` — 한 건의 대화방. 멀티 참여자, 모든 멤버가 자기 언어 설정 보유
- `Message` — `originalText` + `originalLocale` (절대 손실하지 않음) + AI 번역 캐시 `translations: { [locale]: { text, model, confidence } }`

UI 패턴:
- 사용자는 자기 언어로 입력
- 다른 참여자는 자기 언어로 표시 (캐시된 번역 → 없으면 즉시 AI 호출)
- "원문 보기" 토글이 항상 가능
- 번역 신뢰도 < 0.7 시 명시적 경고
- AI 모델·번역 시각·번역자 (사람/AI) 메타데이터 매번 표시

기술:
- 전송: WebSocket Gateway (NestJS `@WebSocketGateway`) 또는 Server-Sent Events (MVP)
- 번역: Anthropic Claude (`apps/ai/`) + 번역 캐시 테이블
- 메시지 저장: Postgres + RLS (대화방 멤버만 접근)

MVP 범위 (이 ADR의 PR 1):
- ✅ Prisma 스키마 + 마이그레이션 + RLS
- ✅ 평이한 말 메시지 (chat 네임스페이스)
- ⏳ WebSocket Gateway / 실시간 송수신 — 후속 PR
- ⏳ 번역 호출 (apps/ai 통합) — 후속 PR

### 3. SDG 시각 대시보드

기존 홈은 17 Goals 그리드만 제공. 본 ADR 이후 4개 영역으로 재구성:

| 영역 | 내용 |
|------|------|
| 🎯 17 Goals | 컬러 + 번호 + 다국어 명칭 (이미 구현) |
| 🎯 169 Targets | Goal 클릭 시 sub-targets 드릴다운 (이미 구현) |
| 🌱 Post-SDGs (2030 이후) | UN High-Level Political Forum이 논의 중인 차기 의제 — 별도 카드 영역 (미래 의제 자리) |
| 📊 우리 임팩트 | 본 플랫폼이 자기 측정한 SDG 기여도 — `docs/21-impact-roadmap.md §5` |

각 영역은 SDG 공식 색상 시스템 (이미 `packages/ui/SdgBadge` 에 정의됨) 으로 시각 일관성 유지. 향후 UN 공식 SDG 아이콘 라이선스 (CC BY 4.0) 도입 검토.

### 4. 두 세션 분리: 외부 큐레이션 vs 자체 발행

`Column` 모델에 `origin` 필드 추가:
- `'external'` — 외부 출처를 큐레이션해 평이한 말로 요약 + 인용 (CONTENT_STANDARD)
- `'internal'` — 본 플랫폼 자체 발행 (큐레이터·연구자·이용자 기고)

UI/API 분리:
```
GET /v1/columns?origin=external   ← 외부 자료 세션
GET /v1/columns?origin=internal   ← 본 플랫폼 세션
GET /feed/{locale}/external.atom  ← 별도 피드
GET /feed/{locale}/internal.atom
```

이용자는 두 세션의 차이를 한눈에 알 수 있어야 한다 — 시각 마커 + 헤더 + 메타데이터.

### 5. 100% 콘텐츠 정합성 검증 (자동)

`ContentIntegrityVerifier` — `apps/api/src/columns/content-integrity.ts`. 외부 자료를 시스템에 들여올 때 **모든 규칙을 통과해야** 한다 (12개 규칙):

| # | 규칙 | 검증 방법 |
|---|------|----------|
| 1 | 출처 도메인이 신뢰 목록에 있거나 검증 가능 | `.gov.*` `.edu.*` 또는 화이트리스트 (UN·LDC 정부·논문 DB·등록 NGO) |
| 2 | 인증 식별자 (DOI / arXiv / ISSN / ISBN) 존재 | 정규식 + (선택) 외부 lookup |
| 3 | 작성자 명시 (익명 SNS 제외) | author 필드 != 'Anonymous' / null |
| 4 | URL https + 응답 200 (live) | optional fetch (MVP는 static check) |
| 5 | 라이선스 호환 또는 공정 인용 가능 | 알려진 CC/공공저작물 화이트리스트 |
| 6 | UN 제재 명단에 없음 | 시드된 sanctions 리스트 매칭 |
| 7 | 중복 아님 (content hash) | DB unique on `content_hash` |
| 8 | SDG 매핑 ≥ 1, confidence ≥ 0.70 OR 인간 확정 | `sdgFocus`/`sdgConfidence` 검사 |
| 9 | 평이한 말 요약 존재 (primary locale) | `bodyI18n[primaryLocale].summary` |
| 10 | 발췌 ≤ 250 단어 (CONTENT_STANDARD §5) | word-count |
| 11 | 본문에 시스템 명령 / prompt injection 의심 패턴 없음 | regex 화이트박스 |
| 12 | 미성년자·민감 PII 자동 검출 (이름 패턴 + 나이 단어) | LLM-assisted, 의심 시 인간 검토 강제 |

규칙은 **AND 결합 — 한 개라도 실패하면 발행 큐 진입 불가**. 시스템은 어떤 규칙이 왜 실패했는지 평이한 말로 큐레이터에게 통보.

### 6. 연구·프로젝트 기획 모듈 (관리자 한정)

새 모델:
- `ResearchProposal` — 큐레이션된 데이터에서 영감받은 신규 연구·프로젝트 기획안. 소유자 = 관리자 또는 인증된 연구자
- `ExpertOutreach` — 외부 전문가에게 협력 제안 (자기존엄·동의 우선; 자동 발신 X — ADR-0012 §협력 워크플로우와 동일)

API:
```
POST /v1/research-proposals       ← 관리자만 작성 (RBAC admin)
GET  /v1/research-proposals       ← 같은 테넌트 admin/reviewer 만 열람
POST /v1/research-proposals/:id/outreach
                                  ← 외부 전문가에게 메시지 초안 — 명시적 인간 발송 클릭 필수
```

### 7. 승인된 관리자만의 모니터링 채널

`MonitoringController` — `apps/api/src/monitoring/`. 다음 정보를 한 화면에 통합:
- 최근 30일 외부 콘텐츠 정합성 검증 통과율
- 발행 칼럼 카탈로그 (origin=external vs internal 비율)
- 승인 대기·만료·거부 통계
- 파트너 웹훅 발신 성공률
- 콘텐츠 기준 §6 균형 (LDC 30%·비영어 40%) 준수율
- 신규 연구 기획안·전문가 협력 제안 현황
- 의심스러운 자동 검증 실패 패턴 (12 규칙별 분포)

접근 통제:
- `@Roles('admin')` + 추가 동의 (관리자 두 명 모니터링 액세스 부여)
- 모든 모니터링 화면 접근은 감사 로그에 기록
- 익스포트 (CSV/JSON) 가능 — 다만 익스포트 자체가 감사 이벤트

## 근거
- 한국어 기본 = 운영 현실 반영 + 다른 사용자 권리 비훼손 (자동 매핑·수동 변경 모두 보장)
- 실시간 채팅 + 자동 번역 = ADR-0011 §4 "각자의 언어로 말하되 서로 이해" 의 직접 구현
- 시각 대시보드 + 두 세션 분리 = 정보 신뢰 (어디서 왔는가) + 인지 부하 감소
- 100% 정합성 = CONTENT_STANDARD.md §8 의 자동화 — 사람의 시간을 정말 중요한 결정에 쓰게 함
- 모니터링 = 신뢰는 "투명한 자기 측정" 에서 옴 (PRINCIPLES.md §10·12)

## 결과
- (+) 한국 사용자 첫 화면 진입 자연스러움 + 외국인 접속 시 모국어 자동 제공
- (+) 정합성 100% 자동 검증 → 큐레이터 시간 80%+ 절감, 잘못된 정보 발행 위험 ↓↓
- (+) 외부 vs 자체 분리로 사용자가 *어떤 출처인지* 항상 알 수 있음
- (+) 관리자 모니터링으로 의사결정 기반 데이터 가시화
- (-) 운영 부담: 신뢰 화이트리스트(도메인) 분기 갱신 필요
- (-) 실시간 채팅 + 번역은 비용·복잡도 큼 → 단계적 구현
- 위험: 100% 자동 검증의 false-negative (잘못된 자료 통과)
  - 완화: 매 발행물에 인간 승인 게이트 (ADR-0013) — 자동 검증은 *최소 기준*, 인간 승인이 *최종 기준*
- 위험: 자동 번역의 뉘앙스 손실
  - 완화: 원문 항상 보존, 신뢰도 표시, "원문 보기" 항상 토글 가능

## MVP 범위 (이 PR)
- ✅ 한국어 기본 + 국가→언어 매핑 (`countryToLocale`)
- ✅ ContentIntegrityVerifier (12 규칙) + 단위 테스트
- ✅ Column에 `origin` 필드 (internal/external) + 마이그레이션
- ✅ ResearchProposal + ExpertOutreach + Conversation + Message Prisma 스키마
- ✅ 마이그레이션 (RLS 적용)
- ✅ MonitoringController (관리자 한정)
- ✅ 13 locale 평이한 말 메시지 (dashboard/chat/research/monitor)

## 후속 PR (이 ADR로 확정된 설계, 구현은 단계적)
- ⏳ 실시간 채팅 WebSocket Gateway + 번역 호출 (apps/ai)
- ⏳ SDG 대시보드 UI (post-SDGs 카드 + 임팩트 패널)
- ⏳ 외부 콘텐츠 자동 신뢰 도메인 갱신 잡 (worker)
- ⏳ 모니터링 대시보드 UI

## 형평 / 신뢰 / 자기존엄 (재확인)
- AI는 **번역만 보조**, 발행·발신·연결 결정은 사람
- 외부 콘텐츠 검증 실패는 평이한 말로 큐레이터에게 *왜* 실패했는지 통보
- 모니터링 자체가 감사로그에 기록 — "감시하는 자도 감시받는다"
- 협력 제안은 자동 발신 절대 금지 (ADR-0012 §협력 재확인)
