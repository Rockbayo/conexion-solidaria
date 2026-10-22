import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-panel-protegido',
  standalone: true,
  imports: [CommonModule],
  template: `
    <main class="panel-container">
      @if (avisoRestringido()) {
        <div class="cs-alert-human" role="alert">
          Esta sección requiere un rol específico de fundación o voluntariado. Te hemos traído a tu panel principal seguro.
        </div>
      }

      @if (authService.usuarioActual(); as usuario) {
        <header class="cs-card welcome-banner">
          <div>
            <span class="role-chip">Rol activo: {{ usuario.roles.join(', ') }}</span>
            <h1>Hola, {{ usuario.nombre_mostrar }}</h1>
            <p>Has ingresado con sesión cifrada JWT a Conexión Solidaria (Sabana Norte de Cundinamarca).</p>
          </div>
          <button type="button" class="btn-logout" (click)="authService.cerrarSesion()">
            Cerrar sesión segura
          </button>
        </header>

        <section class="cards-grid" aria-label="Resumen de tu cuenta y trazabilidad de seguridad">
          <article class="cs-card">
            <h2>Estado de tu Perfil Relacional (5FN)</h2>
            <ul class="clean-list">
              <li><strong>Correo verificado:</strong> {{ usuario.correo_electronico }}</li>
              <li><strong>ID Usuario:</strong> #{{ usuario.id }}</li>
              @if (usuario.fundacion_id) {
                <li><strong>Fundación OSAL vinculada:</strong> ID #{{ usuario.fundacion_id }}</li>
              }
              @if (usuario.donante_id) {
                <li><strong>Perfil Donante activo:</strong> ID #{{ usuario.donante_id }}</li>
              }
              @if (usuario.voluntario_id) {
                <li><strong>Perfil Voluntario activo:</strong> ID #{{ usuario.voluntario_id }}</li>
              }
            </ul>
          </article>

          <article class="cs-card">
            <h2>Bitácora de Seguridad Reciente (logs_auditoria)</h2>
            @if (auditoria().length === 0) {
              <p>Cargando eventos de seguridad o operando desde caché local...</p>
            } @else {
              <ul class="clean-list">
                @for (evento of auditoria(); track evento.id) {
                  <li>
                    <span class="badge-audit">{{ evento.accion }}</span>
                    <span>{{ evento.detalle }}</span>
                  </li>
                }
              </ul>
            }
          </article>
        </section>
      }
    </main>
  `,
  styles: [`
    .panel-container {
      max-width: 1080px;
      margin: 2rem auto;
      padding: 0 1.5rem;
    }
    .welcome-banner {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      margin-bottom: 1.5rem;
      border-color: var(--brand-primary);
    }
    .welcome-banner h1 {
      margin: 0.5rem 0 0.25rem 0;
      font-size: 1.75rem;
    }
    .welcome-banner p {
      margin: 0;
      color: var(--text-secondary);
    }
    .role-chip {
      display: inline-block;
      background-color: var(--status-ok-bg);
      color: var(--status-ok-text);
      font-weight: 700;
      padding: 0.25rem 0.75rem;
      border-radius: 999px;
      font-size: 0.875rem;
    }
    .btn-logout {
      min-height: 48px;
      padding: 0.75rem 1.25rem;
      font-weight: 700;
      border: 2px solid var(--status-err-text);
      background-color: var(--status-err-bg);
      color: var(--status-err-text);
      border-radius: 8px;
      cursor: pointer;
    }
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 1.5rem;
    }
    .cards-grid h2 {
      margin-top: 0;
      font-size: 1.25rem;
    }
    .clean-list {
      list-style: none;
      padding: 0;
      margin: 0;
    }
    .clean-list li {
      padding: 0.65rem 0;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }
    .badge-audit {
      font-weight: 700;
      color: var(--brand-primary);
      font-size: 0.85rem;
    }
  `]
})
export class PanelProtegidoComponent implements OnInit {
  readonly authService = inject(AuthService);
  private readonly route = inject(ActivatedRoute);

  auditoria = signal<Array<{ id: number; accion: string; detalle: string; fecha_evento: string }>>([]);
  avisoRestringido = signal(false);

  ngOnInit(): void {
    this.route.queryParamMap.subscribe((params) => {
      this.avisoRestringido.set(params.get('acceso_restringido') === 'true');
    });

    this.authService.obtenerPerfilremoto().subscribe({
      next: (res) => {
        this.auditoria.set(res.auditoria_reciente);
      },
      error: () => {
        // En caso de pérdida de señal rural, conserva la vista con los datos de sesión en caché
      },
    });
  }
}
