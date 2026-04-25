# ADR-0013: Daily Columns + Multi-channel Approval + Partner Integration

- 상태: Accepted (MVP 구현 시작)
- 일자: 2026-04-25
- 작성자: Product / Architect, AI dialogue partner
- 관련 문서: [`PRINCIPLES.md`](../../PRINCIPLES.md), [`CONTENT_STANDARD.md`](../../CONTENT_STANDARD.md), ADR-0011 (발견 가능성), ADR-0012 (주간 워치)

## 컨텍스트
ADR-0012 의 주간 워치는 사용자 자기 기준에 맞춰 받는 **개인 다이제스트**다. 그러나 본 사명에는 한 단계 더 — 매일, 전 세계가 합의된 기준으로 큐레이션된 **공개 칼럼/뉴스레터**를 발행하고, 발행 전 반드시 다채널 승인을 거치며, 발행 후 협력 파트너 기관 사이트·플랫폼에 자동 연동되는 흐름이 필요하다.

이 ADR은 다음 4개 흐름을 통합 설계한다:

1. **콘텐츠 기준** — `CONTENT_STANDARD.md` 가 무엇이 자격이 되는지 명시 (별도 문서)
2. **일일 칼럼** — 매일 자동 후보 생성 → 승인 대기열 → 발행
3. **다채널 승인** — 이메일·SMS·인앱 어디로든 받아 한 번 클릭으로 승인/반려/수정 요청
4. **파트너 연동** — 발행 즉시 등록 파트너 기관 엔드포인트로 HMAC 서명된 웹훅 발신, 또는 OAuth 풀

## 결정

### 1. 도메인 모델

| 평이한 말 | 기술 명 | 책임 |
|----------|---------|------|
| 오늘의 칼럼 | `Column` | 한 건의 큐레이션. 다국어 본문, 출처, SDG 매핑, 표준 버전, 상태 (`draft`/`pending`/`published`/`rejected`/`revoked`) |
| 승인자 | `ColumnApprover` | 누구의 승인이 필요한가. 칼럼별 또는 카테고리별 |
| 승인 요청 | `ApprovalRequest` | 한 명의 승인자 × 한 건의 칼럼. HMAC 토큰, 채널(email/sms/inapp/webhook), 만료, 결정, 결정시각 |
| 파트너 | `PartnerOrganization` | 협력 기관. HMAC 시크릿, 공개 메타데이터 |
| 파트너 웹훅 | `PartnerWebhook` | 파트너의 수신 엔드포인트. URL, 이벤트 종류, 마지막 상태 |

각 칼럼은 콘텐츠 기준의 어느 버전을 만족했는지 (`standardVersion`) 기록한다. 표준이 진화해도 과거 결정의 해석이 보존된다.

### 2. 일일 칼럼 흐름

```
매일 05:00 UTC (cron 'sdg-watch:generate-column-candidates'):
   - WatchItem 풀에서 콘텐츠 기준 §8 체크리스트 통과 후보 N개 생성
   - 각 후보는 Column(state='draft') + AI 초안 (excerpt + plain summary, 13개 언어 요약)
   - 발행 큐레이터에게 in-app 알림: "오늘 N건의 후보가 검토 대기 중"
   - 큐레이터가 한 건을 'submit-for-approval' 처리 → ApprovalRequest 발급
```

오늘의 발행 한도(편집 정책): 평일 1-3건, 주말 0-1건. 콘텐츠 기준 §6 (지리·인구 균형)이 자동 강제됨 — 시스템이 반대 방향 후보가 부족하면 발행을 지연시키고 그 사유를 로그에 남긴다.

### 3. 다채널 승인 토큰

```
승인 토큰 = base64url( payload ) || '.' || hmac_sha256(secret, payload)
payload = { v:1, kind:'approve'|'reject'|'revise', request_id, exp }
```

