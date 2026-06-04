import { svg, nothing } from 'lit';
import type { SVGTemplateResult } from 'lit';
import type { HistoryPoint } from './types.js';

export interface CurveGeometry {
  /** SVG <path> "d" for the line itself. */
  line: string;
  /** SVG <path> "d" for the closed gradient fill area. */
  area: string;
  /** Leading-edge point in viewBox coords (latest sample). */
  tip: { x: number; y: number } | null;
}

/**
 * Build sparkline geometry from history points. Pure function — unit-testable.
 * viewBox is 0..width x 0..height; higher power = higher on screen.
 */
export function buildCurve(points: HistoryPoint[], width: number, height: number, pad = 2): CurveGeometry {
  const usable = points.filter((p) => Number.isFinite(p.v));
  if (usable.length === 0) {
    return { line: '', area: '', tip: null };
  }
  if (usable.length === 1) {
    const y = height / 2;
    return {
      line: `M ${pad} ${y} L ${width - pad} ${y}`,
      area: `M ${pad} ${y} L ${width - pad} ${y} L ${width - pad} ${height} L ${pad} ${height} Z`,
      tip: { x: width - pad, y },
    };
  }

  const tMin = usable[0].t;
  const tMax = usable[usable.length - 1].t;
  const tSpan = tMax - tMin || 1;

  let vMax = -Infinity;
  let vMin = Infinity;
  for (const p of usable) {
    if (p.v > vMax) vMax = p.v;
    if (p.v < vMin) vMin = p.v;
  }
  // Headroom so a flat plateau doesn't hug the top edge; floor at 0.
  vMin = Math.min(vMin, 0);
  const vSpan = vMax - vMin || 1;

  const innerW = width - pad * 2;
  const innerH = height - pad * 2;

  const xy = usable.map((p) => {
    const x = pad + ((p.t - tMin) / tSpan) * innerW;
    const y = pad + innerH - ((p.v - vMin) / vSpan) * innerH;
    return { x, y };
  });

  let line = `M ${fmt(xy[0].x)} ${fmt(xy[0].y)}`;
  for (let i = 1; i < xy.length; i++) {
    line += ` L ${fmt(xy[i].x)} ${fmt(xy[i].y)}`;
  }

  const last = xy[xy.length - 1];
  const first = xy[0];
  const area = `${line} L ${fmt(last.x)} ${fmt(height)} L ${fmt(first.x)} ${fmt(height)} Z`;

  return { line, area, tip: last };
}

function fmt(n: number): string {
  return (Math.round(n * 100) / 100).toString();
}

export interface RenderCurveOptions {
  width: number;
  height: number;
  gradientId: string;
  /** When false, the leading-edge pulse dot is rendered static. */
  animate: boolean;
  /** When false (idle/offline), no pulse — calm recap line. */
  live: boolean;
}

export function renderCurve(points: HistoryPoint[], opts: RenderCurveOptions): SVGTemplateResult {
  const { width, height, gradientId, animate, live } = opts;
  const geo = buildCurve(points, width, height);

  if (!geo.line) {
    return svg`<svg viewBox="0 0 ${width} ${height}" width="100%" height="${height}" aria-hidden="true"></svg>`;
  }

  const dot = geo.tip
    ? svg`
        <circle
          class="curve-tip ${live ? 'live' : 'static'} ${animate ? 'animate' : 'noanim'}"
          cx="${geo.tip.x}"
          cy="${geo.tip.y}"
          r="2.6"
        ></circle>`
    : nothing;

  return svg`
    <svg viewBox="0 0 ${width} ${height}" width="100%" height="${height}" preserveAspectRatio="none" aria-hidden="true">
      <defs>
        <linearGradient id="${gradientId}" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="var(--wb-accent)" stop-opacity="0.18"></stop>
          <stop offset="100%" stop-color="var(--wb-accent)" stop-opacity="0"></stop>
        </linearGradient>
      </defs>
      <path class="curve-area" d="${geo.area}" fill="url(#${gradientId})"></path>
      <path class="curve-line" d="${geo.line}" fill="none"></path>
      ${dot}
    </svg>
  `;
}
