# 10. UX & 디자인 시스템 (Design System)

## 1. 디자인 원칙
1. **Trust First** — 신뢰 가능한 데이터를 명확히 보여준다 (출처·신뢰도 항상 표기)
2. **Reduce Cognitive Load** — 복잡한 표준을 시각적으로 단순화
3. **Inclusive by Default** — 접근성·다국어를 일급 시민으로
4. **Show the Why** — AI 추천·점수에 근거 제공
5. **Workflow Over Forms** — 입력보다 흐름 중심

## 2. Information Architecture (IA)
```
Root
 ├─ Dashboard (역할별)
 ├─ Activities
 │   ├─ List · Filter · Search
 │   └─ Detail (Mapping, Data Points, Evidence)
 ├─ SDG Catalog
 │   ├─ 17 Goals → Targets → Indicators
 │   └─ Crosswalk View
 ├─ Reports
 │   ├─ Builder (Wizard)
 │   ├─ Library (versions)
 │   └─ Templates
 ├─ Workflows
 │   ├─ Data Collection Campaigns
 │   └─ Approvals & Tasks
 ├─ Analytics
 │   └─ SDG Index, Benchmarks
 ├─ Integrations
 ├─ Admin
 │   ├─ Users & Roles
 │   ├─ Billing & Usage
 │   ├─ Audit Log
 │   └─ Settings
 └─ Help & Learn
```

## 3. 디자인 토큰 (Tokens)

### 3.1 Color
- **Brand**: SDG 17개 공식 색상 시스템 사용 + 자체 Primary
- **Primary**: `#0A6E5C` (지속가능 그린 다크)
- **Accent**: `#F4B400` (Goal 1 노랑 계열, CTA)
- **Semantic**:
  - Success `#16A34A`, Warning `#F59E0B`, Danger `#DC2626`, Info `#2563EB`
- **Neutral 11단계**: gray-50 ~ gray-950
- **다크 모드**: 별도 토큰 세트 자동 매핑

### 3.2 Typography
- **본문 한글**: Pretendard
- **본문 영문**: Inter
- **숫자**: Inter Tabular Lining
- **Scale**: 12 / 14 / 16 / 20 / 24 / 30 / 36 / 48 (line-height 1.5 본문, 1.2 제목)

### 3.3 Spacing & Radius
- 4-base Spacing: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64
- Radius: 4 (chip), 8 (button/card), 16 (modal)

### 3.4 Elevation
- Shadow 0/1/2/3 (z-context별), motion-aware

### 3.5 Motion
- Easing: `cubic-bezier(0.2, 0.8, 0.2, 1)`
- Duration: 100ms (micro), 200ms (default), 400ms (modal)
- `prefers-reduced-motion` 존중

## 4. 컴포넌트 라이브러리
- **기반**: shadcn/ui + Radix Primitives
- **추가**: Recharts (차트), Tiptap (리치 에디터), TanStack Table (그리드)
- **자체 컴포넌트**:
  - `<SDGBadge>` — 17개 컬러 자동
  - `<ConfidenceBar>` — AI 신뢰도 시각화
  - `<MetricSparkline>` — 지표 트렌드
  - `<ApprovalFlow>` — 승인 단계 시각화
  - `<EvidenceChip>` — 첨부 근거
  - `<CitationPopover>` — AI 인용 보기

## 5. 패턴 라이브러리
- **Empty States**: 일러스트 + 첫 액션 CTA
- **Loading**: Skeleton + 의미있는 로딩 메시지
- **Error**: 친화적 카피 + 복구 액션
- **AI 응답**: 신뢰도 + 인용 + "왜 이렇게 추천했나요?" 토글
- **승인 플로우**: 상태 칩, 결재선, 코멘트 사이드바

## 6. 접근성 (a11y) 요구
- 모든 인터랙티브 요소 키보드 접근
- 포커스 링 명확히 (color-contrast 3:1+)
- ARIA 패턴 준수 (Radix 기반)
- 색상만으로 정보 전달 금지 (아이콘·텍스트 병기)
- 폼 라벨·에러 메시지 항상 명시

## 7. 다국어 (i18n)
- 모든 카피 i18n key
- 숫자·날짜·통화 ICU MessageFormat
- 한국어 줄바꿈 word-break: keep-all
- 일본어 행간 1.7배

## 8. 다크 모드
- 기본: Light, 시스템 설정 따라 자동
- 차트·SDG 컬러 다크 모드 톤 보정

## 9. 콘텐츠 가이드 (Voice & Tone)
- **Voice**: 신뢰감 있고 명료, 전문가 동료의 어조
- **Tone**:
  - 정상 흐름 → 차분하고 간결
  - 에러 → 친절·해결책 제시
  - AI 응답 → "추천", "참고" 같은 겸손한 표현
- 전문 용어 첫 등장 시 마이크로 카피로 설명

## 10. 디자인-개발 핸드오프
- Figma 디자인 토큰 → Tailwind 토큰 자동 동기화
- 컴포넌트는 Storybook 필수
- 디자인 변경 시 Visual Regression (Chromatic) 통과

## 11. 메트릭
- **사용성**: SUS ≥ 75, 태스크 성공률 ≥ 90%
- **a11y**: axe 위반 0, 키보드 태스크 성공률 100%
- **성능 UX**: LCP ≤ 2.5s, INP ≤ 200ms
- **만족도**: NPS ≥ 40

## 12. 거버넌스
- 디자인 시스템 변경 RFC + Design Lead 승인
- 분기별 디자인 리뷰
- 외부 a11y 감사 연 1회
