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
    <main class="container" aria-labelledby="cu04-heading">
      <header class="cs-card header-banner">
        <div>
          <span class="tag-pill">CU04 & CU07 · Transacciones y Certificados Tributarios 5FN</span>
          <h1 id="cu04-heading">Registrar Donación y Descargar Certificado PDF</h1>
          <p>
            Reporta tu aporte económico o en especie para una fundación de la Sabana Norte, adjunta tu comprobante y descarga tu certificado tributario inmediato.
          </p>
        </div>
      </header>

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
        <!-- FORMULARIO CU04 -->
        <section class="cs-card" aria-label="Formulario para reportar donación">
          <h2>Reportar Nuevo Aporte Solidario</h2>
          <form (ngSubmit)="enviarDonacion()" novalidate>
            <div class="form-group">
              <label for="campana_sel">1. Campaña Rural a Beneficiar *</label>
              <select id="campana_sel" name="campana_sel" [(ngModel)]="form.campana_id" (ngModelChange)="guardarBorrador()">
                @for (c of campanas(); track c.id) {
                  <option [ngValue]="c.id">{{ c.titulo }} ({{ c.fundacion.municipio }})</option>
                }
              </select>
            </div>

            <div class="form-group">
              <label>2. Modalidad de tu Aporte *</label>
              <div class="modality-toggle">
                <button
                  type="button"
                  class="toggle-btn"
                  [class.active]="form.modalidad === 'ECONOMICA'"
                  (click)="cambiarModalidad('ECONOMICA')"
                >
                  💰 Donación Económica ($ COP)
                </button>
                <button
                  type="button"
                  class="toggle-btn"
                  [class.active]="form.modalidad === 'ESPECIE'"
                  (click)="cambiarModalidad('ESPECIE')"
                >
                  📦 Donación en Especie (Insumos)
                </button>
              </div>
            </div>

            @if (form.modalidad === 'ECONOMICA') {
              <div class="grid-2">
                <div class="form-group">
                  <label for="monto">Monto Donado ($ COP) *</label>
                  <input id="monto" name="monto" type="number" min="5000" step="10000" [(ngModel)]="form.monto" (ngModelChange)="guardarBorrador()" required />
                </div>
                <div class="form-group">
                  <label for="metodo_pago">Método de Pago *</label>
                  <select id="metodo_pago" name="metodo_pago" [(ngModel)]="form.metodo_pago_id" (ngModelChange)="guardarBorrador()">
                    @for (mp of catalogos()?.metodos_pago || []; track mp.id) {
                      <option [ngValue]="mp.id">{{ mp.nombre }}</option>
                    }
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label for="ref_bancaria">Número de Comprobante o Referencia Bancaria *</label>
                <input id="ref_bancaria" name="ref_bancaria" type="text" [(ngModel)]="form.referencia_bancaria" (ngModelChange)="guardarBorrador()" placeholder="Ej: PSE-98451203" required />
              </div>
            } @else {
              <div class="form-group">
                <label for="desc_esp">Descripción de los Artículos o Insumos *</label>
                <input id="desc_esp" name="desc_esp" type="text" [(ngModel)]="form.descripcion_articulos" (ngModelChange)="guardarBorrador()" placeholder="Ej: Kits de semillas de hortalizas y palas agrícolas" required />
              </div>

              <div class="grid-2">
                <div class="form-group">
                  <label for="cantidad_esp">Cantidad *</label>
                  <input id="cantidad_esp" name="cantidad_esp" type="number" min="1" [(ngModel)]="form.cantidad" (ngModelChange)="guardarBorrador()" required />
                </div>
                <div class="form-group">
                  <label for="unidad_esp">Unidad de Medida *</label>
                  <select id="unidad_esp" name="unidad_esp" [(ngModel)]="form.unidad_medida_id" (ngModelChange)="guardarBorrador()">
                    @for (u of catalogos()?.unidades_medida || []; track u.id) {
                      <option [ngValue]="u.id">{{ u.nombre }} ({{ u.simbolo }})</option>
                    }
                  </select>
                </div>
              </div>
            }

            <div class="form-group">
              <label for="comp_file">3. Subir Comprobante o Fotografía del Aporte *</label>
              <input id="comp_file" type="file" accept=".pdf,.png,.jpg" (change)="seleccionarComprobante($event)" />
              <small>Soporte seleccionado: <strong>{{ form.nombre_comprobante }}</strong></small>
            </div>

            <div class="form-group">
              <label for="obs">Mensaje solidario u observaciones de entrega</label>
              <textarea id="obs" name="obs" rows="2" [(ngModel)]="form.observaciones" (ngModelChange)="guardarBorrador()" placeholder="Ej: Entregar en la escuela rural el viernes por la mañana."></textarea>
            </div>

            <button type="submit" class="cs-btn btn-full" [disabled]="enviando()">
              {{ enviando() ? 'Procesando aporte...' : 'Registrar Aporte y Subir Comprobante' }}
            </button>
          </form>
        </section>

        <!-- HISTORIAL Y CERTIFICADOS TRIBUTARIOS PDF (CU07) -->
        <section class="cs-card" aria-label="Aportes registrados y descarga de certificados tributarios">
          <h2>Mis Aportes y Certificados Tributarios (CU07)</h2>
          <p class="helper-text">
            Las donaciones económicas generan un recibo tributario verificable en PDF conforme al Estatuto Tributario.
          </p>

          @if (donaciones().length === 0) {
            <p>Aún no hay donaciones registradas en esta sesión. Registra tu primer aporte en el formulario.</p>
          } @else {
            <div class="donaciones-list">
              @for (d of donaciones(); track d.id) {
                <article class="donacion-item">
                  <div class="donacion-top">
                    <span class="ref-badge">{{ d.codigo_referencia }}</span>
                    <span class="mod-badge">{{ d.modalidad }}</span>
                  </div>
                  <h3>{{ d.campana_titulo }}</h3>
                  <p class="small-meta">Fundación: {{ d.fundacion_nombre }} · Donante: {{ d.donante_nombre }}</p>

                  @if (d.economica) {
                    <p class="amount-highlight">
                      Monto: \${{ d.economica.monto | number:'1.0-0' }} {{ d.economica.moneda }} ({{ d.economica.metodo_pago }})
                    </p>
                    <a
                      class="btn-pdf"
                      [href]="'http://localhost:5000/api/donaciones/economicas/' + d.economica.id + '/certificado-pdf'"
                      target="_blank"
                      rel="noopener"
                    >
                      📄 Descargar Certificado Tributario PDF ({{ d.economica.consecutivo_tributario }})
                    </a>
                  }

                  @if (d.especie) {
                    <p class="amount-highlight">
                      Especie: {{ d.especie.cantidad }} {{ d.especie.unidad_simbolo }} — {{ d.especie.descripcion_articulos }}
                    </p>
                    <span class="logistics-chip">Estado Logístico: {{ d.especie.estado_logistico_actual }}</span>
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
    .container { max-width: 1080px; margin: 2rem auto; padding: 0 1.5rem; }
    .header-banner { margin-bottom: 1.5rem; border-color: var(--brand-primary); }
    .header-banner h1 { margin: 0.4rem 0; font-size: 1.75rem; }
    .tag-pill { display: inline-block; background: var(--status-ok-bg); color: var(--status-ok-text); font-weight: 800; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.85rem; }
    .layout-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 1.5rem; align-items: start; }
    .form-group { display: flex; flex-direction: column; margin-bottom: 1rem; }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 0.85rem; }
    label { font-weight: 700; margin-bottom: 0.35rem; }
    input, select, textarea { min-height: 48px; padding: 0.65rem 0.85rem; font-size: 1rem; border: 2px solid var(--border-strong); border-radius: 8px; }
    .modality-toggle { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; }
    .toggle-btn { min-height: 48px; font-weight: 700; border: 2px solid var(--border-strong); background: #FFFFFF; border-radius: 8px; cursor: pointer; }
    .toggle-btn.active { background: var(--status-ok-bg); border-color: var(--brand-primary); color: var(--status-ok-text); }
    .btn-full { width: 100%; margin-top: 0.5rem; }
    .alert-success { border-left: 6px solid var(--brand-primary); background: var(--status-ok-bg); color: var(--status-ok-text); padding: 1rem; border-radius: 8px; font-weight: 700; margin-bottom: 1rem; }
    .donaciones-list { display: flex; flex-direction: column; gap: 1rem; }
    .donacion-item { border: 2px solid var(--border-subtle); border-radius: 10px; padding: 1rem; background: #F9FAF7; }
    .donacion-top { display: flex; justify-content: space-between; margin-bottom: 0.4rem; }
    .ref-badge { font-weight: 800; color: var(--brand-primary); }
    .mod-badge { background: var(--status-warn-bg); color: var(--status-warn-text); font-weight: 700; padding: 0.15rem 0.5rem; border-radius: 6px; font-size: 0.8rem; }
    .donacion-item h3 { margin: 0.2rem 0; font-size: 1.1rem; }
    .small-meta { margin: 0.2rem 0; font-size: 0.88rem; color: var(--text-secondary); }
    .amount-highlight { font-weight: 800; margin: 0.5rem 0; }
    .btn-pdf { display: inline-flex; align-items: center; min-height: 44px; padding: 0.5rem 0.9rem; background: var(--brand-primary); color: #FFFFFF; font-weight: 700; border-radius: 8px; text-decoration: none; font-size: 0.9rem; }
    .logistics-chip { display: inline-block; background: var(--status-ok-bg); color: var(--status-ok-text); padding: 0.3rem 0.7rem; border-radius: 6px; font-weight: 700; font-size: 0.85rem; }
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
