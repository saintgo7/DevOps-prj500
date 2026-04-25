// Public, well-known SDG-relevant sources to scan weekly.
// Anyone may add to this list via PR; see PRINCIPLES.md §5 (Local hands).
//
// Selection criteria:
// - Publicly accessible (no paywall, no login)
// - SDG-relevant content
// - Stable URL (organisation-level, not campaign-specific)
// - Multilingual where possible
// - Balanced across UN, donors, academia, NGOs, civic tech, regions

export type WatchSourceKind = 'rss' | 'atom' | 'html' | 'github' | 'api';
export type WatchSourceCategory =
  | 'un'         // UN system
  | 'donor'      // bilateral / multilateral donors
  | 'academic'   // research institutions, journals, preprints
  | 'ngo'        // NGOs and civil society
  | 'civic'      // civic tech, open data, hackathons
  | 'regional'   // regional organisations
  | 'funding';   // funding calls and opportunities

export interface SeedWatchSource {
  name: string;
  url: string;
  feedUrl?: string;
  kind: WatchSourceKind;
  category: WatchSourceCategory;
  language: string;
  region?: string;
  sdgFocus?: string[];
}

export const WATCH_SOURCES: SeedWatchSource[] = [
  // UN system ---------------------------------------------------------------
  { name: 'UN SDG News',                url: 'https://www.un.org/sustainabledevelopment/news/', feedUrl: 'https://www.un.org/sustainabledevelopment/blog/feed/', kind: 'rss', category: 'un', language: 'en' },
  { name: 'UN DESA Voice',              url: 'https://www.un.org/development/desa/en/news.html', kind: 'html', category: 'un', language: 'en' },
  { name: 'UNDP Stories',               url: 'https://www.undp.org/stories', kind: 'html', category: 'un', language: 'en' },
  { name: 'UNCTAD LDC News',            url: 'https://unctad.org/topic/least-developed-countries', kind: 'html', category: 'un', language: 'en', sdgFocus: ['SDG-1','SDG-10','SDG-17'] },
  { name: 'UNESCO News',                url: 'https://www.unesco.org/en/articles', kind: 'html', category: 'un', language: 'en', sdgFocus: ['SDG-4','SDG-5'] },
  { name: 'WHO News',                   url: 'https://www.who.int/news', feedUrl: 'https://www.who.int/rss-feeds/news-english.xml', kind: 'rss', category: 'un', language: 'en', sdgFocus: ['SDG-3'] },
  { name: 'Reliefweb (humanitarian)',   url: 'https://reliefweb.int/updates', feedUrl: 'https://reliefweb.int/updates/rss.xml', kind: 'rss', category: 'un', language: 'en' },

  // Regional ---------------------------------------------------------------
  { name: 'UN ESCAP (Asia-Pacific)',    url: 'https://www.unescap.org/news', kind: 'html', category: 'regional', language: 'en', region: 'AS' },
  { name: 'UN ECLAC (Latin America)',   url: 'https://www.cepal.org/en', kind: 'html', category: 'regional', language: 'en', region: 'SA' },
  { name: 'UN ECA (Africa)',            url: 'https://www.uneca.org/news', kind: 'html', category: 'regional', language: 'en', region: 'AF' },
  { name: 'African Union Agenda 2063',  url: 'https://au.int/en/agenda2063', kind: 'html', category: 'regional', language: 'en', region: 'AF' },

  // Bilateral donors --------------------------------------------------------
  { name: 'KOICA News (KO)',            url: 'https://www.koica.go.kr/koica_kr/8255/subview.do', kind: 'html', category: 'donor', language: 'ko', region: 'KR' },
  { name: 'JICA News',                  url: 'https://www.jica.go.jp/english/news/index.html', kind: 'html', category: 'donor', language: 'en', region: 'JP' },
  { name: 'GIZ Press',                  url: 'https://www.giz.de/en/mediacenter/press-releases.html', kind: 'html', category: 'donor', language: 'en', region: 'DE' },
  { name: 'AFD News (FR)',              url: 'https://www.afd.fr/en/actualites', kind: 'html', category: 'donor', language: 'fr', region: 'FR' },
  { name: 'FCDO News',                  url: 'https://www.gov.uk/government/organisations/foreign-commonwealth-development-office', kind: 'html', category: 'donor', language: 'en', region: 'GB' },

  // Multilateral / banks ---------------------------------------------------
  { name: 'World Bank News',            url: 'https://www.worldbank.org/en/news', kind: 'html', category: 'donor', language: 'en' },
  { name: 'ADB News',                   url: 'https://www.adb.org/news', kind: 'html', category: 'donor', language: 'en', region: 'AS' },
  { name: 'Green Climate Fund (GCF)',   url: 'https://www.greenclimate.fund/news', kind: 'html', category: 'funding', language: 'en', sdgFocus: ['SDG-13'] },
  { name: 'Global Environment Facility',url: 'https://www.thegef.org/news', kind: 'html', category: 'funding', language: 'en', sdgFocus: ['SDG-13','SDG-14','SDG-15'] },

  // Academic / research ----------------------------------------------------
  { name: 'arXiv econ.GN',              url: 'https://arxiv.org/list/econ.GN/recent', feedUrl: 'http://export.arxiv.org/rss/econ.GN', kind: 'rss', category: 'academic', language: 'en' },
  { name: 'OpenAlex SDG works',         url: 'https://api.openalex.org/works?filter=sustainable_development_goals.id:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17', kind: 'api', category: 'academic', language: 'en' },

  // NGO / network ----------------------------------------------------------
  { name: 'Local2030',                  url: 'https://www.local2030.org/', kind: 'html', category: 'ngo', language: 'en' },
  { name: 'IIED publications',          url: 'https://www.iied.org/publications', kind: 'html', category: 'ngo', language: 'en' },
  { name: 'ODI publications',           url: 'https://odi.org/en/publications/', kind: 'html', category: 'ngo', language: 'en' },
  { name: 'Devex News',                 url: 'https://www.devex.com/news', kind: 'html', category: 'ngo', language: 'en' },

  // Civic tech -------------------------------------------------------------
  { name: 'GitHub topic: sustainable-development-goals', url: 'https://github.com/topics/sustainable-development-goals', kind: 'github', category: 'civic', language: 'en' },
  { name: 'GitHub topic: climate-action', url: 'https://github.com/topics/climate-action', kind: 'github', category: 'civic', language: 'en', sdgFocus: ['SDG-13'] },
  { name: 'HuggingFace SDG datasets',   url: 'https://huggingface.co/datasets?other=sdg', kind: 'html', category: 'civic', language: 'en' },

  // Funding calls ----------------------------------------------------------
  { name: 'EU Funding & Tenders Portal',url: 'https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/home', kind: 'html', category: 'funding', language: 'en', region: 'EU' },
  { name: 'USAID Business Forecast',    url: 'https://www.usaid.gov/work-usaid/get-grant-or-contract/business-forecast', kind: 'html', category: 'funding', language: 'en' },
];
