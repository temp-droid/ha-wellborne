import { LitElement, html, nothing } from 'lit';
import type { TemplateResult } from 'lit';
import { state } from 'lit/decorators.js';
import { cardStyles } from './styles.js';
import {
  CARD_TAG,
  CARD_VERSION,
  DEFAULT_CONFIG,
  EDITOR_TAG,
  PLACEHOLDER,
  UNAVAILABLE_STATES,
} from './const.js';
import type { EntityKey } from './const.js';
import { resolveEntities } from './entity-resolver.js';
import type { ResolvedEntities } from './entity-resolver.js';
import { computeCost, formatCurrency, resolvePrice } from './cost.js';
import type { ResolvedPrice } from './cost.js';
import { renderCurve } from './power-curve.js';
import { renderSocRing } from './soc-ring.js';
import type {
  CardState,
  HassEntityState,
  HistoryPoint,
  HomeAssistant,
  WellborneCardConfig,
} from './types.js';

// Register the editor element (side-effect import-free; defined here too).
import './editor.js';

const CURVE_W = 220;
const CURVE_H = 56;

export class WellborneChargerCard extends LitElement {
  @state() private _config!: WellborneCardConfig;
  @state() private _history: HistoryPoint[] = [];
  @state() private _price: ResolvedPrice | null = null;

  private _entities: ResolvedEntities = {};
  private _lastHistoryFetch = 0;
  private _historyKey = '';
  private _priceKey = '';

  static styles = cardStyles;

  public static async getConfigElement(): Promise<HTMLElement> {
    await import('./editor.js');
    return document.createElement(EDITOR_TAG);
  }

  public static getStubConfig(): WellborneCardConfig {
    return { type: `custom:${CARD_TAG}`, device: '', ...DEFAULT_CONFIG };
  }

  public getCardSize(): number {
    return 4;
  }

  public setConfig(config: WellborneCardConfig): void {
    if (!config) {
      throw new Error('Invalid configuration');
    }
    this._config = { ...DEFAULT_CONFIG, ...config };
  }

  public set hass(hass: HomeAssistant) {
    this._hass = hass;
    if (!this._config) {
      return;
    }
    this._entities = resolveEntities(hass, this._config);
    this._maybeFetchHistory();
    this._maybeResolvePrice();
    // hass is not a Lit reactive prop here (manual accessor), so nudge a re-render
    // on every coordinator push.
    this.requestUpdate();
  }
  public get hass(): HomeAssistant | undefined {
    return this._hass;
  }
  private _hass?: HomeAssistant;
  private _tick?: ReturnType<typeof setInterval>;

  public connectedCallback(): void {
    super.connectedCallback();
    // Tick the live session duration every second (the entity itself only pushes ~every 4s).
    this._tick = setInterval(() => {
      if (!this._hass || !this._config || this._cardState() !== 'charging') {
        return;
      }
      const st = this._stateOf('session_duration');
      if (typeof st?.attributes?.duration_seconds === 'number') {
        this.requestUpdate();
      }
    }, 1000);
  }

  public disconnectedCallback(): void {
    super.disconnectedCallback();
    if (this._tick) {
      clearInterval(this._tick);
      this._tick = undefined;
    }
  }

  // ---------- data plumbing ----------

  private _maybeResolvePrice(): void {
    if (!this._hass || !this._config.show_cost) {
      return;
    }
    const key = `${this._config.price_entity ?? ''}|${this._config.price ?? ''}|${this._config.use_energy_prefs ?? ''}|${this._priceEntityState()}`;
    if (key === this._priceKey) {
      return;
    }
    this._priceKey = key;
    resolvePrice(this._hass, this._config)
      .then((p) => {
        this._price = p;
      })
      .catch(() => {
        this._price = null;
      });
  }

  private _priceEntityState(): string {
    const id = this._config.price_entity;
    if (!id || !this._hass) {
      return '';
    }
    return this._hass.states[id]?.state ?? '';
  }

