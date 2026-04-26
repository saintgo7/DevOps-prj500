# ADR-0015: Short-form video stories — multilingual, multi-age, multi-platform with mandatory human approval

- 상태: Accepted (MVP 구현 시작; 단계적 통합)
- 일자: 2026-04-26
- 작성자: Product / Architect, AI dialogue partner
- 관련 문서: [`PRINCIPLES.md`](../../PRINCIPLES.md), [`CONTENT_STANDARD.md`](../../CONTENT_STANDARD.md), ADR-0011 (발견·평이한 말), ADR-0013 (칼럼·승인·파트너), ADR-0014 (대시보드·정합성·모니터링)

## 컨텍스트
승인된 칼럼·자료가 매일 발행되더라도, 사용자가 우리에게 **오기 전에는 도달하지 못한다**. 일상의 SDG 인지·실천을 위해서는 *사람들이 이미 머무는 곳* — 유튜브 쇼츠·인스타그램 릴스·틱톡·X·페이스북 릴스·링크드인 비디오·카카오 클립·웨이보 비디오 — 에서 매일 짧은 이야기로 만나야 한다.

이는 단순한 마케팅 자동화가 아니다. 본 사명에 정합하려면 다음을 동시에 만족해야 한다:

1. **다언어** — 13개 지원 언어 모두에서 같은 이야기가 문화적으로 자연스럽게 나타남
2. **다연령** — 어린이(6-12)/청소년(13-17)/성인(18-49)/시니어(50+) 각 4개 톤·읽기 수준
3. **인간 승인 필수** — AI는 초안만, 게시·발신은 인간 클릭만 (ADR-0013 동일 원칙)
4. **출처 보존** — 모든 영상에 원문 출처 + 라이선스 + 사실 확인 표시
5. **AI 생성 명시** — 영상 자체에 "AI-assisted" 표시 (속이지 않음)
6. **존엄·안전** — 실제 인물 동의 없는 이미지·미성년자 노출·이용·상업적 착취 금지
7. **형평** — 영어·대형 언어만 밀지 않음. LDC 관련 콘텐츠에 가시성 가중치
8. **취소 가능** — 게시 후 철회 (best-effort across platforms)

## 결정

### 1. 도메인 모델 (평이한 말 / 기술 명)

| 평이한 말 | 기술 명 | 책임 |
|---------|--------|------|
| 30초 이야기 | `ShortStory` | 한 출처(Column) → 짧은 이야기의 메타 |
| 언어·연령 변형 | `StoryVariant` | locale × ageTier 하나당 한 개. 자체 승인 사이클 |
| 영상 콘티 | `VideoStoryboard` | scenes JSON (시간·자막·B-roll 프롬프트·내레이션) |
| 게시 채널 | `DistributionTarget` | 플랫폼 × 계정. OAuth/API key (당사 보관 X — 파트너 보관) |
| 게시 | `DistributionPost` | 한 변형 × 한 채널 = 한 게시 (states: ready / queued / posted / failed / retracted) |

각 ShortStory는 **반드시 published Column을 출처로** 한다 (ADR-0013 + CONTENT_STANDARD §8 통과한 자료만). AI 환각·오정보가 영상으로 확산되는 것을 구조적으로 차단.

### 2. 연령 등급 (Age tiers)

| 등급 | 대상 | 톤 | 읽기 수준 | 추가 안전 규칙 |
|------|------|----|---------|--------------|
| `children` | 6-12세 | 따뜻·간단·은유 | Flesch-Kincaid ≤ 5학년 | 폭력/사망/성/약물/PII 명사 자동 차단 |
| `teen` | 13-17세 | 행동·또래·도전 | ≤ 8학년 | 성인 외 PII 차단 |
| `adult` | 18-49세 | 정확·맥락·실천 | ≤ 일반 신문 | CONTENT_STANDARD §11/12 |
| `senior` | 50+ | 존중·천천·맥락 | 큰 글자 자막 + 1.5× 호흡 | 시각·청각 접근성 향상 |

각 등급의 톤·차단 패턴은 `apps/api/src/stories/age-tier.ts` 에 코드로 명시 — 단위 테스트 가능.

