// Source: UN Sustainable Development Goals — official names and brand colors.
// https://www.un.org/sustainabledevelopment/
// Names sourced from UN Korean (UN ESCAP), UN Japan, and UN China official sites.

export interface SeedGoal {
  id: string;
  number: number;
  color: string;
  nameI18n: { ko: string; en: string; ja: string; zh: string };
}

export const SDG_GOALS: SeedGoal[] = [
  { id: 'SDG-1', number: 1, color: '#E5243B', nameI18n: { ko: '빈곤 종식', en: 'No Poverty', ja: '貧困をなくそう', zh: '无贫穷' } },
  { id: 'SDG-2', number: 2, color: '#DDA63A', nameI18n: { ko: '기아 종식', en: 'Zero Hunger', ja: '飢餓をゼロに', zh: '零饥饿' } },
  { id: 'SDG-3', number: 3, color: '#4C9F38', nameI18n: { ko: '건강과 웰빙', en: 'Good Health and Well-being', ja: 'すべての人に健康と福祉を', zh: '良好健康与福祉' } },
  { id: 'SDG-4', number: 4, color: '#C5192D', nameI18n: { ko: '양질의 교육', en: 'Quality Education', ja: '質の高い教育をみんなに', zh: '优质教育' } },
  { id: 'SDG-5', number: 5, color: '#FF3A21', nameI18n: { ko: '성평등', en: 'Gender Equality', ja: 'ジェンダー平等を実現しよう', zh: '性别平等' } },
  { id: 'SDG-6', number: 6, color: '#26BDE2', nameI18n: { ko: '깨끗한 물과 위생', en: 'Clean Water and Sanitation', ja: '安全な水とトイレを世界中に', zh: '清洁饮水和卫生设施' } },
  { id: 'SDG-7', number: 7, color: '#FCC30B', nameI18n: { ko: '저렴하고 깨끗한 에너지', en: 'Affordable and Clean Energy', ja: 'エネルギーをみんなに そしてクリーンに', zh: '经济适用的清洁能源' } },
  { id: 'SDG-8', number: 8, color: '#A21942', nameI18n: { ko: '양질의 일자리와 경제 성장', en: 'Decent Work and Economic Growth', ja: '働きがいも経済成長も', zh: '体面工作和经济增长' } },
  { id: 'SDG-9', number: 9, color: '#FD6925', nameI18n: { ko: '산업, 혁신, 사회 인프라', en: 'Industry, Innovation and Infrastructure', ja: '産業と技術革新の基盤をつくろう', zh: '产业、创新和基础设施' } },
  { id: 'SDG-10', number: 10, color: '#DD1367', nameI18n: { ko: '불평등 감소', en: 'Reduced Inequalities', ja: '人や国の不平等をなくそう', zh: '减少不平等' } },
  { id: 'SDG-11', number: 11, color: '#FD9D24', nameI18n: { ko: '지속가능한 도시와 공동체', en: 'Sustainable Cities and Communities', ja: '住み続けられるまちづくりを', zh: '可持续城市和社区' } },
  { id: 'SDG-12', number: 12, color: '#BF8B2E', nameI18n: { ko: '책임있는 소비와 생산', en: 'Responsible Consumption and Production', ja: 'つくる責任 つかう責任', zh: '负责任消费和生产' } },
  { id: 'SDG-13', number: 13, color: '#3F7E44', nameI18n: { ko: '기후변화 대응', en: 'Climate Action', ja: '気候変動に具体的な対策を', zh: '气候行动' } },
  { id: 'SDG-14', number: 14, color: '#0A97D9', nameI18n: { ko: '해양 생태계 보존', en: 'Life Below Water', ja: '海の豊かさを守ろう', zh: '水下生物' } },
  { id: 'SDG-15', number: 15, color: '#56C02B', nameI18n: { ko: '육상 생태계 보존', en: 'Life on Land', ja: '陸の豊かさも守ろう', zh: '陆地生物' } },
  { id: 'SDG-16', number: 16, color: '#00689D', nameI18n: { ko: '평화, 정의, 강력한 제도', en: 'Peace, Justice and Strong Institutions', ja: '平和と公正をすべての人に', zh: '和平、正义与强大机构' } },
  { id: 'SDG-17', number: 17, color: '#19486A', nameI18n: { ko: '목표 달성을 위한 파트너십', en: 'Partnerships for the Goals', ja: 'パートナーシップで目標を達成しよう', zh: '促进目标实现的伙伴关系' } },
];

// Sample targets — one well-known target per goal as a representative seed.
// Full UN target list (169) is loaded via separate ETL in prod (see scripts/etl-sdg.ts — TODO).
export interface SeedTarget {
  id: string;
  goalId: string;
  type: 'outcome' | 'means';
  textI18n: { ko: string; en: string; ja?: string; zh?: string };
}

