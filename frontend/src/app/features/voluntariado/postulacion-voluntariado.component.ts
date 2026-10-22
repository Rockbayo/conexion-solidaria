import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { OfflineSyncService } from '../../core/services/offline-sync.service';
import { AuthService } from '../../core/services/auth.service';
import { getApiBaseUrl } from '../../core/config/api.config';

interface LaborItem {
  necesidad_id: number;
  descripcion_item: string;
  tipo_codigo: string;
  horas_requeridas: number;
  horas_cubiertas: number;
  prioridad: string;
  campana_titulo: string;
  fundacion_nombre: string;
  municipio: string;
}

interface PostulacionItem {
  id: number;
  voluntario_nombre: string;
  labor_descripcion: string;
  motivacion: string;
  disponibilidad_propuesta: string;
  estado_postulacion: string;
  asignacion: {
    tarea_especifica: string;
    horas_comprometidas: number;
    estado_actividad: string;
  } | null;
}

@Component({
  selector: 'app-postulacion-voluntariado',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="sap-page-header">
      <div class="sap-page-header-inner">
        <div>
          <span class="sap-breadcrumb">Capital Humano y Trabajo Comunitario</span>
          <h1 class="sap-page-title">Gestión de Postulaciones y Asignación de Voluntariado</h1>
          <p class="sap-page-subtitle">Inscripción en actividades operativas rurales y seguimiento de órdenes de dedicación horaria.</p>
        </div>
        <a routerLink="/perfil-habilidades" class="sap-btn-secondary">
          Configurar Matriz de Competencias
        </a>
      </div>
    </div>

    <main class="sap-container">
      @if (mensajeHumano()) {
        <div class="cs-alert-human" role="status">{{ mensajeHumano() }}</div>
      }

      <div class="layout-grid">
        <section class="cs-card sap-panel" aria-label="Formulario de postulación a voluntariado">
          <div class="panel-head">
            <h2>Formulario de Inscripción en Labor</h2>
            <span class="sap-badge sap-badge-info">Asignación Automática</span>
          </div>

          <form (ngSubmit)="enviarPostulacion()" novalidate>
            <div class="form-group">
              <label for="labor_sel" class="sap-form-label">Actividad Comunitaria Requerida *</label>
              <select id="labor_sel" name="labor_sel" class="sap-input" [(ngModel)]="form.necesidad_campana_id" (ngModelChange)="guardarBorrador()">
                @for (l of labores(); track l.necesidad_id) {
                  <option [ngValue]="l.necesidad_id">
                    {{ l.municipio }} · {{ l.descripcion_item }} ({{ l.fundacion_nombre }})
                  </option>
                }
              </select>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label for="disp" class="sap-form-label">Franja Horaria Propuesta *</label>
                <input id="disp" name="disp" type="text" class="sap-input" [(ngModel)]="form.disponibilidad_propuesta" (ngModelChange)="guardarBorrador()" placeholder="Ej: Sábados de 7:00 am a 1:00 pm" required />
              </div>
              <div class="form-group">
                <label for="horas" class="sap-form-label">Horas a Comprometer *</label>
                <input id="horas" name="horas" type="number" min="2" max="80" class="sap-input" [(ngModel)]="form.horas_comprometidas" (ngModelChange)="guardarBorrador()" required />
              </div>
            </div>

            <div class="form-group">
              <label for="motiv" class="sap-form-label">Perfil de Aporte y Experiencia *</label>
              <textarea id="motiv" name="motiv" rows="3" class="sap-input" [(ngModel)]="form.motivacion" (ngModelChange)="guardarBorrador()" placeholder="Describe tu experiencia técnica o comunitaria para esta jornada..." required></textarea>
            </div>

            <button type="submit" class="cs-btn btn-full" [disabled]="enviando()">
              {{ enviando() ? 'Procesando solicitud...' : 'Confirmar Postulación' }}
            </button>
          </form>
        </section>

        <section class="cs-card sap-panel" aria-label="Órdenes de voluntariado registradas">
          <div class="panel-head">
            <h2>Órdenes de Actividad y Asignaciones</h2>
            <span class="sap-badge sap-badge-ok">Vigentes</span>
          </div>

          @if (postulaciones().length === 0) {
            <p class="empty-note">No se registran postulaciones activas. Selecciona una actividad comunitaria en el panel izquierdo.</p>
          } @else {
            <div class="post-list">
              @for (p of postulaciones(); track p.id) {
                <article class="post-card">
                  <div class="post-top">
                    <strong>{{ p.voluntario_nombre }}</strong>
                    <span class="sap-badge sap-badge-ok">{{ p.estado_postulacion }}</span>
                  </div>
                  <h3>{{ p.labor_descripcion }}</h3>
                  <p class="small"><strong>Franja horaria:</strong> {{ p.disponibilidad_propuesta }}</p>
                  <p class="small"><strong>Justificación:</strong> {{ p.motivacion }}</p>
                  @if (p.asignacion) {
                    <div class="assign-box">
                      <span><strong>Tarea Asignada:</strong> {{ p.asignacion.tarea_especifica }}</span>
                      <span><strong>Dedicación:</strong> {{ p.asignacion.horas_comprometidas }} horas · Estado: {{ p.asignacion.estado_actividad }}</span>
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
    .sap-panel { border-top: 3px solid var(--sap-brand-primary); }
    .panel-head { display: flex; justify-content: space-between; align-items: center; padding-bottom: 0.85rem; margin-bottom: 1.25rem; border-bottom: 1px solid var(--sap-border-subtle); }
    .panel-head h2 { margin: 0; font-size: 1.12rem; }
    .form-group { margin-bottom: 1rem; }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 0.9rem; }
    .btn-full { width: 100%; }
    .post-list { display: flex; flex-direction: column; gap: 0.9rem; }
    .post-card { border: 1px solid var(--sap-border-subtle); border-radius: 6px; padding: 1rem; background: var(--sap-bg-canvas); }
    .post-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; }
    .post-card h3 { margin: 0.2rem 0 0.5rem 0; font-size: 1rem; }
    .small { margin: 0.25rem 0; font-size: 0.88rem; color: var(--sap-text-secondary); }
    .assign-box { margin-top: 0.65rem; padding: 0.6rem 0.75rem; background: #FFFFFF; border-left: 3px solid var(--sap-brand-primary); border-radius: 4px; display: flex; flex-direction: column; gap: 0.2rem; font-size: 0.85rem; }
  `]
})
export class PostulacionVoluntariadoComponent implements OnInit {
  private readonly http = inject(HttpClient);
  private readonly offlineSync = inject(OfflineSyncService);
  private readonly authService = inject(AuthService);
  private readonly DRAFT_KEY = 'cu05_postulacion_voluntario';

  labores = signal<LaborItem[]>([]);
  postulaciones = signal<PostulacionItem[]>([]);
  enviando = signal(false);
  mensajeHumano = signal('');

  form = {
    necesidad_campana_id: 2,
    disponibilidad_propuesta: 'Sábados de 8:00 am a 2:00 pm',
    horas_comprometidas: 8,
    motivacion: 'Cuento con experiencia en trabajo comunitario con escuelas veredales y manejo de compostaje.',
  };

  ngOnInit(): void {
    const borrador = this.offlineSync.cargarBorradorFormulario<typeof this.form>(this.DRAFT_KEY);
    if (borrador) {
      this.form = borrador;
    }
    this.cargarDatos();
  }

  cargarDatos(): void {
    this.http.get<{ labores: LaborItem[]; postulaciones: PostulacionItem[] }>(`${getApiBaseUrl()}/voluntariado/labores`).subscribe({
      next: (res) => {
        this.labores.set(res.labores);
        this.postulaciones.set(res.postulaciones);
        if (res.labores.length > 0 && !this.form.necesidad_campana_id) {
          this.form.necesidad_campana_id = res.labores[0].necesidad_id;
        }
      },
      error: () => {},
    });
  }

  guardarBorrador(): void {
    this.offlineSync.guardarBorradorFormulario(this.DRAFT_KEY, this.form);
  }

  enviarPostulacion(): void {
    this.mensajeHumano.set('');
    this.enviando.set(true);

    const payload = {
      ...this.form,
      voluntario_id: this.authService.usuarioActual()?.voluntario_id || 1,
    };

    this.http.post<{ mensaje_humano: string }>(`${getApiBaseUrl()}/voluntariado/postular`, payload).subscribe({
      next: (res) => {
        this.enviando.set(false);
        this.mensajeHumano.set(res.mensaje_humano);
        this.offlineSync.limpiarBorradorFormulario(this.DRAFT_KEY);
        this.cargarDatos();
      },
      error: (err) => {
        this.enviando.set(false);
        this.guardarBorrador();
        if (err.status === 0) {
          this.mensajeHumano.set(
            'Tu conexión parece inestable. Hemos guardado tu postulación de voluntariado para enviarla en cuanto recuperes la señal.'
          );
        } else {
          this.mensajeHumano.set(err.error?.mensaje_humano || 'No se pudo procesar tu postulación.');
        }
      },
    });
  }
}