  private _maybeFetchHistory(): void {
    if (!this._hass || !this._config.show_curve) {
      return;
    }
    const powerId = this._entities.power;
    if (!powerId) {
      return;
    }
    // Refetch at most every 25s, or when the power entity_id changed.
    const now = Date.now();
    const changed = powerId !== this._historyKey;
    if (!changed && now - this._lastHistoryFetch < 25_000) {
      return;
    }
    this._historyKey = powerId;
    this._lastHistoryFetch = now;

    const hours = this._config.curve_hours ?? 4;
    const start = new Date(now - hours * 3600_000).toISOString();
    const path = `history/period/${encodeURIComponent(start)}?filter_entity_id=${encodeURIComponent(
      powerId,
    )}&minimal_response&no_attributes`;

    this._hass
      .callApi<HassEntityState[][]>('GET', path)
      .then((res) => {
        this._history = this._parseHistory(res, powerId);
      })
      .catch(() => {
        this._history = [];
      });
  }

  private _parseHistory(res: HassEntityState[][], powerId: string): HistoryPoint[] {
    const series = Array.isArray(res)
      ? res.find((s) => s[0]?.entity_id === powerId) ?? res[0]
      : undefined;
    if (!series) {
      return [];
    }
    const points: HistoryPoint[] = [];
    for (const item of series) {
      const v = Number(item.state);
      if (!Number.isFinite(v)) {
        continue;
      }
      const ts = item.last_changed ?? item.last_updated;
      points.push({ t: ts ? Date.parse(ts) : Date.now(), v });
    }
    return points;
  }

  // ---------- reads (guarded) ----------

  private _stateOf(key: EntityKey): HassEntityState | undefined {
    const id = this._entities[key];
    if (!id || !this._hass) {
      return undefined;
    }
    return this._hass.states[id];
  }

  private _num(key: EntityKey): number | null {
    const st = this._stateOf(key);
    if (!st || UNAVAILABLE_STATES.has(st.state)) {
      return null;
    }
    const n = Number(st.state);
    return Number.isFinite(n) ? n : null;
  }

  private _str(key: EntityKey): string | null {
    const st = this._stateOf(key);
    if (!st || UNAVAILABLE_STATES.has(st.state)) {
      return null;
    }
    return st.state;
  }

  private _bool(key: EntityKey): boolean | null {
    const st = this._stateOf(key);
    if (!st || UNAVAILABLE_STATES.has(st.state)) {
      return null;
    }
    return st.state === 'on';
  }

  private _cardState(): CardState {
    const online = this._bool('charger_online');
    if (online === false) {
      return 'offline';
    }
    const charging = this._bool('charging');
    const status = this._str('status');
    if (charging === true || status === 'charging') {
      return 'charging';
    }
    return 'idle';
  }

  // ---------- render ----------

  protected render(): TemplateResult | typeof nothing {
    if (!this._config || !this._hass) {
      return nothing;
    }
    const state = this._cardState();
    const name =
      this._config.name ??
      this._hass.devices?.[this._config.device ?? '']?.name ??
      'Wellborne Charger';

    return html`
      <ha-card @click=${this._handleTap}>
        <div class="card ${state}">
          ${this._renderHeader(name, state)}
          ${this._renderHero(state)}
          ${this._config.show_curve ? this._renderCurveBlock(state) : nothing}
          ${this._renderChips(state)}
          ${this._renderFooter()}
        </div>
      </ha-card>
    `;
  }

  private _renderHeader(name: string, state: CardState): TemplateResult {
    const online = state !== 'offline';
    const badge =
      state === 'charging'
        ? html`<span class="badge charging"><ha-icon icon="mdi:lightning-bolt"></ha-icon>Charging</span>`
        : state === 'offline'
          ? html`<span class="badge offline"><ha-icon icon="mdi:cloud-off-outline"></ha-icon>Offline</span>`
          : html`<span class="badge"><ha-icon icon="mdi:sleep"></ha-icon>Idle</span>`;
    return html`
      <div class="header">
        <div class="title">${name}</div>
        <div class="header-right">
          ${badge}
          <span class="dot ${online ? 'online' : 'offline'}" title=${online ? 'online' : 'offline'}></span>
        </div>
      </div>
    `;
  }