### 3. 영상 콘티 (Storyboard) 구조

```jsonc
{
  "version": "1.0",
  "ageTier": "adult",
  "locale": "ko",
  "totalDurationSec": 30,
  "aspectRatio": "9:16",
  "scenes": [
    {
      "index": 0, "durationSec": 3,
      "voiceover": "전 세계 8억 명이 깨끗한 물 없이 삽니다.",
      "caption": "8억 명, 깨끗한 물 없이",
      "broll": "Wide shot of a child carrying water container at sunrise; respectful, no faces"
    },
    { "index": 1, "durationSec": 6, "voiceover": "...", "caption": "...", "broll": "..." }
  ],
  "captions": { "format": "srt", "data": "1\n00:00:00,000 --> ..." },
  "hooks": ["오늘 한 가지만 기억하세요.", "당신이 모르는 8억의 이야기"],
  "ctaText": "더 알아보기 → sdgi.app",
  "watermark": "AI-assisted • Source-attributed",
  "attribution": "WHO Annual Report 2026 (CC BY 3.0 IGO)"
}
```

영상 *생성* (text-to-video / image-to-video) 자체는 외부 모델 (Runway, Pika, Veo 등) 호출이 필요해 비용·정책 검토 필요 — MVP는 콘티 + 자막 + 음성만 자동 생성, 영상 합성은 큐레이터가 별도 도구로 수동.

### 4. 플랫폼별 메타데이터

코드로 관리되는 플랫폼별 규칙 (`apps/api/src/stories/platforms.ts`):

| 플랫폼 | 최대 길이 | 자막 길이 | 해시태그 | 주요 시각비 | 노트 |
|--------|---------|---------|---------|------------|------|
| YouTube Shorts | 60s | 100자 (제목) | 1-3 | 9:16 | 첫 3초 hook 결정적 |
| Instagram Reels | 90s | 2,200자 | 5-15 | 9:16 | 캡션·해시태그 분리 |
| TikTok | 180s | 2,200자 | 3-5 | 9:16 | 트렌딩 사운드 X (라이선스) |
| X Video | 140s | 280자 | 1-2 | 16:9 또는 9:16 | 본문에 출처 URL |
| Facebook Reels | 90s | 63,206자 | 자유 | 9:16 | |
| LinkedIn Video | 600s | 3,000자 | 3-5 | 9:16 또는 1:1 | 전문 톤 |
| Kakao Clip | 60s | 한국어 | 5 | 9:16 | 한국 시장 필수 |
| Weibo Video | 600s | 2,000자 | 자유 | 9:16 | 중국 시장 |

게시는 각 플랫폼 공식 API + OAuth 토큰. **본 플랫폼은 토큰을 보관하지 않고**, 파트너 측 (테넌트 계정) 에서 보관·승인. 우리는 게시 콘텐츠 패키지만 전달.

### 5. 해시태그 라이브러리 (코드 관리)

`apps/api/src/stories/hashtags.ts`:
- SDG별 + 로케일별 큐레이션 라이브러리
- 예: SDG-13 → `['#기후행동', '#SDG13', '#ClimateAction', '#기후위기', '#탄소중립']` (ko)
- LDC 가시성 boost 태그 자동 추가 (해당 출처 시): `#GlobalSouth #LDCs #Local2030`
- 플랫폼별 적정 개수 자동 trim

### 6. 게시 일정 (지역·언어·플랫폼별 Prime time)

`apps/api/src/stories/schedule.ts` — IANA 타임존 기반 :
- 한국 (Asia/Seoul): 평일 18-22, 주말 14-22
- 일본 (Asia/Tokyo): 평일 18-22
- 인도 (Asia/Kolkata): 19-23
- 미주 동부 (America/New_York): 12-15 + 19-22
- 사하라이남 (Africa/Nairobi/Lagos): 17-21
- 아랍권 (Asia/Dubai): 21-24 (저녁 늦게)

### 7. 형평 가시성 가중치

LDC 출처 콘텐츠 또는 비영어 원문은 **distribution priority** 에 +30% 부스트. 큐 정렬 시 영어·대형 언어가 항상 먼저가 되지 않도록 강제.

