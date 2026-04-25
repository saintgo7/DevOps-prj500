// n-of-m approval tally for daily columns. See ADR-0013 §4.
//
// Rules:
// - For 'standard' sensitivity: 1 approval is enough; 1 rejection blocks.
// - For 'sensitive' sensitivity (medical/legal/child/conflict):
//   2 distinct sensitive-OK approvals are required; any rejection blocks.
// - 'revise' decisions do not count as approvals; the column moves back to
//   draft state for editing and re-submission.

export type Decision = 'approve' | 'reject' | 'revise' | null;
export type Sensitivity = 'standard' | 'sensitive';

export interface RequestRecord {
  decision: Decision;
  approverIsSensitiveOk?: boolean;
}

export type TallyOutcome =
  | { result: 'pending'; reason: string }
  | { result: 'publish' }
  | { result: 'reject'; reason: string }
  | { result: 'revise'; reason: string };

export function tally(
  sensitivity: Sensitivity,
  requests: RequestRecord[],
): TallyOutcome {
  const reject = requests.find((r) => r.decision === 'reject');
  if (reject) {
    return { result: 'reject', reason: 'one approver rejected' };
  }
  const revise = requests.find((r) => r.decision === 'revise');
  if (revise) {
    return { result: 'revise', reason: 'one approver requested revision' };
  }
  const approvals = requests.filter((r) => r.decision === 'approve');
  if (sensitivity === 'sensitive') {
    const sensitiveApprovals = approvals.filter((a) => a.approverIsSensitiveOk).length;
    if (sensitiveApprovals >= 2) return { result: 'publish' };
    return {
      result: 'pending',
      reason: `sensitive column needs 2 approvals from sensitive-OK approvers; have ${sensitiveApprovals}`,
    };
  }
  if (approvals.length >= 1) return { result: 'publish' };
  return { result: 'pending', reason: 'awaiting at least one approval' };
}