  private _renderHero(state: CardState): TemplateResult {
    const offline = state === 'offline';
    const powerW = this._num('power');
    const kw = offline || powerW === null ? PLACEHOLDER : (powerW / 1000).toFixed(1);
    const duration = this._durationDisplay(state);

    return html`
      <div class="hero">
        ${this._renderRing(state)}
        <div class="hero-main">
          <div class="live-row">
            <div class="kw">${kw}<span class="unit">${kw === PLACEHOLDER ? '' : 'kW'}</span></div>
            <div class="duration">${duration}</div>
          </div>
        </div>
      </div>
    `;
  }

  private _renderRing(state: CardState): TemplateResult | typeof nothing {
    const id = this._config.battery_entity;
    if (!id || !this._hass) {
      return nothing;
    }
    const st = this._hass.states[id];
    if (!st || UNAVAILABLE_STATES.has(st.state)) {
      return nothing;
    }
    const pct = Number(st.state);
    if (!Number.isFinite(pct)) {
      return nothing;
    }
    const rangeLabel = this._rangeLabel(state);
    return html`
      <div class="ring-wrap">
        ${renderSocRing({ percent: pct, rangeLabel, animate: !this._reducedMotion() })}
      </div>
    `;
  }

  private _rangeLabel(state: CardState): string | undefined {
    if (state === 'offline') {
      return undefined;
    }
    const rangeEntity = this._config.range_entity;
    if (rangeEntity && this._hass) {
      const st = this._hass.states[rangeEntity];
      if (st && !UNAVAILABLE_STATES.has(st.state) && Number.isFinite(Number(st.state))) {
        return `${Math.round(Number(st.state))} km`;
      }
    }
    const added = this._num('added_range');
    return added === null ? undefined : `+${Math.round(added)} km`;
  }

  private _renderCurveBlock(state: CardState): TemplateResult {
    const live = state === 'charging';
    const label = live ? 'Live power' : 'Last session';
    return html`
      <div class="curve ${state}">
        <span class="curve-label">${label}</span>
        ${renderCurve(this._history, {
          width: CURVE_W,
          height: CURVE_H,
          gradientId: 'wb-curve-grad',
          animate: !this._reducedMotion(),
          live,
        })}
      </div>
    `;
  }

  private _chip(icon: string, value: string, on = false): TemplateResult {
    return html`<span class="chip ${on ? 'on' : ''}"><ha-icon icon=${icon}></ha-icon>${value}</span>`;
  }

  private _renderChips(state: CardState): TemplateResult {
    const offline = state === 'offline';
    const connected = this._bool('vehicle_connected');
    const current = offline ? null : this._num('current');
    const maxCurrent = offline ? null : this._num('max_current');
    const currentLabel =
      current === null
        ? PLACEHOLDER
        : maxCurrent === null
          ? `${current.toFixed(0)} A`
          : `${current.toFixed(0)} / ${maxCurrent.toFixed(0)} A`;
    const energy = offline ? null : this._num('energy');
    const added = offline ? null : this._num('added_range');
    // Live running cost of the active session (from the SSE `cost` field). Shown only when present.
    const cost = offline ? null : this._num('session_cost');

    // vehicle_connected reads unknown when idle -> render — (never "disconnected").
    const connectedChip =
      connected === true
        ? this._chip('mdi:power-plug', 'Connected', true)
        : this._chip('mdi:power-plug-outline', PLACEHOLDER);

    return html`
      <div class="chips">
        ${connectedChip} ${this._chip('mdi:current-ac', currentLabel)}
        ${this._chip('mdi:lightning-bolt', energy === null ? PLACEHOLDER : `${energy.toFixed(1)} kWh`)}
        ${this._chip('mdi:map-marker-distance', added === null ? PLACEHOLDER : `+${Math.round(added)} km`)}
        ${cost === null || this._hass === undefined
          ? nothing
          : this._chip('mdi:cash', formatCurrency(this._hass, this._config, cost))}
      </div>
    `;
  }

  private _renderFooter(): TemplateResult | typeof nothing {
    const showTotals = this._config.show_totals;
    const showCost = this._config.show_cost;
    if (!showTotals && !showCost) {
      return nothing;
    }

    return html`
      <div class="footer">
        ${showTotals ? this._renderTotals() : nothing}
        ${showCost ? this._renderLastCharge() : nothing}
      </div>
    `;
  }

