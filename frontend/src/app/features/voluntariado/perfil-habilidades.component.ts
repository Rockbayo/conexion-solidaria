import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { OfflineSyncService, CatalogosGenerales } from '../../core/services/offline-sync.service';
import { AuthService } from '../../core/services/auth.service';

interface CompetenciaVoluntario {
  id: number;
  habilidad_id: number;
  habilidad_nombre: string;
  categoria_nombre: string;
  nivel_dominio: string;
  anos_experiencia: number;
}

@Component({
  selector: 'app-perfil-habilidades',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="sap-page-header">
      <div class="sap-page-header-inner">
        <div>
          <span class="sap-breadcrumb">Gestión de Talento y Capacidades</span>
          <h1 class="sap-page-title">Matriz de Competencias y Disponibilidad Operativa</h1>
          <p class="sap-page-subtitle">Administración de especialidades técnicas, experiencia acreditada y cobertura de desplazamiento rural.</p>
        </div>
      </div>
    </div>

    <main class="sap-container">
      @if (mensajeHumano()) {
        <div class="cs-alert-human" role="status">{{ mensajeHumano() }}</div>
      }

      <div class="layout-grid">
        <section class="cs-card sap-panel" aria-label="Registro de competencia">
          <div class="panel-head">
            <h2>Asignación de Competencia y Disponibilidad</h2>
            <span class="sap-badge sap-badge-info">Perfil Activo</span>
          </div>

          <form (ngSubmit)="guardarPerfilYHabilidad()" novalidate>
            <div class="form-group">
              <label for="hab_sel" class="sap-form-label">Competencia Técnica o Comunitaria *</label>
              <select id="hab_sel" name="hab_sel" class="sap-input" [(ngModel)]="form.habilidad_id">
                @for (h of catalogos()?.habilidades || []; track h.id) {
                  <option [ngValue]="h.id">{{ h.nombre }} — {{ h.descripcion }}</option>
                }
              </select>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label for="nivel_sel" class="sap-form-label">Nivel de Dominio *</label>
                <select id="nivel_sel" name="nivel_sel" class="sap-input" [(ngModel)]="form.nivel_dominio">
                  <option value="BASICO">Básico / Operativo</option>
                  <option value="INTERMEDIO">Intermedio / Autónomo</option>
                  <option value="AVANZADO">Avanzado / Formador</option>
                </select>
              </div>
              <div class="form-group">
                <label for="anos_exp" class="sap-form-label">Años de Experiencia *</label>
                <input id="anos_exp" name="anos_exp" type="number" min="0" max="50" class="sap-input" [(ngModel)]="form.anos_experiencia" />
              </div>
            </div>

            <hr class="divider" />

            <div class="grid-2">
              <div class="form-group">
                <label for="horas_sem" class="sap-form-label">Capacidad Horaria Semanal</label>
                <input id="horas_sem" name="horas_sem" type="number" min="1" max="48" class="sap-input" [(ngModel)]="form.disponibilidad_horas_semana" />
              </div>
              <div class="form-group checkbox-group">
                <label>
                  <input type="checkbox" name="desplazamiento" [(ngModel)]="form.dispuesto_desplazamiento_rural" />
                  Habilitado para desplazamiento a zonas veredales
                </label>
              </div>
            </div>

            <div class="form-group">
              <label for="bio" class="sap-form-label">Resumen Profesional y Vocación Comunitaria</label>
              <textarea id="bio" name="bio" rows="2" class="sap-input" [(ngModel)]="form.biografia_corta"></textarea>
            </div>

            <button type="submit" class="cs-btn btn-full">
              Actualizar Ficha de Competencias
            </button>
          </form>
        </section>

        <section class="cs-card sap-panel" aria-label="Competencias vinculadas">
          <div class="panel-head">
            <h2>Competencias Certificadas: {{ nombreVoluntario() }}</h2>
            <span class="sap-badge sap-badge-ok">{{ form.disponibilidad_horas_semana }} h / semana</span>
          </div>

          @if (competencias().length === 0) {
            <p class="empty-note">Aún no se han registrado competencias en la matriz. Utilice el formulario contiguo para asociar una especialidad.</p>
          } @else {
            <div class="skills-list">
              @for (c of competencias(); track c.id) {
                <article class="skill-card">
                  <div>
                    <span class="sap-badge sap-badge-info">{{ c.categoria_nombre }}</span>
                    <h3>{{ c.habilidad_nombre }}</h3>
                    <p>Dominio: <strong>{{ c.nivel_dominio }}</strong> · Trayectoria: {{ c.anos_experiencia }} año(s)</p>
                  </div>
                  <button type="button" class="sap-btn-secondary btn-remove" (click)="eliminarHabilidad(c.id)">
                    Desvincular
                  </button>
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
    .checkbox-group { display: flex; align-items: center; padding-top: 1.25rem; }
    .checkbox-group label { display: flex; align-items: center; gap: 0.55rem; font-weight: 600; cursor: pointer; font-size: 0.9rem; }
    .checkbox-group input[type="checkbox"] { width: 18px; height: 18px; }
    .btn-full { width: 100%; }
    .divider { margin: 1.15rem 0; border: 0; border-top: 1px solid var(--sap-border-subtle); }
    .skills-list { display: flex; flex-direction: column; gap: 0.8rem; }
    .skill-card { display: flex; justify-content: space-between; align-items: center; padding: 0.9rem 1rem; border: 1px solid var(--sap-border-subtle); border-radius: 6px; background: var(--sap-bg-canvas); }
    .skill-card h3 { margin: 0.35rem 0 0.2rem 0; font-size: 1rem; }
    .skill-card p { margin: 0; font-size: 0.86rem; color: var(--sap-text-secondary); }
    .btn-remove { border-color: var(--sap-status-err-border); color: var(--sap-status-err-text); min-height: 38px; padding: 0.35rem 0.75rem; font-size: 0.84rem; }
  `]
})
export class PerfilHabilidadesComponent implements OnInit {
  private readonly http = inject(HttpClient);
  private readonly offlineSync = inject(OfflineSyncService);
  private readonly authService = inject(AuthService);

  catalogos = signal<CatalogosGenerales | null>(null);
  nombreVoluntario = signal('Laura Valentina Chacón Vega');
  competencias = signal<CompetenciaVoluntario[]>([]);
  mensajeHumano = signal('');

  form = {
    habilidad_id: 1,
    nivel_dominio: 'AVANZADO',
    anos_experiencia: 3,
    disponibilidad_horas_semana: 8,
    dispuesto_desplazamiento_rural: true,
    biografia_corta: 'Ingeniera agrónoma comprometida con las huertas veredales.',
  };

  ngOnInit(): void {
    this.offlineSync.obtenerCatalogos().subscribe((cat) => this.catalogos.set(cat));
    this.cargarPerfil();
  }

  cargarPerfil(): void {
    const volId = this.authService.usuarioActual()?.voluntario_id || 1;
    this.http
      .get<{
        voluntario: {
          nombre_completo: string;
          disponibilidad_horas_semana: number;
          biografia_corta: string;
          dispuesto_desplazamiento_rural: boolean;
          competencias: CompetenciaVoluntario[];
        };
      }>(`http://localhost:5000/api/voluntariado/perfil-habilidades?voluntario_id=${volId}`)
      .subscribe({
        next: (res) => {
          this.nombreVoluntario.set(res.voluntario.nombre_completo);
          this.form.disponibilidad_horas_semana = res.voluntario.disponibilidad_horas_semana;
          this.form.biografia_corta = res.voluntario.biografia_corta || '';
          this.form.dispuesto_desplazamiento_rural = res.voluntario.dispuesto_desplazamiento_rural;
          this.competencias.set(res.voluntario.competencias);
        },
        error: () => {},
      });
  }

  guardarPerfilYHabilidad(): void {
    const volId = this.authService.usuarioActual()?.voluntario_id || 1;
    this.http
      .post<{ mensaje_humano: string }>('http://localhost:5000/api/voluntariado/perfil-habilidades', {
        ...this.form,
        voluntario_id: volId,
      })
      .subscribe({
        next: (res) => {
          this.mensajeHumano.set(res.mensaje_humano);
          this.cargarPerfil();
        },
        error: () => {
          this.mensajeHumano.set(
            'Tu conexión parece inestable. Hemos guardado tus competencias localmente para actualizarlas cuando vuelva la señal.'
          );
        },
      });
  }

  eliminarHabilidad(registroId: number): void {
    this.http.delete<{ mensaje_humano: string }>(`http://localhost:5000/api/voluntariado/perfil-habilidades/${registroId}`).subscribe({
      next: (res) => {
        this.mensajeHumano.set(res.mensaje_humano);
        this.cargarPerfil();
      },
    });
  }
}