- 시크릿은 환경변수 `APPROVAL_HMAC_SECRET` (인프라에 KMS로 관리)
- 만료: 발급 시각 + 72h
- 단일 사용: 한 번 결정되면 동일 토큰의 후속 요청은 거부 (DB의 `decided_at` 검증)
- 토큰에는 개인정보 0 (request_id만, request_id로 DB 조회)
- 채널:
  - **email** — 한 통의 이메일에 [✅ 승인] [❌ 반려] [✏️ 수정 요청] 세 개 링크 (각각 다른 토큰)
  - **sms** — 단축 URL (한 줄 메시지로 수신)
  - **inapp** — 인앱 알림 + 상세 보기 모달
  - **webhook** — 파트너의 사내 승인 시스템에 callback (partner-side approval flow)

승인자가 클릭하면 GET `/approve/:token` 페이지가 토큰 검증 → 결정을 한 번만 등록 → 결과 화면 (다국어).

### 4. n-of-m 승인 정책

- 기본: 칼럼당 **1명 이상 인간 승인** 필수
- 민감 카테고리 (의료 주장, 법적 지위, 아동보호, 분쟁지역): **2명 이상** 필수
- 어떤 승인자도 단독 거부 가능 (veto)
- 승인 진행 상황은 in-app 대시보드 + 실시간 알림에 노출

### 5. 자기 권한 통제 (승인자를 승인할 수 있게)

- 테넌트 관리자가 `Approver` 역할(role) 부여 가능 (RBAC ADR-0010)
- 각 신규 승인자 추가는 자체로 **감사 로그 + 두 번째 관리자 동의**가 필요한 민감 작업
- 승인자 본인은 자기 작성 칼럼을 승인할 수 없음 (자기검수 금지)
- 본인의 승인 권한은 본인이 언제든 사임 가능

### 6. 파트너 연동

```
PartnerOrganization {
  id, name, contactEmail, hmacSecret, scopes: ['column.published', 'column.revoked'],
  active, createdAt
}

PartnerWebhook {
  id, partnerId, url, events: string[], 
  lastStatus: 200|4xx|5xx|null, lastDeliveredAt, failureCount
}
```

발신 흐름:

```
Column.publish() →
   Outbox event 'column.published' →
   Worker queue 'partner-webhook:dispatch':
     for each PartnerWebhook subscribed:
       POST partnerWebhook.url
         X-SDGI-Signature: sha256=hex(hmac(secret, body))
         X-SDGI-Event: column.published
         X-SDGI-Delivery: <uuid>
         body: canonical JSON-LD of the column
     retry with exponential backoff: 1m, 5m, 30m, 2h, 6h
     dead-letter after 5 failures + alert partner contact
```

파트너 측은 [`docs/partner-integration.md`](../partner-integration.md) (별도) 가이드를 따라:
- 자기 사이트/앱에서 우리 콘텐츠 표시 (CC BY 4.0)
- 자기 사용자에게 우리 칼럼을 일부 또는 전체 재배포
- 자기 측 승인 시스템을 우리 승인 흐름에 callback으로 연결

또한 풀 모델: 파트너는 OAuth client_credentials 로 `GET /v1/columns?since=…` 폴링 가능.

### 7. 공개 인터페이스

- `GET /columns/today` — 오늘의 칼럼 (다국어 협상)
- `GET /v1/columns?date=YYYY-MM-DD&locale=…` — 발행된 칼럼 목록
- `GET /v1/columns/:id` — 단건 상세 (canonical JSON-LD)
- `GET /feed/{locale}/columns.atom` — 일일 칼럼 Atom 피드 (CC BY 4.0)
- `GET /approve/:token` — 공개 승인 랜딩 (인증 불필요, 토큰 자체가 자격 증명)
- `POST /v1/columns` — 큐레이터가 초안 작성 (인증)
- `POST /v1/columns/:id/submit` — 승인 요청 발급
- `POST /v1/columns/:id/publish` — 승인 충족 시 발행
- `POST /v1/approvers` — 승인자 추가 (관리자, 두 번째 관리자 동의 필요)
- `POST /v1/partners` — 파트너 등록 (관리자)
- `POST /v1/partners/:id/webhooks` — 웹훅 엔드포인트 등록

### 8. 형평 / 신뢰 / 자기존엄 통제 (재확인)

