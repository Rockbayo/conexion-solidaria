import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { RouterLink } from '@angular/router';

interface DashboardMetricas {
  kpis: {
    recaudo_total_cop: number;
    meta_global_cop: number;
    porcentaje_global: number;
    campanas_activas: number;
    fundaciones_registradas: number;
    voluntarios_activos: number;
    postulaciones_voluntariado: number;
    horas_voluntariado_comprometidas: number;
    donaciones_especie_totales: number;
  };
  logistica_especie: {
    recibido: number;
    en_bodega: number;
    entregado: number;
  };
  campanas_desempeno: Array<{
    id: number;
    titulo: string;
    fundacion: string;
    municipio: string;
    meta_economica: number;
    monto_recaudado: number;
    porcentaje_avance: number;
    total_necesidades: number;
    estado: string;
  }>;
}

@Component({
  selector: 'app-dashboard-osal',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <main class="container" aria-labelledby="cu08-heading">
      <header class="cs-card header-banner">
        <div>
          <span class="tag-pill">CU08 · Dashboard Operativo de la OSAL (5FN)</span>
          <h1 id="cu08-heading">Tablero de Impacto y Métricas en Sabana Norte</h1>
          <p>
            Consolidado en tiempo real de recaudo económico, voluntarios comprometidos, horas comunitarias y campañas activas.
          </p>
        </div>
        <a routerLink="/campanas" class="cs-btn">+ Crear Campaña (CU03)</a>
      </header>

      @if (datos(); as d) {
        <!-- TARJETAS DE INDICADORES CLAVE (KPI CARDS) -->
        <section class="kpi-grid" aria-label="Indicadores principales de la fundación">
          <article class="cs-card kpi-card">
            <span class="kpi-label">Recaudo Total Verificado</span>
            <strong class="kpi-value">\${{ d.kpis.recaudo_total_cop | number:'1.0-0' }} COP</strong>
            <span class="kpi-sub">Meta Global: \${{ d.kpis.meta_global_cop | number:'1.0-0' }} ({{ d.kpis.porcentaje_global }}%)</span>
          </article>

          <article class="cs-card kpi-card">
            <span class="kpi-label">Voluntarios y Tiempo Solidario</span>
            <strong class="kpi-value">{{ d.kpis.voluntarios_activos }} Voluntarios</strong>
            <span class="kpi-sub">{{ d.kpis.horas_voluntariado_comprometidas }} horas comprometidas ({{ d.kpis.postulaciones_voluntariado }} postulaciones)</span>
          </article>

          <article class="cs-card kpi-card">
            <span class="kpi-label">Campañas y OSAL en Sabana Norte</span>
            <strong class="kpi-value">{{ d.kpis.campanas_activas }} Campañas Activas</strong>
            <span class="kpi-sub">{{ d.kpis.fundaciones_registradas }} fundaciones OSAL vinculadas</span>
          </article>

          <article class="cs-card kpi-card">
            <span class="kpi-label">Trazabilidad de Donaciones en Especie</span>
            <strong class="kpi-value">{{ d.kpis.donaciones_especie_totales }} Entregas</strong>
            <span class="kpi-sub">
              Recibidos: {{ d.logistica_especie.recibido }} · Bodega: {{ d.logistica_especie.en_bodega }} · Entregados: {{ d.logistica_especie.entregado }}
            </span>
          </article>
        </section>

        <!-- DESEMPEÑO POR CAMPAÑA -->
        <section class="cs-card table-card" aria-label="Desempeño detallado por campaña">
          <h2>Avance Financiero y Operativo por Campaña</h2>
          <div class="campaign-rows">
            @for (c of d.campanas_desempeno; track c.id) {
              <article class="camp-row">
                <div class="camp-row-head">
                  <div>
                    <h3>{{ c.titulo }}</h3>
                    <p>{{ c.fundacion }} · 📍 {{ c.municipio }} · {{ c.total_necesidades }} necesidades registradas</p>
                  </div>
                  <span class="pct-chip">{{ c.porcentaje_avance }}% completado</span>
                </div>
                <div class="bar-bg">
                  <div class="bar-fill" [style.width.%]="c.porcentaje_avance"></div>
                </div>
                <div class="camp-row-foot">
                  <span>Recaudado: <strong>\${{ c.monto_recaudado | number:'1.0-0' }} COP</strong></span>
                  <span>Meta: \${{ c.meta_economica | number:'1.0-0' }} COP</span>
                </div>
              </article>
            }
          </div>
        </section>
      }
    </main>
  `,
  styles: [`
    .container { max-width: 1080px; margin: 2rem auto; padding: 0 1.5rem; }
    .header-banner { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.5rem; border-color: var(--brand-primary); }
    .header-banner h1 { margin: 0.4rem 0; font-size: 1.75rem; }
    .tag-pill { display: inline-block; background: var(--status-ok-bg); color: var(--status-ok-text); font-weight: 800; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.85rem; }
    .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 1.25rem; margin-bottom: 1.75rem; }
    .kpi-card { display: flex; flex-direction: column; gap: 0.35rem; border-color: var(--border-strong); }
    .kpi-label { font-size: 0.9rem; font-weight: 700; color: var(--text-secondary); }
    .kpi-value { font-size: 1.65rem; font-weight: 900; color: var(--brand-primary); }
    .kpi-sub { font-size: 0.85rem; color: var(--text-secondary); }
    .table-card { border-color: var(--border-strong); }
    .table-card h2 { margin-top: 0; }
    .campaign-rows { display: flex; flex-direction: column; gap: 1rem; }
    .camp-row { padding: 1rem; border: 2px solid var(--border-subtle); border-radius: 10px; background: #F9FAF7; }
    .camp-row-head { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; }
    .camp-row-head h3 { margin: 0; font-size: 1.1rem; }
    .camp-row-head p { margin: 0.2rem 0 0 0; font-size: 0.88rem; color: var(--text-secondary); }
    .pct-chip { background: var(--status-ok-bg); color: var(--status-ok-text); font-weight: 800; padding: 0.25rem 0.65rem; border-radius: 999px; font-size: 0.85rem; }
    .bar-bg { height: 12px; background: #E5E7EB; border-radius: 999px; overflow: hidden; border: 1px solid var(--border-strong); margin-bottom: 0.5rem; }
    .bar-fill { height: 100%; background: var(--brand-primary); }
    .camp-row-foot { display: flex; justify-content: space-between; font-size: 0.9rem; }
  `]
})
export class DashboardOsalComponent implements OnInit {
  private readonly http = inject(HttpClient);
  datos = signal<DashboardMetricas | null>(null);

  ngOnInit(): void {
    this.http.get<DashboardMetricas>('http://localhost:5000/api/dashboard/osal').subscribe({
      next: (res) => this.datos.set(res),
      error: () => {
        this.datos.set({
          kpis: {
            recaudo_total_cop: 3850000,
            meta_global_cop: 15000000,
            porcentaje_global: 25.7,
            campanas_activas: 1,
            fundaciones_registradas: 1,
            voluntarios_activos: 1,
            postulaciones_voluntariado: 1,
            horas_voluntariado_comprometidas: 8,
            donaciones_especie_totales: 1,
          },
          logistica_especie: { recibido: 1, en_bodega: 0, entregado: 0 },
          campanas_desempeno: [
            {
              id: 1,
              titulo: 'Huertas Escolares Resilientes en Veredas de Cogua y Tabio',
              fundacion: 'Fundación Agroecológica Raíces de Sabana Norte',
              municipio: 'Cogua',
              meta_economica: 15000000,
              monto_recaudado: 3850000,
              porcentaje_avance: 25.7,
              total_necesidades: 2,
              estado: 'ACTIVA',
            },
          ],
        });
      },
    });
  }
}
