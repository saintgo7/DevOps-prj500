import type { CSSProperties, ReactElement } from 'react';

const SDG_COLORS: Record<number, string> = {
  1: '#E5243B',
  2: '#DDA63A',
  3: '#4C9F38',
  4: '#C5192D',
  5: '#FF3A21',
  6: '#26BDE2',
  7: '#FCC30B',
  8: '#A21942',
  9: '#FD6925',
  10: '#DD1367',
  11: '#FD9D24',
  12: '#BF8B2E',
  13: '#3F7E44',
  14: '#0A97D9',
  15: '#56C02B',
  16: '#00689D',
  17: '#19486A',
};

export interface SdgBadgeProps {
  goal: number;
  label?: string;
  size?: 'sm' | 'md';
}

export function SdgBadge({ goal, label, size = 'md' }: SdgBadgeProps): ReactElement {
  const color = SDG_COLORS[goal] ?? '#666';
  const dim = size === 'sm' ? 28 : 36;
  const style: CSSProperties = {
    display: 'inline-flex',
    alignItems: 'center',
    gap: 8,
    padding: size === 'sm' ? '2px 8px' : '4px 12px',
    borderRadius: 4,
    background: color,
    color: 'white',
    fontWeight: 600,
    fontSize: size === 'sm' ? 12 : 14,
  };
  return (
    <span
      style={style}
      role="img"
      aria-label={label ? `SDG ${goal} — ${label}` : `SDG ${goal}`}
    >
      <span style={{ width: dim / 2, textAlign: 'center' }}>{goal}</span>
      {label ? <span>{label}</span> : null}
    </span>
  );
}
