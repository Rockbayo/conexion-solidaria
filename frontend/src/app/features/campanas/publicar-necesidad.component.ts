import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { OfflineSyncService, CatalogosGenerales } from '../../core/services/offline-sync.service';
import { AuthService } from '../../core/services/auth.service';

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
    <main class="container" aria-labelledby="cu03-heading">
      <header class="cs-card header-banner">
        <div>
          <span class="tag-pill">CU03 · Catálogo de Causas 5FN</span>
          <h1 id="cu03-heading">Campañas y Necesidades Rurales</h1>
          <p>Publica los requerimientos de tu fundación (Apoyo Económico, Especie o Tiempo de Voluntariado) y explora las causas activas en la Sabana Norte.</p>
        </div>
        <button type="button" class="cs-btn" (click)="mostrarFormulario.set(!mostrarFormulario())">
          {{ mostrarFormulario() ? 'Ocultar formulario' : '+ Publicar Nueva Necesidad' }}
        </button>
      </header>

      @if (avisoHumano()) {
        <div class="cs-alert-human" role="status">{{ avisoHumano() }}</div>
      }

      @if (mostrarFormulario()) {
        <section class="cs-card form-section" aria-label="Formulario para publicar campaña y necesidades">
          <h2>Publicar Nueva Campaña para tu OSAL</h2>
          <form (ngSubmit)="guardarCampana()" novalidate>
            <div class="grid-2">
              <div class="form-group">
                <label for="titulo">Título claro de la campaña *</label>
                <input id="titulo" name="titulo" type="text" [(ngModel)]="nueva.titulo" (ngModelChange)="guardarBorrador()" placeholder="Ej: Dotación de filtros de agua para escuela veredal" required />
              </div>
              <div class="form-group">
                <label for="meta">Meta Económica Estimada ($ COP)</label>
                <input id="meta" name="meta" type="number" min="0" step="50000" [(ngModel)]="nueva.meta_economica" (ngModelChange)="guardarBorrador()" />
              </div>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label for="cat_causa">Categoría de la Causa *</label>
                <select id="cat_causa" name="cat_causa" [(ngModel)]="nueva.categoria_causa_id">
                  @for (c of catalogos()?.categorias_causas || []; track c.id) {
                    <option [ngValue]="c.id">{{ c.nombre }}</option>
                  }
                </select>
              </div>
              <div class="form-group">
                <label for="ods_sel">Objetivo de Desarrollo Sostenible (ODS) *</label>
                <select id="ods_sel" name="ods_sel" [(ngModel)]="nueva.ods_id">
                  @for (o of catalogos()?.ods_objetivos || []; track o.id) {
                    <option [ngValue]="o.id">ODS {{ o.numero_ods }}: {{ o.titulo }}</option>
                  }
                </select>
              </div>
            </div>

            <div class="form-group">
              <label for="desc_camp">Historia y propósito comunitario *</label>
              <textarea id="desc_camp" name="desc_camp" rows="3" [(ngModel)]="nueva.descripcion" (ngModelChange)="guardarBorrador()" placeholder="Explica cómo este apoyo transformará la vereda..." required></textarea>
            </div>

            <div class="necesidades-box">
              <h3>Desglose de Necesidades (Económica, Especie o Tiempo)</h3>
              @for (item of nueva.necesidades; track $index) {
                <div class="necesidad-row">
                  <select [name]="'tipo_' + $index" [(ngModel)]="item.tipo_codigo" aria-label="Tipo de necesidad">
                    <option value="ECONOMICA">Apoyo Económico</option>
                    <option value="ESPECIE">Donación en Especie</option>
                    <option value="TIEMPO_VOLUNTARIADO">Tiempo de Voluntariado</option>
                  </select>
                  <input [name]="'desc_' + $index" type="text" [(ngModel)]="item.descripcion_item" placeholder="Ej: 50 bultos de abono orgánico o 20 horas de taller" />
                  <input [name]="'cant_' + $index" type="number" min="1" [(ngModel)]="item.cantidad_requerida" placeholder="Cant." style="max-width: 110px;" />
                  <select [name]="'prio_' + $index" [(ngModel)]="item.prioridad" style="max-width: 130px;">
                    <option value="ALTA">Prioridad Alta</option>
                    <option value="MEDIA">Prioridad Media</option>
                  </select>
                </div>
              }
              <button type="button" class="btn-outline-sm" (click)="agregarFilaNecesidad()">
                + Añadir otra necesidad específica a la campaña
              </button>
            </div>

            <div class="form-actions">
              <button type="submit" class="cs-btn" [disabled]="guardando()">
                {{ guardando() ? 'Publicando campaña...' : 'Publicar Campaña Ahora' }}
              </button>
            </div>
          </form>
        </section>
      }

      <!-- TARJETAS DE CAMPAÑAS (CARDS ACCESIBLES WCAG 2.2) -->
      <section class="cards-grid" aria-label="Listado de campañas solidarias en tarjetas">
        @for (c of campanas(); track c.id) {
          <article class="cs-card campaign-card">
            <div class="card-meta">
              <span class="ods-badge">ODS {{ c.ods.numero }} · {{ c.ods.titulo }}</span>
              <span class="mun-badge">📍 {{ c.fundacion.municipio }} ({{ c.fundacion.vereda }})</span>
            </div>

            <h2>{{ c.titulo }}</h2>
            <p class="osal-name">Organiza: <strong>{{ c.fundacion.razon_social }}</strong></p>
            <p class="camp-desc">{{ c.descripcion }}</p>

            <div class="progress-block">
              <div class="progress-labels">
                <span>Recaudado: <strong>\${{ c.monto_recaudado | number:'1.0-0' }} COP</strong></span>
                <span>Meta: \${{ c.meta_economica | number:'1.0-0' }} COP</span>
              </div>
              <div class="progress-bar-bg">
                <div class="progress-bar-fill" [style.width.%]="calcularPorcentaje(c.monto_recaudado, c.meta_economica)"></div>
              </div>
            </div>

            <div class="needs-list">
              <h3>Necesidades Requeridas:</h3>
              <ul>
                @for (n of c.necesidades; track n.id) {
                  <li>
                    <span class="need-type">[{{ n.tipo_codigo }}]</span>
                    {{ n.descripcion_item }} — <strong>Meta: {{ n.cantidad_requerida }}</strong> (Cubierto: {{ n.cantidad_cubierta }})
                  </li>
                }
              </ul>
            </div>

            <div class="card-footer">
              <a routerLink="/donar" [queryParams]="{ campana_id: c.id }" class="cs-btn">
                Hacer Donación
              </a>
              <a routerLink="/voluntariado" [queryParams]="{ campana_id: c.id }" class="btn-secondary-link">
                Postularme como Voluntario
              </a>
            </div>
          </article>
        }
      </section>
    </main>
  `,
  styles: [`
    .container { max-width: 1080px; margin: 2rem auto; padding: 0 1.5rem; }
    .header-banner { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.5rem; border-color: var(--brand-primary); }
    .header-banner h1 { margin: 0.4rem 0; font-size: 1.75rem; }
    .header-banner p { margin: 0; color: var(--text-secondary); max-width: 680px; }
    .tag-pill { display: inline-block; background: var(--status-ok-bg); color: var(--status-ok-text); font-weight: 800; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.85rem; }
    .form-section { margin-bottom: 2rem; border-color: var(--border-strong); }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; }
    .form-group { display: flex; flex-direction: column; margin-bottom: 1rem; }
    label { font-weight: 700; margin-bottom: 0.35rem; }
    input, select, textarea { min-height: 48px; padding: 0.65rem 0.9rem; font-size: 1rem; border: 2px solid var(--border-strong); border-radius: 8px; }
    .necesidades-box { background: #F3F4F6; padding: 1rem; border-radius: 10px; border: 2px solid var(--border-subtle); margin-bottom: 1.25rem; }
    .necesidad-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.75rem; }
    .necesidad-row > * { flex: 1 1 180px; }
    .btn-outline-sm { min-height: 44px; padding: 0.5rem 1rem; font-weight: 700; border: 2px solid var(--brand-primary); background: #FFFFFF; color: var(--brand-primary); border-radius: 8px; cursor: pointer; }
    .cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 1.5rem; }
    .campaign-card { display: flex; flex-direction: column; justify-content: space-between; border-color: var(--border-strong); }
    .card-meta { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.75rem; }
    .ods-badge { background: var(--status-ok-bg); color: var(--status-ok-text); font-weight: 800; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.82rem; }
    .mun-badge { background: var(--status-warn-bg); color: var(--status-warn-text); font-weight: 700; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.82rem; }
    .osal-name { margin: 0.25rem 0; color: var(--brand-primary); }
    .camp-desc { color: var(--text-secondary); margin: 0.5rem 0 1rem 0; }
    .progress-block { margin-bottom: 1rem; }
    .progress-labels { display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 0.35rem; }
    .progress-bar-bg { height: 12px; background: #E5E7EB; border-radius: 999px; overflow: hidden; border: 1px solid var(--border-strong); }
    .progress-bar-fill { height: 100%; background: var(--brand-primary); }
    .needs-list { background: #F9FAF7; padding: 0.75rem 1rem; border-radius: 8px; border: 1px solid var(--border-subtle); margin-bottom: 1.25rem; }
    .needs-list h3 { margin: 0 0 0.5rem 0; font-size: 0.95rem; }
    .needs-list ul { margin: 0; padding-left: 1.1rem; font-size: 0.9rem; }
    .need-type { font-weight: 800; color: var(--brand-primary); }
    .card-footer { display: flex; flex-wrap: wrap; gap: 0.75rem; }
    .btn-secondary-link { display: inline-flex; align-items: center; justify-content: center; min-height: 48px; padding: 0.75rem 1rem; font-weight: 700; border: 2px solid var(--brand-primary); color: var(--brand-primary); border-radius: 8px; text-decoration: none; background: #FFFFFF; }
  `]
})
export class PublicarNecesidadComponent implements OnInit {
  private readonly http = inject(HttpClient);
  private readonly offlineSync = inject(OfflineSyncService);
  private readonly authService = inject(AuthService);
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
    this.http.get<{ campanas: CampanaItem[] }>('http://localhost:5000/api/campanas').subscribe({
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

    this.http.post<{ mensaje_humano: string }>('http://localhost:5000/api/campanas', payload).subscribe({
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

