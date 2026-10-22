import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
import { OfflineSyncService, CatalogosGenerales } from '../../core/services/offline-sync.service';
import { AuthService } from '../../core/services/auth.service';
import { CampanaItem } from '../campanas/publicar-necesidad.component';

interface DonacionResumen {
  id: number;
  codigo_referencia: string;
  modalidad: string;
  estado_aporte: string;
  url_comprobante: string;
  fecha_aporte: string;
  donante_nombre: string;
  campana_titulo: string;
  fundacion_nombre: string;
  economica?: {
    id: number;
    monto: number;
    moneda: string;
    metodo_pago: string;
    referencia_bancaria: string;
    consecutivo_tributario: string;
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
  imports: [CommonModule, FormsModule],
  template: `
    <div class="sap-page-header">
      <div class="sap-page-header-inner">
        <div>
          <span class="sap-breadcrumb">Gestión Financiera y Donaciones</span>
          <h1 class="sap-page-title">Registro Transaccional de Aportes y Certificación Tributaria</h1>
          <p class="sap-page-subtitle">Radicación de aportes monetarios o en especie con emisión automática de certificados PDF verificables.</p>
        </div>
      </div>
    </div>

    <main class="sap-container">
      @if (mensajeOfflineHumano()) {
        <div class="cs-alert-human" role="alert">
          {{ mensajeOfflineHumano() }}
        </div>
      }

      @if (mensajeExito()) {
        <div class="alert-success" role="status">
          {{ mensajeExito() }}
        </div>
      }

      <div class="layout-grid">
        <section class="cs-card sap-form-panel" aria-label="Formulario de registro de donación">
          <div class="panel-head">
            <h2>Formulario de Radicación de Aporte</h2>
            <span class="sap-badge sap-badge-info">Transacción Segura</span>
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
                  <label for="monto" class="sap-form-label">Importe ($ COP) *</label>
                  <input id="monto" name="monto" type="number" min="5000" step="10000" class="sap-input" [(ngModel)]="form.monto" (ngModelChange)="guardarBorrador()" required />
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
                <label for="desc_esp" class="sap-form-label">Detalle Técnico de los Bienes o Insumos *</label>
                <input id="desc_esp" name="desc_esp" type="text" class="sap-input" [(ngModel)]="form.descripcion_articulos" (ngModelChange)="guardarBorrador()" placeholder="Ej: Kits de semillas de hortalizas y herramientas" required />
              </div>

              <div class="grid-2">
                <div class="form-group">
                  <label for="cantidad_esp" class="sap-form-label">Cantidad *</label>
                  <input id="cantidad_esp" name="cantidad_esp" type="number" min="1" class="sap-input" [(ngModel)]="form.cantidad" (ngModelChange)="guardarBorrador()" required />
                </div>
                <div class="form-group">
                  <label for="unidad_esp" class="sap-form-label">Unidad de Medida *</label>
                  <select id="unidad_esp" name="unidad_esp" class="sap-input" [(ngModel)]="form.unidad_medida_id" (ngModelChange)="guardarBorrador()">
                    @for (u of catalogos()?.unidades_medida || []; track u.id) {
                      <option [ngValue]="u.id">{{ u.nombre }} ({{ u.simbolo }})</option>
                    }
                  </select>
                </div>
              </div>
            }

            <div class="form-group">
              <label for="comp_file" class="sap-form-label">Soporte Documental del Aporte *</label>
              <input id="comp_file" type="file" class="sap-input" accept=".pdf,.png,.jpg" (change)="seleccionarComprobante($event)" />
              <small class="file-hint">Archivo seleccionado: <strong>{{ form.nombre_comprobante }}</strong></small>
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
            <span class="sap-badge sap-badge-ok">Emisión PDF</span>
          </div>

          @if (donaciones().length === 0) {
            <p class="empty-msg">No se registran movimientos en el libro actual. Utiliza el formulario adjunto para radicar un aporte.</p>
          } @else {
            <div class="donaciones-list">
              @for (d of donaciones(); track d.id) {
                <article class="donacion-item">
                  <div class="donacion-top">
                    <span class="ref-badge">{{ d.codigo_referencia }}</span>
                    <span class="sap-badge sap-badge-info">{{ d.modalidad }}</span>
                  </div>
                  <h3>{{ d.campana_titulo }}</h3>
                  <p class="small-meta">Entidad: {{ d.fundacion_nombre }} · Aportante: {{ d.donante_nombre }}</p>

                  @if (d.economica) {
                    <div class="fin-summary">
                      <span>Importe Verificado: <strong>\${{ d.economica.monto | number:'1.0-0' }} {{ d.economica.moneda }}</strong></span>
                      <span>Medio: {{ d.economica.metodo_pago }}</span>
                    </div>
                    <a
                      class="cs-btn btn-pdf"
                      [href]="'http://localhost:5000/api/donaciones/economicas/' + d.economica.id + '/certificado-pdf'"
                      target="_blank"
                      rel="noopener"
                    >
                      Descargar Certificado Tributario PDF ({{ d.economica.consecutivo_tributario }})
                    </a>
                  }

                  @if (d.especie) {
                    <div class="fin-summary">
                      <span>Detalle: <strong>{{ d.especie.cantidad }} {{ d.especie.unidad_simbolo }}</strong> — {{ d.especie.descripcion_articulos }}</span>
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
    .layout-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 1.5rem; align-items: start; }
    .sap-form-panel { border-top: 3px solid var(--sap-brand-primary); }
    .panel-head { display: flex; justify-content: space-between; align-items: center; padding-bottom: 0.85rem; margin-bottom: 1.25rem; border-bottom: 1px solid var(--sap-border-subtle); }
    .panel-head h2 { margin: 0; font-size: 1.12rem; }
    .form-group { margin-bottom: 1rem; }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 0.9rem; }
    .modality-toggle { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; }
    .toggle-btn { min-height: 42px; font-weight: 700; font-size: 0.9rem; border: 1px solid var(--sap-border-strong); background: var(--sap-bg-surface); border-radius: 4px; cursor: pointer; }
    .toggle-btn.active { background: #E8F1FF; border-color: var(--sap-brand-primary); color: var(--sap-brand-primary); }
    .file-hint { display: block; margin-top: 0.35rem; font-size: 0.82rem; color: var(--sap-text-secondary); }
    .btn-full { width: 100%; margin-top: 0.5rem; }
    .alert-success { border-left: 4px solid var(--sap-status-ok-border); background: var(--sap-status-ok-bg); color: var(--sap-status-ok-text); padding: 0.9rem 1.2rem; border-radius: 6px; font-weight: 600; margin-bottom: 1.25rem; }
    .donaciones-list { display: flex; flex-direction: column; gap: 0.9rem; }
    .donacion-item { border: 1px solid var(--sap-border-subtle); border-radius: 6px; padding: 1rem; background: var(--sap-bg-canvas); }
    .donacion-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; }
    .ref-badge { font-family: monospace; font-weight: 700; color: var(--sap-brand-primary); font-size: 0.9rem; }
    .donacion-item h3 { margin: 0.2rem 0; font-size: 1rem; }
    .small-meta { margin: 0.2rem 0 0.65rem 0; font-size: 0.85rem; color: var(--sap-text-secondary); }
    .fin-summary { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; padding: 0.6rem 0.75rem; background: #FFFFFF; border: 1px solid var(--sap-border-subtle); border-radius: 4px; font-size: 0.88rem; margin-bottom: 0.75rem; }
    .btn-pdf { width: 100%; font-size: 0.88rem; min-height: 40px; }
  `]
})
export class RegistrarDonacionComponent implements OnInit {
  private readonly http = inject(HttpClient);
  private readonly route = inject(ActivatedRoute);
  private readonly offlineSync = inject(OfflineSyncService);
  private readonly authService = inject(AuthService);
  private readonly DRAFT_KEY = 'cu04_borrador_donacion';

