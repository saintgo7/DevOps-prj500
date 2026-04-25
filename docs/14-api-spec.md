# 14. API 명세 (API Specification)

## 1. API 전략
- **REST + JSON** 1차, **GraphQL** 분석/대시보드용 2차
- OpenAPI 3.1 단일 진실 소스 → 코드/문서/Postman 자동 생성
- 버저닝: URI prefix `/v1/`, deprecated 12개월 유지
- 응답 표준: 성공 `{ data, meta }`, 에러 RFC 7807 Problem Details

## 2. 인증·인가
| 호출자 | 방식 |
|--------|------|
| 웹 UI | Cookie 세션 (BFF) → API mTLS |
| 외부 API (서버) | OAuth2 Client Credentials, scope 단위 |
| 외부 API (사용자) | OAuth2 Authorization Code + PKCE |
| Webhook 수신 | HMAC SHA-256 서명 검증 |

- 모든 API에 RBAC + 테넌트 컨텍스트 필수
- 토큰 수명: Access 15분, Refresh 30일

## 3. 공통 헤더
- `X-Tenant-Id` — Enterprise 멀티 테넌트 사용자
- `X-Request-Id` — 추적
- `Idempotency-Key` — POST 멱등 (24h)
- `If-Match` — 동시성 (ETag)

## 4. 페이지네이션
- 기본: 커서 기반 `?cursor=…&limit=50`
- 최대 limit 200
- 응답 `meta.next_cursor`, `meta.total` (옵션)

## 5. 핵심 엔드포인트 (요약)

### 5.1 Identity
| Method | Path | 설명 |
|--------|------|------|
| POST | `/v1/auth/login` | 이메일·비밀번호 |
| POST | `/v1/auth/refresh` | 토큰 갱신 |
| POST | `/v1/auth/logout` | |
| GET  | `/v1/me` | 프로파일 |
| GET  | `/v1/tenants/me` | 조직 |

### 5.2 Catalog (SDG)
| Method | Path | 설명 |
|--------|------|------|
| GET | `/v1/catalog/goals` | 17 Goals |
| GET | `/v1/catalog/targets?goal=13` | Targets by goal |
| GET | `/v1/catalog/indicators/{code}` | 단건 상세 |
| GET | `/v1/catalog/crosswalk?from=GRI-305-1&to=SDG` | 매핑 |

### 5.3 Activities
| Method | Path | 설명 |
|--------|------|------|
| GET    | `/v1/activities` | 목록 (필터·검색) |
| POST   | `/v1/activities` | 생성 |
| GET    | `/v1/activities/{id}` | 상세 |
| PATCH  | `/v1/activities/{id}` | 부분 수정 |
| DELETE | `/v1/activities/{id}` | 소프트 삭제 |
| POST   | `/v1/activities/{id}/mappings` | SDG 매핑 추가 |
| DELETE | `/v1/activities/{id}/mappings/{targetCode}` | 매핑 제거 |

### 5.4 Data Points
| Method | Path | 설명 |
|--------|------|------|
| GET  | `/v1/activities/{id}/data-points` | 시계열 |
| POST | `/v1/activities/{id}/data-points` | 입력 (배열, 멱등키) |
| POST | `/v1/data-points/import` | 엑셀/CSV 비동기 임포트 |

### 5.5 AI
| Method | Path | 설명 |
|--------|------|------|
| POST | `/v1/ai/map-activity` | 텍스트 → SDG 후보 (동기) |
| POST | `/v1/ai/extract-document` | PDF → 활동/메트릭 추출 (비동기) |
| POST | `/v1/ai/draft-report` | 보고서 초안 생성 (비동기) |
| GET  | `/v1/ai/jobs/{id}` | 잡 상태 |

### 5.6 Reports
| Method | Path | 설명 |
|--------|------|------|
| GET    | `/v1/reports` | 목록 |
| POST   | `/v1/reports` | 생성 (표준·기간·범위) |
| GET    | `/v1/reports/{id}` | 본문 |
| PATCH  | `/v1/reports/{id}/sections/{sectionId}` | 단락 수정 |
| POST   | `/v1/reports/{id}/regenerate-section` | 단락 재생성 |
| POST   | `/v1/reports/{id}/submit-for-approval` | 결재 |
| POST   | `/v1/reports/{id}/publish` | 발행 |
| GET    | `/v1/reports/{id}/export?format=pdf|html|ixbrl` | 출력 |

### 5.7 Campaigns
| Method | Path |
|--------|------|
| POST | `/v1/campaigns` |
| GET  | `/v1/campaigns/{id}` |
| POST | `/v1/campaigns/{id}/tasks/{taskId}/submit` |
| POST | `/v1/campaigns/{id}/tasks/{taskId}/review` |

### 5.8 Webhooks (수신용 이벤트 발신)
- `/v1/webhooks` 등록·해제
- 이벤트: `activity.created`, `report.published`, `mapping.verified`, `data_point.created`
- 페이로드 서명 `X-Sdgi-Signature: t=...,v1=...`

## 6. 에러 모델 (Problem Details)
```json
{
  "type": "https://docs.sdgi.app/errors/validation",
  "title": "Validation failed",
  "status": 422,
  "detail": "value must be >= 0",
  "instance": "/v1/data-points/abc",
  "errors": [
    { "field": "value", "code": "min", "message": "must be >= 0" }
  ],
  "request_id": "req_01HZ…"
}
```

## 7. 일반 응답 코드
| 코드 | 의미 |
|------|------|
| 200 | OK |
| 201 | Created (Location 헤더) |
| 202 | Accepted (비동기 잡) |
| 204 | No Content |
| 400 | Validation 외 |
| 401 | 인증 실패 |
| 403 | 권한 부족 |
| 404 | 자원 없음 (테넌트 격리 보호) |
| 409 | 충돌 (ETag) |
| 422 | 비즈니스 검증 실패 |
| 429 | Rate limit |
| 5xx | 서버 오류 (request_id 첨부) |

## 8. Rate Limit
| 티어 | RPS | 일일 |
|------|-----|------|
| Starter | 5 | 50K |
| Growth | 20 | 500K |
| Enterprise | 100+ | 협의 |
- 초과 시 `429` + `Retry-After`
- AI 엔드포인트 별도 한도

## 9. GraphQL (분석)
- `/graphql` 단일 엔드포인트
- 스키마: `Query.metricSeries`, `Query.sdgIndex`, `Query.benchmark`
- 영속화 쿼리(persisted operations) 의무
- Depth limit 8, Cost limit

## 10. 클라이언트 SDK
- TypeScript (자동 생성, OpenAPI Generator)
- Python (자동 생성)
- Postman Collection
- Webhook 검증 헬퍼 (Node, Python)

## 11. 호환성·버전
- 변경 분류: Breaking / Non-breaking
- Breaking: 메이저 버전 (`/v2/`), 12개월 병행 유지
- 사전 공지 90일, deprecation 헤더

## 12. 관측·로깅
- 모든 요청 `request_id`, 사용자, 테넌트, 작업 분류 기록
- AI 엔드포인트는 추가 메타(모델·토큰·캐시 hit)
- PII 마스킹 후 저장

## 13. 테스트
- Pact 계약 테스트 (FE-BE 간)
- OpenAPI Schemathesis로 무작위 테스트
- E2E Playwright (UI 통한 핵심 흐름)

## 14. 문서·DX
- Stoplight 호스팅 OpenAPI 문서
- 변경 시 자동 빌드·배포
- Try-it-out + Postman one-click
- 한·영 문서, 코드 예시 4개 언어 (ts/python/curl/go)
