import { describe, expect, it } from 'vitest';
import { tally } from './approval-tally';

describe('approval-tally', () => {
  it('pending when nobody has decided yet', () => {
    expect(tally('standard', [{ decision: null }, { decision: null }]).result).toBe('pending');
  });

  it('one approval is enough for standard sensitivity', () => {
    expect(tally('standard', [{ decision: 'approve' }]).result).toBe('publish');
  });

  it('one rejection blocks regardless of approvals', () => {
    const out = tally('standard', [
      { decision: 'approve' },
      { decision: 'reject' },
      { decision: 'approve' },
    ]);
    expect(out.result).toBe('reject');
  });

  it('one revision request takes precedence over approvals', () => {
    const out = tally('standard', [
      { decision: 'approve' },
      { decision: 'revise' },
    ]);
    expect(out.result).toBe('revise');
  });

  it('sensitive columns require two sensitive-OK approvals', () => {
    expect(
      tally('sensitive', [
        { decision: 'approve', approverIsSensitiveOk: true },
        { decision: 'approve', approverIsSensitiveOk: false },
      ]).result,
    ).toBe('pending');

    expect(
      tally('sensitive', [
        { decision: 'approve', approverIsSensitiveOk: true },
        { decision: 'approve', approverIsSensitiveOk: true },
      ]).result,
    ).toBe('publish');
  });

  it('rejection in sensitive flow still blocks even with two sensitive approvals', () => {
    expect(
      tally('sensitive', [
        { decision: 'approve', approverIsSensitiveOk: true },
        { decision: 'approve', approverIsSensitiveOk: true },
        { decision: 'reject', approverIsSensitiveOk: true },
      ]).result,
    ).toBe('reject');
  });
});
