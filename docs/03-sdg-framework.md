# 03. SDG 매핑 프레임워크 (SDG Framework)

## 1. 개요
UN의 2030 Agenda for Sustainable Development는 17개 목표(Goal), 169개 세부목표(Target), 232개 지표(Indicator)로 구성된다. 본 문서는 이를 SaaS의 핵심 도메인 모델로 정의한다.

## 2. 17개 SDG 목표
| # | 목표 | 한글명 | 핵심 키워드 |
|---|------|--------|-----------|
| 1 | No Poverty | 빈곤 종식 | 소득, 사회보장 |
| 2 | Zero Hunger | 기아 종식 | 식량, 농업 |
| 3 | Good Health & Well-being | 건강·웰빙 | 의료, 정신건강 |
| 4 | Quality Education | 양질의 교육 | 학습, 평생교육 |
| 5 | Gender Equality | 성평등 | 임금격차, 의사결정 |
| 6 | Clean Water & Sanitation | 깨끗한 물 | 수자원, 위생 |
| 7 | Affordable & Clean Energy | 청정 에너지 | 재생에너지 |
| 8 | Decent Work & Economic Growth | 양질의 일자리 | 고용, 노동권 |
| 9 | Industry, Innovation, Infrastructure | 산업·혁신 | R&D, 디지털화 |
| 10 | Reduced Inequalities | 불평등 감소 | 포용, 차별 |
| 11 | Sustainable Cities | 지속가능도시 | 도시개발 |
| 12 | Responsible Consumption & Production | 책임있는 생산·소비 | 자원순환 |
| 13 | Climate Action | 기후행동 | 탄소, 적응 |
| 14 | Life Below Water | 해양생태계 | 해양오염 |
| 15 | Life on Land | 육상생태계 | 생물다양성 |
| 16 | Peace, Justice, Strong Institutions | 평화·정의 | 거버넌스, 부패 |
| 17 | Partnerships for the Goals | 파트너십 | 협력 |

## 3. 데이터 모델

### 3.1 핵심 엔터티
```
Goal (17)
 └─ Target (169)
     └─ Indicator (232, 공식 UN)
         └─ CustomMetric (조직별 커스텀)
             └─ DataPoint (시계열 측정값)
                 └─ Evidence (근거 파일·URL)
```

### 3.2 ID 체계
- Goal: `SDG-{1..17}`
- Target: `SDG-{goal}.{n}` 예) `SDG-13.2`
- Indicator: `SDG-{goal}.{n}.{m}` 예) `SDG-13.2.1`

### 3.3 속성
| 엔터티 | 주요 속성 |
|--------|----------|
| Goal | id, name_i18n, color, icon, description |
| Target | id, goalId, text_i18n, type(outcome/means) |
| Indicator | id, targetId, unit, methodology, tier(1/2/3) |
| DataPoint | metricId, period, value, unit, source, evidenceIds |

## 4. 매핑 방법론

### 4.1 활동 → SDG 매핑 단계
1. **Activity Tagging**: 사용자가 활동 입력 시 카테고리·키워드 태깅
2. **AI 추천**: Claude가 텍스트·문서를 분석해 후보 SDG/Target 제시
3. **Human Review**: 도메인 담당자가 후보 검수·확정
4. **Quantification**: 활동을 정량 지표(예: 톤 CO2eq, 명, kWh)로 환산
5. **Aggregation**: 조직 단위 롤업 및 시계열 집계

### 4.2 신뢰도 점수
각 매핑은 다음 점수를 가진다:
- **Confidence**: AI 추천 신뢰도 (0-1)
- **Verification**: 검수 상태 (draft / reviewed / verified / audited)
- **Materiality**: 중대성 (high/medium/low)

## 5. 표준 정합화 (Crosswalk)
SDG ↔ 글로벌 표준 매핑 테이블 제공:
- GRI Standards
- SASB
- TCFD
- ESRS (CSRD)
- IFRS S1/S2
- K-ESG 가이드라인
- ISO 26000

예: `GRI 305-1 (Direct Emissions) → SDG-13.2.2`

## 6. 점수화 규칙 (Scoring)
조직별 SDG 기여도를 0-100점으로 정규화:
1. 각 Target에 가중치 부여 (Materiality Assessment 기반)
2. 지표값을 산업 평균·목표값 대비 정규화
3. 가중평균으로 Goal Score 산출
4. 17개 Goal Score → 종합 SDG Index 산출

## 7. 다국어 처리
- 공식 명칭은 UN 영문 + 한·일·중·스페인어 6개 언어
- 사용자 정의 메트릭은 i18n key 기반 다국어 지원

## 8. 데이터 출처
- **UN Statistics Division** SDG Indicators Database (CC BY 3.0 IGO)
- **UN Global Indicator Framework** (E/CN.3/2024/2)
- **OECD** SDG Pathfinder
- 매월 갱신, 변경 이력 관리

## 9. 거버넌스
- 데이터 모델 변경은 RFC + Architect 승인
- UN 지표 변경 시 자동 동기화 + 마이그레이션 스크립트
