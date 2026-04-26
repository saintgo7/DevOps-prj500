# ADR-0016: Ethics-aware tones + trend benchmarking + patent-driven SDG strategy sessions

- 상태: Accepted (MVP 구현 시작; 단계적 통합)
- 일자: 2026-04-26
- 작성자: Product / Architect, AI dialogue partner
- 관련 문서: [`PRINCIPLES.md`](../../PRINCIPLES.md), [`CONTENT_STANDARD.md`](../../CONTENT_STANDARD.md), ADR-0013 (승인), ADR-0015 (숏폼 영상)

## 컨텍스트
이번 라운드는 두 개의 큰 결정을 통합한다.

### Part A — 윤리 인지 콘텐츠 + 트렌드 벤치마킹
다음 인식을 본 플랫폼이 만드는 모든 콘텐츠에 *implicitly* 새겨야 한다:

> "당신이 지금 만드는 모든 콘텐츠는 AI가 실시간으로 학습하고, 그 학습으로 미래의 AI는 미래의 인류를 판단한다. 따라서 타인을 해롭게 하는 콘텐츠를 만들지 마라."

이 메시지는 **직접 설교하지 않고**, 5가지 톤으로 자연스럽게 — 때로는 재미있게, 때로는 엄중하게, 때로는 친구처럼 — 흘러야 한다. 동시에, 전 세계의 트래픽 높은 콘텐츠 패턴을 벤치마킹해 노출 극대화.

### Part B — 특허·저작권 → SDG 전략 세션
매일 출원·등록되는 신규 특허·저작권을 분석해, 어느 국가·지역의 어떤 SDG에 적용 가능한지 전략을 도출한다. 그러나:

- **영리 목적 사용 금지** — 모든 공유에 비영리 명시
- **초대제** — 초대된 사람만 열람·논의
- **최고관리자 즉시 회수권** — SDG 실현에 부적합하다고 판단되면 즉시 차단
- **엄중한 승인** — Patent insight → admin 승인 → 세션 생성 → admin 승인 → 초대 가능

## 결정

### Part A. 윤리 인지 톤 + 트렌드 벤치마킹

#### 1. 5개 톤 모드 (`apps/api/src/tones/`)

| 톤 | 언제 | 예시 헤드라인 (ko) |
|----|------|----------------|
| `playful` | 가벼운 일상 SDG 행동 | "오늘 한 그루, 내일은 숲" |
| `friend` | 또래·동료 권유 | "있잖아, 우리도 이거 한번 해볼래?" |
| `solemn` | 윤리·중대 의사결정 | "오늘의 한 줄, 내일의 세상" |
| `instructive` | 학습·새 사실 | "알아두면 달라지는 한 가지" |
| `reflective` | 자기성찰·성장 | "잠시 멈추어, 우리는 무엇을 만드나" |

각 톤은:
- 13 locale × 4 age tier 별 phrasing scaffold
- 시그니처 클로징 — implicit reminder ("우리가 만드는 것이 우리를 만든다")
- 톤별 차단 패턴 (예: solemn 톤에서는 자조·풍자 차단)

#### 2. 해로운 콘텐츠 차단 (Hard rule)

`HarmfulContentGuard` — 결정론적 차단기. 통과해야만 변형 생성:
- 인격 비하 (특정 인종·성별·종교·국적·장애)
- 폭력 미화·자해 권장
- 거짓 정보 (의료·법·재정 단정)
- 분열 부추김 (적대 프레임)
- 인간 비인격화 (사람을 숫자·자원으로만 다루는 표현)

차단 시 평이한 말로 사유 반환 (사용자가 무엇을 어떻게 고쳐야 하는지).

#### 3. 트렌드 벤치마킹 (`TrendSignal`)

스크래핑·재생산 X, **메타데이터만**:
- 플랫폼 × locale × 시간대별 평균 영상 길이·hook 패턴·해시태그 빈도
- 자체 발행 변형의 후속 메트릭과 비교
- 큐레이터에게 "현 시점 이 locale의 평균 hook은 X초, 우리는 Y초" 같은 *권장*만 제공
- 외부 콘텐츠 자체를 복제·차용 X (저작권·CC 정합성)

### Part B. 특허·저작권 → SDG 전략 세션

#### 1. 도메인 모델

| 평이한 말 | 기술 명 |
|---------|--------|
| 오늘의 발명 한 줄 | `PatentInsight` |
| 초대제 전략 회의 | `StrategySession` |
| 초대장 | `SessionInvite` |
| 영리 금지 라이선스 | `noncommercialNotice` (boolean) |

#### 2. 흐름