  catalogos = signal<CatalogosGenerales | null>(null);
  campanas = signal<CampanaItem[]>([]);
  donaciones = signal<DonacionResumen[]>([]);
  enviando = signal(false);
  mensajeExito = signal('');
  mensajeOfflineHumano = signal('');

  form = {
    campana_id: 1,
    modalidad: 'ECONOMICA',
    monto: 120000,
    metodo_pago_id: 1,
    referencia_bancaria: 'PSE-20261022-881',
    descripcion_articulos: 'Kits de semillas nativas de maíz y frijol sabanero',
    cantidad: 25,
    unidad_medida_id: 3,
    nombre_comprobante: 'Soporte_Transferencia_Solidaria.pdf',
    observaciones: '',
  };

  ngOnInit(): void {
    this.offlineSync.obtenerCatalogos().subscribe((cat) => this.catalogos.set(cat));
    const borrador = this.offlineSync.cargarBorradorFormulario<typeof this.form>(this.DRAFT_KEY);
    if (borrador) {
      this.form = borrador;
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

  cargarCampanas(): void {
    this.http.get<{ campanas: CampanaItem[] }>('http://localhost:5000/api/campanas').subscribe({
      next: (res) => this.campanas.set(res.campanas),
      error: () => {},
    });
  }

  cargarDonaciones(): void {
    this.http.get<{ donaciones: DonacionResumen[] }>('http://localhost:5000/api/donaciones').subscribe({
      next: (res) => this.donaciones.set(res.donaciones),
      error: () => {},
    });
  }

  cambiarModalidad(mod: 'ECONOMICA' | 'ESPECIE'): void {
    this.form.modalidad = mod;
    this.guardarBorrador();
  }

  seleccionarComprobante(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (file) {
      this.form.nombre_comprobante = file.name;
      this.guardarBorrador();
    }
  }

  guardarBorrador(): void {
    this.offlineSync.guardarBorradorFormulario(this.DRAFT_KEY, this.form);
  }

  enviarDonacion(): void {
    this.mensajeExito.set('');
    this.mensajeOfflineHumano.set('');
    this.enviando.set(true);

    const payload = {
      ...this.form,
      donante_id: this.authService.usuarioActual()?.donante_id || 1,
    };

    this.http.post<{ mensaje_humano: string }>('http://localhost:5000/api/donaciones', payload).subscribe({
      next: (res) => {
        this.enviando.set(false);
        this.mensajeExito.set(res.mensaje_humano);
        this.offlineSync.limpiarBorradorFormulario(this.DRAFT_KEY);
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
          this.mensajeOfflineHumano.set(err.error?.mensaje_humano || 'No pudimos registrar el aporte en este momento.');
        }
      },
    });
  }
}
