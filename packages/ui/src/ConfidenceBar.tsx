import type { ReactElement } from 'react';

export interface ConfidenceBarProps {
  value: number; // 0..1
  ariaLabel?: string;
}

export function ConfidenceBar({ value, ariaLabel }: ConfidenceBarProps): ReactElement {
  const clamped = Math.max(0, Math.min(1, value));
  const pct = Math.round(clamped * 100);
  const tone = clamped >= 0.8 ? '#16A34A' : clamped >= 0.5 ? '#F59E0B' : '#DC2626';
  return (
    <div
      role="progressbar"
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={pct}
      aria-label={ariaLabel ?? 'AI confidence'}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 6,
        width: 120,
      }}
    >
      <div
        style={{
          flex: 1,
          height: 6,
          background: '#E5E7EB',
          borderRadius: 999,
          overflow: 'hidden',
        }}
      >
        <div style={{ width: `${pct}%`, height: '100%', background: tone }} />
      </div>
      <span style={{ fontSize: 12, color: '#374151', minWidth: 32, textAlign: 'right' }}>
        {pct}%
      </span>
    </div>
  );
}