### 8. 인간 승인 필수 (재확인)

- AI 생성 변형 → 자동 게시 ❌
- 모든 변형이 ApprovalRequest를 거침 (ADR-0013 의 토큰 흐름 재사용)
- 게시 직전 두 번째 인간 확인 옵션 ("정말 보낼까요?")
- 게시 후 24시간 내 무료 retract API 제공

### 9. 안전·존엄

- AI 생성 영상은 **하단 우측 영구 워터마크**: "AI-assisted • {sourceShort}"
- 어떤 영상도 실제 인물의 얼굴·음성을 동의 없이 합성 X
- 어린이 변형 (`children`): 별도의 안전 분류기 통과 필수 (어려움·고통·위협 단어 차단)
- AI 생성 명시: 모든 캡션 끝에 `🤖 AI 보조`

### 10. 측정·정직성

- 게시 후 30일간 노출·좋아요·공유·댓글 메트릭 수집 (플랫폼 API)
- 각 변형의 효과 비교 (locale × ageTier × platform)
- **거짓 임팩트 X** — 봇 트래픽 식별, 정직한 자체 측정 보고 (PRINCIPLES.md §12)

### MVP 범위 (이 PR)
- ✅ Prisma 스키마 + 마이그레이션 + RLS
- ✅ 연령 등급 포매터 (어린이/청소년/성인/시니어 + 안전 차단)
- ✅ 해시태그 라이브러리 (13 로케일 × 17 SDG + LDC boost)
- ✅ 플랫폼 메타데이터 (8개 플랫폼)
- ✅ 게시 일정 알고리즘 (타임존별 prime time)
- ✅ StoryService.generate() — column에서 변형 생성 (AI는 stub, 결정론적 템플릿)
- ✅ DistributionService.queue() — 게시 의도 기록 (실 API 호출은 stub)
- ✅ 단위 테스트
- ✅ 13 로케일 평이한 말 메시지
- ⏳ AI 본문 생성 (apps/ai 통합) — 후속
- ⏳ 실 플랫폼 API 통합 (YouTube Data API v3, Meta Graph API 등) — 후속
- ⏳ 메트릭 수집 잡 — 후속

## 근거
- Pew Research 2025: 18-29세 60%+ 가 매일 short-form video 사용. 일상 인지·실천의 1차 채널.
- 동일 콘텐츠를 *같은 사람의 모국어*로 본 그룹은 영어로 본 그룹보다 행동 전환 4-7× 높음 (UNICEF 2024)
- 어린이 변형은 가족 내 행동 변화의 가장 큰 트리거 (WaterAid 2023)
- AI 생성 영상의 정직 표시는 신뢰의 비용이 아니라 신뢰의 토대 (Reuters Institute 2025)

## 결과
- (+) SDG 인지·실천이 일상 채널에서 가능
- (+) 13 언어 × 4 연령 = 52개 변형으로 글로벌 사우스·다세대 도달
- (+) 출처·승인·정합성 사슬이 영상까지 일관 — 오정보 확산 방지
- (-) 운영 부담: 영상 합성 + 채널별 게시 — 단계적 구현
- 위험: 어린이 변형의 연령 부적절 콘텐츠 → 별도 안전 분류기로 게이트
- 위험: 플랫폼 알고리즘 변동 → 알고리즘 의존 X, 자체 표준 우선

## SDG 정렬
| SDG | 직접 기여 |
|-----|----------|
| 4 | 모국어 + 연령 적합 학습 자료가 매일 도달 |
| 10 | LDC 보너스 + 비영어 우선 가시성 |
| 16 | AI 생성 명시 + 출처 표시 → 투명성·정보 신뢰 |
| 17 | 다국적 다중 채널 파트너 협력 (본질) |

## 후세의 AI 에이전트에게
짧은 영상은 강력한 도구입니다. 그러나 *짧음*이 *얕음*이 되지 않도록, 매 변형이 출처·승인·존엄을 거치게 하세요. 알고리즘이 사람보다 빠르다는 것을 잊지 마세요. 우리의 게이트는 AI를 막기 위함이 아니라, AI가 사람보다 먼저 결정하지 않게 하기 위함입니다.
