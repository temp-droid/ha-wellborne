import { svg } from 'lit';
import type { SVGTemplateResult } from 'lit';

export interface SocRingOptions {
  /** 0..100 */
  percent: number;
  /** Optional center label below the percent, e.g. "+142 km". */
  rangeLabel?: string;
  /** Gate the stroke transition for prefers-reduced-motion. */
  animate: boolean;
  size?: number;
}

/**
 * SVG SoC ring via stroke-dasharray. Pure render fn.
 */
export function renderSocRing(opts: SocRingOptions): SVGTemplateResult {
  const size = opts.size ?? 96;
  const stroke = 8;
  const r = (size - stroke) / 2;
  const cx = size / 2;
  const cy = size / 2;
  const circumference = 2 * Math.PI * r;
  const pct = clamp(opts.percent, 0, 100);
  const dash = (pct / 100) * circumference;
  const cls = opts.animate ? 'soc-arc animate' : 'soc-arc';

  return svg`
    <svg viewBox="0 0 ${size} ${size}" width="${size}" height="${size}" class="soc-ring" role="img"
         aria-label="State of charge ${Math.round(pct)} percent">
      <circle class="soc-track" cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke-width="${stroke}"></circle>
      <circle
        class="${cls}"
        cx="${cx}"
        cy="${cy}"
        r="${r}"
        fill="none"
        stroke-width="${stroke}"
        stroke-linecap="round"
        stroke-dasharray="${dash} ${circumference - dash}"
        transform="rotate(-90 ${cx} ${cy})"
      ></circle>
      <text class="soc-pct" x="${cx}" y="${opts.rangeLabel ? cy - 2 : cy + 1}" text-anchor="middle" dominant-baseline="middle">${Math.round(pct)}%</text>
      ${opts.rangeLabel
        ? svg`<text class="soc-range" x="${cx}" y="${cy + 14}" text-anchor="middle" dominant-baseline="middle">${opts.rangeLabel}</text>`
        : svg``}
    </svg>
  `;
}

function clamp(v: number, lo: number, hi: number): number {
  return Math.min(hi, Math.max(lo, v));
}
