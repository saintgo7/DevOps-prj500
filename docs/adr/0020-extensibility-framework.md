# ADR-0020: 확장성 프레임워크 — 미래의 SDG 혁신가가 코어를 건드리지 않고 새 기능을 더할 수 있게

- 상태: Accepted (MVP 구현 시작; 단계적 통합)
- 일자: 2026-04-26
- 작성자: Product / Architect, AI dialogue partner
- 관련 문서: ADR-0001 (모듈러 모놀리스), ADR-0002 (RLS), ADR-0007 (관측), ADR-0008 (보안 가드), ADR-0011 (평이한 언어), ADR-0013 (승인·파트너 webhook), ADR-0017 (감사·일관성), ADR-0019 (AI provenance)

## 컨텍스트

ADR-0019까지 우리는 발견 → 큐레이션 → 연구 → 도서 → 임팩트 검증 → 자금 → 메이커 → 매칭 → AI 사업계획서까지 **15개 도메인**을 코드로 만들었다. 그러나 SDG는 살아 있는 의제다. 내일의 실천가가 오늘 우리가 미처 생각하지 못한 도메인을 필요로 할 것이다 — 예를 들어:

- 지역별 생물다양성 모니터링 카드
- 청소년 동아리 출석·참여 기록
- 공유 농기구 예약·반납
- 마을 단위 발전 가능성 평가지표
- 무동력 정수기 정비 일지

각 도메인을 매번 ADR + Prisma 모델 + 서비스 + 컨트롤러로 만드는 건 *확장가능하지 않다.* 우리는 다음을 보장하면서 *코어를 건드리지 않고* 도메인을 추가할 수 있는 길을 만들어야 한다:

1. **멀티테넌시 격리** — 새 도메인도 RLS 안에서 살아간다
2. **본 플랫폼 원칙 자동 상속** — 비영리, 평이한 언어, 해로운 콘텐츠 가드, AI provenance, 감사 로그
3. **거버넌스** — 검수 게이트 + super-admin 즉시 차단
4. **보안** — 잘못 만든 확장이 다른 테넌트의 데이터를 새지 않게

## 결정

확장은 다음 6가지 빌딩 블록으로만 표현된다:

1. **PluginManifest** — 확장 한 건의 신원 (id, version, owner, scopes, signed manifest hash)
2. **CustomDomain** — 새 데이터 타입의 *선언* (이름 + JSON Schema)
3. **CustomRecord** — CustomDomain의 인스턴스 (RLS-bound)
4. **CustomWorkflow** — CustomDomain 위에 올라가는 *선언적* 상태 머신
5. **DomainEvent** — 코어 + 커스텀 도메인이 emit하는 append-only 감사·구독용 이벤트
6. **EventSubscription** + **CapabilityToken** + **FeatureFlag** — 확장이 *외부로* 통신하는 길과 super-admin 차단 스위치

새 코드를 한 줄도 안 쓰는 확장이 가능해야 한다. 코드를 쓰는 확장은 본 플랫폼의 partner SDK를 통해서만 (별도 ADR).

---

### A. PluginManifest — 확장 한 건의 신원

```
PluginManifest {
  id, tenantId,
  pluginKey,           // unique within tenant, e.g. 'biodiv-monitor'
  name, version,        // semver
  authorEmail,
  homepageUrl?,
  ownerUserId,
  // 확장이 *요청한* 권한. super-admin가 부여 시 capabilityTokens가 발급된다.
  requestedScopes,      // ['custom-domain.write','event.subscribe','event.emit']
  // 확장이 만들어 내는 콘텐츠가 본 플랫폼 원칙을 따른다는 명시 동의.
  noncommercialPledge,  // boolean, must be true (DB CHECK)
  plainLanguagePledge,  // boolean, must be true
  // 매니페스트 자체의 SHA-256. 변경 감지 + 무단 교체 방지.
  manifestHash,
  state,                // 'draft' | 'review' | 'approved' | 'paused' | 'retired'
  approvedAt, approvedBy,
  pausedAt, pauseReason,
  createdAt
}
```

#### Hard rules

1. `pluginKey`는 한 테넌트 안에서 유일.
2. `noncommercialPledge` + `plainLanguagePledge`는 둘 다 true (DB CHECK).
3. `approved`로 가려면 admin 승인 필요. ODA·정책 영향 플러그인은 super-admin 추가 승인 필요 — 매니페스트 메타에 `governanceTier='strict'` 표시.
4. super-admin은 언제든 `paused`로 전환 가능 — 사유 ≥ 30자 영구 보존.

