import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { OfflineSyncService } from '../../core/services/offline-sync.service';
import { AuthService } from '../../core/services/auth.service';

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
    <main class="container" aria-labelledby="cu05-heading">
      <header class="cs-card header-banner">
        <div>
          <span class="tag-pill">CU05 · Postulación y Asignación de Voluntariado 5FN</span>
          <h1 id="cu05-heading">Postulación a Labores Comunitarias en Sabana Norte</h1>
          <p>
            Elige una labor rural activa, propón tu horario de apoyo y recibe tu asignación inmediata de actividades.
          </p>
        </div>
        <a routerLink="/perfil-habilidades" class="cs-btn">
          Gestionar mis Habilidades (CU10)
        </a>
      </header>

      @if (mensajeHumano()) {
        <div class="cs-alert-human" role="status">{{ mensajeHumano() }}</div>
      }

      <div class="layout-grid">
        <!-- FORMULARIO DE POSTULACIÓN CU05 -->
        <section class="cs-card" aria-label="Formulario de postulación a voluntariado">
          <h2>Postularme a una Labor Específica</h2>
          <form (ngSubmit)="enviarPostulacion()" novalidate>
            <div class="form-group">
              <label for="labor_sel">1. Selecciona la Labor Comunitaria *</label>
              <select id="labor_sel" name="labor_sel" [(ngModel)]="form.necesidad_campana_id" (ngModelChange)="guardarBorrador()">
                @for (l of labores(); track l.necesidad_id) {
                  <option [ngValue]="l.necesidad_id">
                    [{{ l.municipio }}] {{ l.descripcion_item }} — {{ l.fundacion_nombre }}
                  </option>
                }
              </select>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label for="disp">2. Disponibilidad de Horario *</label>
                <input id="disp" name="disp" type="text" [(ngModel)]="form.disponibilidad_propuesta" (ngModelChange)="guardarBorrador()" placeholder="Ej: Sábados de 7:00 am a 1:00 pm" required />
              </div>
              <div class="form-group">
                <label for="horas">3. Horas a Comprometer *</label>
                <input id="horas" name="horas" type="number" min="2" max="80" [(ngModel)]="form.horas_comprometidas" (ngModelChange)="guardarBorrador()" required />
              </div>
            </div>

            <div class="form-group">
              <label for="motiv">4. ¿Cómo puedes aportar en esta jornada rural? *</label>
              <textarea id="motiv" name="motiv" rows="3" [(ngModel)]="form.motivacion" (ngModelChange)="guardarBorrador()" placeholder="Cuéntale a la fundación tu experiencia y motivación..." required></textarea>
            </div>

            <button type="submit" class="cs-btn btn-full" [disabled]="enviando()">
              {{ enviando() ? 'Enviando postulación...' : 'Confirmar Postulación Solidaria' }}
            </button>
          </form>
        </section>

        <!-- LISTADO DE POSTULACIONES Y ASIGNACIONES -->
        <section class="cs-card" aria-label="Mis postulaciones y actividades asignadas">
          <h2>Mis Postulaciones y Actividades Asignadas</h2>
          @if (postulaciones().length === 0) {
            <p>Aún no tienes postulaciones activas. Selecciona una labor en el formulario para empezar.</p>
          } @else {
            <div class="post-list">
              @for (p of postulaciones(); track p.id) {
                <article class="post-card">
                  <div class="post-top">
                    <span class="status-chip">{{ p.estado_postulacion }}</span>
                    <strong>{{ p.voluntario_nombre }}</strong>
                  </div>
                  <h3>{{ p.labor_descripcion }}</h3>
                  <p class="small"><strong>Disponibilidad:</strong> {{ p.disponibilidad_propuesta }}</p>
                  <p class="small"><strong>Motivación:</strong> {{ p.motivacion }}</p>
                  @if (p.asignacion) {
                    <div class="assign-box">
                      <strong>Asignación (asignaciones_actividades):</strong>
                      <span>{{ p.asignacion.tarea_especifica }} ({{ p.asignacion.horas_comprometidas }} horas · {{ p.asignacion.estado_actividad }})</span>
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
    .container { max-width: 1080px; margin: 2rem auto; padding: 0 1.5rem; }
    .header-banner { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.5rem; border-color: var(--brand-primary); }
    .header-banner h1 { margin: 0.4rem 0; font-size: 1.75rem; }
    .tag-pill { display: inline-block; background: var(--status-ok-bg); color: var(--status-ok-text); font-weight: 800; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.85rem; }
    .layout-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 1.5rem; align-items: start; }
    .form-group { display: flex; flex-direction: column; margin-bottom: 1rem; }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 0.85rem; }
    label { font-weight: 700; margin-bottom: 0.35rem; }
    input, select, textarea { min-height: 48px; padding: 0.65rem 0.85rem; font-size: 1rem; border: 2px solid var(--border-strong); border-radius: 8px; }
    .btn-full { width: 100%; }
    .post-list { display: flex; flex-direction: column; gap: 1rem; }
    .post-card { border: 2px solid var(--border-subtle); border-radius: 10px; padding: 1rem; background: #F9FAF7; }
    .post-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; }
    .status-chip { background: var(--status-ok-bg); color: var(--status-ok-text); font-weight: 800; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.8rem; }
    .post-card h3 { margin: 0.2rem 0 0.5rem 0; font-size: 1.1rem; }
    .small { margin: 0.25rem 0; font-size: 0.9rem; color: var(--text-secondary); }
    .assign-box { margin-top: 0.65rem; padding: 0.6rem; background: #FFFFFF; border-left: 4px solid var(--brand-primary); border-radius: 6px; display: flex; flex-direction: column; font-size: 0.88rem; }
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
    this.http.get<{ labores: LaborItem[]; postulaciones: PostulacionItem[] }>('http://localhost:5000/api/voluntariado/labores').subscribe({
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

    this.http.post<{ mensaje_humano: string }>('http://localhost:5000/api/voluntariado/postular', payload).subscribe({
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

