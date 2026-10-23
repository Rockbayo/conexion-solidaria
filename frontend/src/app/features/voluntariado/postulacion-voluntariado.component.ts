import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { OfflineSyncService, CatalogosGenerales } from '../../core/services/offline-sync.service';
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
  campana_titulo?: string;
  fundacion_nombre?: string;
  motivacion: string;
  disponibilidad_propuesta: string;
  estado_postulacion: string;
  asignacion: {
    tarea_especifica: string;
    horas_comprometidas: number;
    estado_actividad: string;
  } | null;
}

interface ResumenDisponibilidad {
  disponibilidad_horas_semana: number;
  horas_comprometidas: number;
  horas_disponibles_restantes: number;
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
          <h1 class="sap-page-title">Inscripción de Voluntariado Comunitario</h1>
          <p class="sap-page-subtitle">Postúlate a las actividades comunitarias en las veredas según tu disponibilidad semanal registrada.</p>
        </div>
        <div class="header-actions">
          <a routerLink="/perfil-habilidades" class="sap-btn-secondary">
            Configurar Mis Competencias
          </a>
          <a routerLink="/panel" class="cs-btn">
            Finalizar y Volver a Mi Resumen
          </a>
        </div>
      </div>
    </div>

    <main class="sap-container">
      <!-- Barra informativa de cupo horario del voluntario -->
      <section class="capacity-strip" aria-label="Tu disponibilidad semanal registrada">
        <div class="cap-item">
          <span class="cap-label">Horas Semanales Registradas</span>
          <strong>{{ resumenDisp().disponibilidad_horas_semana }} horas / semana</strong>
        </div>
        <div class="cap-item">
          <span class="cap-label">Horas Ya Comprometidas</span>
          <strong>{{ resumenDisp().horas_comprometidas }} horas</strong>
        </div>
        <div class="cap-item highlight">
          <span class="cap-label">Cupo Disponible para Postular</span>
          <strong>{{ resumenDisp().horas_disponibles_restantes }} horas libres</strong>
        </div>
      </section>

      @if (mensajeExito()) {
        <div class="alert-success" role="status">
          ✅ {{ mensajeExito() }}
        </div>
      }

      @if (mensajeError()) {
        <div class="alert-error" role="alert">
          ⚠️ {{ mensajeError() }}
        </div>
      }

      @if (mensajeOffline()) {
        <div class="cs-alert-human" role="status">{{ mensajeOffline() }}</div>
      }

      <div class="layout-grid">
        <section class="cs-card sap-panel" aria-label="Formulario de postulación a voluntariado">
          <div class="panel-head">
            <h2>Formulario de Inscripción en Labor</h2>
            <span class="sap-badge sap-badge-info">Asignación Inmediata</span>
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

            <div class="form-group">
              <label for="franja_sel" class="sap-form-label">Franja Horaria Propuesta *</label>
              <select id="franja_sel" name="franja_sel" class="sap-input" [(ngModel)]="form.disponibilidad_propuesta" (ngModelChange)="guardarBorrador()" required>
                @for (fh of catalogos()?.franjas_horarias || []; track fh.id) {
                  <option [value]="fh.nombre">{{ fh.nombre }}</option>
                }
              </select>
            </div>

            <div class="form-group">
              <label for="horas" class="sap-form-label">
                Horas a Comprometer (Máximo disponible: {{ resumenDisp().horas_disponibles_restantes }} h) *
              </label>
              <input
                id="horas"
                name="horas"
                type="number"
                min="1"
                [max]="resumenDisp().horas_disponibles_restantes || resumenDisp().disponibilidad_horas_semana"
                class="sap-input"
                [(ngModel)]="form.horas_comprometidas"
                (ngModelChange)="guardarBorrador()"
                required
              />
              <small class="field-hint">
                No puede superar las {{ resumenDisp().disponibilidad_horas_semana }} horas semanales que definiste en tu inscripción ({{ resumenDisp().horas_disponibles_restantes }} h disponibles actualmente).
              </small>
            </div>

            <div class="form-group">
              <label for="motiv" class="sap-form-label">Perfil de Aporte y Experiencia *</label>
              <textarea id="motiv" name="motiv" rows="3" class="sap-input" [(ngModel)]="form.motivacion" (ngModelChange)="guardarBorrador()" placeholder="Describe tu experiencia técnica o comunitaria para apoyar esta jornada..." required></textarea>
            </div>