  private _renderTotals(): TemplateResult {
    return html`
      <div class="stats">
        ${this._statTile('This month', this._num('monthly_energy'))}
        ${this._statTile('This year', this._num('yearly_energy'))}
      </div>
    `;
  }

  /** A total tile: kWh headline + a muted derived-cost sub-line (energy × price). */
  private _statTile(label: string, energy: number | null): TemplateResult {
    const price = this._price?.price ?? null;
    const cost = price !== null && energy !== null ? energy * price : null;
    const cp = cost === null ? null : this._costParts(cost);
    return html`
      <div class="stat">
        <span class="stat-label">${label}</span>
        <span class="stat-value"
          >${energy === null ? PLACEHOLDER : this._fmtKwh(energy)}<span class="stat-unit">kWh</span></span
        >
        ${cp === null
          ? nothing
          : html`<span class="stat-cost">${cp.value}<span class="stat-cost-unit">${cp.unit}</span></span>`}
      </div>
    `;
  }

  private _renderLastCharge(): TemplateResult {
    const energy = this._num('last_session_energy');
    const dur = this._num('last_session_duration');
    // Range (km) and finish time arrive as attributes on the last_session_energy
    // entity; both are optional and silently skipped when absent.
    const attrs = this._stateOf('last_session_energy')?.attributes;
    const km = typeof attrs?.added_range === 'number' ? attrs.added_range : null;
    const when = this._formatWhen(attrs?.end_time);

    // Same disposition as the stat tiles above: uppercase label (+ date) on top,
    // a row of bold values with small muted units below. The cost is the last metric,
    // styled like the others (accent-colored), and hidden when no price resolves.
    const dp = this._durationParts(dur);
    const metrics: TemplateResult[] = [
      this._metric(energy === null ? PLACEHOLDER : this._fmtKwh(energy), energy === null ? '' : 'kWh'),
      this._metric(dp.value, dp.unit),
    ];
    if (km !== null && Number.isFinite(km)) {
      metrics.push(this._metric(`+${Math.round(km)}`, 'km'));
    }
    const cost = this._price === null ? null : computeCost(energy, this._price.price);
    if (cost !== null) {
      const cp = this._costParts(cost);
      metrics.push(this._metric(cp.value, cp.unit));
    }

    return html`
      <div class="last">
        <div class="last-head">
          <span class="last-label">Last charge</span>
          ${when === null ? nothing : html`<span class="last-when">${when}</span>`}
        </div>
        <div class="last-detail">
          ${metrics.map((m, i) => html`${i > 0 ? html`<span class="sep">·</span>` : nothing}${m}`)}
        </div>
      </div>
    `;
  }

  /** A "value + small muted unit" pair, matching the stat-tile unit treatment. */
  private _metric(value: string, unit: string): TemplateResult {
    return html`<span class="metric"
      >${value}${unit === '' ? nothing : html`<span class="unit">${unit}</span>`}</span
    >`;
  }

  /**
   * Split a duration (minutes) into a value + a calculated unit so it reads like the
   * other metrics: under an hour → "45" + "min"; otherwise → "H:MM" + "h".
   */
  private _durationParts(minutes: number | null): { value: string; unit: string } {
    if (minutes === null || !Number.isFinite(minutes) || minutes < 0) {
      return { value: PLACEHOLDER, unit: '' };
    }
    if (minutes < 60) {
      return { value: String(Math.round(minutes)), unit: 'min' };
    }
    const h = Math.floor(minutes / 60);
    const m = Math.round(minutes % 60);
    return { value: `${h}:${m.toString().padStart(2, '0')}`, unit: 'h' };
  }

