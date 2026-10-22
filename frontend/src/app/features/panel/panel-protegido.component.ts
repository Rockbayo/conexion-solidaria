import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-panel-protegido',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (authService.usuarioActual(); as usuario) {
      <div class="sap-page-header">
        <div class="sap-page-header-inner">
          <div>
            <span class="sap-breadcrumb">Administración de Cuenta y Seguridad</span>
            <h1 class="sap-page-title">{{ usuario.nombre_mostrar }}</h1>
            <p class="sap-page-subtitle">Rol asignado: {{ usuario.roles.join(' · ') }} — Sabana Norte de Cundinamarca</p>
          </div>
          <button type="button" class="sap-btn-secondary btn-logout" (click)="authService.cerrarSesion()">
            Finalizar Sesión
          </button>
        </div>
      </div>

      <main class="sap-container">
        @if (avisoRestringido()) {
          <div class="cs-alert-human" role="alert">
            Esta vista requiere permisos adicionales. Te hemos dirigido a tu centro de cuenta principal.
          </div>
        }

        <section class="sap-grid" aria-label="Información de perfil y auditoría de accesos">
          <article class="cs-card sap-object-card">
            <div class="card-head">
              <h2>Ficha de Identidad y Vínculos</h2>
              <span class="sap-badge sap-badge-ok">Cuenta Activa</span>
            </div>

            <div class="kv-grid">
              <div class="kv-item">
                <span class="kv-label">Correo Electrónico</span>
                <strong class="kv-value">{{ usuario.correo_electronico }}</strong>
              </div>
              <div class="kv-item">
                <span class="kv-label">Identificador Interno</span>
                <strong class="kv-value">USR-{{ usuario.id }}</strong>
              </div>
              <div class="kv-item">
                <span class="kv-label">Organización OSAL Asociada</span>
                <strong class="kv-value">{{ usuario.fundacion_id ? 'OSAL #' + usuario.fundacion_id : 'No aplica' }}</strong>
              </div>
              <div class="kv-item">
                <span class="kv-label">Registro de Donante / Voluntario</span>
                <strong class="kv-value">
                  {{ usuario.donante_id ? 'Donante #' + usuario.donante_id : '' }}
                  {{ usuario.voluntario_id ? 'Voluntario #' + usuario.voluntario_id : '' }}
                  {{ !usuario.donante_id && !usuario.voluntario_id ? 'Representante Institucional' : '' }}
                </strong>
              </div>
            </div>
          </article>

          <article class="cs-card sap-object-card">
            <div class="card-head">
              <h2>Registro de Auditoría de Seguridad</h2>
              <span class="sap-badge sap-badge-info">Trazabilidad</span>
            </div>

            @if (auditoria().length === 0) {
              <p class="empty-note">Consultando historial de eventos de seguridad...</p>
            } @else {
              <div class="audit-table">
                @for (evento of auditoria(); track evento.id) {
                  <div class="audit-row">
                    <div class="audit-main">
                      <span class="sap-badge sap-badge-ok">{{ evento.accion }}</span>
                      <span class="audit-detail">{{ evento.detalle }}</span>
                    </div>
                    <time class="audit-time">{{ evento.fecha_evento | date:'yyyy-MM-dd HH:mm' }}</time>
                  </div>
                }
              </div>
            }
          </article>
        </section>
      </main>
    }
  `,
  styles: [`
    .btn-logout {
      border-color: var(--sap-status-err-border);
      color: var(--sap-status-err-text);
    }
    .sap-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
      gap: 1.5rem;
    }
    .sap-object-card {
      border-top: 3px solid var(--sap-brand-primary);
    }
    .card-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 0.85rem;
      margin-bottom: 1.15rem;
      border-bottom: 1px solid var(--sap-border-subtle);
    }
    .card-head h2 {
      margin: 0;
      font-size: 1.1rem;
    }
    .kv-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 1rem;
    }
    .kv-item {
      display: flex;
      flex-direction: column;
      padding: 0.75rem;
      background: var(--sap-bg-canvas);
      border: 1px solid var(--sap-border-subtle);
      border-radius: 6px;
    }
    .kv-label {
      font-size: 0.78rem;
      color: var(--sap-text-secondary);
      margin-bottom: 0.25rem;
    }
    .kv-value {
      font-size: 0.95rem;
      color: var(--sap-text-primary);
    }
    .audit-table {
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
    }
    .audit-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      padding: 0.65rem 0.85rem;
      background: var(--sap-bg-canvas);
      border: 1px solid var(--sap-border-subtle);
      border-radius: 6px;
    }
    .audit-main {
      display: flex;
      align-items: center;
      gap: 0.65rem;
      flex-wrap: wrap;
    }
    .audit-detail {
      font-size: 0.9rem;
    }
    .audit-time {
      font-size: 0.8rem;
      color: var(--sap-text-secondary);
      white-space: nowrap;
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
      error: () => {},
    });
  }
}
