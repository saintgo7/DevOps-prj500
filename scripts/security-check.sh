#!/usr/bin/env bash
# Quick local security checks. Mirrors a subset of CI security scans.
#
# Usage:
#   bash scripts/security-check.sh
#
# What it checks:
#   1. Secrets accidentally staged (heuristic regex)
#   2. .env / *.pem files staged
#   3. Common dangerous patterns in code (no-verify hooks, eval, etc)
#   4. pnpm audit (high+ severity only, advisory not blocking by default)
#
# Exit codes:
#   0 = all clean (warnings allowed via WARN_ONLY=1)
#   1 = at least one finding

set -uo pipefail

WARN_ONLY="${WARN_ONLY:-0}"
FINDINGS=0

step() { printf '\n[security-check] %s\n' "$*"; }
fail() {
  printf '  ✗ %s\n' "$*"
  FINDINGS=$((FINDINGS + 1))
}
ok() { printf '  ✓ %s\n' "$*"; }

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$repo_root"

step "1. Looking for committed secrets / pem keys / env files"
secret_patterns=(
  '-----BEGIN ((RSA|EC|DSA|OPENSSH|PRIVATE) )?PRIVATE KEY-----'
  'AKIA[0-9A-Z]{16}'                       # AWS access key
  'AIza[0-9A-Za-z_\-]{35}'                  # Google API key
  'ghp_[0-9A-Za-z]{36,}'                   # GitHub PAT
  'sk-[A-Za-z0-9]{20,}'                    # OpenAI/Anthropic-style API keys
)
hits=0
for pat in "${secret_patterns[@]}"; do
  if git grep -nIE "$pat" -- ':(exclude)pnpm-lock.yaml' ':(exclude)node_modules' ':(exclude)docs/' >/dev/null 2>&1; then
    git grep -nIE "$pat" -- ':(exclude)pnpm-lock.yaml' ':(exclude)node_modules' ':(exclude)docs/' || true
    hits=$((hits + 1))
  fi
done
if [ "$hits" -gt 0 ]; then fail "found $hits potential secret patterns"; else ok "no obvious secrets in tracked files"; fi

step "2. .env files staged"
if git ls-files | grep -E '^\.env(\..+)?$' | grep -v '^.env.example$' >/dev/null; then
  fail ".env file is tracked"
else
  ok "no .env files tracked"
fi

step "3. Dangerous patterns"
bad_patterns=(
  '--no-verify'
  'eval\(.+\)'
  'process\.env\..*\|\|.*"production"'
)
for pat in "${bad_patterns[@]}"; do
  if git grep -nE "$pat" -- ':(exclude)pnpm-lock.yaml' ':(exclude)docs/' ':(exclude)scripts/security-check.sh' >/dev/null 2>&1; then
    git grep -nE "$pat" -- ':(exclude)pnpm-lock.yaml' ':(exclude)docs/' ':(exclude)scripts/security-check.sh' | head -5
    fail "matches pattern: $pat"
  fi
done

step "4. pnpm audit (high+)"
if command -v pnpm >/dev/null 2>&1; then
  if pnpm audit --audit-level=high 2>&1 | tail -5; then
    ok "pnpm audit clean (or only low/moderate)"
  else
    if [ "$WARN_ONLY" = "1" ]; then
      ok "pnpm audit warnings (WARN_ONLY=1, not failing)"
    else
      fail "pnpm audit reported issues"
    fi
  fi
else
  ok "pnpm not installed — skipped"
fi

echo
if [ "$FINDINGS" -gt 0 ]; then
  echo "[security-check] $FINDINGS finding(s)"
  exit 1
fi
echo "[security-check] all clean"