  /**
   * Split a cost into a numeric value + the currency symbol as a trailing unit, so it
   * reads like the other metrics ("16.23" + "€"). Uses formatToParts so the symbol and
   * number separate correctly regardless of locale/currency placement.
   */
  private _costParts(cost: number): { value: string; unit: string } {
    const currency = this._config.currency ?? this._hass!.config.currency ?? 'EUR';
    try {
      const parts = new Intl.NumberFormat(this._hass!.locale.language, {
        style: 'currency',
        currency,
        currencyDisplay: 'narrowSymbol',
      }).formatToParts(cost);
      const unit = parts.find((p) => p.type === 'currency')?.value ?? currency;
      const value = parts
        .filter((p) => p.type !== 'currency' && p.type !== 'literal')
        .map((p) => p.value)
        .join('');
      return { value, unit };
    } catch {
      return { value: cost.toFixed(2), unit: '€' };
    }
  }

  /** Format the last-session ISO end time as a short localized "Jun 2, 20:30". */
  private _formatWhen(iso: unknown): string | null {
    if (typeof iso !== 'string' || iso === '') {
      return null;
    }
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) {
      return null;
    }
    return new Intl.DateTimeFormat(this._hass!.locale.language, {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    }).format(d);
  }

  // ---------- helpers ----------

  private _formatDuration(minutes: number | null): string {
    if (minutes === null || !Number.isFinite(minutes) || minutes < 0) {
      return PLACEHOLDER;
    }
    const h = Math.floor(minutes / 60);
    const m = Math.round(minutes % 60);
    return `${h}:${m.toString().padStart(2, '0')}`;
  }

  /**
   * Live session duration as H:MM:SS (or M:SS under an hour). Prefers the integration's
   * `duration_seconds` attribute (parsed from the charger's `charingTimeText`) and, while
   * charging, extrapolates from the value's `last_updated` so it ticks every second between
   * the ~4s entity pushes — capped so a stalled stream can't run the timer away. Falls back
   * to the whole-minute sensor value when the attribute isn't present.
   */
  private _durationDisplay(state: CardState): string {
    if (state === 'offline') {
      return PLACEHOLDER;
    }
    const st = this._stateOf('session_duration');
    const secs = st?.attributes?.duration_seconds;
    if (typeof secs === 'number' && Number.isFinite(secs)) {
      let total = secs;
      if (state === 'charging' && st?.last_updated) {
        const elapsed = (Date.now() - new Date(st.last_updated).getTime()) / 1000;
        if (elapsed > 0 && elapsed < 15) {
          total += elapsed;
        }
      }
      return this._formatHMS(total);
    }
    return this._formatDuration(this._num('session_duration'));
  }

  private _formatHMS(totalSeconds: number): string {
    const s = Math.max(0, Math.floor(totalSeconds));
    const h = Math.floor(s / 3600);
    const m = Math.floor((s % 3600) / 60);
    const sec = s % 60;
    const mm = m.toString().padStart(2, '0');
    const ss = sec.toString().padStart(2, '0');
    return h > 0 ? `${h}:${mm}:${ss}` : `${m}:${ss}`;
  }

  private _fmtKwh(v: number): string {
    return new Intl.NumberFormat(this._hass!.locale.language, {
      maximumFractionDigits: 1,
    }).format(v);
  }

  private _reducedMotion(): boolean {
    return (
      typeof window !== 'undefined' &&
      typeof window.matchMedia === 'function' &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches
    );
  }

  private _handleTap(): void {
    // Standard HA more-info on the primary status entity, if available.
    const target = this._entities.status ?? this._entities.power ?? this._entities.charger_online;
    if (!target) {
      return;
    }
    this.dispatchEvent(
      new CustomEvent('hass-more-info', {
        detail: { entityId: target },
        bubbles: true,
        composed: true,
      }),
    );
  }
}

if (!customElements.get(CARD_TAG)) {
  customElements.define(CARD_TAG, WellborneChargerCard);
}

window.customCards = window.customCards ?? [];
window.customCards.push({
  type: CARD_TAG,
  name: 'Wellborne Charger Card',
  description: 'Monitoring card for the Wellborne EV charger (live status, energy, cost).',
  preview: true,
  documentationURL: 'https://github.com/your/repo/tree/main/charger-card',
});

// eslint-disable-next-line no-console
console.info(`%c WELLBORNE-CHARGER-CARD %c v${CARD_VERSION} `, 'background:#0f9d58;color:#fff', '');