            <div class="form-actions-row">
              <button type="submit" class="cs-btn btn-full" [disabled]="enviando()">
                {{ enviando() ? 'Procesando solicitud...' : 'Confirmar Postulación' }}
              </button>
              <a routerLink="/panel" class="sap-btn-secondary btn-full">
                Finalizar e Ir a Mi Resumen
              </a>
            </div>
          </form>
        </section>

        <section class="cs-card sap-panel" aria-label="Mis postulaciones registradas">
          <div class="panel-head">
            <h2>Mis Postulaciones y Tareas Asignadas</h2>
            <span class="sap-badge sap-badge-ok">{{ postulaciones().length }} Activa(s)</span>
          </div>

          @if (postulaciones().length === 0) {
            <p class="empty-note">Aún no tienes postulaciones activas en tu cuenta. Selecciona una actividad comunitaria en el formulario izquierdo para inscribirte.</p>
          } @else {
            <div class="post-list">
              @for (p of postulaciones(); track p.id) {
                <article class="post-card">
                  <div class="post-top">
                    <strong>{{ p.fundacion_nombre || 'Fundación Sabana Norte' }}</strong>
                    <span class="sap-badge sap-badge-ok">{{ p.estado_postulacion }}</span>
                  </div>
                  <h3>{{ p.labor_descripcion }}</h3>
                  <p class="small"><strong>Franja horaria elegida:</strong> {{ p.disponibilidad_propuesta }}</p>
                  <p class="small"><strong>Mi motivación:</strong> {{ p.motivacion }}</p>
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
    .header-actions { display: flex; flex-wrap: wrap; gap: 0.65rem; align-items: center; }
    .capacity-strip {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1rem;
      margin-bottom: 1.35rem;
    }
    .cap-item {
      padding: 0.9rem 1.15rem;
      background: var(--sap-bg-surface);
      border: 1px solid var(--sap-border-subtle);
      border-left: 4px solid var(--sap-brand-primary);
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      gap: 0.2rem;
    }
    .cap-item.highlight {
      border-left-color: var(--sap-status-ok-border);
      background: #F0FDF4;
    }
    .cap-label { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.03em; color: var(--sap-text-secondary); font-weight: 700; }
    .cap-item strong { font-size: 1.15rem; color: var(--sap-text-primary); }
    .alert-success {
      border-left: 5px solid #15803D;
      background: #DCFCE7;
      color: #14532D;
      padding: 0.95rem 1.2rem;
      border-radius: 6px;
      font-weight: 700;
      margin-bottom: 1.25rem;
    }
    .alert-error {
      border-left: 5px solid #B91C1C;
      background: #FEE2E2;
      color: #7F1D1D;
      padding: 0.95rem 1.2rem;
      border-radius: 6px;
      font-weight: 700;
      margin-bottom: 1.25rem;
    }
    .layout-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 1.5rem; align-items: start; }
    .sap-panel { border-top: 3px solid var(--sap-brand-primary); }
    .panel-head { display: flex; justify-content: space-between; align-items: center; padding-bottom: 0.85rem; margin-bottom: 1.25rem; border-bottom: 1px solid var(--sap-border-subtle); }
    .panel-head h2 { margin: 0; font-size: 1.12rem; }
    .form-group { margin-bottom: 1rem; }
    .field-hint { display: block; margin-top: 0.35rem; font-size: 0.8rem; color: var(--sap-text-secondary); }
    .form-actions-row { display: flex; flex-direction: column; gap: 0.65rem; margin-top: 1rem; }
    .btn-full { width: 100%; text-align: center; }
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

  catalogos = signal<CatalogosGenerales | null>(null);
  labores = signal<LaborItem[]>([]);
  postulaciones = signal<PostulacionItem[]>([]);
  resumenDisp = signal<ResumenDisponibilidad>({
    disponibilidad_horas_semana: 8,
    horas_comprometidas: 0,
    horas_disponibles_restantes: 8,
  });

  enviando = signal(false);
  mensajeExito = signal('');
  mensajeError = signal('');
  mensajeOffline = signal('');

  form = {
    necesidad_campana_id: 2,
    disponibilidad_propuesta: 'Fines de semana en la mañana (Sábados y Domingos 7:00 a.m. - 12:00 m.)',
    horas_comprometidas: 4,
    motivacion: 'Cuento con experiencia en trabajo comunitario con escuelas veredales y manejo de compostaje.',
  };

  ngOnInit(): void {
    this.offlineSync.obtenerCatalogos().subscribe((cat) => {
      this.catalogos.set(cat);
      if (cat.franjas_horarias?.length && !this.form.disponibilidad_propuesta) {
        this.form.disponibilidad_propuesta = cat.franjas_horarias[0].nombre;
      }
    });

    const borrador = this.offlineSync.cargarBorradorFormulario<typeof this.form>(this.DRAFT_KEY);
    if (borrador) {
      this.form = borrador;
    }
    this.cargarDatos();
  }

  cargarDatos(): void {
    this.http
      .get<{
        labores: LaborItem[];
        postulaciones: PostulacionItem[];
        resumen_disponibilidad?: ResumenDisponibilidad;
      }>(`${getApiBaseUrl()}/voluntariado/labores`)
      .subscribe({
        next: (res) => {
          this.labores.set(res.labores);
          this.postulaciones.set(res.postulaciones);
          if (res.resumen_disponibilidad) {
            this.resumenDisp.set(res.resumen_disponibilidad);
            if (
              res.resumen_disponibilidad.horas_disponibles_restantes > 0 &&
              this.form.horas_comprometidas > res.resumen_disponibilidad.horas_disponibles_restantes
            ) {
              this.form.horas_comprometidas = res.resumen_disponibilidad.horas_disponibles_restantes;
            }
          }
          if (res.labores.length > 0 && !res.labores.some((l) => l.necesidad_id === this.form.necesidad_campana_id)) {
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
    this.mensajeExito.set('');
    this.mensajeError.set('');
    this.mensajeOffline.set('');

    const dispMax = this.resumenDisp().disponibilidad_horas_semana;
    const dispRestante = this.resumenDisp().horas_disponibles_restantes;
    const horasSolicitadas = Number(this.form.horas_comprometidas);

    if (!horasSolicitadas || horasSolicitadas < 1) {
      this.mensajeError.set('Debes comprometer al menos 1 hora para postularte a la actividad comunitaria.');
      return;
    }

    if (horasSolicitadas > dispMax) {
      this.mensajeError.set(
        `No puedes comprometer ${horasSolicitadas} horas porque supera las ${dispMax} horas semanales que registraste como disponibles en tu inscripción.`
      );
      return;
    }

    if (horasSolicitadas > dispRestante) {
      this.mensajeError.set(
        `Ya tienes ${this.resumenDisp().horas_comprometidas} horas comprometidas de tus ${dispMax} horas semanales. Solo puedes comprometer hasta ${dispRestante} hora(s) adicional(es).`
      );
      return;
    }

    if (!this.form.motivacion.trim()) {
      this.mensajeError.set('Por favor describe brevemente tu perfil de apoyo y experiencia para esta jornada.');
      return;
    }

    this.enviando.set(true);

    const payload = {
      ...this.form,
      horas_comprometidas: horasSolicitadas,
      voluntario_id: this.authService.usuarioActual()?.voluntario_id || 1,
    };

    this.http.post<{ mensaje_humano: string }>(`${getApiBaseUrl()}/voluntariado/postular`, payload).subscribe({
      next: (res) => {
        this.enviando.set(false);
        this.mensajeExito.set(res.mensaje_humano);
        this.offlineSync.limpiarBorradorFormulario(this.DRAFT_KEY);
        this.cargarDatos();
      },
      error: (err) => {
        this.enviando.set(false);
        this.guardarBorrador();
        if (err.status === 0) {
          this.mensajeOffline.set(
            'Tu conexión parece inestable. Hemos guardado tu postulación de voluntariado para enviarla en cuanto recuperes la señal.'
          );
        } else {
          this.mensajeError.set(
            err.error?.mensaje_humano || 'No fue posible registrar tu postulación en esta actividad.'
          );
        }
      },
    });
  }
}
