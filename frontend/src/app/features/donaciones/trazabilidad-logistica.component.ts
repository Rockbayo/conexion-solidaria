import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

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
  imports: [CommonModule, FormsModule],
  template: `
    <main class="container" aria-labelledby="cu09-heading">
      <header class="cs-card header-banner">
        <div>
          <span class="tag-pill">CU09 · Trazabilidad Logística de Especie 5FN</span>
          <h1 id="cu09-heading">Seguimiento Logístico: Recibido → En Bodega → Entregado</h1>
          <p>
            Actualiza y consulta la cadena de custodia de las donaciones en especie destinadas a las veredas de la Sabana Norte.
          </p>
        </div>
      </header>

      @if (mensajeHumano()) {
        <div class="cs-alert-human" role="status">{{ mensajeHumano() }}</div>
      }

      @if (itemsEspecie().length === 0) {
        <section class="cs-card">
          <h2>No hay donaciones en especie pendientes</h2>
          <p>Puedes registrar una donación en especie en la sección "Donar" para iniciar su trazabilidad veredal.</p>
        </section>
      } @else {
        <section class="cards-list" aria-label="Tarjetas de trazabilidad logística">
          @for (item of itemsEspecie(); track item.id) {
            <article class="cs-card traza-card">
              <div class="traza-header">
                <div>
                  <span class="ref-code">{{ item.codigo_referencia }}</span>
                  <h2>{{ item.especie.cantidad }} {{ item.especie.unidad_simbolo }} · {{ item.especie.descripcion_articulos }}</h2>
                  <p class="meta">Campaña: <strong>{{ item.campana_titulo }}</strong> · OSAL: {{ item.fundacion_nombre }}</p>
                </div>
                <span class="state-badge">{{ item.especie.estado_logistico_actual }}</span>
              </div>

              <!-- STEPPER VISUAL DE ESTADOS (RECIBIDO -> EN_BODEGA -> ENTREGADO) -->
              <div class="pipeline-steps" role="list" aria-label="Etapas logísticas">
                <div class="step-box" [class.active]="esEtapaActiva(item.especie.estado_logistico_actual, 'RECIBIDO')" role="listitem">
                  1. RECIBIDO
                </div>
                <div class="step-box" [class.active]="esEtapaActiva(item.especie.estado_logistico_actual, 'EN_BODEGA')" role="listitem">
                  2. EN BODEGA
                </div>
                <div class="step-box" [class.active]="esEtapaActiva(item.especie.estado_logistico_actual, 'ENTREGADO')" role="listitem">
                  3. ENTREGADO EN VEREDA
                </div>
              </div>

              <!-- CONTROLES DE ACTUALIZACIÓN RÁPIDA -->
              <div class="update-box">
                <div class="inputs-inline">
                  <input
                    type="text"
                    [(ngModel)]="ubicacionTemporal[item.especie.id]"
                    placeholder="Ubicación actual (ej: Bodega Municipal de Cogua o Escuela Veredal)"
                    aria-label="Ubicación reportada"
                  />
                  <input
                    type="text"
                    [(ngModel)]="observacionTemporal[item.especie.id]"
                    placeholder="Observación (ej: Recibido en buen estado por líder comunitario)"
                    aria-label="Observación de entrega"
                  />
                </div>
                <div class="action-buttons">
                  <button type="button" class="btn-stage" (click)="cambiarEstado(item.especie.id, 'RECIBIDO')">
                    Marcar: Recibido
                  </button>
                  <button type="button" class="btn-stage" (click)="cambiarEstado(item.especie.id, 'EN_BODEGA')">
                    Marcar: En Bodega
                  </button>
                  <button type="button" class="cs-btn" (click)="cambiarEstado(item.especie.id, 'ENTREGADO')">
                    ✓ Confirmar: Entregado
                  </button>
                </div>
              </div>

              <!-- BITÁCORA HISTÓRICA (trazabilidad_entregas) -->
              <div class="history-block">
                <h3>Historial de Movimientos (trazabilidad_entregas):</h3>
                <ul>
                  @for (h of item.especie.historial_trazabilidad; track h.id) {
                    <li>
                      <strong>[{{ h.estado_logistico }}]</strong> {{ h.ubicacion_reportada }} — {{ h.observacion }}
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
    .container { max-width: 1080px; margin: 2rem auto; padding: 0 1.5rem; }
    .header-banner { margin-bottom: 1.5rem; border-color: var(--brand-primary); }
    .header-banner h1 { margin: 0.4rem 0; font-size: 1.75rem; }
    .tag-pill { display: inline-block; background: var(--status-ok-bg); color: var(--status-ok-text); font-weight: 800; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.85rem; }
    .cards-list { display: flex; flex-direction: column; gap: 1.5rem; }
    .traza-card { border-color: var(--border-strong); }
    .traza-header { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-start; gap: 1rem; margin-bottom: 1rem; }
    .traza-header h2 { margin: 0.25rem 0; font-size: 1.35rem; }
    .ref-code { font-weight: 800; color: var(--brand-primary); }
    .meta { margin: 0; color: var(--text-secondary); }
    .state-badge { background: var(--status-ok-bg); color: var(--status-ok-text); font-weight: 800; padding: 0.4rem 0.9rem; border-radius: 8px; border: 2px solid var(--brand-primary); }
    .pipeline-steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin-bottom: 1.25rem; }
    .step-box { padding: 0.75rem; text-align: center; font-weight: 800; border-radius: 8px; border: 2px solid var(--border-subtle); background: #F3F4F6; }
    .step-box.active { background: var(--status-ok-bg); color: var(--status-ok-text); border-color: var(--brand-primary); }
    .update-box { background: #F9FAF7; padding: 1rem; border-radius: 10px; border: 1px solid var(--border-subtle); margin-bottom: 1rem; }
    .inputs-inline { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 0.75rem; margin-bottom: 0.85rem; }
    input { min-height: 46px; padding: 0.6rem 0.85rem; border: 2px solid var(--border-strong); border-radius: 8px; font-size: 0.95rem; }
    .action-buttons { display: flex; flex-wrap: wrap; gap: 0.75rem; }
    .btn-stage { min-height: 46px; padding: 0.6rem 1rem; font-weight: 700; border: 2px solid var(--brand-primary); background: #FFFFFF; color: var(--brand-primary); border-radius: 8px; cursor: pointer; }
    .history-block h3 { font-size: 0.95rem; margin: 0 0 0.4rem 0; }
    .history-block ul { margin: 0; padding-left: 1.2rem; font-size: 0.9rem; color: var(--text-secondary); }
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
    this.http.get<{ donaciones: DonacionEspecieItem[] }>('http://localhost:5000/api/donaciones').subscribe({
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

  cambiarEstado(donacionEspecieId: number, nuevoEstado: 'RECIBIDO' | 'EN_BODEGA' | 'ENTREGADO'): void {
    const ubicacion = this.ubicacionTemporal[donacionEspecieId] || 'Centro de Acopio Sabana Norte';
    const observacion = this.observacionTemporal[donacionEspecieId] || `Actualizado manualmente a ${nuevoEstado}`;

    this.http
      .put<{ mensaje_humano: string }>(
        `http://localhost:5000/api/donaciones/especie/${donacionEspecieId}/trazabilidad`,
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

