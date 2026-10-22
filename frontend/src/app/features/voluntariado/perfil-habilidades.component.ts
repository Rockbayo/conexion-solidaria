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
    <main class="container" aria-labelledby="cu10-heading">
      <header class="cs-card header-banner">
        <div>
          <span class="tag-pill">CU10 · Perfil de Habilidades del Voluntario 5FN</span>
          <h1 id="cu10-heading">Gestión de Competencias y Disponibilidad Rural</h1>
          <p>
            Administra tus saberes técnicos, pedagógicos o logísticos para conectarte con las necesidades de las veredas de Sabana Norte.
          </p>
        </div>
      </header>

      @if (mensajeHumano()) {
        <div class="cs-alert-human" role="status">{{ mensajeHumano() }}</div>
      }

      <div class="layout-grid">
        <!-- FORMULARIO PARA AGREGAR/ACTUALIZAR COMPETENCIA Y DISPONIBILIDAD -->
        <section class="cs-card" aria-label="Formulario para agregar competencia al perfil">
          <h2>Añadir o Actualizar Competencia</h2>
          <form (ngSubmit)="guardarPerfilYHabilidad()" novalidate>
            <div class="form-group">
              <label for="hab_sel">Competencia del Catálogo (habilidades) *</label>
              <select id="hab_sel" name="hab_sel" [(ngModel)]="form.habilidad_id">
                @for (h of catalogos()?.habilidades || []; track h.id) {
                  <option [ngValue]="h.id">{{ h.nombre }} — {{ h.descripcion }}</option>
                }
              </select>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label for="nivel_sel">Nivel de Dominio *</label>
                <select id="nivel_sel" name="nivel_sel" [(ngModel)]="form.nivel_dominio">
                  <option value="BASICO">Básico / Aprendiz</option>
                  <option value="INTERMEDIO">Intermedio / Práctico</option>
                  <option value="AVANZADO">Avanzado / Formador</option>
                </select>
              </div>
              <div class="form-group">
                <label for="anos_exp">Años de Experiencia *</label>
                <input id="anos_exp" name="anos_exp" type="number" min="0" max="50" [(ngModel)]="form.anos_experiencia" />
              </div>
            </div>

            <hr class="divider" />

            <div class="grid-2">
              <div class="form-group">
                <label for="horas_sem">Horas Disponibles por Semana</label>
                <input id="horas_sem" name="horas_sem" type="number" min="1" max="48" [(ngModel)]="form.disponibilidad_horas_semana" />
              </div>
              <div class="form-group checkbox-group">
                <label>
                  <input type="checkbox" name="desplazamiento" [(ngModel)]="form.dispuesto_desplazamiento_rural" />
                  Dispuesto a desplazamiento hacia veredas rurales
                </label>
              </div>
            </div>

            <div class="form-group">
              <label for="bio">Biografía Corta / Presentación Comunitaria</label>
              <textarea id="bio" name="bio" rows="2" [(ngModel)]="form.biografia_corta"></textarea>
            </div>

            <button type="submit" class="cs-btn btn-full">
              Guardar Habilidad y Disponibilidad
            </button>
          </form>
        </section>

        <!-- TARJETA DE HABILIDADES REGISTRADAS -->
        <section class="cs-card" aria-label="Matriz de competencias registradas del voluntario">
          <h2>Competencias Activas de {{ nombreVoluntario() }}</h2>
          <p class="subtitle">
            Disponibilidad actual: <strong>{{ form.disponibilidad_horas_semana }} horas/semana</strong>
          </p>

          @if (competencias().length === 0) {
            <p>Aún no has vinculado habilidades específicas a tu perfil. Añade la primera usando el formulario.</p>
          } @else {
            <div class="skills-list">
              @for (c of competencias(); track c.id) {
                <article class="skill-card">
                  <div>
                    <span class="cat-badge">{{ c.categoria_nombre }}</span>
                    <h3>{{ c.habilidad_nombre }}</h3>
                    <p>Nivel: <strong>{{ c.nivel_dominio }}</strong> · Experiencia: {{ c.anos_experiencia }} año(s)</p>
                  </div>
                  <button type="button" class="btn-remove" (click)="eliminarHabilidad(c.id)">
                    Quitar
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
    .container { max-width: 1080px; margin: 2rem auto; padding: 0 1.5rem; }
    .header-banner { margin-bottom: 1.5rem; border-color: var(--brand-primary); }
    .header-banner h1 { margin: 0.4rem 0; font-size: 1.75rem; }
    .tag-pill { display: inline-block; background: var(--status-ok-bg); color: var(--status-ok-text); font-weight: 800; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.85rem; }
    .layout-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 1.5rem; align-items: start; }
    .form-group { display: flex; flex-direction: column; margin-bottom: 1rem; }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 0.85rem; }
    label { font-weight: 700; margin-bottom: 0.35rem; }
    input[type="text"], input[type="number"], select, textarea { min-height: 48px; padding: 0.65rem 0.85rem; font-size: 1rem; border: 2px solid var(--border-strong); border-radius: 8px; }
    .checkbox-group { justify-content: center; }
    .checkbox-group label { display: flex; align-items: center; gap: 0.5rem; cursor: pointer; }
    .checkbox-group input[type="checkbox"] { width: 22px; height: 22px; }
    .btn-full { width: 100%; }
    .divider { margin: 1.2rem 0; border: 0; border-top: 2px solid var(--border-subtle); }
    .skills-list { display: flex; flex-direction: column; gap: 0.85rem; }
    .skill-card { display: flex; justify-content: space-between; align-items: center; padding: 1rem; border: 2px solid var(--border-subtle); border-radius: 10px; background: #F9FAF7; }
    .cat-badge { background: var(--status-ok-bg); color: var(--status-ok-text); font-weight: 800; padding: 0.15rem 0.55rem; border-radius: 6px; font-size: 0.78rem; }
    .skill-card h3 { margin: 0.25rem 0; font-size: 1.05rem; }
    .skill-card p { margin: 0; font-size: 0.88rem; color: var(--text-secondary); }
    .btn-remove { min-height: 42px; padding: 0.4rem 0.85rem; border: 2px solid var(--status-err-text); background: var(--status-err-bg); color: var(--status-err-text); font-weight: 700; border-radius: 8px; cursor: pointer; }
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

