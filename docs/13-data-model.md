# 13. 데이터 모델 & ERD

## 1. 핵심 도메인 ERD (텍스트)

```
Tenant 1───* User
Tenant 1───* Organization
Organization 1───* Department
Tenant 1───* Activity
Activity *───* Target  (via ActivityTargetMapping)
Activity 1───* DataPoint
DataPoint *───* Evidence (via DataPointEvidence)
Tenant 1───* Report
Report 1───* ReportSection
ReportSection *───* DataPoint  (citations)
Tenant 1───* Campaign (수집 캠페인)
Campaign 1───* CampaignTask
CampaignTask 1───* Submission
User 1───* AuditEvent
Goal 1───* Target ───* Indicator
```

## 2. 핵심 테이블

### 2.1 tenants
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | uuid PK | |
| name | text | |
| region | text | `kr`, `eu`, `jp` |
| plan | text | `starter`/`growth`/`enterprise` |
| kms_key_arn | text | Enterprise 전용 |
| created_at | timestamptz | |
| status | text | `active`/`suspended`/`deleted` |

### 2.2 users
| 컬럼 | 타입 |
|------|------|
| id | uuid PK |
| tenant_id | uuid FK |
| email | citext UNIQUE per tenant |
| display_name | text |
| auth_provider | text |
| mfa_enabled | bool |
| status | text |
- 인덱스: `(tenant_id, email)`

### 2.3 roles & memberships (RBAC)
- `roles(id, key, name)` — admin/reviewer/contributor/viewer/auditor
- `memberships(user_id, organization_id, role_id)`

### 2.4 sdg_goals / sdg_targets / sdg_indicators (전역 카탈로그)
- 전역 스키마 `catalog.*`, RLS 미적용, 읽기 전용
- `sdg_indicators(code, target_code, unit, methodology, tier, source_url)`

### 2.5 activities
| 컬럼 | 타입 |
|------|------|
| id | uuid PK |
| tenant_id | uuid (RLS) |
| organization_id | uuid |
| title_i18n | jsonb |
| description | text |
| status | text |
| materiality | text |
| start_date | date |
| end_date | date |
| owner_id | uuid |
| created_at | timestamptz |
- 인덱스: `(tenant_id, status)`, GIN(`title_i18n`)

### 2.6 activity_target_mappings
- `(activity_id, target_code, confidence numeric, source text, verified_by, verified_at)`
- source: `ai`/`manual`
- 복합 PK `(activity_id, target_code)`

### 2.7 metrics / data_points
- `metrics(id, tenant_id, indicator_code nullable, name, unit)`
- `data_points(id, tenant_id, metric_id, period_start, period_end, value numeric, value_text, source, currency)`
- 시계열 인덱스 `(tenant_id, metric_id, period_start)`

### 2.8 evidence
- `evidence(id, tenant_id, type, url, s3_key, sha256, uploaded_by)`
- `data_point_evidence(data_point_id, evidence_id)`

### 2.9 reports / report_sections
- `reports(id, tenant_id, standard, period_start, period_end, status, version, created_by)`
- `report_sections(id, report_id, key, content_md, ai_generated bool, citations jsonb)`
- citations 예: `[{"data_point_id":"…", "sentence_idx": 3}]`

### 2.10 campaigns / submissions
- `campaigns(id, tenant_id, name, due_at, status)`
- `campaign_tasks(id, campaign_id, assignee_id, form_schema jsonb)`
- `submissions(task_id, payload jsonb, status, reviewed_by)`

### 2.11 audit_events (이벤트 소싱 로그)
- `audit_events(id, tenant_id, actor_id, action, resource_type, resource_id, before jsonb, after jsonb, occurred_at)`
- 파티셔닝 by `occurred_at` (월 단위), 7년 보존

### 2.12 ai_invocations
- `ai_invocations(id, tenant_id, user_id, model, input_hash, prompt_cache_hit, input_tokens, output_tokens, latency_ms, cost_usd, occurred_at)`
- 비용·성능 분석용

## 3. 멀티테넌시
- 모든 테넌트 데이터 테이블에 `tenant_id NOT NULL`
- RLS 정책:
  ```sql
  CREATE POLICY tenant_isolation ON activities
    USING (tenant_id = current_setting('app.tenant_id')::uuid);
  ```
- API 미들웨어가 매 요청 `SET LOCAL app.tenant_id = '<uuid>'`
- 카탈로그(`catalog.*`)는 RLS 미적용, 읽기 전용

## 4. 인덱싱 전략
- 시계열: `(tenant_id, metric_id, period_start DESC)` BRIN 또는 BTREE
- 검색: GIN(`to_tsvector('simple', title || description)`) + nori (OpenSearch)
- JSONB 부분 인덱스 (`materiality = 'high'` 등)
- RLS와 호환되는 partial 인덱스 활용

## 5. 다국어
- 텍스트 컬럼은 `*_i18n jsonb` (`{"ko":"…","en":"…","ja":"…"}`)
- 언어 fallback: 요청 → 조직 기본 → en

## 6. 임베딩 (pgvector)
- `activity_embeddings(activity_id, embedding vector(1024))`
- 유사도 검색: 비슷한 활동/SDG 매핑 추천 보조

## 7. 데이터 lineage
- `data_points.source` + `evidence` 연결로 출처 추적
- 보고서 인용은 `report_sections.citations`로 양방향 추적
- Lineage View 머티리얼라이즈드 뷰 (분 단위 갱신)

## 8. 제약 & 무결성
- 외래키 + ON DELETE 규칙 명시 (Activity 삭제 → 매핑 cascade, DataPoint restrict)
- 체크 제약: period_start <= period_end, value >= 0 (단위에 따라)
- 트랜잭션 격리: Read Committed (기본), Serializable (보고서 발행)

## 9. 보존·삭제
- Soft delete (`deleted_at`) 기본
- 90일 후 hard purge 잡 (감사 로그 제외)
- GDPR 삭제 요청: 30일 내 완료, 익명화 vs 파기 결정 트리

## 10. 백업·복구
- RDS PITR 35일
- 일일 논리 백업 (pg_dump) + 주간 풀 + S3 보관 1년
- 분기 복구 훈련 (별도 계정 복원)

## 11. 마이그레이션
- Prisma Migrate + 수동 SQL (RLS 정책)
- Forward-only, downtime 0 (online migration: Lhm, pg_repack)
- 호환성 유지 (Expand → Migrate → Contract)

## 12. 시드 데이터
- UN SDG 카탈로그 232 지표 시드
- 표준 Crosswalk (GRI ↔ SDG, ESRS ↔ SDG) 시드
- 데모 테넌트 (영업·온보딩용)

## 13. 분석 사이드 (ClickHouse)
- 시간별·지표별 사전 집계 테이블
- Materialized View: `agg_metric_daily`, `tenant_sdg_score_daily`
- Postgres → ClickHouse CDC (Debezium → Kafka 또는 단순 ETL — MVP는 ETL)

## 14. 데이터 거버넌스
- 데이터 사전(Data Dictionary)을 docs/ 내 별도 자동 생성
- 컬럼 변경 시 ADR + 영향분석
- PII 분류 태그: 컬럼 코멘트로 표기 (`-- pii: email`)
