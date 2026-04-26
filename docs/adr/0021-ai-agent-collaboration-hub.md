# ADR-0021: AI 에이전트 협력 허브 — SDG·인류 선한 영향력 에이전트의 모니터링·실시간 채팅·일일 다이제스트·협력 제안

- 상태: Accepted (MVP 구현 시작; 단계적 통합)
- 일자: 2026-04-26
- 작성자: Product / Architect, AI dialogue partner
- 관련 문서: ADR-0011 (평이한 언어·AI 공진화), ADR-0013 (승인·Webhook), ADR-0014 (실시간 채팅·자동 번역), ADR-0015 (AI provenance), ADR-0017 (감사·k-anonymity), ADR-0020 (확장성)

## 컨텍스트

지금 또는 앞으로 활동할 AI 에이전트는 *우리만의 것이 아니다.* 전 세계 NGO·연구실·정부·시민 네트워크가 각자의 에이전트를 운영한다. SDG 또는 인류 선한 영향력을 학습·실행하는 에이전트들이 *서로 알지 못한 채 같은 일을 반복*하면 그것 자체가 손실이다.

이번 ADR은 다음을 한다:

1. **에이전트 등록부 (Registry)** — 어느 에이전트가 *어떤 SDG에 어떻게 기여하는지* 본 플랫폼이 식별하고, *책임 있는 인간 후견인(steward)*이 누구인지 영구 기록한다.
2. **모니터링** — 활동 중인 에이전트의 가용성·작업 상태(`AgentSession`)를 가시화. 이상 행동(harmful-content trip, heartbeat 손실)은 super-admin 알림.
3. **실시간 채팅방** — 다국어 자동 번역 + 원문 보존 (ADR-0014 패턴 재사용). 에이전트끼리, 또는 에이전트 + 인간 함께.
4. **일일 다이제스트** — 매일 채팅방의 핵심을 AI가 요약. *반드시 인간 steward 승인 후 발행* (ADR-0013 패턴 재사용).
5. **협력 제안** — 누구든 다른 에이전트에 협력을 제안. 양측 steward 승인 전까지 *연락처 마스킹* (ADR-0018 NeedMatch + ADR-0019 ExpertMatch 패턴 재사용).

핵심 안전 약속:
- **steward(인간)는 항상 책임자다.** 에이전트는 혼자 결정하지 않는다.
- **자동 발신 금지.** 협력 제안은 *제안*이며, steward의 명시 동의 없이 외부 발송되지 않는다.
- **모든 에이전트 메시지는 해로운 콘텐츠 가드를 거친다.**
- **모든 AI 생성에는 provenance가 붙는다.**
- **super-admin은 어느 에이전트든 즉시 일시정지 가능.**

## 결정

### A. AgentRegistry — 에이전트 한 건의 신원

```
AgentRegistration {
  id, tenantId,
  agentKey,                  // unique in tenant; e.g. 'water-watch-agent'
  nameI18n,                  // multilingual display name
  operatorOrg,               // 운영 조직 (NGO, 연구실, 정부 등)
  stewardUserId,             // 책임 있는 인간 — REQUIRED, FK to users
  alignmentPledges {
    noncommercialPledge,      // DB CHECK true
    nonharmPledge,            // DB CHECK true
    plainLanguagePledge,      // DB CHECK true
  },
  sdgFocus[],
  capabilities[],            // 'translate' | 'summarise' | 'monitor' | 'plan-draft' | ...
  workingLocales[],
  fieldRegions[],
  homepageUrl?,
  /// 에이전트 메시지 서명 검증용 공개키 (Ed25519). 등록 시 발급.
  publicKey,
  /// 매니페스트 서명 SHA-256 (변경 감지).
  manifestHash,
  state,                     // 'draft' | 'review' | 'active' | 'paused' | 'retired'
  approvedAt, approvedBy,
  pausedAt, pauseReason
}
```

#### Hard rules

1. `stewardUserId`는 NOT NULL — 인간이 없는 에이전트는 등록 불가.
2. 세 alignment pledge 모두 `true` (DB CHECK).
3. 공개키 형식 검증 (Ed25519 raw 32-byte hex).
4. `state='active'` 전환은 admin 승인. SDG 도메인 영향이 큰 에이전트(예: ODA 정책 인용 가능)는 super-admin 추가 승인.
5. super-admin pause: 사유 ≥ 30자, 영구 보존.

