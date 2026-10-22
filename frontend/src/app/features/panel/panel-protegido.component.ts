import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { getApiBaseUrl } from '../../core/config/api.config';

interface FundacionExpediente {
  id: number;
  nit: string;
  razon_social: string;
  sigla: string;
  mision: string;
  telefono_institucional: string;
  estado_validacion: string;
  representante_nombre: string;
  municipio: string;
  vereda_o_barrio: string;
  documentos_legales: Array<{
    id: number;
    tipo_soporte: string;
    nombre_archivo: string;
    estado_revision: string;
  }>;
}

@Component({
  selector: 'app-panel-protegido',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (authService.usuarioActual(); as usuario) {
      <div class="sap-page-header">
        <div class="sap-page-header-inner">
          <div>
            <span class="sap-breadcrumb">Gobernanza de Seguridad · Tríada CIA y Mínimo Privilegio</span>
            <h1 class="sap-page-title">{{ usuario.nombre_mostrar }}</h1>
            <p class="sap-page-subtitle">
              Perfil Autenticado: <strong>{{ authService.etiquetaRolPrincipal() }}</strong> · Rol Técnico: {{ usuario.roles.join(', ') }}
            </p>
          </div>
          <button type="button" class="sap-btn-secondary btn-logout" (click)="authService.cerrarSesion()">
            Cerrar Sesión Segura
          </button>
        </div>
      </div>

      <main class="sap-container">
        @if (avisoRestringido()) {
          <div class="cs-alert-human" role="alert">
            Principio de Mínimo Privilegio: Tu rol actual ({{ usuario.roles.join(', ') }}) no tiene autorización para acceder al módulo solicitado. Se ha registrado el evento en auditoría.
          </div>
        }

        @if (mensajeAdmin()) {
          <div class="alert-ok" role="status">{{ mensajeAdmin() }}</div>
        }

        <!-- SECCIÓN EXCLUSIVA DEL ADMINISTRADOR DE LA PLATAFORMA (ROL: ADMIN) -->
        @if (authService.tieneRol('ADMIN')) {
          <section class="cs-card admin-gov-card" aria-label="Bandeja de aprobación de fundaciones OSAL">
            <div class="card-head">
              <div>
                <h2>Bandeja de Gobernanza: Validación Legal de Fundaciones OSAL</h2>
                <p class="sub-head">Facultad exclusiva del Administrador General para verificar soportes legales (RUT / Cámara de Comercio) y habilitar OSAL en Sabana Norte.</p>
              </div>
              <span class="sap-badge sap-badge-info">Privilegio: ADMIN</span>
            </div>

            <div class="osal-approval-list">
              @for (f of fundaciones(); track f.id) {
                <article class="osal-approval-row">
                  <div class="osal-main-info">
                    <div class="osal-title-line">
                      <strong>{{ f.razon_social }} (NIT: {{ f.nit }})</strong>
                      <span
                        class="sap-badge"
                        [class.sap-badge-ok]="f.estado_validacion === 'APROBADA'"
                        [class.sap-badge-warn]="f.estado_validacion === 'PENDIENTE'"
                      >
                        {{ f.estado_validacion }}
                      </span>
                    </div>
                    <p class="osal-meta">
                      📍 {{ f.municipio }} ({{ f.vereda_o_barrio }}) · Representante: {{ f.representante_nombre }} · Tel: {{ f.telefono_institucional }}
                    </p>
                    <div class="docs-chips">
                      @for (doc of f.documentos_legales; track doc.id) {
                        <span class="doc-chip">📄 {{ doc.tipo_soporte }}: {{ doc.nombre_archivo }} ({{ doc.estado_revision }})</span>
                      }
                    </div>
                  </div>

                  <div class="osal-actions">
                    <button
                      type="button"
                      class="cs-btn btn-sm"
                      [disabled]="f.estado_validacion === 'APROBADA'"
                      (click)="cambiarEstadoOsal(f.id, 'APROBADA')"
                    >
                      Aprobar OSAL
                    </button>
                    <button
                      type="button"
                      class="sap-btn-secondary btn-sm btn-reject"
                      [disabled]="f.estado_validacion === 'RECHAZADA'"
                      (click)="cambiarEstadoOsal(f.id, 'RECHAZADA')"
                    >
                      Rechazar
                    </button>
                  </div>
                </article>
              }
            </div>
          </section>
        }

        <section class="sap-grid" aria-label="Ficha de identidad y bitácora de auditoría">
          <article class="cs-card sap-object-card">
            <div class="card-head">
              <h2>Matriz de Identidad y Mínimo Privilegio</h2>
              <span class="sap-badge sap-badge-ok">Sesión Verificada</span>
            </div>

            <div class="kv-grid">
              <div class="kv-item">
                <span class="kv-label">Correo Electrónico</span>
                <strong class="kv-value">{{ usuario.correo_electronico }}</strong>
              </div>
              <div class="kv-item">
                <span class="kv-label">Rol de Seguridad (RBAC)</span>
                <strong class="kv-value">{{ authService.etiquetaRolPrincipal() }}</strong>
              </div>
              <div class="kv-item">
                <span class="kv-label">Alcance de Permisos</span>
                <strong class="kv-value">
                  @if (authService.tieneRol('ADMIN')) {
                    Gobernanza Global, Aprobación OSAL y Auditoría Total
                  } @else if (authService.tieneRol('REPRESENTANTE_OSAL')) {
                    Gestión de Campañas, Dashboard y Logística de su OSAL
                  } @else if (authService.tieneRol('VOLUNTARIO')) {
                    Postulación a Labores y Matriz de Competencias
                  } @else if (authService.tieneRol('DONANTE')) {
                    Radicación de Aportes y Descarga de Certificados PDF
                  }
                </strong>
              </div>
              <div class="kv-item">
                <span class="kv-label">Vínculo Relacional (5FN)</span>
                <strong class="kv-value">
                  {{ usuario.fundacion_nombre ? usuario.fundacion_nombre + ' (' + usuario.fundacion_estado + ')' : '' }}
                  {{ usuario.donante_id ? 'Registro Donante #' + usuario.donante_id : '' }}
                  {{ usuario.voluntario_id ? 'Registro Voluntario #' + usuario.voluntario_id : '' }}
                  {{ authService.tieneRol('ADMIN') ? 'Supervisión Sabana Norte' : '' }}
                </strong>
              </div>
            </div>
          </article>

          <article class="cs-card sap-object-card">
            <div class="card-head">
              <h2>Bitácora Inmutable de Auditoría (Integridad CIA)</h2>
              <span class="sap-badge sap-badge-info">
                {{ authService.tieneRol('ADMIN') ? 'Vista Global de Plataforma' : 'Eventos de mi Cuenta' }}
              </span>
            </div>

            @if (auditoria().length === 0) {
              <p class="empty-note">Consultando historial de eventos de seguridad...</p>
            } @else {
              <div class="audit-table">
                @for (evento of auditoria(); track evento.id) {
                  <div class="audit-row">
                    <div class="audit-main">
                      <span
                        class="sap-badge"
                        [class.sap-badge-ok]="!evento.accion.includes('FALLIDO') && !evento.accion.includes('DENEGADO')"
                        [class.sap-badge-warn]="evento.accion.includes('FALLIDO') || evento.accion.includes('DENEGADO')"
                      >
                        {{ evento.accion }}
                      </span>
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
    .btn-logout { border-color: var(--sap-status-err-border); color: var(--sap-status-err-text); }
    .alert-ok {
      border-left: 4px solid var(--sap-status-ok-border);
      background: var(--sap-status-ok-bg);
      color: var(--sap-status-ok-text);
      padding: 0.85rem 1.15rem;
      border-radius: 6px;
      font-weight: 700;
      margin-bottom: 1.25rem;
    }
    .admin-gov-card {
      border-top: 4px solid var(--sap-brand-primary);
      margin-bottom: 1.5rem;
    }
    .sub-head { margin: 0.25rem 0 0 0; font-size: 0.86rem; color: var(--sap-text-secondary); }
    .osal-approval-list { display: flex; flex-direction: column; gap: 0.85rem; }
    .osal-approval-row {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      padding: 1rem;
      background: var(--sap-bg-canvas);
      border: 1px solid var(--sap-border-subtle);
      border-radius: 6px;
    }
    .osal-title-line { display: flex; align-items: center; gap: 0.65rem; flex-wrap: wrap; margin-bottom: 0.3rem; }
    .osal-meta { margin: 0 0 0.5rem 0; font-size: 0.86rem; color: var(--sap-text-secondary); }
    .docs-chips { display: flex; flex-wrap: wrap; gap: 0.5rem; }
    .doc-chip { font-size: 0.78rem; background: #FFFFFF; border: 1px solid var(--sap-border-subtle); padding: 0.2rem 0.55rem; border-radius: 4px; }
    .osal-actions { display: flex; gap: 0.5rem; }
    .btn-sm { min-height: 38px; padding: 0.4rem 0.9rem; font-size: 0.85rem; }
    .btn-reject { border-color: var(--sap-status-err-border); color: var(--sap-status-err-text); }
    .sap-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 1.5rem; }
    .sap-object-card { border-top: 3px solid var(--sap-brand-primary); }
    .card-head { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; padding-bottom: 0.85rem; margin-bottom: 1.15rem; border-bottom: 1px solid var(--sap-border-subtle); }
    .card-head h2 { margin: 0; font-size: 1.1rem; }
    .kv-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }
    .kv-item { display: flex; flex-direction: column; padding: 0.75rem; background: var(--sap-bg-canvas); border: 1px solid var(--sap-border-subtle); border-radius: 6px; }
    .kv-label { font-size: 0.78rem; color: var(--sap-text-secondary); margin-bottom: 0.25rem; }
    .kv-value { font-size: 0.92rem; color: var(--sap-text-primary); }
    .audit-table { display: flex; flex-direction: column; gap: 0.65rem; }
    .audit-row { display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: 0.65rem 0.85rem; background: var(--sap-bg-canvas); border: 1px solid var(--sap-border-subtle); border-radius: 6px; }
    .audit-main { display: flex; align-items: center; gap: 0.65rem; flex-wrap: wrap; }
    .audit-detail { font-size: 0.88rem; }
    .audit-time { font-size: 0.78rem; color: var(--sap-text-secondary); white-space: nowrap; }
  `]
})
export class PanelProtegidoComponent implements OnInit {
  readonly authService = inject(AuthService);
  private readonly http = inject(HttpClient);
  private readonly route = inject(ActivatedRoute);

  auditoria = signal<Array<{ id: number; accion: string; detalle: string; fecha_evento: string }>>([]);
  fundaciones = signal<FundacionExpediente[]>([]);
  avisoRestringido = signal(false);
  mensajeAdmin = signal('');

  ngOnInit(): void {
    this.route.queryParamMap.subscribe((params) => {
      this.avisoRestringido.set(params.get('acceso_restringido') === 'true');
    });

    this.cargarPerfilYAuditoria();
    if (this.authService.tieneRol('ADMIN')) {
      this.cargarFundacionesParaGobernanza();
    }
  }

  cargarPerfilYAuditoria(): void {
    this.authService.obtenerPerfilremoto().subscribe({
      next: (res) => {
        this.auditoria.set(res.auditoria_reciente);
      },
      error: () => {},
    });
  }

  cargarFundacionesParaGobernanza(): void {
    this.http.get<{ fundaciones: FundacionExpediente[] }>(`${getApiBaseUrl()}/osal`).subscribe({
      next: (res) => this.fundaciones.set(res.fundaciones),
      error: () => {},
    });
  }

  cambiarEstadoOsal(fundacionId: number, nuevoEstado: 'APROBADA' | 'RECHAZADA'): void {
    this.http
      .put<{ mensaje_humano: string }>(`${getApiBaseUrl()}/osal/${fundacionId}/estado-validacion`, {
        estado_validacion: nuevoEstado,
      })
      .subscribe({
        next: (res) => {
          this.mensajeAdmin.set(res.mensaje_humano);
          this.cargarFundacionesParaGobernanza();
          this.cargarPerfilYAuditoria();
        },
      });
  }
}
