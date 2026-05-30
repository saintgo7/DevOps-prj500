# Infrastructure (Terraform)

자세한 설계는 [`docs/16-infrastructure.md`](../docs/16-infrastructure.md) 참조.

## 디렉터리 구조
```
infra/
├── modules/        # 재사용 모듈 (network, ecs-service, rds-postgres, ...)
└── envs/           # 환경별 루트 (dev, staging, prod-kr, prod-eu)
```

## 사전 요구사항
- Terraform >= 1.9
- AWS CLI 구성, 또는 OIDC 단기 자격 (CI)
- 백엔드(state) 버킷 별도 설정 (각 envs/ 안의 backend.tf)

## 개발 환경 적용
```bash
cd infra/envs/dev
terraform init
terraform plan
terraform apply
```

## 정책·가드레일
- `tfsec`, `checkov`, `OPA Conftest`로 정책 검사
- 태깅 의무: `env`, `service`, `owner`
- AWS Organizations · 계정 분리 (prod/staging/dev/security/shared)