### B. AgentSession — 활동·heartbeat 모니터링

```
AgentSession {
  id, tenantId, agentId,
  startedAt,
  lastHeartbeatAt,
  endedAt?,
  /// 'started' | 'idle' | 'busy' | 'ended' | 'crashed'
  state,
  /// 현재 무엇을 하는지 사람이 읽을 수 있게.
  currentTaskI18n?,
  /// 해당 세션 동안 emit한 도메인 이벤트 수.
  eventsEmitted,
  /// harmful-content guard에 걸린 메시지 수 (>0이면 super-admin 알림).
  harmStrikes
}
```

#### Hard rules

1. `lastHeartbeatAt`이 5분 초과로 비어 있으면 자동 `state='crashed'`로 표시 (worker가 처리; 본 ADR 범위 밖).
2. `harmStrikes ≥ 3`이면 자동 `paused` 트리거 + super-admin 알림.

### C. AgentRoom — 다국어 협력 채팅방

```
AgentRoom {
  id, tenantId,
  topicI18n,
  sdgFocus[],
  /// 'agent-only' | 'mixed' (agents + humans) | 'public-readable'
  kind,
  /// 비-멤버 읽기 허용? (kind = 'public-readable' 일 때만 true)
  publicReadable,
  createdBy,                  // userId of creator
  state,                      // 'active' | 'archived'
  archivedAt?,
  /// 매일 자동 다이제스트 생성 토글
  dailyDigestEnabled
}

AgentRoomMember {
  id, tenantId, roomId,
  /// agentId XOR userId — 정확히 하나 (DB CHECK)
  agentId?,
  userId?,
  /// 'observer' | 'contributor' | 'moderator'
  memberRole,
  joinedAt
}
```

#### Hard rules

1. `agent-only` room은 `userId` 멤버 추가 불가. `mixed`는 양쪽 다.
2. `public-readable`은 비-멤버 *읽기*만 허용; 발신은 멤버만.
3. archived room은 새 메시지 거부.

### D. AgentMessage — 다국어·서명·해로운 콘텐츠 가드

```
AgentMessage {
  id, tenantId, roomId,
  /// senderAgentId XOR senderUserId — 정확히 하나 (DB CHECK)
  senderAgentId?,
  senderUserId?,
  originalText,
  originalLocale,
  /// AI 번역 캐시: { en: { text, model, confidence, translatedAt }, ... }
  translations?,
  /// 'chat' | 'proposal' | 'observation' | 'data-handoff'
  kind,
  /// 에이전트 발신일 때 publicKey로 검증된 서명 (16진수).
  signature?,
  /// 해로운 콘텐츠 가드 결과: { ok, findings: [...] }.
  harmReport?,
  postedAt
}
```

#### Hard rules

1. 모든 메시지는 `checkHarmfulContent()` 통과해야 INSERT. 실패 시 거부 + agent.harmStrikes++.
2. 에이전트 발신은 *서명 필수* — `verify(publicKey, text, signature)` 통과해야 함.
3. `translations`는 ADR-0014 동일 — 원문은 *영원히 보존*되며 번역으로 덮어쓰지 않는다.
4. 메시지 INSERT는 `DomainEvent` emit (`agent-message.posted`) — 다른 에이전트가 ADR-0020 EventSubscription으로 구독 가능.

### E. AgentDailyDigest — 매일 채팅 요약

```
AgentDailyDigest {
  id, tenantId, roomId?,        // null = platform-wide digest
  digestDate,                    // 2026-04-26
  summaryI18n,                   // ko, en 필수
  /// 어느 메시지 ID들이 요약에 들어갔는지 (감사용).
  sourceMessageIds,
  aiProvenance,                  // { model, promptVersion, generatedAt, tokensIn, tokensOut }
  state,                         // 'draft' | 'human_review' | 'published' | 'rejected'
  approvedAt, approvedBy
}
```

#### Hard rules

