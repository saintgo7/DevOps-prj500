// Source: UN Sustainable Development Goals — official names and brand colors.
// https://www.un.org/sustainabledevelopment/

export interface SeedGoal {
  id: string;
  number: number;
  color: string;
  nameI18n: { ko: string; en: string; ja: string };
}

export const SDG_GOALS: SeedGoal[] = [
  { id: 'SDG-1', number: 1, color: '#E5243B', nameI18n: { ko: '빈곤 종식', en: 'No Poverty', ja: '貧困をなくそう' } },
  { id: 'SDG-2', number: 2, color: '#DDA63A', nameI18n: { ko: '기아 종식', en: 'Zero Hunger', ja: '飢餓をゼロに' } },
  { id: 'SDG-3', number: 3, color: '#4C9F38', nameI18n: { ko: '건강과 웰빙', en: 'Good Health and Well-being', ja: 'すべての人に健康と福祉を' } },
  { id: 'SDG-4', number: 4, color: '#C5192D', nameI18n: { ko: '양질의 교육', en: 'Quality Education', ja: '質の高い教育をみんなに' } },
  { id: 'SDG-5', number: 5, color: '#FF3A21', nameI18n: { ko: '성평등', en: 'Gender Equality', ja: 'ジェンダー平等を実現しよう' } },
  { id: 'SDG-6', number: 6, color: '#26BDE2', nameI18n: { ko: '깨끗한 물과 위생', en: 'Clean Water and Sanitation', ja: '安全な水とトイレを世界中に' } },
  { id: 'SDG-7', number: 7, color: '#FCC30B', nameI18n: { ko: '저렴하고 깨끗한 에너지', en: 'Affordable and Clean Energy', ja: 'エネルギーをみんなに そしてクリーンに' } },
  { id: 'SDG-8', number: 8, color: '#A21942', nameI18n: { ko: '양질의 일자리와 경제 성장', en: 'Decent Work and Economic Growth', ja: '働きがいも経済成長も' } },
  { id: 'SDG-9', number: 9, color: '#FD6925', nameI18n: { ko: '산업, 혁신, 사회 인프라', en: 'Industry, Innovation and Infrastructure', ja: '産業と技術革新の基盤をつくろう' } },
  { id: 'SDG-10', number: 10, color: '#DD1367', nameI18n: { ko: '불평등 감소', en: 'Reduced Inequalities', ja: '人や国の不平等をなくそう' } },
  { id: 'SDG-11', number: 11, color: '#FD9D24', nameI18n: { ko: '지속가능한 도시와 공동체', en: 'Sustainable Cities and Communities', ja: '住み続けられるまちづくりを' } },
  { id: 'SDG-12', number: 12, color: '#BF8B2E', nameI18n: { ko: '책임있는 소비와 생산', en: 'Responsible Consumption and Production', ja: 'つくる責任 つかう責任' } },
  { id: 'SDG-13', number: 13, color: '#3F7E44', nameI18n: { ko: '기후변화 대응', en: 'Climate Action', ja: '気候変動に具体的な対策を' } },
  { id: 'SDG-14', number: 14, color: '#0A97D9', nameI18n: { ko: '해양 생태계 보존', en: 'Life Below Water', ja: '海の豊かさを守ろう' } },
  { id: 'SDG-15', number: 15, color: '#56C02B', nameI18n: { ko: '육상 생태계 보존', en: 'Life on Land', ja: '陸の豊かさも守ろう' } },
  { id: 'SDG-16', number: 16, color: '#00689D', nameI18n: { ko: '평화, 정의, 강력한 제도', en: 'Peace, Justice and Strong Institutions', ja: '平和と公正をすべての人に' } },
  { id: 'SDG-17', number: 17, color: '#19486A', nameI18n: { ko: '목표 달성을 위한 파트너십', en: 'Partnerships for the Goals', ja: 'パートナーシップで目標を達成しよう' } },
];

// Sample targets — one well-known target per goal as a representative seed.
// Full UN target list (169) is loaded via separate ETL in prod (see scripts/etl-sdg.ts — TODO).
export interface SeedTarget {
  id: string;
  goalId: string;
  type: 'outcome' | 'means';
  textI18n: { ko: string; en: string };
}

