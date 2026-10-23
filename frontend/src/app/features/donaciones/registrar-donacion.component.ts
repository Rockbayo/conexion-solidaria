import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { OfflineSyncService, CatalogosGenerales } from '../../core/services/offline-sync.service';
import { AuthService } from '../../core/services/auth.service';
import { getApiBaseUrl } from '../../core/config/api.config';
import { CampanaItem } from '../campanas/publicar-necesidad.component';

interface DonacionResumen {
  id: number;
  codigo_referencia: string;
  modalidad: string;
  estado_aporte: string;
  url_comprobante: string;
  fecha_aporte: string;
  donante_nombre: string;
  donante_correo?: string;
  campana_titulo: string;
  fundacion_nombre: string;
  economica?: {
    id: number;
    monto: number;
    moneda: string;
    metodo_pago: string;
    referencia_bancaria: string;
    consecutivo_tributario: string;
    enviado_correo?: boolean;
    correo_destino?: string;
  };
  especie?: {
    id: number;
    descripcion_articulos: string;
    cantidad: number;
    unidad_simbolo: string;
    estado_logistico_actual: string;
  };
}

@Component({
  selector: 'app-registrar-donacion',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="sap-page-header">
      <div class="sap-page-header-inner">
        <div>
          <span class="sap-breadcrumb">Gestión Financiera y Donaciones</span>
          <h1 class="sap-page-title">Registro Transaccional de Aportes y Certificación Tributaria</h1>
          <p class="sap-page-subtitle">Radicación de aportes monetarios o en especie con emisión de Comprobante Electrónico PDF (Art. 125-2 y 257 E.T.).</p>
        </div>
        <div class="header-actions">
          <a routerLink="/campanas" class="sap-btn-secondary">Ver Causas</a>
          <a routerLink="/panel" class="cs-btn">Finalizar y Volver a Mi Resumen</a>
        </div>
      </div>
    </div>

    <main class="sap-container">
      @if (mensajeOfflineHumano()) {
        <div class="cs-alert-human" role="alert">
          {{ mensajeOfflineHumano() }}
        </div>
      }

      @if (mensajeError()) {
        <div class="alert-error" role="alert">
          ⚠️ {{ mensajeError() }}
        </div>
      }

      @if (mensajeExito()) {
        <div class="alert-success" role="status">
          ✅ {{ mensajeExito() }}
        </div>
      }

      <div class="layout-grid">
        <section class="cs-card sap-form-panel" aria-label="Formulario de registro de donación">
          <div class="panel-head">
            <h2>Formulario de Radicación de Aporte</h2>
            <span class="sap-badge sap-badge-info">Validación Obligatoria</span>
          </div>

          <form (ngSubmit)="enviarDonacion()" novalidate>
            <div class="form-group">
              <label for="campana_sel" class="sap-form-label">Campaña Destinataria *</label>
              <select id="campana_sel" name="campana_sel" class="sap-input" [(ngModel)]="form.campana_id" (ngModelChange)="guardarBorrador()">
                @for (c of campanas(); track c.id) {
                  <option [ngValue]="c.id">{{ c.titulo }} ({{ c.fundacion.municipio }})</option>
                }
              </select>
            </div>

            <div class="form-group">
              <label class="sap-form-label">Modalidad del Aporte *</label>
              <div class="modality-toggle">
                <button
                  type="button"
                  class="toggle-btn"
                  [class.active]="form.modalidad === 'ECONOMICA'"
                  (click)="cambiarModalidad('ECONOMICA')"
                >
                  Aporte Monetario ($ COP)
                </button>
                <button
                  type="button"
                  class="toggle-btn"
                  [class.active]="form.modalidad === 'ESPECIE'"
                  (click)="cambiarModalidad('ESPECIE')"
                >
                  Aporte en Especie (Insumos)
                </button>
              </div>
            </div>

            @if (form.modalidad === 'ECONOMICA') {
              <div class="grid-2">
                <div class="form-group">
                  <label for="monto_fmt" class="sap-form-label">Importe ($ COP · Mínimo $10.000) *</label>
                  <input
                    id="monto_fmt"
                    name="monto_fmt"
                    type="text"
                    inputmode="numeric"
                    class="sap-input money-input"
                    [ngModel]="montoFormateado"
                    (ngModelChange)="actualizarMontoDesdeInput($event)"
                    placeholder="Ej: 50.000"
                    required
                  />
                  <small class="file-hint">Solo pesos enteros con separador de miles (mínimo $10.000 COP).</small>
                </div>
                <div class="form-group">
                  <label for="metodo_pago" class="sap-form-label">Medio de Pago *</label>
                  <select id="metodo_pago" name="metodo_pago" class="sap-input" [(ngModel)]="form.metodo_pago_id" (ngModelChange)="guardarBorrador()">
                    @for (mp of catalogos()?.metodos_pago || []; track mp.id) {
                      <option [ngValue]="mp.id">{{ mp.nombre }}</option>
                    }
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label for="ref_bancaria" class="sap-form-label">Referencia o Comprobante Bancario *</label>
                <input id="ref_bancaria" name="ref_bancaria" type="text" class="sap-input" [(ngModel)]="form.referencia_bancaria" (ngModelChange)="guardarBorrador()" placeholder="Ej: PSE-98451203" required />
              </div>
            } @else {
              <div class="form-group">
                <label for="desc_esp" class="sap-form-label">Detalle de los Bienes o Insumos *</label>
                <input id="desc_esp" name="desc_esp" type="text" class="sap-input" [(ngModel)]="form.descripcion_articulos" (ngModelChange)="guardarBorrador()" placeholder="Ej: Kits de semillas de hortalizas y herramientas" required />
              </div>

              <div class="grid-2">
                <div class="form-group">
                  <label for="cantidad_esp" class="sap-form-label">Cantidad *</label>
                  <input id="cantidad_esp" name="cantidad_esp" type="number" min="1" step="1" class="sap-input" [(ngModel)]="form.cantidad" (ngModelChange)="guardarBorrador()" required />
                </div>
                <div class="form-group">
                  <label for="unidad_esp" class="sap-form-label">Unidad de Medida *</label>
                  <select id="unidad_esp" name="unidad_esp" class="sap-input" [(ngModel)]="form.unidad_medida_id" (ngModelChange)="guardarBorrador()">
                    @for (u of unidadesEspecie(); track u.id) {
                      <option [ngValue]="u.id">{{ u.nombre }}</option>
                    }
                  </select>
                </div>
              </div>
            }

            <div class="form-group upload-box" [class.upload-ready]="!!form.nombre_comprobante">
              <label for="comp_file" class="sap-form-label">Soporte Documental del Aporte (Obligatorio) *</label>
              <input id="comp_file" type="file" class="sap-input" accept=".pdf,.png,.jpg" (change)="seleccionarComprobante($event)" required />
              @if (form.nombre_comprobante) {
                <small class="file-hint ok">✅ Soporte adjunto: <strong>{{ form.nombre_comprobante }}</strong></small>
              } @else {
                <small class="file-hint pending">⚠️ Debes seleccionar el archivo del comprobante (.pdf, .png o .jpg) para poder registrar el aporte.</small>
              }
            </div>

            <div class="form-group">
              <label for="obs" class="sap-form-label">Observaciones de Destinación o Entrega</label>
              <textarea id="obs" name="obs" rows="2" class="sap-input" [(ngModel)]="form.observaciones" (ngModelChange)="guardarBorrador()" placeholder="Notas adicionales para la fundación receptora..."></textarea>
            </div>

            <button type="submit" class="cs-btn btn-full" [disabled]="enviando()">
              {{ enviando() ? 'Contabilizando aporte...' : 'Registrar Aporte y Emitir Soporte' }}
            </button>
          </form>
        </section>

        <section class="cs-card sap-form-panel" aria-label="Libro de aportes y certificados tributarios">
          <div class="panel-head">
            <h2>Libro de Transacciones y Certificados Tributarios</h2>
            <span class="sap-badge sap-badge-ok">Factura / Certificado Digital</span>
          </div>

          @if (donaciones().length === 0) {
            <p class="empty-msg">No se registran movimientos en tu libro actual. Utiliza el formulario adjunto para radicar un aporte.</p>
          } @else {
            <div class="donaciones-list">
              @for (d of donaciones(); track d.id) {
                <article class="donacion-item">
                  <div class="donacion-top">
                    <span class="ref-badge">{{ d.codigo_referencia }}</span>
                    <span class="sap-badge sap-badge-info">{{ d.modalidad === 'ECONOMICA' ? 'Aporte Monetario' : 'Aporte en Especie' }}</span>
                  </div>
                  <h3>{{ d.campana_titulo }}</h3>
                  <p class="small-meta">Entidad Receptora: <strong>{{ d.fundacion_nombre }}</strong> · Aportante: {{ d.donante_nombre }}</p>

                  @if (d.economica) {
                    <div class="fin-summary">
                      <span>Importe Certificado: <strong>\${{ formatearEnteroConPuntos(d.economica.monto) }} {{ d.economica.moneda }}</strong></span>
                      <span>Medio: {{ d.economica.metodo_pago }}</span>
                    </div>
                    <div class="cert-actions-grid">
                      <a
                        class="cs-btn btn-pdf"
                        [href]="apiBaseUrl + '/donaciones/economicas/' + d.economica.id + '/certificado-pdf'"
                        target="_blank"
                        rel="noopener"
                      >
                        📄 Descargar Certificado PDF ({{ d.economica.consecutivo_tributario }})
                      </a>
                      <button
                        type="button"
                        class="sap-btn-secondary btn-email"
                        [disabled]="enviandoCorreoId() === d.economica.id"
                        (click)="enviarCertificadoPorCorreo(d.economica.id)"
                      >
                        {{ enviandoCorreoId() === d.economica.id ? 'Enviando...' : '✉️ Enviar por Correo' }}
                      </button>
                    </div>
                    @if (d.economica.enviado_correo) {
                      <small class="sent-tag">✅ Copia digital remitida a: {{ d.economica.correo_destino || d.donante_correo }}</small>
                    }
                  }

                  @if (d.especie) {
                    <div class="fin-summary">
                      <span>Detalle: <strong>{{ d.especie.cantidad | number:'1.0-0' }} {{ d.especie.unidad_simbolo }}</strong> — {{ d.especie.descripcion_articulos }}</span>
                      <span class="sap-badge sap-badge-ok">Estado: {{ d.especie.estado_logistico_actual }}</span>
                    </div>
                  }
                </article>
              }
            </div>
          }
        </section>
      </div>
    </main>
  `,
  styles: [`
    .header-actions { display: flex; flex-wrap: wrap; gap: 0.65rem; align-items: center; }
    .layout-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 1.5rem; align-items: start; }
    .sap-form-panel { border-top: 3px solid var(--sap-brand-primary); }
    .panel-head { display: flex; justify-content: space-between; align-items: center; padding-bottom: 0.85rem; margin-bottom: 1.25rem; border-bottom: 1px solid var(--sap-border-subtle); }
    .panel-head h2 { margin: 0; font-size: 1.12rem; }
    .form-group { margin-bottom: 1rem; }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 0.9rem; }
    .money-input { font-weight: 700; font-size: 1.05rem; color: var(--sap-brand-primary); letter-spacing: 0.02em; }
    .modality-toggle { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; }
    .toggle-btn { min-height: 42px; font-weight: 700; font-size: 0.9rem; border: 1px solid var(--sap-border-strong); background: var(--sap-bg-surface); border-radius: 4px; cursor: pointer; }
    .toggle-btn.active { background: #E8F1FF; border-color: var(--sap-brand-primary); color: var(--sap-brand-primary); }
    .upload-box { padding: 0.85rem; border: 1px solid var(--sap-border-subtle); border-radius: 6px; background: var(--sap-bg-canvas); }
    .upload-box.upload-ready { border-color: #15803D; background: #F0FDF4; }
    .file-hint { display: block; margin-top: 0.35rem; font-size: 0.82rem; color: var(--sap-text-secondary); }
    .file-hint.ok { color: #15803D; font-weight: 700; }
    .file-hint.pending { color: #B91C1C; font-weight: 600; }
    .btn-full { width: 100%; margin-top: 0.5rem; }
    .alert-success { border-left: 5px solid #15803D; background: #DCFCE7; color: #14532D; padding: 0.9rem 1.2rem; border-radius: 6px; font-weight: 700; margin-bottom: 1.25rem; }
    .alert-error { border-left: 5px solid #B91C1C; background: #FEE2E2; color: #7F1D1D; padding: 0.9rem 1.2rem; border-radius: 6px; font-weight: 700; margin-bottom: 1.25rem; }
    .donaciones-list { display: flex; flex-direction: column; gap: 0.9rem; }
    .donacion-item { border: 1px solid var(--sap-border-subtle); border-radius: 6px; padding: 1rem; background: var(--sap-bg-canvas); }
    .donacion-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; }
    .ref-badge { font-family: monospace; font-weight: 700; color: var(--sap-brand-primary); font-size: 0.9rem; }
    .donacion-item h3 { margin: 0.2rem 0; font-size: 1rem; }
    .small-meta { margin: 0.2rem 0 0.65rem 0; font-size: 0.85rem; color: var(--sap-text-secondary); }
    .fin-summary { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; padding: 0.6rem 0.75rem; background: #FFFFFF; border: 1px solid var(--sap-border-subtle); border-radius: 4px; font-size: 0.88rem; margin-bottom: 0.75rem; }
    .cert-actions-grid { display: grid; grid-template-columns: 1.4fr 1fr; gap: 0.55rem; }
    @media (max-width: 600px) { .cert-actions-grid { grid-template-columns: 1fr; } }
    .btn-pdf, .btn-email { font-size: 0.84rem; min-height: 40px; text-align: center; justify-content: center; }
    .sent-tag { display: block; margin-top: 0.45rem; font-size: 0.78rem; color: #15803D; font-weight: 700; }
  `]
})
export class RegistrarDonacionComponent implements OnInit {
  private readonly http = inject(HttpClient);
  private readonly route = inject(ActivatedRoute);
  private readonly offlineSync = inject(OfflineSyncService);
  private readonly authService = inject(AuthService);
  private readonly DRAFT_KEY = 'cu04_borrador_donacion';
  readonly apiBaseUrl = getApiBaseUrl();

  catalogos = signal<CatalogosGenerales | null>(null);
  campanas = signal<CampanaItem[]>([]);
  donaciones = signal<DonacionResumen[]>([]);
  enviando = signal(false);
  enviandoCorreoId = signal<number | null>(null);
  mensajeExito = signal('');
  mensajeError = signal('');
  mensajeOfflineHumano = signal('');

  montoFormateado = '50.000';

  form = {
    campana_id: 1,
    modalidad: 'ECONOMICA',
    monto: 50000,
    metodo_pago_id: 1,
    referencia_bancaria: '',
    descripcion_articulos: '',
    cantidad: 10,
    unidad_medida_id: 2,
    nombre_comprobante: '',
    observaciones: '',
  };

  ngOnInit(): void {
    this.offlineSync.obtenerCatalogos().subscribe((cat) => this.catalogos.set(cat));
    const borrador = this.offlineSync.cargarBorradorFormulario<typeof this.form>(this.DRAFT_KEY);
    if (borrador) {
      if (borrador.nombre_comprobante === 'Soporte_Transferencia_Solidaria.pdf') {
        borrador.nombre_comprobante = '';
      }
      this.form = borrador;
      this.montoFormateado = this.form.monto > 0 ? this.formatearEnteroConPuntos(this.form.monto) : '';
    }

    this.route.queryParamMap.subscribe((params) => {
      const cid = params.get('campana_id');
      if (cid) {
        this.form.campana_id = Number(cid);
      }
    });

    this.cargarCampanas();
    this.cargarDonaciones();
  }

  unidadesEspecie() {
    const todas = this.catalogos()?.unidades_medida || [];
    return todas.filter((u) => u.simbolo !== 'COP' && u.simbolo !== 'HORAS');
  }

  formatearEnteroConPuntos(valor: number): string {
    const entero = Math.floor(Math.abs(Number(valor) || 0));
    if (entero === 0) return '0';
    return entero.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  }

  actualizarMontoDesdeInput(valorTexto: string): void {
    const soloDigitos = (valorTexto || '').replace(/\D+/g, '');
    if (!soloDigitos) {
      this.form.monto = 0;
      this.montoFormateado = '';
    } else {
      const numeroEntero = parseInt(soloDigitos, 10);
      this.form.monto = numeroEntero;
      this.montoFormateado = this.formatearEnteroConPuntos(numeroEntero);
    }
    this.guardarBorrador();
  }

  cargarCampanas(): void {
    this.http.get<{ campanas: CampanaItem[] }>(`${this.apiBaseUrl}/campanas`).subscribe({
      next: (res) => this.campanas.set(res.campanas),
      error: () => {},
    });
  }

  cargarDonaciones(): void {
    this.http.get<{ donaciones: DonacionResumen[] }>(`${this.apiBaseUrl}/donaciones`).subscribe({
      next: (res) => this.donaciones.set(res.donaciones),
      error: () => {},
    });
  }

  cambiarModalidad(mod: 'ECONOMICA' | 'ESPECIE'): void {
    this.form.modalidad = mod;
    this.mensajeError.set('');
    this.guardarBorrador();
  }

  seleccionarComprobante(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (file) {
      this.form.nombre_comprobante = file.name;
      this.mensajeError.set('');
      this.guardarBorrador();
    }
  }

  guardarBorrador(): void {
    this.offlineSync.guardarBorradorFormulario(this.DRAFT_KEY, this.form);
  }

  enviarDonacion(): void {
    this.mensajeExito.set('');
    this.mensajeError.set('');
    this.mensajeOfflineHumano.set('');

    if (this.form.modalidad === 'ECONOMICA') {
      if (!this.form.monto || this.form.monto < 10000) {
        this.mensajeError.set(
          'El importe del aporte monetario no puede ser menor a $10.000 COP y no debe contener decimales.'
        );
        return;
      }
      if (!this.form.referencia_bancaria.trim()) {
        this.mensajeError.set('Por favor ingresa la referencia o número de comprobante bancario de tu transferencia.');
        return;
      }
    } else {
      if (!this.form.descripcion_articulos.trim() || !this.form.cantidad || this.form.cantidad < 1) {
        this.mensajeError.set('Por favor ingresa el detalle de los insumos a donar y una cantidad válida mayor o igual a 1.');
        return;
      }
    }

    if (!this.form.nombre_comprobante.trim()) {
      this.mensajeError.set(
        'No es posible registrar la donación sin haber cargado el archivo de soporte documental (.pdf, .png o .jpg).'
      );
      return;
    }

    this.enviando.set(true);

    const payload = {
      ...this.form,
      donante_id: this.authService.usuarioActual()?.donante_id || 1,
    };

    this.http.post<{ mensaje_humano: string }>(`${this.apiBaseUrl}/donaciones`, payload).subscribe({
      next: (res) => {
        this.enviando.set(false);
        this.mensajeExito.set(res.mensaje_humano);
        this.offlineSync.limpiarBorradorFormulario(this.DRAFT_KEY);
        this.form.nombre_comprobante = '';
        this.form.referencia_bancaria = '';
        this.cargarDonaciones();
      },
      error: (err) => {
        this.enviando.set(false);
        this.guardarBorrador();
        if (err.status === 0) {
          this.mensajeOfflineHumano.set(
            'Tu conexión parece inestable. Hemos guardado tu donación para enviarla en cuanto recuperes la señal.'
          );
        } else {
          this.mensajeError.set(err.error?.mensaje_humano || 'No pudimos registrar el aporte en este momento.');
        }
      },
    });
  }

  enviarCertificadoPorCorreo(donacionEconomicaId: number): void {
    this.mensajeError.set('');
    this.enviandoCorreoId.set(donacionEconomicaId);

    this.http
      .post<{ mensaje_humano: string }>(
        `${this.apiBaseUrl}/donaciones/economicas/${donacionEconomicaId}/enviar-correo`,
        {}
      )
      .subscribe({
        next: (res) => {
          this.enviandoCorreoId.set(null);
          this.mensajeExito.set(res.mensaje_humano);
          this.cargarDonaciones();
        },
        error: (err) => {
          this.enviandoCorreoId.set(null);
          this.mensajeError.set(err.error?.mensaje_humano || 'No fue posible enviar el certificado por correo.');
        },
      });
  }
}