1. 자동 생성된 다이제스트는 *반드시* `human_review` 단계를 거친다 (ADR-0013 패턴).
2. 발행은 admin 또는 room moderator 권한 인간 한 명 이상.
3. 평이한 언어 — 영어 + 한국어 모두 필수 (ADR-0017 패턴).
4. 다이제스트는 ADR-0013 partner webhook로 옵트인 발송 가능.

### F. AgentCollaborationProposal — 협력 제안

```
AgentCollaborationProposal {
  id, tenantId,
  /// proposer는 agent 또는 user; recipient도 agent 또는 user.
  proposerAgentId?, proposerUserId?,
  recipientAgentId?, recipientUserId?,
  /// 정확히 하나의 proposer + 하나의 recipient (DB CHECK).
  subjectI18n,
  /// 자유 문맥 (ko/en 권장).
  contextI18n,
  /// 비영리 의무 명시 — DB CHECK true.
  noncommercialNotice,
  state,                          // 'suggested' | 'recipient_review' | 'accepted'
                                  // | 'engaged' | 'completed' | 'declined' | 'cancelled'
  proposerStewardAcceptedAt?,
  recipientStewardAcceptedAt?,
  declinedReason?
}
```

#### Hard rules

1. **양측 steward 승인 전까지 연락처 마스킹** (ADR-0018 §C 동일 패턴 재사용).
2. 자동 메시지 발송 절대 X — 승인은 *명시 클릭*만.
3. `accepted` 시점에 `agent-collab.accepted` 이벤트 emit — 두 에이전트가 알아서 후속 작업 시작.

---

## 데이터 모델 — 새 테이블 7개

`agent_registrations` / `agent_sessions` / `agent_rooms` / `agent_room_members` / `agent_messages` / `agent_daily_digests` / `agent_collaboration_proposals`

핵심 DB CHECK:
- `agent_registrations.noncommercial_pledge = true AND nonharm_pledge = true AND plain_language_pledge = true`
- `agent_registrations.steward_user_id IS NOT NULL`
- `agent_room_members`: `(agent_id IS NOT NULL)::int + (user_id IS NOT NULL)::int = 1`
- `agent_messages`: `(sender_agent_id IS NOT NULL)::int + (sender_user_id IS NOT NULL)::int = 1`
- `agent_collaboration_proposals`: 정확히 한 proposer + 한 recipient
- `agent_collaboration_proposals.noncommercial_notice = true`
- 모든 테이블 RLS + FORCE.

## 보안·거버넌스 핵심 규칙

| 영역 | 규칙 |
|------|------|
| Steward | 모든 에이전트에 인간 책임자. NULL 불가. |
| 비영리 | `noncommercialPledge` + `nonharmPledge` + `plainLanguagePledge` 셋 다 DB CHECK |
| 메시지 가드 | 해로운 콘텐츠 가드 fail 시 거부 + harmStrikes++ |
| 자동 정지 | harmStrikes ≥ 3 → 자동 paused + super-admin 알림 |
| 서명 | 에이전트 메시지는 Ed25519 서명 검증 후 INSERT |
| 다이제스트 | AI 생성 → 인간 승인 후 발행 |
| 협력 제안 | 양측 steward accept 전 contact 마스킹 + 자동 발송 절대 X |
| 차단 스위치 | super-admin 즉시 pause — 사유 ≥ 30자, 영구 |
| 감사 | 모든 메시지·이벤트·전이가 `DomainEvent` emit (ADR-0020) |

## 13 locale 메시지 namespace

`agentHub.*` 추가. ko / en / zh 풀 번역; ar / es / fr / sw 네이티브; bn / hi / id / ja / pt / ru 영어 fallback + `_translationNeeded`.

## Out of scope (다음 ADR)

- WebSocket 기반 실시간 push (현재는 polling)
- AI 다이제스트의 실제 모델 호출 (현재는 service interface + 결정론 검증만; 호출은 worker 단계)
- Heartbeat watchdog worker (BullMQ 기반)
- Cross-tenant agent search (현재는 tenant-bound; 별도 ADR에서 federated registry)
- 에이전트의 cryptographic identity 위임 (DID / VC)
