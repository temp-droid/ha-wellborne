import { LitElement, html, css, nothing } from 'lit';
import type { TemplateResult } from 'lit';
import { property, state } from 'lit/decorators.js';
import { EDITOR_TAG } from './const.js';
import type { HomeAssistant, WellborneCardConfig } from './types.js';

const TOGGLES: Array<{ key: keyof WellborneCardConfig; label: string }> = [
  { key: 'show_curve', label: 'Power curve (sparkline)' },
  { key: 'show_totals', label: 'Month / year totals' },
  { key: 'show_cost', label: 'Last-charge cost' },
];

/**
 * GUI config editor: device picker, optional battery/price fields, show_* toggles.
 * Uses HA's own ha-form-style elements when available, falling back to native
 * inputs so the editor still works in the standalone preview harness.
 */
export class WellborneChargerCardEditor extends LitElement {
  @property({ attribute: false }) public hass?: HomeAssistant;
  @state() private _config?: WellborneCardConfig;

  public setConfig(config: WellborneCardConfig): void {
    this._config = config;
  }

  protected render(): TemplateResult | typeof nothing {
    if (!this._config) {
      return nothing;
    }
    const c = this._config;

    return html`
      <div class="form">
        ${this._renderDevicePicker(c)}

        <label class="field">
          <span>Name (optional)</span>
          <input
            type="text"
            .value=${c.name ?? ''}
            @input=${(e: Event) => this._set('name', (e.target as HTMLInputElement).value || undefined)}
          />
        </label>

        <label class="field">
          <span>Battery entity (car SoC, optional)</span>
          <input
            type="text"
            placeholder="sensor.ioniq5_battery_level"
            .value=${c.battery_entity ?? ''}
            @input=${(e: Event) =>
              this._set('battery_entity', (e.target as HTMLInputElement).value || undefined)}
          />
        </label>

        <label class="field">
          <span>Price entity (€/kWh, optional)</span>
          <input
            type="text"
            placeholder="sensor.wallonia_electricity_price"
            .value=${c.price_entity ?? ''}
            @input=${(e: Event) =>
              this._set('price_entity', (e.target as HTMLInputElement).value || undefined)}
          />
        </label>

        <label class="field">
          <span>Static price fallback (€/kWh, optional)</span>
          <input
            type="number"
            step="0.0001"
            placeholder="0.3783"
            .value=${c.price !== undefined ? String(c.price) : ''}
            @input=${(e: Event) => {
              const v = (e.target as HTMLInputElement).value;
              this._set('price', v === '' ? undefined : Number(v));
            }}
          />
        </label>

        <label class="field toggle">
          <span>Use Home Assistant Energy price</span>
          <input
            type="checkbox"
            .checked=${c.use_energy_prefs ?? false}
            @change=${(e: Event) => this._set('use_energy_prefs', (e.target as HTMLInputElement).checked)}
          />
        </label>

        <label class="field">
          <span>Curve lookback (hours)</span>
          <input
            type="number"
            min="1"
            max="24"
            .value=${String(c.curve_hours ?? 4)}
            @input=${(e: Event) => this._set('curve_hours', Number((e.target as HTMLInputElement).value))}
          />
        </label>

        ${TOGGLES.map(
          (t) => html`
            <label class="field toggle">
              <span>${t.label}</span>
              <input
                type="checkbox"
                .checked=${(c[t.key] as boolean | undefined) ?? true}
                @change=${(e: Event) => this._set(t.key, (e.target as HTMLInputElement).checked)}
              />
            </label>
          `,
        )}
      </div>
    `;
  }

  private _renderDevicePicker(c: WellborneCardConfig): TemplateResult {
    // ha-device-picker is registered by HA at runtime; if absent, fall back to a text field.
    if (customElements.get('ha-device-picker') && this.hass) {
      return html`
        <ha-device-picker
          .hass=${this.hass}
          .value=${c.device ?? ''}
          .label=${'Wellborne device'}
          .includeDomains=${['wellborne']}
          @value-changed=${(e: CustomEvent) => this._set('device', e.detail.value || undefined)}
        ></ha-device-picker>
      `;
    }
    return html`
      <label class="field">
        <span>Wellborne device id</span>
        <input
          type="text"
          .value=${c.device ?? ''}
          @input=${(e: Event) => this._set('device', (e.target as HTMLInputElement).value || undefined)}
        />
      </label>
    `;
  }

  private _set<K extends keyof WellborneCardConfig>(key: K, value: WellborneCardConfig[K]): void {
    if (!this._config) {
      return;
    }
    const next: WellborneCardConfig = { ...this._config };
    if (value === undefined || value === '') {
      delete next[key];
    } else {
      next[key] = value;
    }
    this._config = next;
    this.dispatchEvent(
      new CustomEvent('config-changed', {
        detail: { config: next },
        bubbles: true,
        composed: true,
      }),
    );
  }

  static styles = css`
    .form {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 8px 0;
    }
    .field {
      display: flex;
      flex-direction: column;
      gap: 4px;
      font-size: 0.9rem;
      color: var(--primary-text-color, #e1e1e1);
    }
    .field.toggle {
      flex-direction: row;
      align-items: center;
      justify-content: space-between;
    }
    .field span {
      color: var(--secondary-text-color, #9b9b9b);
    }
    input[type='text'],
    input[type='number'] {
      padding: 8px;
      border-radius: 6px;
      border: 1px solid var(--divider-color, #444);
      background: var(--card-background-color, #2a2a2c);
      color: var(--primary-text-color, #e1e1e1);
      font: inherit;
    }
  `;
}

if (!customElements.get(EDITOR_TAG)) {
  customElements.define(EDITOR_TAG, WellborneChargerCardEditor);
}