### B. CustomDomain — 새 데이터 타입 *선언*

```
CustomDomain {
  id, tenantId, pluginId,
  domainKey,            // 'biodiv-card', 'shared-tool-reservation', ...
  name,                 // i18n
  jsonSchema,           // JSON Schema (draft 2020-12) — record validation
  // 어떤 코어 자료에 연결될 수 있는가. 예: ['watch_item','column','need_request']
  linksToCoreKinds,
  // PII 보호 마킹 — schema 안의 어떤 필드가 PII인지 명시
  piiFields,            // ['ownerName','ownerEmail']
  state,                // 'draft' | 'active' | 'retired'
  createdAt
}
```

#### Hard rules

1. `domainKey`는 (tenantId, pluginId) 안에서 유일.
2. JSON Schema는 *write 시점*에 모든 record를 검증한다. fail시 BadRequestException.
3. `piiFields`로 표시된 필드는 *AI 호출 전 자동 마스킹* (ADR-0015 패턴 재사용).
4. 활성 record가 있는 CustomDomain은 retired될 수 없다 — 먼저 모든 record를 archive하라.

### C. CustomRecord — CustomDomain 인스턴스

```
CustomRecord {
  id, tenantId, domainId,
  ownerId,
  // 임의의 JSON. CustomDomain.jsonSchema로 매번 검증.
  payload,
  // CustomWorkflow가 정의한 상태 (있을 때).
  state,
  createdAt, updatedAt
}
```

#### Hard rules

1. `payload`는 매 write마다 schema-validate.
2. PII 마스킹은 `piiFields` 기준으로 자동 적용. AI 호출에 들어가는 payload는 자동 마스킹된 사본.
3. write마다 `DomainEvent` emit ('record.created' / 'record.updated' / 'record.state_changed').
4. tenant_id 인덱스 + GIN(payload) 인덱스로 검색 가능.

### D. CustomWorkflow — 선언적 상태 머신

```
CustomWorkflow {
  id, tenantId, domainId,
  workflowKey,          // 'reservation-lifecycle'
  // 상태 정의. 예: { 'requested': ['approved','denied'], 'approved': ['returned','overdue'], ... }
  transitions,          // JSON
  // 'approved' 등 일부 상태에 대한 사이드 이펙트 트리거.
  // 트리거는 본 플랫폼이 안전하다고 인증한 슬롯에만 매핑된다 (free-form 코드 X).
  triggers,             // [{ on: 'approved', emit: 'reservation.approved' }, ...]
  initialState,
  terminalStates,       // 더 이상 transition 불가
  createdAt
}
```

#### Hard rules

1. `transitions`는 *방향성 그래프*. 사이클 가능, 단 terminal state로 들어가면 빠져나올 수 없다.
2. `triggers.emit`은 *event 이름만* 가질 수 있다. 임의 코드 실행 불가 — emit된 event는 EventSubscription이 받는다.
3. `transition` 호출은 본 플랫폼의 audit + RBAC 가드를 그대로 통과한다.

### E. DomainEvent — append-only 이벤트 로그

```
DomainEvent {
  id, tenantId,
  // 이벤트 발생자: 코어 모듈 또는 plugin
  source,               // 'core.column' | 'plugin.biodiv-monitor' | ...
  eventName,            // 'column.published' | 'biodiv-card.created' | ...
  // 이벤트 페이로드 — *PII 마스킹된* 것만 들어온다.
  payload,
  // 같은 비즈니스 작업의 일부라면 묶기 위한 ID
  correlationId,
  occurredAt
}
```

#### Hard rules

1. **append-only** — UPDATE / DELETE 거부 (Prisma 측 readonly + 감사 로그).
2. payload에 들어가기 전에 본 플랫폼의 PII 마스킹 (ADR-0015) 자동 통과.
3. RLS — 다른 테넌트의 이벤트는 보이지 않는다.
4. 30일 retention 인덱스 (별도 작업으로 정리 — 본 ADR 범위 밖).

### F. EventSubscription + CapabilityToken + FeatureFlag

