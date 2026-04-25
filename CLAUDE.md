# CLAUDE.md

이 파일은 향후 Claude Code 세션이 본 레포지토리에서 작업할 때 사용할 컨텍스트를 정의합니다.

## 프로젝트 한눈에
- **이름**: SDG Impact Cloud
- **유형**: 멀티테넌시 SaaS (SDG/ESG 임팩트 측정·보고)
- **상태**: 기획 단계 — 코드 미작성, 21개 산출 문서 v1 완료
- **주요 문서**: `README.md`, `PROJECT_PLAN.md`, `docs/`, `BACKLOG.md`

## 작업 시 우선 참고할 문서
- 무엇을 만드는가: `docs/01-project-charter.md`, `docs/08-functional-requirements.md`
- 어떻게 만드는가: `docs/11-system-architecture.md`, `docs/12-tech-stack.md`, `docs/13-data-model.md`, `docs/14-api-spec.md`
- 무엇이 위험한가: `docs/05-risk-compliance.md`, `docs/15-security-design.md`
- 다음 액션: `BACKLOG.md`

## 의사결정 규칙
1. **새 기술/패턴 도입은 ADR이 필요하다.** `docs/12-tech-stack.md`의 결정과 충돌하면 ADR 추가 PR을 먼저 제안하라.
2. **AI 기능은 모두 `docs/15` AI 보안 절을 따른다.** PII 마스킹, 인용 표기, 인간 검수 게이트를 우회하지 마라.
3. **멀티테넌시 격리는 절대 깨지 않는다.** 모든 테넌트 데이터 쿼리는 RLS 기반(`current_setting('app.tenant_id')`).
4. **백워드 호환성**: 공개 API 변경은 SemVer + 12개월 deprecation.
5. **언어**: 코드·코멘트·커밋 메시지는 영어. 사용자 향 문서·UI는 한·영·일 다국어.

## 코드 컨벤션 (구현 시작 후 적용)
- TypeScript strict + `noUncheckedIndexedAccess`
- Python 3.13, Ruff + mypy strict
- ESLint + Prettier (또는 Biome)
- 커밋: Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`)
- PR: 머지 = squash, 2명 리뷰 (주요 변경)

## 디렉터리 (예정)
```
.
├── README.md
├── PROJECT_PLAN.md
├── BACKLOG.md
├── CLAUDE.md
├── docs/                # 21개 산출 문서
├── apps/                # (예정) Next.js, NestJS, FastAPI(AI Gateway)
├── packages/            # (예정) shared, ui, types, sdk
├── infra/               # (예정) Terraform 모듈·환경
├── .github/             # 워크플로우, 이슈/PR 템플릿
└── scripts/             # 운영 스크립트
```

## 절대 하지 말 것
- 비밀(API 키, DB 접속) 커밋
- AI 출력에서 인용·신뢰도 제거
- 멀티테넌시 RLS 우회
- main 브랜치에 직접 push (PR 필수)
- `--no-verify` 등 훅 우회

## 자주 쓰는 명령 (구현 후 채울 것)
```
# 로컬 개발 환경 (예정)
pnpm i && pnpm dev

# 테스트
pnpm test            # 단위
pnpm e2e             # E2E
pnpm typecheck

# 인프라
cd infra/envs/dev && terraform plan
```

## 작업 위임 가이드
- **탐색**: 모르는 영역은 docs/README.md 인덱스에서 시작
- **변경 영향**: 데이터 모델·API·보안 변경은 docs/13/14/15에 동시 반영
- **결정 추적**: 큰 결정은 ADR (`docs/adr/NNNN-title.md`) 추가

## 컨택트
- Product Owner: TBD
- Tech Lead: TBD
- Security Lead: TBD
- (구현 단계에서 갱신)
