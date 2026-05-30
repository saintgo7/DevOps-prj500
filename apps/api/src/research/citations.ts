// Citation chain validator. Pure module — no Prisma, no IO.
//
// Rules (ADR-0017 §A.3):
//   1. Each citation must point at exactly one source. (DB CHECK enforces it
//      too, but we surface a friendly error before the round-trip.)
//   2. Self-citation ratio ≤ 20% unless `selfCiteOverrideReason` is set.
//   3. External citations must have a DOI or a permanent URL.
//   4. Position must be unique and start at 1.

export interface CitationDraft {
  position: number;
  rendered: string;
  sourceColumnId?: string;
  sourceManuscriptId?: string;
  sourcePatentInsightId?: string;
  sourceWatchItemId?: string;
  externalDoi?: string;
  externalUrl?: string;
}

export interface CitationCheck {
  ok: boolean;
  errors: string[];
}

const PERMANENT_URL_PREFIXES = ['https://doi.org/', 'https://arxiv.org/', 'https://www.ncbi.nlm.nih.gov/'];

export function countSources(c: CitationDraft): number {
  return (
    (c.sourceColumnId ? 1 : 0) +
    (c.sourceManuscriptId ? 1 : 0) +
    (c.sourcePatentInsightId ? 1 : 0) +
    (c.sourceWatchItemId ? 1 : 0) +
    (c.externalDoi ? 1 : 0) +
    (c.externalUrl ? 1 : 0)
  );
}

export interface ValidateOptions {
  /** This manuscript's own id, so we can detect self-citations. */
  selfManuscriptId: string;
  selfCiteOverrideReason?: string;
}

export function validateCitations(
  citations: readonly CitationDraft[],
  opts: ValidateOptions,
): CitationCheck {
  const errors: string[] = [];

  const positions = new Set<number>();
  let selfCount = 0;

  for (const c of citations) {
    const sources = countSources(c);
    if (sources !== 1) {
      errors.push(
        `Citation #${c.position} ("${c.rendered}") must point at exactly one source — got ${sources}.`,
      );
    }

    if (positions.has(c.position)) {
      errors.push(`Citation position ${c.position} is duplicated.`);
    }
    positions.add(c.position);

    if (c.externalUrl && !c.externalDoi) {
      const ok = PERMANENT_URL_PREFIXES.some((p) => c.externalUrl!.startsWith(p));
      if (!ok) {
        errors.push(
          `Citation #${c.position} uses an external URL that is not a permanent identifier (DOI / arXiv / PMC).`,
        );
      }
    }

    if (c.sourceManuscriptId === opts.selfManuscriptId) {
      selfCount += 1;
    }

    if (!c.rendered || c.rendered.trim().length === 0) {
      errors.push(`Citation #${c.position} is missing a rendered string.`);
    }
  }

  // Position should start at 1 and be contiguous. Catching gaps early avoids
  // confusing "Smith [3]" appearing before "[2]" in the rendered manuscript.
  const sorted = [...positions].sort((a, b) => a - b);
  for (let i = 0; i < sorted.length; i += 1) {
    if (sorted[i] !== i + 1) {
      errors.push(`Citation positions must start at 1 and be contiguous — found a gap at ${i + 1}.`);
      break;
    }
  }

  if (citations.length > 0) {
    const ratio = selfCount / citations.length;
    if (ratio > 0.2 && !opts.selfCiteOverrideReason) {
      errors.push(
        `Self-citation ratio is ${(ratio * 100).toFixed(0)}% — over the 20% threshold. ` +
          `Provide an editor override reason to proceed.`,
      );
    }
  }

  return { ok: errors.length === 0, errors };
}
