import { useId } from "react";

// Compact chip mark: favicon, app header and app icons. Drawn from the logo palette.
const PIN_CENTERS = [24, 32, 40];

export function ChipMark({ size = 32, tile = false }: { size?: number; tile?: boolean }) {
  // Each instance needs its own gradient id: a shared id breaks when the first copy is hidden.
  const gradientId = `chip-mark-body-${useId().replace(/:/g, "")}`;
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" aria-hidden="true" focusable="false">
      <defs>
        <linearGradient id={gradientId} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#7fc4ff" />
          <stop offset="0.55" stopColor="#2f9dfb" />
          <stop offset="1" stopColor="#1668d6" />
        </linearGradient>
      </defs>
      {tile && <rect width="64" height="64" rx="14" fill="#04101f" />}
      <g fill="#7fc4ff">
        {PIN_CENTERS.map((c) => (
          <g key={c}>
            <rect x={c - 2} y={8} width={4} height={9} rx={1.5} />
            <rect x={c - 2} y={47} width={4} height={9} rx={1.5} />
            <rect x={8} y={c - 2} width={9} height={4} rx={1.5} />
            <rect x={47} y={c - 2} width={9} height={4} rx={1.5} />
          </g>
        ))}
      </g>
      <rect x="15" y="15" width="34" height="34" rx="6" fill={`url(#${gradientId})`} />
      <rect x="24" y="24" width="16" height="16" rx="2.5" fill="none" stroke="#e9f8ff" strokeWidth="2.5" />
      <circle cx="20.5" cy="20.5" r="2" fill="#e9f8ff" />
    </svg>
  );
}

export function Wordmark() {
  return (
    <span className="wordmark">
      <span className="wordmark-top">HBCU CHIPS</span>
      <span className="wordmark-bottom">Network</span>
    </span>
  );
}
