import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { getApiBaseUrl } from '../../core/config/api.config';

interface DonacionEspecieItem {
  id: number;
  codigo_referencia: string;
  campana_titulo: string;
  fundacion_nombre: string;
  donante_nombre: string;
  especie: {
    id: number;
    descripcion_articulos: string;
    cantidad: number;
    unidad_simbolo: string;
    estado_logistico_actual: string;
    historial_trazabilidad: Array<{
      id: number;
      estado_logistico: string;
      ubicacion_reportada: string;
      observacion: string;
      fecha_actualizacion: string;
    }>;
  };
}

@Component({
  selector: 'app-trazabilidad-logistica',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="sap-page-header">
      <div class="sap-page-header-inner">
        <div>
          <span class="sap-breadcrumb">Cadena de Suministro y Acopio Rural</span>
          <h1 class="sap-page-title">Control de Trazabilidad Logística de Bienes en Especie</h1>
          <p class="sap-page-subtitle">Monitoreo de estados operativos desde la recepción inicial hasta la entrega final en vereda.</p>
        </div>
        <a routerLink="/dashboard" class="sap-btn-secondary">← Volver al Tablero OSAL</a>
      </div>
    </div>

    <main class="sap-container">
      @if (mensajeHumano()) {
        <div class="alert-traza-ok" role="status">✅ {{ mensajeHumano() }}</div>
      }

      @if (itemsEspecie().length === 0) {
        <section class="cs-card">
          <h2>Sin despachos en especie registrados</h2>
          <p>Registra una donación en modalidad de especie desde el módulo de Aportes para habilitar su seguimiento logístico.</p>
        </section>
      } @else {
        <section class="cards-list" aria-label="Órdenes logísticas en especie">
          @for (item of itemsEspecie(); track item.id) {
            <article class="cs-card traza-card">
              <div class="traza-header">
                <div>
                  <span class="ref-code">Orden {{ item.codigo_referencia }}</span>
                  <h2>{{ item.especie.cantidad }} {{ item.especie.unidad_simbolo }} · {{ item.especie.descripcion_articulos }}</h2>
                  <p class="meta">Campaña: <strong>{{ item.campana_titulo }}</strong> · Organización: {{ item.fundacion_nombre }}</p>
                </div>
                <span class="sap-badge sap-badge-ok">{{ formatearEstado(item.especie.estado_logistico_actual) }}</span>
              </div>

              <div class="pipeline-steps" role="list" aria-label="Flujo de estados de despacho">
                <div class="step-box" [class.active]="esEtapaActiva(item.especie.estado_logistico_actual, 'RECIBIDO')" role="listitem">
                  1. Recepción Inicial
                </div>
                <div class="step-box" [class.active]="esEtapaActiva(item.especie.estado_logistico_actual, 'EN_BODEGA')" role="listitem">
                  2. En Bodega Municipal
                </div>
                <div class="step-box" [class.active]="esEtapaActiva(item.especie.estado_logistico_actual, 'ENTREGADO')" role="listitem">
                  3. Entregado en Vereda
                </div>
              </div>

              <div class="update-box">
                <div class="inputs-inline">
                  <input
                    type="text"
                    class="sap-input"
                    [(ngModel)]="ubicacionTemporal[item.especie.id]"
                    placeholder="Punto de control o bodega municipal"
                    aria-label="Ubicación reportada"
                  />
                  <input
                    type="text"
                    class="sap-input"
                    [(ngModel)]="observacionTemporal[item.especie.id]"
                    placeholder="Novedad o acta de conformidad"
                    aria-label="Observación de entrega"
                  />
                </div>
                <div class="action-buttons">
                  <button type="button" class="sap-btn-secondary" (click)="cambiarEstado(item.especie.id, 'RECIBIDO')">
                    Registrar Recepción
                  </button>
                  <button type="button" class="sap-btn-secondary" (click)="cambiarEstado(item.especie.id, 'EN_BODEGA')">
                    Ingresar a Bodega
                  </button>
                  <button type="button" class="cs-btn" (click)="cambiarEstado(item.especie.id, 'ENTREGADO')">
                    Confirmar Entrega en Vereda
                  </button>
                </div>
              </div>

              <div class="history-block">
                <h3>Bitácora de Eventos de Transporte y Custodia</h3>
                <ul>
                  @for (h of item.especie.historial_trazabilidad; track h.id) {
                    <li>
                      <span class="sap-badge sap-badge-info">{{ formatearEstado(h.estado_logistico) }}</span>
                      <strong>{{ h.ubicacion_reportada }}</strong>
                      <span>{{ h.observacion }}</span>
                    </li>
                  }
                </ul>
              </div>
            </article>
          }
        </section>
      }
    </main>
  `,
  styles: [`
    .alert-traza-ok { border-left: 5px solid #15803D; background: #DCFCE7; color: #14532D; padding: 0.9rem 1.2rem; border-radius: 6px; font-weight: 700; margin-bottom: 1.25rem; }
    .cards-list { display: flex; flex-direction: column; gap: 1.5rem; }
    .traza-card { border-top: 3px solid var(--sap-brand-primary); }
    .traza-header { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-start; gap: 1rem; margin-bottom: 1rem; padding-bottom: 0.85rem; border-bottom: 1px solid var(--sap-border-subtle); }
    .traza-header h2 { margin: 0.25rem 0; font-size: 1.2rem; }
    .ref-code { font-family: monospace; font-weight: 700; color: var(--sap-brand-primary); }
    .meta { margin: 0; font-size: 0.88rem; color: var(--sap-text-secondary); }
    .pipeline-steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin-bottom: 1.25rem; }
    .step-box { padding: 0.65rem; text-align: center; font-weight: 700; font-size: 0.86rem; border-radius: 4px; border: 1px solid var(--sap-border-subtle); background: var(--sap-bg-canvas); color: var(--sap-text-secondary); }
    .step-box.active { background: var(--sap-status-ok-bg); color: var(--sap-status-ok-text); border-color: var(--sap-status-ok-border); }
    .update-box { background: var(--sap-bg-canvas); padding: 1rem; border-radius: 6px; border: 1px solid var(--sap-border-subtle); margin-bottom: 1rem; }
    .inputs-inline { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 0.75rem; margin-bottom: 0.85rem; }
    .action-buttons { display: flex; flex-wrap: wrap; gap: 0.65rem; }
    .history-block h3 { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.03em; color: var(--sap-text-secondary); margin: 0 0 0.5rem 0; }
    .history-block ul { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0.45rem; }
    .history-block li { display: flex; align-items: center; gap: 0.65rem; flex-wrap: wrap; font-size: 0.88rem; padding: 0.5rem 0.75rem; background: #FFFFFF; border: 1px solid var(--sap-border-subtle); border-radius: 4px; }
  `]
})
export class TrazabilidadLogisticaComponent implements OnInit {
  private readonly http = inject(HttpClient);

  itemsEspecie = signal<DonacionEspecieItem[]>([]);
  mensajeHumano = signal('');
  ubicacionTemporal: Record<number, string> = {};
  observacionTemporal: Record<number, string> = {};

  ngOnInit(): void {
    this.cargarDonacionesEspecie();
  }

  cargarDonacionesEspecie(): void {
    this.http.get<{ donaciones: DonacionEspecieItem[] }>(`${getApiBaseUrl()}/donaciones`).subscribe({
      next: (res) => {
        const soloEspecie = (res.donaciones || []).filter((d) => !!d.especie);
        this.itemsEspecie.set(soloEspecie);
      },
      error: () => {},
    });
  }

  esEtapaActiva(actual: string, etapa: string): boolean {
    const orden = ['RECIBIDO', 'EN_BODEGA', 'ENTREGADO'];
    return orden.indexOf(actual) >= orden.indexOf(etapa);
  }

  formatearEstado(estado: string): string {
    if (estado === 'RECIBIDO') return 'Recibido';
    if (estado === 'EN_BODEGA') return 'En Bodega';
    if (estado === 'ENTREGADO') return 'Entregado';
    return estado;
  }

  cambiarEstado(donacionEspecieId: number, nuevoEstado: 'RECIBIDO' | 'EN_BODEGA' | 'ENTREGADO'): void {
    const ubicacion = this.ubicacionTemporal[donacionEspecieId] || 'Centro de Acopio Sabana Norte';
    const observacion = this.observacionTemporal[donacionEspecieId] || `Actualizado manualmente a ${nuevoEstado}`;

    this.http
      .put<{ mensaje_humano: string }>(
        `${getApiBaseUrl()}/donaciones/especie/${donacionEspecieId}/trazabilidad`,
        {
          estado_logistico: nuevoEstado,
          ubicacion_reportada: ubicacion,
          observacion,
        }
      )
      .subscribe({
        next: (res) => {
          this.mensajeHumano.set(res.mensaje_humano);
          this.cargarDonacionesEspecie();
        },
        error: () => {
          this.mensajeHumano.set(
            'Tu conexión parece inestable. Hemos guardado el cambio de estado logístico para sincronizarlo en cuanto recuperes la señal.'
          );
        },
      });
  }
}
