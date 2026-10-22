import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { OfflineSyncService, CatalogosGenerales } from '../../core/services/offline-sync.service';
import { AuthService } from '../../core/services/auth.service';
import { getApiBaseUrl } from '../../core/config/api.config';

export interface CampanaItem {
  id: number;
  titulo: string;
  descripcion: string;
  meta_economica: number;
  monto_recaudado: number;
  fecha_inicio: string;
  fecha_fin: string;
  estado: string;
  fundacion: {
    id: number;
    razon_social: string;
    municipio: string;
    vereda: string;
  };
  categoria_causa: string;
  ods: { numero: number; titulo: string };
  necesidades: Array<{
    id: number;
    tipo_codigo: string;
    tipo_nombre: string;
    descripcion_item: string;
    cantidad_requerida: number;
    cantidad_cubierta: number;
    prioridad: string;
  }>;
}

@Component({
  selector: 'app-publicar-necesidad',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="sap-page-header">
      <div class="sap-page-header-inner">
        <div>
          <span class="sap-breadcrumb">Gestión de Programas · Sabana Norte</span>
          <h1 class="sap-page-title">Catálogo de Causas y Necesidades Comunitarias</h1>
          <p class="sap-page-subtitle">Administración de campañas sociales y requerimientos de recursos económicos, en especie y voluntariado.</p>
        </div>
        @if (authService.tieneRol('REPRESENTANTE_OSAL', 'ADMIN')) {
          <button type="button" class="cs-btn" (click)="mostrarFormulario.set(!mostrarFormulario())">
            {{ mostrarFormulario() ? 'Cerrar Editor de Campaña' : 'Crear Nueva Campaña' }}
          </button>
        }
      </div>
    </div>

    <main class="sap-container">
      @if (avisoHumano()) {
        <div class="cs-alert-human" role="status">{{ avisoHumano() }}</div>
      }

      @if (mostrarFormulario()) {
        <section class="cs-card form-section" aria-label="Formulario de creación de campaña">
          <div class="section-head">
            <h2>Registro de Nueva Campaña y Requerimientos</h2>
            <span class="sap-badge sap-badge-info">Respaldo Local Activo</span>
          </div>

          <form (ngSubmit)="guardarCampana()" novalidate>
            <div class="grid-2">
              <div class="form-group">
                <label for="titulo" class="sap-form-label">Denominación de la Campaña *</label>
                <input id="titulo" name="titulo" type="text" class="sap-input" [(ngModel)]="nueva.titulo" (ngModelChange)="guardarBorrador()" placeholder="Ej: Dotación de sistemas de filtrado de agua veredal" required />
              </div>
              <div class="form-group">
                <label for="meta" class="sap-form-label">Presupuesto Meta Estimado ($ COP)</label>
                <input id="meta" name="meta" type="number" min="0" step="50000" class="sap-input" [(ngModel)]="nueva.meta_economica" (ngModelChange)="guardarBorrador()" />
              </div>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label for="cat_causa" class="sap-form-label">Línea de Intervención *</label>
                <select id="cat_causa" name="cat_causa" class="sap-input" [(ngModel)]="nueva.categoria_causa_id">
                  @for (c of catalogos()?.categorias_causas || []; track c.id) {
                    <option [ngValue]="c.id">{{ c.nombre }}</option>
                  }
                </select>
              </div>
              <div class="form-group">
                <label for="ods_sel" class="sap-form-label">Objetivo de Desarrollo Sostenible (ODS) *</label>
                <select id="ods_sel" name="ods_sel" class="sap-input" [(ngModel)]="nueva.ods_id">
                  @for (o of catalogos()?.ods_objetivos || []; track o.id) {
                    <option [ngValue]="o.id">ODS {{ o.numero_ods }} · {{ o.titulo }}</option>
                  }
                </select>
              </div>
            </div>

            <div class="form-group">
              <label for="desc_camp" class="sap-form-label">Justificación y Alcance Comunitario *</label>
              <textarea id="desc_camp" name="desc_camp" rows="3" class="sap-input" [(ngModel)]="nueva.descripcion" (ngModelChange)="guardarBorrador()" placeholder="Detalle el impacto esperado en la comunidad rural..." required></textarea>
            </div>

            <div class="necesidades-box">
              <div class="nec-header">
                <h3>Matriz de Requerimientos Específicos</h3>
                <button type="button" class="sap-btn-secondary" (click)="agregarFilaNecesidad()">
                  Añadir Fila de Requerimiento
                </button>
              </div>

              @for (item of nueva.necesidades; track $index) {
                <div class="necesidad-row">
                  <select [name]="'tipo_' + $index" class="sap-input" [(ngModel)]="item.tipo_codigo" aria-label="Modalidad del requerimiento">
                    <option value="ECONOMICA">Recurso Económico</option>
                    <option value="ESPECIE">Insumos en Especie</option>
                    <option value="TIEMPO_VOLUNTARIADO">Horas de Voluntariado</option>
                  </select>
                  <input [name]="'desc_' + $index" type="text" class="sap-input" [(ngModel)]="item.descripcion_item" placeholder="Descripción técnica del ítem o actividad" />
                  <input [name]="'cant_' + $index" type="number" min="1" class="sap-input" [(ngModel)]="item.cantidad_requerida" placeholder="Meta" style="max-width: 120px;" />
                  <select [name]="'prio_' + $index" class="sap-input" [(ngModel)]="item.prioridad" style="max-width: 150px;">
                    <option value="ALTA">Prioridad Alta</option>
                    <option value="MEDIA">Prioridad Media</option>
                  </select>
                </div>
              }
            </div>

            <div class="form-actions">
              <button type="submit" class="cs-btn" [disabled]="guardando()">
                {{ guardando() ? 'Publicando campaña...' : 'Confirmar y Publicar Campaña' }}
              </button>
            </div>
          </form>
        </section>
      }

      <section class="cards-grid" aria-label="Tarjetas de campañas activas">
        @for (c of campanas(); track c.id) {
          <article class="cs-card campaign-card">
            <div>
              <div class="card-meta">
                <span class="sap-badge sap-badge-info">ODS {{ c.ods.numero }} · {{ c.ods.titulo }}</span>
                <span class="sap-badge sap-badge-ok">{{ c.fundacion.municipio }} · {{ c.fundacion.vereda }}</span>
              </div>

              <h2>{{ c.titulo }}</h2>
              <p class="osal-name">Entidad Ejecutora: <strong>{{ c.fundacion.razon_social }}</strong></p>
              <p class="camp-desc">{{ c.descripcion }}</p>

              <div class="progress-block">
                <div class="progress-labels">
                  <span>Ejecución Financiera: <strong>\${{ c.monto_recaudado | number:'1.0-0' }} COP</strong></span>
                  <span>Presupuesto: \${{ c.meta_economica | number:'1.0-0' }} COP</span>
                </div>
                <div class="progress-bar-bg">
                  <div class="progress-bar-fill" [style.width.%]="calcularPorcentaje(c.monto_recaudado, c.meta_economica)"></div>
                </div>
              </div>

              <div class="needs-list">
                <h3>Requerimientos Asociados</h3>
                <ul>
                  @for (n of c.necesidades; track n.id) {
                    <li>
                      <span class="need-type">{{ n.tipo_codigo }}</span>
                      <span>{{ n.descripcion_item }}</span>
                      <strong>{{ n.cantidad_cubierta }} / {{ n.cantidad_requerida }}</strong>
                    </li>
                  }
                </ul>
              </div>
            </div>

            <div class="card-footer">
              <a routerLink="/donar" [queryParams]="{ campana_id: c.id }" class="cs-btn">
                Registrar Aporte
              </a>
              <a routerLink="/voluntariado" [queryParams]="{ campana_id: c.id }" class="sap-btn-secondary">
                Vincularme como Voluntario
              </a>
            </div>
          </article>
        }
      </section>
    </main>
  `,
  styles: [`
    .form-section { margin-bottom: 2rem; border-top: 3px solid var(--sap-brand-primary); }
    .section-head { display: flex; justify-content: space-between; align-items: center; padding-bottom: 0.85rem; margin-bottom: 1.25rem; border-bottom: 1px solid var(--sap-border-subtle); }
    .section-head h2 { margin: 0; font-size: 1.15rem; }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.15rem; }
    .form-group { margin-bottom: 1rem; }
    .necesidades-box { background: var(--sap-bg-canvas); padding: 1.15rem; border-radius: 6px; border: 1px solid var(--sap-border-subtle); margin-bottom: 1.25rem; }
    .nec-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
    .nec-header h3 { margin: 0; font-size: 1rem; }
    .necesidad-row { display: flex; flex-wrap: wrap; gap: 0.65rem; margin-bottom: 0.65rem; }
    .necesidad-row > * { flex: 1 1 180px; }
    .cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 1.5rem; }
    .campaign-card { display: flex; flex-direction: column; justify-content: space-between; border-top: 3px solid var(--sap-brand-primary); }
    .card-meta { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.75rem; }
    .campaign-card h2 { margin: 0 0 0.35rem 0; font-size: 1.2rem; }
    .osal-name { margin: 0; font-size: 0.9rem; color: var(--sap-brand-primary); }
    .camp-desc { color: var(--sap-text-secondary); margin: 0.6rem 0 1.15rem 0; font-size: 0.92rem; }
    .progress-block { margin-bottom: 1.15rem; padding: 0.85rem; background: var(--sap-bg-canvas); border-radius: 6px; border: 1px solid var(--sap-border-subtle); }
    .progress-labels { display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.45rem; }
    .progress-bar-bg { height: 8px; background: #CBD5E1; border-radius: 999px; overflow: hidden; }
    .progress-bar-fill { height: 100%; background: var(--sap-brand-primary); }
    .needs-list { margin-bottom: 1.25rem; }
    .needs-list h3 { margin: 0 0 0.5rem 0; font-size: 0.88rem; text-transform: uppercase; letter-spacing: 0.03em; color: var(--sap-text-secondary); }
    .needs-list ul { list-style: none; margin: 0; padding: 0; border: 1px solid var(--sap-border-subtle); border-radius: 6px; overflow: hidden; }
    .needs-list li { display: grid; grid-template-columns: auto 1fr auto; gap: 0.65rem; align-items: center; padding: 0.55rem 0.75rem; font-size: 0.88rem; border-bottom: 1px solid var(--sap-border-subtle); background: #FFFFFF; }
    .needs-list li:last-child { border-bottom: none; }
    .need-type { font-size: 0.74rem; font-weight: 700; padding: 0.15rem 0.45rem; border-radius: 4px; background: var(--sap-bg-subtle); color: var(--sap-text-primary); }
    .card-footer { display: flex; flex-wrap: wrap; gap: 0.75rem; padding-top: 1rem; border-top: 1px solid var(--sap-border-subtle); }
  `]
})
export class PublicarNecesidadComponent implements OnInit {
  private readonly http = inject(HttpClient);
  private readonly offlineSync = inject(OfflineSyncService);
  readonly authService = inject(AuthService);
  private readonly DRAFT_KEY = 'cu03_nueva_campana';

  catalogos = signal<CatalogosGenerales | null>(null);
  campanas = signal<CampanaItem[]>([]);
  mostrarFormulario = signal(false);
  guardando = signal(false);
  avisoHumano = signal('');

  nueva = {
    titulo: '',
    descripcion: '',
    meta_economica: 5000000,
    categoria_causa_id: 1,
    ods_id: 2,
    necesidades: [
      { tipo_codigo: 'ESPECIE', descripcion_item: 'Herramientas agrícolas y semillas nativas', cantidad_requerida: 30, prioridad: 'ALTA' },
      { tipo_codigo: 'TIEMPO_VOLUNTARIADO', descripcion_item: 'Acompañamiento técnico en siembra comunitaria', cantidad_requerida: 16, prioridad: 'ALTA' },
    ],
  };

  ngOnInit(): void {
    this.offlineSync.obtenerCatalogos().subscribe((cat) => this.catalogos.set(cat));
    const borrador = this.offlineSync.cargarBorradorFormulario<typeof this.nueva>(this.DRAFT_KEY);
    if (borrador) {
      this.nueva = borrador;
    }
    this.cargarCampanas();
  }

  cargarCampanas(): void {
    this.http.get<{ campanas: CampanaItem[] }>(`${getApiBaseUrl()}/campanas`).subscribe({
      next: (res) => this.campanas.set(res.campanas),
      error: () => {
        this.campanas.set([
          {
            id: 1,
            titulo: 'Huertas Escolares Resilientes en Veredas de Cogua y Tabio',
            descripcion: 'Dotación de semillas nativas, herramientas e invernaderos comunitarios para 4 escuelas rurales.',
            meta_economica: 15000000,
            monto_recaudado: 3850000,
            fecha_inicio: '2026-01-15',
            fecha_fin: '2026-12-20',
            estado: 'ACTIVA',
            fundacion: { id: 1, razon_social: 'Fundación Agroecológica Raíces de Sabana Norte', municipio: 'Cogua', vereda: 'Vereda Quebrada Honda' },
            categoria_causa: 'Soberanía Alimentaria y Huertas',
            ods: { numero: 2, titulo: 'Hambre Cero' },
            necesidades: [
              { id: 1, tipo_codigo: 'ESPECIE', tipo_nombre: 'Donación en Especie', descripcion_item: 'Kits de semillas nativas (maíz, quinua, hortalizas)', cantidad_requerida: 120, cantidad_cubierta: 35, prioridad: 'ALTA' },
              { id: 2, tipo_codigo: 'TIEMPO_VOLUNTARIADO', tipo_nombre: 'Tiempo de Voluntariado', descripcion_item: 'Talleres de compostaje y preparación de camas de siembra', cantidad_requerida: 40, cantidad_cubierta: 12, prioridad: 'ALTA' },
            ],
          },
        ]);
      },
    });
  }

  guardarBorrador(): void {
    this.offlineSync.guardarBorradorFormulario(this.DRAFT_KEY, this.nueva);
  }

  agregarFilaNecesidad(): void {
    this.nueva.necesidades.push({
      tipo_codigo: 'ESPECIE',
      descripcion_item: '',
      cantidad_requerida: 10,
      prioridad: 'ALTA',
    });
    this.guardarBorrador();
  }

  calcularPorcentaje(recaudado: number, meta: number): number {
    if (!meta || meta <= 0) return 0;
    return Math.min(100, Math.round((recaudado / meta) * 100));
  }

  guardarCampana(): void {
    if (!this.nueva.titulo.trim() || !this.nueva.descripcion.trim()) {
      this.avisoHumano.set('Por favor escribe el título y la descripción de tu campaña antes de publicarla.');
      return;
    }

    this.guardando.set(true);
    const payload = {
      ...this.nueva,
      fundacion_id: this.authService.usuarioActual()?.fundacion_id || 1,
    };

    this.http.post<{ mensaje_humano: string }>(`${getApiBaseUrl()}/campanas`, payload).subscribe({
      next: (res) => {
        this.guardando.set(false);
        this.avisoHumano.set(res.mensaje_humano);
        this.offlineSync.limpiarBorradorFormulario(this.DRAFT_KEY);
        this.mostrarFormulario.set(false);
        this.cargarCampanas();
      },
      error: (err) => {
        this.guardando.set(false);
        this.guardarBorrador();
        if (err.status === 0) {
          this.avisoHumano.set(
            'Tu conexión parece inestable. Hemos guardado tu campaña y todas sus necesidades en este equipo para publicarla en cuanto recuperes la señal.'
          );
        } else {
          this.avisoHumano.set(err.error?.mensaje_humano || 'No se pudo publicar la campaña.');
        }
      },
    });
  }
}
