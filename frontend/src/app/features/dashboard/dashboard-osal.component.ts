import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { getApiBaseUrl } from '../../core/config/api.config';

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
  voluntarios_postulados?: Array<{
    postulacion_id: number;
    voluntario_nombre: string;
    telefono: string;
    correo: string;
    habilidades: string[];
    labor_descripcion: string;
    campana_titulo: string;
    disponibilidad_propuesta: string;
    horas_comprometidas: number;
    estado_postulacion: string;
  }>;
}

@Component({
  selector: 'app-dashboard-osal',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="sap-page-header">
      <div class="sap-page-header-inner">
        <div>
          <span class="sap-breadcrumb">Analítica e Inteligencia Operativa</span>
          <h1 class="sap-page-title">Tablero de Control e Indicadores de Gestión OSAL</h1>
          <p class="sap-page-subtitle">Consolidado financiero, ejecución de campañas, equipo de voluntariado postulado y cadena de suministro rural.</p>
        </div>
        <div class="header-actions">
          <a routerLink="/trazabilidad" class="sap-btn-secondary">Logística en Especie</a>
          <a routerLink="/campanas" class="cs-btn">+ Publicar Nueva Campaña</a>
        </div>
      </div>
    </div>

    <main class="sap-container">
      @if (datos(); as d) {
        <section class="kpi-grid" aria-label="Indicadores ejecutivos de gestión">
          <article class="cs-card kpi-card">
            <div class="kpi-top">
              <span class="kpi-label">Ejecución de Recaudo Monetario</span>
              <span class="sap-badge sap-badge-info">COP</span>
            </div>
            <strong class="kpi-value">\${{ d.kpis.recaudo_total_cop | number:'1.0-0' }}</strong>
            <span class="kpi-sub">Presupuesto Meta: \${{ d.kpis.meta_global_cop | number:'1.0-0' }} ({{ d.kpis.porcentaje_global }}%)</span>
          </article>

          <article class="cs-card kpi-card">
            <div class="kpi-top">
              <span class="kpi-label">Capacidad de Voluntariado</span>
              <span class="sap-badge sap-badge-ok">Activo</span>
            </div>
            <strong class="kpi-value">{{ d.kpis.horas_voluntariado_comprometidas }} Horas</strong>
            <span class="kpi-sub">{{ d.kpis.voluntarios_activos }} voluntarios · {{ d.kpis.postulaciones_voluntariado }} asignaciones</span>
          </article>

          <article class="cs-card kpi-card">
            <div class="kpi-top">
              <span class="kpi-label">Cobertura de Programas</span>
              <span class="sap-badge sap-badge-info">Sabana Norte</span>
            </div>
            <strong class="kpi-value">{{ d.kpis.campanas_activas }} Campañas</strong>
            <span class="kpi-sub">{{ d.kpis.fundaciones_registradas }} organización(es) activa(s)</span>
          </article>

          <article class="cs-card kpi-card">
            <div class="kpi-top">
              <span class="kpi-label">Operaciones en Especie</span>
              <span class="sap-badge sap-badge-ok">Logística</span>
            </div>
            <strong class="kpi-value">{{ d.kpis.donaciones_especie_totales }} Despachos</strong>
            <span class="kpi-sub">
              Recibidos: {{ d.logistica_especie.recibido }} · Bodega: {{ d.logistica_especie.en_bodega }} · Entregados: {{ d.logistica_especie.entregado }}
            </span>
          </article>
        </section>

        <section class="cs-card table-card" aria-label="Estado de ejecución por programa">
          <div class="table-head">
            <h2>Detalle de Ejecución Presupuestal por Campaña</h2>
            <span class="sap-badge sap-badge-info">{{ d.campanas_desempeno.length }} Registros</span>
          </div>

          <div class="campaign-rows">
            @for (c of d.campanas_desempeno; track c.id) {
              <article class="camp-row">
                <div class="camp-row-head">
                  <div>
                    <h3>{{ c.titulo }}</h3>
                    <p>{{ c.fundacion }} · Jurisdicción: {{ c.municipio }} · {{ c.total_necesidades }} requerimientos</p>
                  </div>
                  <span class="sap-badge sap-badge-ok">{{ c.porcentaje_avance }}% Ejecutado</span>
                </div>
                <div class="bar-bg">
                  <div class="bar-fill" [style.width.%]="c.porcentaje_avance"></div>
                </div>
                <div class="camp-row-foot">
                  <span>Recaudo Verificado: <strong>\${{ c.monto_recaudado | number:'1.0-0' }} COP</strong></span>
                  <span>Meta Presupuestal: \${{ c.meta_economica | number:'1.0-0' }} COP</span>
                </div>
              </article>
            }
          </div>
        </section>

        <!-- SECCIÓN EXCLUSIVA PARA OSAL / ADMIN: VOLUNTARIOS POSTULADOS A SUS CAMPAÑAS -->
        <section class="cs-card table-card" style="margin-top: 1.5rem;" aria-label="Voluntarios asignados a la fundación">
          <div class="table-head">
            <div>
              <h2>Directorio de Voluntarios Postulados a Nuestras Causas</h2>
              <p class="sub-head">Información de contacto, habilidades certificadas y horarios comprometidos por cada voluntario.</p>
            </div>
            <span class="sap-badge sap-badge-ok">{{ (d.voluntarios_postulados || []).length }} Postulación(es)</span>
          </div>

          @if (!d.voluntarios_postulados || d.voluntarios_postulados.length === 0) {
            <p class="empty-note">Aún no se registran postulaciones de voluntarios en las campañas de esta organización.</p>
          } @else {
            <div class="campaign-rows">
              @for (v of d.voluntarios_postulados; track v.postulacion_id) {
                <article class="camp-row">
                  <div class="camp-row-head">
                    <div>
                      <h3>{{ v.voluntario_nombre }}</h3>
                      <p>📞 Teléfono: <strong>{{ v.telefono }}</strong> · ✉️ Correo: {{ v.correo || 'Registrado' }}</p>
                    </div>
                    <span class="sap-badge sap-badge-ok">{{ v.horas_comprometidas }} Horas Comprometidas ({{ v.estado_postulacion }})</span>
                  </div>
                  <p class="vol-detail">
                    <strong>Actividad asignada:</strong> {{ v.labor_descripcion }} ({{ v.campana_titulo }})<br/>
                    <strong>Franja horaria disponible:</strong> {{ v.disponibilidad_propuesta }}
                  </p>
                  @if (v.habilidades && v.habilidades.length > 0) {
                    <div class="skills-row">
                      @for (hab of v.habilidades; track hab) {
                        <span class="skill-chip">🌱 {{ hab }}</span>
                      }
                    </div>
                  }
                </article>
              }
            </div>
          }
        </section>
      }
    </main>
  `,
  styles: [`
    .header-actions { display: flex; flex-wrap: wrap; gap: 0.65rem; align-items: center; }
    .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.25rem; margin-bottom: 1.75rem; }
    .kpi-card { display: flex; flex-direction: column; gap: 0.45rem; border-top: 3px solid var(--sap-brand-primary); }
    .kpi-top { display: flex; justify-content: space-between; align-items: center; }
    .kpi-label { font-size: 0.84rem; font-weight: 700; color: var(--sap-text-secondary); }
    .kpi-value { font-size: 1.6rem; font-weight: 800; color: var(--sap-text-primary); }
    .kpi-sub { font-size: 0.82rem; color: var(--sap-text-secondary); }
    .table-card { border-top: 3px solid var(--sap-brand-primary); }
    .table-head { display: flex; justify-content: space-between; align-items: center; padding-bottom: 0.85rem; margin-bottom: 1.15rem; border-bottom: 1px solid var(--sap-border-subtle); }
    .table-head h2 { margin: 0; font-size: 1.12rem; }
    .sub-head { margin: 0.2rem 0 0 0; font-size: 0.85rem; color: var(--sap-text-secondary); }
    .campaign-rows { display: flex; flex-direction: column; gap: 0.9rem; }
    .camp-row { padding: 1rem; border: 1px solid var(--sap-border-subtle); border-radius: 6px; background: var(--sap-bg-canvas); }
    .camp-row-head { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.5rem; margin-bottom: 0.6rem; }
    .camp-row-head h3 { margin: 0; font-size: 1.02rem; }
    .camp-row-head p { margin: 0.2rem 0 0 0; font-size: 0.84rem; color: var(--sap-text-secondary); }
    .bar-bg { height: 8px; background: #CBD5E1; border-radius: 999px; overflow: hidden; margin-bottom: 0.5rem; }
    .bar-fill { height: 100%; background: var(--sap-brand-primary); }
    .camp-row-foot { display: flex; justify-content: space-between; font-size: 0.86rem; }
    .vol-detail { margin: 0.35rem 0; font-size: 0.88rem; color: var(--sap-text-primary); line-height: 1.45; }
    .skills-row { display: flex; flex-wrap: wrap; gap: 0.45rem; margin-top: 0.5rem; }
    .skill-chip { font-size: 0.78rem; font-weight: 600; padding: 0.2rem 0.6rem; background: #E8F1FF; color: var(--sap-brand-primary); border-radius: 999px; }
  `]
})
export class DashboardOsalComponent implements OnInit {
  private readonly http = inject(HttpClient);
  datos = signal<DashboardMetricas | null>(null);

  ngOnInit(): void {
    this.http.get<DashboardMetricas>(`${getApiBaseUrl()}/dashboard/osal`).subscribe({
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
          logistica_especie: {
            recibido: 1,
            en_bodega: 0,
            entregado: 0,
          },
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
          voluntarios_postulados: [],
        });
      },
    });
  }
}
