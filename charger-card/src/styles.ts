import { css } from 'lit';

export const cardStyles = css`
  :host {
    /* Theme-adaptive tokens with doc section-2 fallbacks. */
    --wb-surface: var(--ha-card-background, var(--card-background-color, #1c1c1e));
    --wb-primary: var(--primary-text-color, #e1e1e1);
    --wb-secondary: var(--secondary-text-color, #9b9b9b);
    --wb-divider: var(--divider-color, rgba(255, 255, 255, 0.12));
    --wb-accent: var(--wellborne-charging-color, #0f9d58);
    --wb-error: var(--error-color, #db4437);
    /* Subtle fill used by pill chips / stat tiles (Mushroom-style). */
    --wb-chip-bg: color-mix(in srgb, var(--wb-primary) 8%, transparent);
    display: block;
  }

  ha-card {
    position: relative;
    padding: 16px;
    background: var(--wb-surface);
    overflow: hidden;
  }
  /* Status-tinted depth glow behind the hero; only visible while charging. */
  .card.charging::before {
    content: '';
    position: absolute;
    top: -40%;
    left: -10%;
    width: 70%;
    height: 80%;
    background: radial-gradient(
      circle at 30% 30%,
      color-mix(in srgb, var(--wb-accent) 22%, transparent),
      transparent 70%
    );
    pointer-events: none;
    z-index: 0;
  }
  .card > * {
    position: relative;
    z-index: 1;
  }

  .card.offline {
    opacity: 0.55;
  }

  /* ----- header ----- */
  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 12px;
  }
  .title {
    font-family: var(--ha-card-header-font-family, inherit);
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--wb-primary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .header-right {
    display: flex;
    align-items: center;
    gap: 10px;
    flex: none;
  }
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 12px;
    color: var(--wb-secondary);
    background: color-mix(in srgb, var(--wb-secondary) 16%, transparent);
  }
  .badge.charging {
    color: var(--wb-accent);
    background: color-mix(in srgb, var(--wb-accent) 18%, transparent);
  }
  .badge.offline {
    color: var(--wb-error);
    background: color-mix(in srgb, var(--wb-error) 18%, transparent);
  }
  .badge ha-icon {
    --mdc-icon-size: 16px;
  }
  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--wb-secondary);
    flex: none;
  }
  .dot.online {
    background: var(--wb-accent);
  }
  .dot.offline {
    background: var(--wb-error);
  }

  /* ----- hero ----- */
  .hero {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .hero-main {
    flex: 1 1 auto;
    min-width: 0;
  }
  .live-row {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 4px;
  }
  .kw {
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--wb-primary);
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
  }
  .kw .unit {
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--wb-secondary);
    margin-left: 3px;
  }
  .duration {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--wb-secondary);
    font-variant-numeric: tabular-nums;
    margin-left: auto;
  }
  .ring-wrap {
    flex: none;
  }

  /* ----- curve ----- */
  .curve {
    position: relative;
    margin-top: 6px;
  }
  .curve-label {
    position: absolute;
    top: 0;
    left: 0;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--wb-secondary);
    opacity: 0.7;
    pointer-events: none;
  }
  .curve-line {
    stroke: var(--wb-accent);
    stroke-width: 2;
    stroke-linejoin: round;
    stroke-linecap: round;
  }
  .card.offline .curve-line,
  .curve .idle .curve-line {
    stroke: var(--wb-secondary);
  }
  .curve-tip {
    fill: var(--wb-accent);
  }
  .curve-tip.static,
  .curve-tip.noanim {
    fill: var(--wb-secondary);
  }
  .curve-tip.live.animate {
    fill: var(--wb-accent);
    animation: wb-pulse 1.6s ease-out infinite;
    transform-box: fill-box;
    transform-origin: center;
  }
  @keyframes wb-pulse {
    0% {
      r: 2.6;
      opacity: 1;
    }
    70% {
      r: 5.5;
      opacity: 0.15;
    }
    100% {
      r: 2.6;
      opacity: 1;
    }
  }

  /* ----- chip row (Mushroom-style pills) ----- */
  .chips {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 6px;
    margin-top: 14px;
  }
  .chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--wb-primary);
    background: var(--wb-chip-bg);
    border-radius: 14px;
    padding: 4px 10px 4px 8px;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
  }
  .chip ha-icon {
    --mdc-icon-size: 15px;
    color: var(--wb-secondary);
  }
  .chip.on {
    color: var(--wb-accent);
    background: color-mix(in srgb, var(--wb-accent) 14%, transparent);
  }
  .chip.on ha-icon {
    color: var(--wb-accent);
  }

  /* ----- footer block ----- */
  .footer {
    margin-top: 14px;
    padding-top: 14px;
    border-top: 1px solid var(--wb-divider);
  }
  .stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }
  .stat {
    display: flex;
    flex-direction: column;
    gap: 2px;
    background: var(--wb-chip-bg);
    border-radius: 12px;
    padding: 8px 12px;
  }
  .stat-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--wb-secondary);
  }
  .stat-value {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--wb-primary);
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
  }
  .stat-unit {
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--wb-secondary);
    margin-left: 4px;
  }
  /* Mirror the stat tiles: uppercase label (+ date) on top, bold value row below. */
  .last {
    display: flex;
    flex-direction: column;
    gap: 2px;
    margin-top: 8px;
    background: var(--wb-chip-bg);
    border-radius: 12px;
    padding: 8px 12px;
  }
  .last-head {
    display: flex;
    align-items: baseline;
    gap: 6px;
  }
  .last-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--wb-secondary);
  }
  .last-when {
    font-size: 0.72rem;
    color: var(--wb-secondary);
    opacity: 0.85;
    font-variant-numeric: tabular-nums;
  }
  .last-when::before {
    content: '·';
    margin-right: 6px;
    opacity: 0.6;
  }
  /* Value row matches .stat-value / .stat-unit exactly for cross-tile consistency. */
  .last-detail {
    font-size: 1.15rem;
    font-weight: 700;
    line-height: 1.1;
    color: var(--wb-primary);
    font-variant-numeric: tabular-nums;
  }
  .last-detail .metric {
    white-space: nowrap;
  }
  .last-detail .unit {
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--wb-secondary);
    margin-left: 4px;
  }
  .last-detail .sep {
    margin: 0 6px;
    font-weight: 500;
    color: var(--wb-secondary);
    opacity: 0.55;
  }

  /* ----- SoC ring svg ----- */
  .soc-track {
    stroke: var(--wb-divider);
  }
  .soc-arc {
    stroke: var(--wb-accent);
  }
  .soc-arc.animate {
    transition: stroke-dasharray 280ms ease-out;
  }
  .soc-pct {
    fill: var(--wb-primary);
    font-size: 18px;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
  }
  .soc-range {
    fill: var(--wb-secondary);
    font-size: 9px;
    font-weight: 600;
  }

  /* ----- responsive ----- */
  @media (max-width: 360px) {
    .hero {
      flex-direction: column-reverse;
      align-items: stretch;
    }
    .ring-wrap {
      align-self: center;
    }
    .duration {
      margin-left: auto;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .curve-tip.live.animate {
      animation: none;
    }
    .soc-arc.animate {
      transition: none;
    }
  }
`;