export const SDG_TARGETS_SAMPLE: SeedTarget[] = [
  { id: 'SDG-1.1', goalId: 'SDG-1', type: 'outcome', textI18n: { ko: '2030년까지 모든 곳의 모든 사람들에 대한 극심한 빈곤 종식', en: 'Eradicate extreme poverty for all people everywhere by 2030', ja: '2030年までに、現在1日1.25ドル未満で生活する人々と定義されている極度の貧困をあらゆる場所で終わらせる', zh: '到2030年,在世界各地消除所有人的极端贫困' } },
  { id: 'SDG-3.4', goalId: 'SDG-3', type: 'outcome', textI18n: { ko: '2030년까지 비전염성 질환으로 인한 조기 사망률 1/3 감소', en: 'Reduce premature mortality from non-communicable diseases by one third by 2030', ja: '2030年までに、非感染性疾患による若年死亡率を予防や治療を通じて3分の1減少させる', zh: '到2030年,通过预防、治疗及促进身心健康,将非传染性疾病导致的过早死亡减少三分之一' } },
  { id: 'SDG-5.5', goalId: 'SDG-5', type: 'outcome', textI18n: { ko: '의사결정 분야에서 여성의 완전하고 효과적인 참여 보장', en: 'Ensure women’s full and effective participation in leadership and decision-making', ja: '政治、経済、公共分野でのあらゆるレベルの意思決定において、完全かつ効果的な女性の参画と平等なリーダーシップの機会を確保する', zh: '确保妇女全面有效参与政治、经济和公共生活各级决策,并享有进入领导层的平等机会' } },
  { id: 'SDG-7.2', goalId: 'SDG-7', type: 'outcome', textI18n: { ko: '2030년까지 글로벌 에너지 믹스에서 재생에너지 비중 대폭 확대', en: 'Increase substantially the share of renewable energy in the global energy mix by 2030', ja: '2030年までに、世界のエネルギーミックスにおける再生可能エネルギーの割合を大幅に拡大させる', zh: '到2030年,大幅增加可再生能源在全球能源结构中的比例' } },
  { id: 'SDG-8.5', goalId: 'SDG-8', type: 'outcome', textI18n: { ko: '2030년까지 모두를 위한 완전·생산적 고용과 양질의 일자리 달성', en: 'Achieve full and productive employment and decent work for all by 2030', ja: '2030年までに、若者や障害者を含むすべての男性および女性の、完全かつ生産的な雇用および働きがいのある人間らしい仕事を達成する', zh: '到2030年,实现包括青年和残疾人在内所有男女实现充分和生产性就业,有体面工作' } },
  { id: 'SDG-9.5', goalId: 'SDG-9', type: 'outcome', textI18n: { ko: '모든 국가에서 과학 연구 강화 및 산업 부문의 기술 역량 향상', en: 'Enhance scientific research, upgrade industrial sectors’ technological capabilities', ja: '科学研究を強化し、すべての国の産業セクターにおける技術能力を向上させる', zh: '在所有国家加强科学研究,提升工业部门的技术能力' } },
  { id: 'SDG-12.6', goalId: 'SDG-12', type: 'means', textI18n: { ko: '기업, 특히 대기업·다국적 기업의 지속가능 정보 보고 채택 장려', en: 'Encourage companies to adopt sustainable practices and integrate sustainability info into reporting', ja: '特に大企業や多国籍企業に対し、持続可能な慣行を採用し、持続可能性に関する情報を定期報告に盛り込むよう奨励する', zh: '鼓励各国公司,特别是大公司和跨国公司,采用可持续的做法,并将可持续性信息纳入它们的报告周期' } },
  { id: 'SDG-13.2', goalId: 'SDG-13', type: 'outcome', textI18n: { ko: '국가 정책, 전략, 계획에 기후변화 조치 통합', en: 'Integrate climate change measures into national policies, strategies and planning', ja: '気候変動対策を国別の政策、戦略および計画に盛り込む', zh: '把应对气候变化的举措纳入国家政策、战略和规划' } },
  { id: 'SDG-13.3', goalId: 'SDG-13', type: 'outcome', textI18n: { ko: '기후변화 완화·적응·영향 저감에 대한 교육 및 인식 개선', en: 'Improve education, awareness, and capacity on climate change mitigation, adaptation', ja: '気候変動の緩和、適応、影響軽減および早期警戒に関する教育、啓発、人的能力および制度機能を改善する', zh: '加强气候变化减缓、适应、减少影响和早期预警等方面的教育和宣传,加强人员和机构能力' } },
  { id: 'SDG-17.16', goalId: 'SDG-17', type: 'means', textI18n: { ko: '지속가능발전을 위한 글로벌 파트너십 강화', en: 'Enhance the global partnership for sustainable development', ja: '持続可能な開発のためのグローバル・パートナーシップを強化する', zh: '加强可持续发展全球伙伴关系' } },
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