```
EventSubscription {
  id, tenantId, pluginId,
  eventPattern,         // 'core.column.*' | 'biodiv-card.created' | '*.failed'
  // 이벤트를 받는 길:
  deliveryKind,         // 'inproc' | 'webhook'
  webhookUrl?,
  // HMAC secret hashed (raw never returned after creation).
  webhookSecretHash?,
  active,
  failureCount,
  lastDeliveredAt,
  createdAt
}

CapabilityToken {
  id, tenantId, pluginId,
  // 부여된 권한. PluginManifest.requestedScopes의 부분집합 또는 동일.
  grantedScopes,
  // 토큰의 SHA-256 만 저장. raw는 발급 시 1회만 회신.
  tokenHash,
  expiresAt,
  revokedAt,
  createdAt
}

FeatureFlag {
  id, tenantId,
  // 'plugin.biodiv-monitor' | 'core.experimental.dashboard-v2' | ...
  flagKey,
  enabled,
  // 't,e,s,t,e,r' 같은 사용자/롤 한정 flag — 부분 롤아웃.
  audience,             // JSON
  updatedBy,
  updatedAt
}
```

#### Hard rules

1. **EventSubscription webhook**은 ADR-0013과 동일 HMAC-SHA256 서명. `webhookSecret`는 hash-only 저장.
2. webhook 실패 5회 연속 → `active=false` 자동 비활성. super-admin이 명시적으로 reset 해야 다시 켜진다.
3. **CapabilityToken**은 발급 시 raw 1회만. 잃어버리면 새 토큰을 발급해야 한다.
4. token 만료 default 90일. 만료된 토큰으로 호출 시 401.
5. **FeatureFlag**는 super-admin만 setting 가능. flag로 plugin 전체를 즉시 끄는 것이 *최종 안전망*.

---

## 보안·거버넌스 핵심 규칙

| 영역 | 규칙 |
|------|------|
| PII | `CustomDomain.piiFields` 기반 자동 마스킹 — AI 호출 전 |
| 비영리 | `noncommercialPledge` 필수 (DB CHECK) |
| 평이한 언어 | `plainLanguagePledge` 필수 (DB CHECK) |
| 해로운 콘텐츠 | 모든 write는 `checkHarmfulContent()` 통과 |
| 격리 | 모든 새 테이블 RLS + FORCE |
| 감사 | DomainEvent 가 append-only + 모든 write가 emit |
| 차단 스위치 | super-admin은 PluginManifest를 즉시 paused로 — 사유 영구 |
| 권한 | CapabilityToken으로만 외부 호출. scope-bound. |
| webhook | ADR-0013 HMAC-SHA256 + 5회 실패 자동 차단 |

## 데이터 모델 — 새 테이블 8개

`plugin_manifests` / `custom_domains` / `custom_records` / `custom_workflows` / `domain_events` / `event_subscriptions` / `capability_tokens` / `feature_flags`

핵심 DB CHECK:
- `plugin_manifests.noncommercial_pledge = true`
- `plugin_manifests.plain_language_pledge = true`
- `plugin_manifests.state ∈ {draft, review, approved, paused, retired}`
- `custom_domains.state ∈ {draft, active, retired}`
- `event_subscriptions.delivery_kind ∈ {inproc, webhook}`
- `event_subscriptions.delivery_kind='webhook' AND webhook_url IS NOT NULL` 조건적 NOT NULL 검증

## 구현 우선순위 (MVP 범위)

이번 ADR에서는 **데이터 모델 + 핵심 가드 서비스 + 컨트롤러 + 테스트**를 만든다. 다음은 *별도 ADR*에서:
- Plugin SDK (TypeScript / Python helper 라이브러리)
- 시각적 워크플로 디자이너 (관리자 UI)
- Plugin marketplace (검색·발견)
- 외부 webhook 재시도 큐 (BullMQ-기반)
- JSON Schema → 자동 폼 생성기

## 13 locale 메시지 namespace

`extensibility.*` 추가. ko / en / zh 풀 번역; ar / es / fr / sw 네이티브; bn / hi / id / ja / pt / ru 영어 fallback + `_translationNeeded`.

## Out of scope (다음 ADR)

- 실시간 in-process event bus (현재는 DomainEvent 테이블 기반 polling)
- 외부 webhook 재시도/dead-letter
- Plugin SDK
- 시각적 워크플로 / 폼 디자이너 UI
- Plugin marketplace + 디지털 서명 검증 (Sigstore?)
- JSON Schema 자동 마이그레이션 (현재는 schema 변경 시 새 CustomDomain 권장)