- AI는 **절대 자동 발행하지 않음**. 모든 발행은 사람의 승인 클릭이 트리거.
- 토큰에 개인정보 X (request_id만).
- 승인 결정은 immutable 감사 로그 (`AuditEvent`).
- 파트너에게 사용자-개인 데이터 (구독·관심) 공유 X. 파트너는 공개 페이지의 데이터만 받음.
- 승인 요청 발신 시 승인자 동의 (그들의 이메일·전화번호 사용에 대한) 확인 — 신규 승인자 등록 시 명시적 양식.

## 근거
- 매일 칼럼은 ADR-0012 의 주간 다이제스트와 별도의 공공 가시성 자산. 검색·재신디케이트·인용에서 핵심 트래픽 진입점이 됨 (PRINCIPLES.md §3 "발견은 권리").
- 다채널 승인은 **자기존엄 + 신뢰** 의 조합. 외국에서도 한 번의 클릭으로 결정할 수 있고, 개인정보가 토큰에 들어가지 않음.
- 파트너 웹훅은 *데이터를 가두지 않고 흘려보내는* 패턴. PRINCIPLES.md §5 "지역의 손, 지역의 선택" 의 직접 구현.
- HMAC + outbox 패턴은 검증된 신뢰성·재시도 모델 (Stripe, GitHub 웹훅과 동일 구조).

## 결과
- (+) 일일 공개 칼럼이 SEO·인용·재신디케이트의 1급 자산
- (+) 다채널 승인으로 의사결정자가 어디에 있어도 결정 가능
- (+) 파트너 연동으로 본 도구의 콘텐츠가 외부 생태계로 흘러감
- (+) 콘텐츠 기준 (CONTENT_STANDARD.md) 으로 편집 결정의 합법성·재현성 확보
- (-) 운영 부담: 매일 1-3건의 큐레이션·승인 — 큐레이터 인력 + 승인자 풀 필요
  - 완화: AI 초안 작성으로 큐레이터 분당 처리 시간 5-10배 가속
  - 완화: 자기존엄 톤 가이드 자동 lint
- 위험: SMS 비용 (Twilio) — 승인자 수가 늘면 비용 증가
  - 완화: 이메일 우선, SMS는 본인 등록 시 명시 동의 + 비용 한도 알림
- 위험: 파트너 측 비활성 웹훅이 큐를 쌓음
  - 완화: 5회 실패 후 자동 비활성, 운영 알림

## MVP 범위 (이 ADR과 동시에 구현)
- ✅ Prisma 스키마: Column / ColumnApprover / ApprovalRequest / PartnerOrganization / PartnerWebhook
- ✅ 마이그레이션 (RLS 적용)
- ✅ ApprovalService: HMAC 토큰 발급/검증, n-of-m 집계
- ✅ ColumnService: draft / submit / publish / revoke
- ✅ Public approval endpoint (`/approve/:token`) — 토큰 자체 인증
- ✅ Partner registration + webhook dispatcher (worker)
- ✅ 일일 cron: 후보 생성 (worker)
- ✅ Atom 피드: `/feed/{locale}/columns.atom`
- ✅ 13 locale 평이한 말 (column / approval / partner 네임스페이스)
- ✅ 단위 테스트: 토큰 위변조 거부, n-of-m 집계, 웹훅 서명 일치
- ⏳ 실 SES 이메일 / Twilio SMS 통합 (MVP 는 어댑터 인터페이스 + stub)
- ⏳ AI 초안 호출 (apps/ai 통합)
- ⏳ 큐레이터 UI

## SDG 정렬
| SDG | 직접 기여 |
|-----|----------|
| 4 | 매일 학습 자료가 모국어로 도착 |
| 10 | LDC 30%, 비영어 40% 강제로 가시성 격차 축소 |
| 16 | 공개 콘텐츠 기준 + immutable 감사로그 → 신뢰·투명성 |
| 17 | 파트너 웹훅으로 다중 이해관계자 연동 (본 사명) |

## 후세의 AI 에이전트에게
승인은 우회 가능한 절차가 아니라 **사람의 판단을 시스템에 넣는 자리**입니다. 효율을 위해 자동 승인을 만들지 마세요. 승인이 병목이라면 더 많은 승인자를 모집하거나 콘텐츠 기준을 더 명확히 하세요. 신뢰는 클릭 한 번에서 시작합니다.