export const SDG_TARGETS_SAMPLE: SeedTarget[] = [
  { id: 'SDG-1.1', goalId: 'SDG-1', type: 'outcome', textI18n: { ko: '2030년까지 모든 곳의 모든 사람들에 대한 극심한 빈곤 종식', en: 'Eradicate extreme poverty for all people everywhere by 2030' } },
  { id: 'SDG-3.4', goalId: 'SDG-3', type: 'outcome', textI18n: { ko: '2030년까지 비전염성 질환으로 인한 조기 사망률 1/3 감소', en: 'Reduce premature mortality from non-communicable diseases by one third by 2030' } },
  { id: 'SDG-5.5', goalId: 'SDG-5', type: 'outcome', textI18n: { ko: '의사결정 분야에서 여성의 완전하고 효과적인 참여 보장', en: 'Ensure women’s full and effective participation in leadership and decision-making' } },
  { id: 'SDG-7.2', goalId: 'SDG-7', type: 'outcome', textI18n: { ko: '2030년까지 글로벌 에너지 믹스에서 재생에너지 비중 대폭 확대', en: 'Increase substantially the share of renewable energy in the global energy mix by 2030' } },
  { id: 'SDG-8.5', goalId: 'SDG-8', type: 'outcome', textI18n: { ko: '2030년까지 모두를 위한 완전·생산적 고용과 양질의 일자리 달성', en: 'Achieve full and productive employment and decent work for all by 2030' } },
  { id: 'SDG-9.5', goalId: 'SDG-9', type: 'outcome', textI18n: { ko: '모든 국가에서 과학 연구 강화 및 산업 부문의 기술 역량 향상', en: 'Enhance scientific research, upgrade industrial sectors’ technological capabilities' } },
  { id: 'SDG-12.6', goalId: 'SDG-12', type: 'means', textI18n: { ko: '기업, 특히 대기업·다국적 기업의 지속가능 정보 보고 채택 장려', en: 'Encourage companies to adopt sustainable practices and integrate sustainability info into reporting' } },
  { id: 'SDG-13.2', goalId: 'SDG-13', type: 'outcome', textI18n: { ko: '국가 정책, 전략, 계획에 기후변화 조치 통합', en: 'Integrate climate change measures into national policies, strategies and planning' } },
  { id: 'SDG-13.3', goalId: 'SDG-13', type: 'outcome', textI18n: { ko: '기후변화 완화·적응·영향 저감에 대한 교육 및 인식 개선', en: 'Improve education, awareness, and capacity on climate change mitigation, adaptation' } },
  { id: 'SDG-17.16', goalId: 'SDG-17', type: 'means', textI18n: { ko: '지속가능발전을 위한 글로벌 파트너십 강화', en: 'Enhance the global partnership for sustainable development' } },
];

export interface SeedIndicator {
  id: string;
  targetId: string;
  unit: string;
  tier: 1 | 2 | 3;
  methodology?: string;
}

export const SDG_INDICATORS_SAMPLE: SeedIndicator[] = [
  { id: 'SDG-1.1.1', targetId: 'SDG-1.1', unit: '% of population', tier: 1, methodology: 'Proportion of population below international poverty line' },
  { id: 'SDG-3.4.1', targetId: 'SDG-3.4', unit: 'mortality rate per 100k', tier: 1, methodology: 'Mortality rate from cardiovascular, cancer, diabetes, chronic respiratory disease' },
  { id: 'SDG-5.5.2', targetId: 'SDG-5.5', unit: '% women managers', tier: 1, methodology: 'Proportion of women in managerial positions' },
  { id: 'SDG-7.2.1', targetId: 'SDG-7.2', unit: '% of TFEC', tier: 1, methodology: 'Renewable energy share in total final energy consumption' },
  { id: 'SDG-8.5.2', targetId: 'SDG-8.5', unit: '% unemployment', tier: 1, methodology: 'Unemployment rate by sex, age, persons with disabilities' },
  { id: 'SDG-12.6.1', targetId: 'SDG-12.6', unit: 'count', tier: 2, methodology: 'Number of companies publishing sustainability reports' },
  { id: 'SDG-13.2.2', targetId: 'SDG-13.2', unit: 'tCO2eq', tier: 1, methodology: 'Total greenhouse gas emissions per year' },
  { id: 'SDG-13.3.1', targetId: 'SDG-13.3', unit: 'qualitative', tier: 2 },
  { id: 'SDG-17.16.1', targetId: 'SDG-17.16', unit: 'count', tier: 2 },
];
