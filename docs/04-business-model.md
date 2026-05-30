# 04. 비즈니스 모델 (Business Model Canvas)

## 1. Business Model Canvas

### 1.1 Customer Segments
- **Primary**: 자산 2조원+ 상장사 ESG 담당부서 (한·일)
- **Secondary**: EU CSRD 대상 한국·일본 자회사
- **Tertiary**: 임팩트 NGO, 사회적기업, 액셀러레이터
- **Long-tail**: 중견·중소기업 (Self-serve)

### 1.2 Value Propositions
| 페인 포인트 | 우리 솔루션 |
|------------|-----------|
| 보고서 작성에 분기 200+시간 | AI 초안 → 80% 시간 단축 |
| 데이터 분산·엑셀 지옥 | 통합 데이터 허브 |
| SDG-ESG-규제 매핑 어려움 | 자동 Crosswalk |
| 검증·감사 추적 곤란 | Evidence 트레일·감사로그 |
| 글로벌 표준 변경 추적 | 자동 업데이트 |

### 1.3 Channels
- 직판 (Enterprise Sales)
- 파트너 (회계·컨설팅 펌: BDO, Deloitte, Samil PwC)
- Self-serve (Web Signup) — 중견 이하
- 컨퍼런스·웨비나 (KoSIF, GRI Korea)
- 콘텐츠 마케팅 (블로그·뉴스레터)

### 1.4 Customer Relationships
- Enterprise: 전담 CSM + Quarterly Business Review
- Self-serve: In-app onboarding, 커뮤니티
- 모든 티어: 도메인 전문가 자문 (시간제)

### 1.5 Revenue Streams
**핵심 SaaS 구독** (연간/월간)
- Starter: $250/월 (소규모 NGO·중소기업)
- Growth: $1,500/월 (중견기업)
- Enterprise: $4,000+/월 (대기업, 커스텀)

**부가 수익**
- 보고서 인증·검증 서비스 (파트너 위탁)
- API 호출 사용량 초과분
- 컨설팅·교육 (자체)
- 데이터 마켓플레이스 (장기)

### 1.6 Key Resources
- 도메인 전문가 (지속가능성 PhD/석사)
- AI 모델 활용 노하우 (Claude API)
- SDG·표준 데이터셋 (지속 갱신)
- 멀티테넌시 SaaS 인프라

### 1.7 Key Activities
- 제품 개발·운영
- AI 모델 프롬프트·매핑 정확도 지속 개선
- 규제·표준 추적 및 반영
- 파트너 채널 관리

### 1.8 Key Partners
- AWS (인프라 크레딧)
- Anthropic (AI Partner)
- 회계·컨설팅 펌 (리셀러)
- 학회/협회 (KoSIF, 한국ESG기준원)
- 데이터 제공자 (CDP, MSCI ESG — 장기)

### 1.9 Cost Structure
| 항목 | 비중 (Year 1) |
|------|--------------|
| 인건비 | 65% |
| AI API (Claude) | 8% |
| 클라우드 인프라 | 7% |
| 마케팅·영업 | 12% |
| 법무·컨설팅 | 5% |
| 기타 | 3% |

## 2. 가격 정책 상세

### 2.1 티어 비교
| 기능 | Starter | Growth | Enterprise |
|------|---------|--------|-----------|
| 사용자 수 | 5 | 25 | 무제한 |
| 데이터 용량 | 5 GB | 50 GB | 커스텀 |
| 활동 항목 수 | 100 | 1,000 | 무제한 |
| AI 보고서 생성 | 월 5회 | 월 50회 | 무제한 |
| GRI/SASB/TCFD 템플릿 | ✓ | ✓ | ✓ |
| ESRS/CSRD 모듈 | — | ✓ | ✓ |
| API 액세스 | — | Read-only | Full |
| SSO | — | ✓ | ✓ + SAML |
| SLA | 99% | 99.5% | 99.9% |
| 전담 CSM | — | — | ✓ |
| 커스텀 통합 | — | — | ✓ |

### 2.2 단위 경제 (Unit Economics)
| 지표 | Starter | Growth | Enterprise |
|------|---------|--------|-----------|
| ACV | $3K | $18K | $48K+ |
| Gross Margin | 75% | 80% | 78% |
| CAC | $1K | $6K | $20K |
| Payback (월) | 6 | 5 | 7 |
| LTV (3년) | $8K | $50K | $130K+ |
| LTV/CAC | 8x | 8.3x | 6.5x |

## 3. Go-to-Market 가설
- **Year 1**: 한국 직판, 30개 고객, ARR $700K
- **Year 2**: 일본 진출 (현지 파트너), 100개 고객, ARR $3M
- **Year 3**: EU CSRD 한국 자회사, 250개 고객, ARR $10M

## 4. 핵심 가설 (Test Plan)
| 가설 | 검증 방법 | 성공 기준 |
|------|----------|----------|
| 보고서 80% 시간 단축이 가능하다 | 파일럿 3개사 전후 측정 | 평균 70%+ 단축 |
| Growth 티어에 PMF가 있다 | 무료 트라이얼 → 유료 전환율 | 15%+ |
| AI 매핑 정확도가 도메인 전문가와 비슷하다 | 100건 더블블라인드 비교 | F1 0.85+ |
| 일본 시장 진입 가능 | 현지 파트너 1사 LOI | 6개월 내 1사 |

## 5. 종료 신호 (Pivot Triggers)
- Year 1 종료 시 ARR < $300K → 가격·고객 세그먼트 재검토
- AI 매핑 정확도 < 0.7 → 제품 가치 제안 재정의
- 규제 일정 1년 이상 지연 → ESG 전반으로 확장