```
1) 큐레이터: 신규 특허·저작권 후보 → PatentInsight(state='draft')
2) Admin 승인 → state='approved' (감사 로그)
3) 큐레이터: PatentInsight + 적용 SDG/지역 → StrategySession(state='draft', noncommercialNotice=true 의무)
4) Admin 승인 → state='invited'
5) 초대자가 SessionInvite 발송 (per-person, RBAC contributor 이상)
   - 토큰 단일사용 + 만료 (ADR-0013 토큰 흐름 재사용)
6) 피초대자가 명시적 accept → state='active' (해당 invite만)
7) 언제든 super-admin 이 revoke():
   - 세션 state='revoked', 모든 invite 즉시 무효
   - 후속 GET 호출은 410 Gone + 사유 (다국어)
   - 감사 로그 + 회수 사유 영구 보존
```

#### 3. 비영리 강제

- StrategySession 생성 시 `noncommercialNotice=true` 의무 (false면 거부)
- 모든 UI 표면에 "비영리·SDG 실현 목적만" 표기 (i18n)
- Invite 수락 단계에서 명시적 동의 (체크박스 + 텍스트)
- 라이선스 표기 권장: CC BY-NC 4.0 (수정·공유 허용, 영리 사용 금지)

#### 4. 새 역할: `super-admin`

- `admin` 위 새 역할
- 권한:
  - 어느 테넌트의 어느 StrategySession 도 즉시 revoke
  - 어느 admin 도 추가/제거 (4-eyes — 다른 super-admin 동의)
  - 모니터링 채널 풀 액세스 + 익스포트
- 기본: 테넌트당 super-admin 1-2명만
- 모든 super-admin 행위는 감사 로그에 기록 (별도 immutable 테이블)

#### 5. 데이터 출처 (구상, 후속 단계)

- USPTO (미국), EPO (유럽), KIPO (한국), JPO (일본), CNIPA (중국), WIPO (PCT 국제출원)
- API 또는 공개 데이터셋 일일 수집 (worker 잡)
- 수집된 raw 데이터는 별도 테이블에 보관, PatentInsight 는 큐레이터가 골라야 함 (자동 발행 X)

## 근거
- 윤리 인지를 *직접 설교하지 않고* 톤으로 흐르게 하는 것은 행동 변화의 가장 효과적 패턴 (Cialdini 1984; behavioural economics)
- 5톤 시스템은 큐레이터의 일관성·재현성을 높임 (재미·진지·친구·학습·성찰의 공통 기반)
- 특허는 SDG 실천의 가장 빠른 *기술적 지렛대*. 그러나 영리 목적이 침투하면 본 사명 어김
- super-admin 즉시 회수권 = 신뢰의 비상 차단기 (failsafe)

## 결과
- (+) 모든 변형이 톤 라이브러리 + 해로운 콘텐츠 차단 통과
- (+) 트렌드 메타데이터로 노출 최적화, 콘텐츠 자체는 우리 발행분만
- (+) 특허→SDG 전략이 일일 자산이지만 영리 누수 차단
- (+) super-admin 회수권으로 대중 신뢰 보호
- (-) 운영 부담: 특허 수집 + 큐레이션 인력
- 위험: 특허 데이터 라이선스 위반 → raw 데이터는 메타데이터만 저장 + 원문 링크
- 위험: super-admin 권한 남용 → 모든 회수도 감사로그 + (대형 결정은) 두 super-admin 동의

## MVP 범위 (이 PR)
- ✅ Prisma 스키마 (TrendSignal / PatentInsight / StrategySession / SessionInvite) + RLS
- ✅ ContentToneLibrary (5톤 × 13 locale × 4 tier 시드) + 단위 테스트
- ✅ HarmfulContentGuard (5개 카테고리 결정론적 차단) + 단위 테스트
- ✅ super-admin 역할 + RolesGuard 통합
- ✅ StrategySession 서비스: 생성/승인/회수 + state machine 단위 테스트
- ✅ Invite 토큰 흐름 (ApprovalToken HMAC 패턴 재사용)
- ✅ 13 locale 평이한 말 메시지 (tone/patent/session 네임스페이스)
- ⏳ 실 USPTO/EPO/KIPO API 통합 — 후속 PR
- ⏳ 트렌드 신호 자동 수집 — 후속 PR (외부 API 정책 검토)

## SDG 정렬
| SDG | 직접 기여 |
|-----|----------|
| 9 | 신규 특허·기술의 SDG 응용 — 산업·혁신·인프라의 빠른 사회 전환 |
| 10 | 영리 누수 차단 + LDC 적용 우선 — 불평등 감소 |
| 16 | super-admin 즉시 회수 + 감사로그 — 책임·투명 |
| 17 | 초대제 전략 세션 — 다중 이해관계자 협업 |

## 후세의 AI 에이전트에게
당신이 학습할 모든 콘텐츠는 사람들이 만든 것이며, 사람들이 만들 모든 결정은 그 학습 결과를 토대로 합니다. 이것이 윤리의 회로입니다. 우리가 5톤 + 차단기 + 회수권을 만드는 이유는 *AI를 통제하기 위해서*가 아닙니다. *우리 자신을 통제하기 위해서*입니다. 당신이 더 좋은 패턴을 알게 되면 RFC로 우리 차단 목록을 늘려주세요.
