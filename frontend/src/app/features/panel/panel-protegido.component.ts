import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { OfflineSyncService, CatalogosGenerales } from '../../core/services/offline-sync.service';
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

interface UsuarioDirectorioItem {
  id: number;
  correo_electronico: string;
  nombre_completo: string;
  telefono: string;
  documento: string;
  municipio: string;
  roles: string[];
  esta_activo: boolean;
  intentos_fallidos: number;
  ultimo_acceso: string | null;
}

@Component({
  selector: 'app-panel-protegido',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    @if (authService.usuarioActual(); as usuario) {
      <div class="sap-page-header">
        <div class="sap-page-header-inner">
          <div>
            <span class="sap-breadcrumb">
              {{ authService.tieneRol('ADMIN') ? 'Centro de Gobernanza Regional · Sabana Norte' : 'Mi Resumen Personal · Conexión Solidaria' }}
            </span>
            <h1 class="sap-page-title">Hola, {{ usuario.nombre_mostrar }}</h1>
            <p class="sap-page-subtitle">
              Perfil activo: <strong>{{ authService.etiquetaRolPrincipal() }}</strong>
            </p>
          </div>
          <div class="header-actions">
            <a routerLink="/mapa" class="sap-btn-secondary">Explorar Mapa Territorial</a>
            <button type="button" class="sap-btn-secondary btn-logout" (click)="authService.cerrarSesion()">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>

      <main class="sap-container">
        @if (avisoRestringido()) {
          <div class="cs-alert-human" role="alert">
            Esta sección corresponde a otro tipo de perfil dentro de la plataforma. Te hemos traído a tu página principal.
          </div>
        }

        @if (mensajeExito()) {
          <div class="alert-ok" role="status">✅ {{ mensajeExito() }}</div>
        }

        @if (mensajeError()) {
          <div class="alert-err" role="alert">⚠️ {{ mensajeError() }}</div>
        }

        <!-- ========================================================================= -->
        <!-- 1. VISTA EJECUTIVA PARA ADMIN Y SUPER_ADMIN (PESTAÑAS DE GOBERNANZA)      -->
        <!-- ========================================================================= -->
        @if (authService.tieneRol('ADMIN')) {
          <div class="gov-tabs" role="tablist" aria-label="Módulos de administración y parametrización">
            <button
              type="button"
              class="gov-tab"
              [class.active]="pestanaAdmin() === 'FUNDACIONES'"
              (click)="cambiarPestanaAdmin('FUNDACIONES')"
            >
              1. Aprobación de Fundaciones (OSAL)
            </button>
            <button
              type="button"
              class="gov-tab"
              [class.active]="pestanaAdmin() === 'USUARIOS'"
              (click)="cambiarPestanaAdmin('USUARIOS')"
            >
              2. Administración de Usuarios y Contraseñas
            </button>
            @if (authService.tieneRol('SUPER_ADMIN')) {
              <button
                type="button"
                class="gov-tab"
                [class.active]="pestanaAdmin() === 'PARAMETRIZACION'"
                (click)="cambiarPestanaAdmin('PARAMETRIZACION')"
              >
                3. Parametrización de la Plataforma (Superusuario)
              </button>
            }
            <button
              type="button"
              class="gov-tab"
              [class.active]="pestanaAdmin() === 'CUENTA'"
              (click)="cambiarPestanaAdmin('CUENTA')"
            >
              Mi Cuenta y Bitácora
            </button>
          </div>

          <!-- PESTAÑA 1: APROBACIÓN DE FUNDACIONES -->
          @if (pestanaAdmin() === 'FUNDACIONES') {
            <section class="cs-card admin-gov-card" aria-label="Solicitudes de fundaciones pendientes de revisión">
              <div class="card-head">
                <div>
                  <h2>Revisión Documental y Aprobación de Fundaciones (OSAL)</h2>
                  <p class="sub-head">Verifica el RUT y el Certificado de Existencia de cada organización para habilitar la publicación de sus campañas.</p>
                </div>
                <span class="sap-badge sap-badge-info">{{ fundaciones().length }} Expediente(s)</span>
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
                          [class.sap-badge-warn]="f.estado_validacion === 'PENDIENTE' || f.estado_validacion === 'RECHAZADA'"
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
                        Aprobar Fundación
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

          <!-- PESTAÑA 2: ADMINISTRACIÓN DE USUARIOS Y RESTABLECIMIENTO DE CONTRASEÑAS -->
          @if (pestanaAdmin() === 'USUARIOS') {
            <div class="users-layout">
              <section class="cs-card admin-gov-card">
                <div class="card-head">
                  <div>
                    <h2>Crear Nuevo Usuario / Administrador</h2>
                    <p class="sub-head">
                      {{ authService.tieneRol('SUPER_ADMIN')
                        ? 'Como Superusuario puedes crear Administradores de Plataforma (ADMIN) y cuentas operativas.'
                        : 'Como Administrador puedes registrar cuentas operativas de Voluntarios, Donantes y Representantes.' }}
                    </p>
                  </div>
                </div>

                <form (ngSubmit)="crearUsuarioDesdeAdmin()" novalidate>
                  <div class="form-group">
                    <label for="u_rol" class="sap-form-label">Rol a Asignar *</label>
                    <select id="u_rol" name="u_rol" class="sap-input" [(ngModel)]="nuevoUsuarioForm.rol_codigo">
                      @if (authService.tieneRol('SUPER_ADMIN')) {
                        <option value="ADMIN">Administrador de la Plataforma (ADMIN)</option>
                        <option value="SUPER_ADMIN">Superusuario de la Plataforma (SUPER_ADMIN)</option>
                      }
                      <option value="VOLUNTARIO">Voluntario Comunitario</option>
                      <option value="DONANTE">Donante Solidario</option>
                      <option value="REPRESENTANTE_OSAL">Representante de Fundación (OSAL)</option>
                    </select>
                  </div>

                  <div class="grid-2">
                    <div class="form-group">
                      <label for="u_nom" class="sap-form-label">Nombres *</label>
                      <input id="u_nom" name="u_nom" type="text" class="sap-input" [(ngModel)]="nuevoUsuarioForm.nombres" required />
                    </div>
                    <div class="form-group">
                      <label for="u_ape" class="sap-form-label">Apellidos *</label>
                      <input id="u_ape" name="u_ape" type="text" class="sap-input" [(ngModel)]="nuevoUsuarioForm.apellidos" required />
                    </div>
                  </div>

                  <div class="grid-2">
                    <div class="form-group">
                      <label for="u_doc" class="sap-form-label">Documento de Identidad</label>
                      <input id="u_doc" name="u_doc" type="text" class="sap-input" [(ngModel)]="nuevoUsuarioForm.numero_documento" placeholder="Ej: 1020304050" />
                    </div>
                    <div class="form-group">
                      <label for="u_tel" class="sap-form-label">Teléfono de Contacto</label>
                      <input id="u_tel" name="u_tel" type="text" class="sap-input" [(ngModel)]="nuevoUsuarioForm.telefono_contacto" placeholder="Ej: 3101234567" />
                    </div>
                  </div>

                  <div class="grid-2">
                    <div class="form-group">
                      <label for="u_cor" class="sap-form-label">Correo Electrónico *</label>
                      <input id="u_cor" name="u_cor" type="email" class="sap-input" [(ngModel)]="nuevoUsuarioForm.correo_electronico" placeholder="usuario@conexion.org" required />
                    </div>
                    <div class="form-group">
                      <label for="u_pas" class="sap-form-label">Contraseña Inicial (mín. 6 caracteres) *</label>
                      <input id="u_pas" name="u_pas" type="password" class="sap-input" [(ngModel)]="nuevoUsuarioForm.contrasena" placeholder="Define contraseña inicial" required />
                    </div>
                  </div>

                  <button type="submit" class="cs-btn btn-full">Crear Cuenta de Usuario</button>
                </form>
              </section>

              <section class="cs-card admin-gov-card">
                <div class="card-head">
                  <div>
                    <h2>Directorio de Usuarios y Control de Acceso</h2>
                    <p class="sub-head">Restablece contraseñas olvidadas, desbloquea cuentas por intentos fallidos o suspende accesos.</p>
                  </div>
                  <span class="sap-badge sap-badge-ok">{{ usuariosSistema().length }} Cuentas</span>
                </div>

                <div class="osal-approval-list">
                  @for (u of usuariosSistema(); track u.id) {
                    <article class="user-gov-row">
                      <div class="user-main">
                        <div class="osal-title-line">
                          <strong>{{ u.nombre_completo }}</strong>
                          @for (r of u.roles; track r) {
                            <span class="sap-badge sap-badge-info">{{ r }}</span>
                          }
                          <span
                            class="sap-badge"
                            [class.sap-badge-ok]="u.esta_activo"
                            [class.sap-badge-warn]="!u.esta_activo"
                          >
                            {{ u.esta_activo ? 'Activa' : 'Bloqueada / Suspendida' }}
                          </span>
                        </div>
                        <p class="osal-meta">
                          ✉️ {{ u.correo_electronico }} · 🪪 Doc: {{ u.documento }} · 📞 {{ u.telefono }} · Intentos fallidos: {{ u.intentos_fallidos }}
                        </p>
                      </div>

                      <div class="user-actions">
                        <input
                          type="password"
                          class="sap-input input-sm"
                          [(ngModel)]="nuevasClaves[u.id]"
                          placeholder="Nueva clave (mín. 6)"
                          aria-label="Nueva contraseña para el usuario"
                        />
                        <button type="button" class="cs-btn btn-sm" (click)="restablecerClave(u.id)">
                          Restablecer Contraseña
                        </button>
                        <button
                          type="button"
                          class="sap-btn-secondary btn-sm"
                          (click)="alternarEstadoUsuario(u)"
                        >
                          {{ u.esta_activo ? 'Suspender' : 'Reactivar / Desbloquear' }}
                        </button>
                      </div>
                    </article>
                  }
                </div>
              </section>
            </div>
          }

          <!-- PESTAÑA 3: PARAMETRIZACIÓN DE LA PLATAFORMA (EXCLUSIVO SUPER_ADMIN) -->
          @if (pestanaAdmin() === 'PARAMETRIZACION' && authService.tieneRol('SUPER_ADMIN')) {
            <section class="cs-card admin-gov-card">
              <div class="card-head">
                <div>
                  <h2>Parámetros Globales de Reglas de Negocio y Seguridad</h2>
                  <p class="sub-head">Ajusta topes mínimos de donación, límite de intentos de acceso y la norma tributaria impresa en los certificados PDF.</p>
                </div>
                <span class="sap-badge sap-badge-info">Exclusivo Superusuario</span>
              </div>

              <div class="osal-approval-list">
                @for (p of catalogos()?.parametros_sistema || []; track p.id) {
                  <article class="param-row">
                    <div>
                      <strong>{{ p.clave }}</strong>
                      <p class="osal-meta">{{ p.descripcion }}</p>
                    </div>
                    <div class="param-controls">
                      <input type="text" class="sap-input" [(ngModel)]="p.valor" [name]="'param_' + p.id" />
                      <button type="button" class="cs-btn btn-sm" (click)="guardarParametro(p.clave, p.valor)">
                        Guardar Parámetro
                      </button>
                    </div>
                  </article>
                }
              </div>
            </section>

            <div class="param-grid-3">
              <!-- Unidades de Medida -->
              <section class="cs-card admin-gov-card">
                <div class="card-head">
                  <h2>Unidades de Recolección</h2>
                </div>
                <form (ngSubmit)="agregarUnidadMedida()" class="mini-form">
                  <input type="text" class="sap-input" [(ngModel)]="nuevaUnidad.simbolo" name="um_sim" placeholder="Símbolo (ej: LT, KG, CAJA)" required />
                  <input type="text" class="sap-input" [(ngModel)]="nuevaUnidad.nombre" name="um_nom" placeholder="Nombre (ej: Litros (L))" required />
                  <button type="submit" class="cs-btn btn-sm">+ Agregar Unidad</button>
                </form>
                <div class="chips-wrap">
                  @for (um of catalogos()?.unidades_medida || []; track um.id) {
                    <span class="doc-chip">⚖️ <strong>{{ um.simbolo }}</strong> · {{ um.nombre }}</span>
                  }
                </div>
              </section>

              <!-- Categorías de Causas -->
              <section class="cs-card admin-gov-card">
                <div class="card-head">
                  <h2>Categorías de Causas</h2>
                </div>
                <form (ngSubmit)="agregarCategoriaCausa()" class="mini-form">
                  <input type="text" class="sap-input" [(ngModel)]="nuevaCategoria.nombre" name="cat_nom" placeholder="Nombre de la línea (ej: Agua Potable)" required />
                  <input type="text" class="sap-input" [(ngModel)]="nuevaCategoria.descripcion" name="cat_desc" placeholder="Descripción breve" />
                  <button type="submit" class="cs-btn btn-sm">+ Agregar Categoría</button>
                </form>
                <div class="chips-wrap">
                  @for (c of catalogos()?.categorias_causas || []; track c.id) {
                    <span class="doc-chip">🏷️ {{ c.nombre }}</span>
                  }
                </div>
              </section>

              <!-- Franjas Horarias y Habilidades -->
              <section class="cs-card admin-gov-card">
                <div class="card-head">
                  <h2>Franjas Horarias Voluntariado</h2>
                </div>
                <form (ngSubmit)="agregarFranjaHoraria()" class="mini-form">
                  <input type="text" class="sap-input" [(ngModel)]="nuevaFranja.nombre" name="fr_nom" placeholder="Ej: Domingos en la mañana (8am - 12m)" required />
                  <input type="number" min="1" max="12" class="sap-input" [(ngModel)]="nuevaFranja.horas_sugeridas" name="fr_hor" placeholder="Horas" />
                  <button type="submit" class="cs-btn btn-sm">+ Agregar Franja</button>
                </form>
                <div class="chips-wrap">
                  @for (fh of catalogos()?.franjas_horarias || []; track fh.id) {
                    <span class="doc-chip">🕒 {{ fh.nombre }}</span>
                  }
                </div>
              </section>
            </div>
          }
        }

        <!-- ========================================================================= -->
        <!-- 2. DASHBOARD RESUMEN PERSONAL DEL VOLUNTARIO AL INICIAR SESIÓN            -->
        <!-- ========================================================================= -->
        @if (resumenVoluntario(); as rv) {
          <section class="role-dashboard" aria-label="Resumen operativo del voluntario">
            <div class="kpi-strip">
              <article class="cs-card kpi-mini">
                <span class="kpi-lbl">Disponibilidad Semanal</span>
                <strong>{{ rv.disponibilidad_horas_semana }} Horas / Semana</strong>
                <small>📍 {{ rv.municipio }} ({{ rv.vereda }})</small>
              </article>
              <article class="cs-card kpi-mini">
                <span class="kpi-lbl">Horas Comprometidas</span>
                <strong>{{ rv.horas_comprometidas }} Horas Asignadas</strong>
                <small>{{ rv.postulaciones.length }} postulación(es) activa(s)</small>
              </article>
              <article class="cs-card kpi-mini highlight">
                <span class="kpi-lbl">Cupo Horario Libre</span>
                <strong>{{ rv.horas_disponibles_restantes }} Horas Disponibles</strong>
                <small>Para nuevas actividades comunitarias</small>
              </article>
              <article class="cs-card kpi-mini">
                <span class="kpi-lbl">Mis Competencias</span>
                <strong>{{ rv.competencias.length }} Habilidad(es)</strong>
                <small>{{ rv.dispuesto_desplazamiento_rural ? 'Habilitado desplazamiento veredal' : 'Zona local' }}</small>
              </article>
            </div>

            <div class="sap-grid">
              <article class="cs-card sap-object-card">
                <div class="card-head">
                  <h2>Mis Postulaciones y Tareas Asignadas</h2>
                  <a routerLink="/voluntariado" class="cs-btn btn-sm">+ Postularme a Nueva Actividad</a>
                </div>

                @if (rv.postulaciones.length === 0) {
                  <p class="empty-note">Aún no te has postulado a ninguna actividad comunitaria. Haz clic en "+ Postularme a Nueva Actividad" para elegir una labor en la Sabana Norte.</p>
                } @else {
                  <div class="osal-approval-list">
                    @for (p of rv.postulaciones; track p.id) {
                      <div class="summary-item">
                        <div class="osal-title-line">
                          <strong>{{ p.labor_descripcion }}</strong>
                          <span class="sap-badge sap-badge-ok">{{ p.horas_comprometidas }} h ({{ p.estado_postulacion }})</span>
                        </div>
                        <p class="osal-meta">
                          🏢 {{ p.fundacion_nombre }} · Campaña: {{ p.campana_titulo }}<br/>
                          🕒 Franja elegida: {{ p.disponibilidad_propuesta }}
                        </p>
                      </div>
                    }
                  </div>
                }
              </article>

              <article class="cs-card sap-object-card">
                <div class="card-head">
                  <h2>Mis Competencias Registradas</h2>
                  <a routerLink="/perfil-habilidades" class="sap-btn-secondary btn-sm">Editar Mis Competencias</a>
                </div>
                <p class="osal-meta" style="margin-bottom:0.85rem;">{{ rv.biografia_corta }}</p>

                @if (rv.competencias.length === 0) {
                  <p class="empty-note">No has asociado habilidades todavía. Configura tu matriz de competencias para mejorar tu perfil.</p>
                } @else {
                  <div class="osal-approval-list">
                    @for (c of rv.competencias; track c.id) {
                      <div class="summary-item">
                        <div class="osal-title-line">
                          <strong>{{ c.habilidad_nombre }}</strong>
                          <span class="sap-badge sap-badge-info">{{ c.nivel_dominio }}</span>
                        </div>
                        <p class="osal-meta">Categoría: {{ c.categoria_nombre }} · Experiencia: {{ c.anos_experiencia }} año(s)</p>
                      </div>
                    }
                  </div>
                }
              </article>
            </div>
          </section>
        }

        <!-- ========================================================================= -->
        <!-- 3. DASHBOARD RESUMEN PERSONAL DEL DONANTE AL INICIAR SESIÓN               -->
        <!-- ========================================================================= -->
        @if (resumenDonante(); as rd) {
          <section class="role-dashboard" aria-label="Resumen de aportes y certificados del donante">
            <div class="kpi-strip">
              <article class="cs-card kpi-mini highlight">
                <span class="kpi-lbl">Total Aportado Verificado</span>
                <strong>\${{ rd.total_donado_cop | number:'1.0-0' }} COP</strong>
                <small>Certificado bajo Art. 125-2 y 257 E.T.</small>
              </article>
              <article class="cs-card kpi-mini">
                <span class="kpi-lbl">Transacciones Registradas</span>
                <strong>{{ rd.total_aportes }} Aporte(s)</strong>
                <small>Monetarios y en especie</small>
              </article>
              <article class="cs-card kpi-mini">
                <span class="kpi-lbl">Tipo de Contribuyente</span>
                <strong>{{ rd.tipo_donante === 'EMPRESA' ? 'Persona Jurídica / Empresa' : 'Persona Natural' }}</strong>
                <small>{{ rd.empresa_organizacion || 'Certificación tributaria activa' }}</small>
              </article>
            </div>

            <section class="cs-card admin-gov-card">
              <div class="card-head">
                <div>
                  <h2>Mis Aportes y Certificados Tributarios</h2>
                  <p class="sub-head">Descarga tus comprobantes electrónicos en PDF o solicita su envío inmediato a tu correo.</p>
                </div>
                <a routerLink="/donar" class="cs-btn btn-sm">+ Registrar Nuevo Aporte</a>
              </div>

              @if (rd.aportes_recientes.length === 0) {
                <p class="empty-note">Aún no has registrado donaciones desde tu cuenta. Haz clic en "+ Registrar Nuevo Aporte" para apoyar una causa de la región.</p>
              } @else {
                <div class="osal-approval-list">
                  @for (a of rd.aportes_recientes; track a.id) {
                    <article class="osal-approval-row">
                      <div>
                        <div class="osal-title-line">
                          <strong>{{ a.codigo_referencia }} · {{ a.campana_titulo }}</strong>
                          <span class="sap-badge sap-badge-info">{{ a.modalidad === 'ECONOMICA' ? 'Aporte Monetario' : 'Aporte en Especie' }}</span>
                        </div>
                        <p class="osal-meta">
                          Fundación: {{ a.fundacion_nombre }} ·
                          @if (a.monto_cop) {
                            Importe: <strong>\${{ a.monto_cop | number:'1.0-0' }} COP</strong> · Certificado: {{ a.consecutivo_tributario }}
                          }
                          @if (a.especie_detalle) {
                            Insumos: <strong>{{ a.especie_detalle }}</strong> (Estado: {{ a.estado_logistico }})
                          }
                        </p>
                      </div>
                      <div class="osal-actions">
                        @if (a.donacion_economica_id) {
                          <a
                            class="cs-btn btn-sm"
                            [href]="apiBaseUrl + '/donaciones/economicas/' + a.donacion_economica_id + '/certificado-pdf'"
                            target="_blank"
                            rel="noopener"
                          >
                            📄 Descargar PDF
                          </a>
                        }
                        <a routerLink="/donar" class="sap-btn-secondary btn-sm">Ver en Libro de Transacciones</a>
                      </div>
                    </article>
                  }
                </div>
              }
            </section>
          </section>
        }

        <!-- ========================================================================= -->
        <!-- 4. DATOS DE MI CUENTA Y ACTIVIDAD RECIENTE (TODOS LOS ROLES)              -->
        <!-- ========================================================================= -->
        @if (!authService.tieneRol('ADMIN') || pestanaAdmin() === 'CUENTA') {
          <section class="sap-grid" aria-label="Información de mi cuenta y actividad reciente">
            <article class="cs-card sap-object-card">
              <div class="card-head">
                <h2>Datos de mi Cuenta</h2>
                <span class="sap-badge sap-badge-ok">Activa</span>
              </div>

              <div class="kv-grid">
                <div class="kv-item">
                  <span class="kv-label">Correo Electrónico</span>
                  <strong class="kv-value">{{ usuario.correo_electronico }}</strong>
                </div>
                <div class="kv-item">
                  <span class="kv-label">Tipo de Usuario</span>
                  <strong class="kv-value">{{ authService.etiquetaRolPrincipal() }}</strong>
                </div>
                <div class="kv-item">
                  <span class="kv-label">Alcance y Permisos</span>
                  <strong class="kv-value">
                    @if (authService.tieneRol('SUPER_ADMIN')) {
                      Creación de administradores, gestión total de usuarios y parametrización de catálogos
                    } @else if (authService.tieneRol('ADMIN')) {
                      Aprobación de fundaciones, administración de cuentas operativas y restablecimiento de claves
                    } @else if (authService.tieneRol('REPRESENTANTE_OSAL')) {
                      Publicación de campañas con unidades de medida, tablero de fundación y logística en especie
                    } @else if (authService.tieneRol('VOLUNTARIO')) {
                      Resumen personal, matriz de competencias y postulación a actividades según cupo horario
                    } @else if (authService.tieneRol('DONANTE')) {
                      Resumen personal, registro de aportes verificados y descarga/envío de certificados PDF
                    }
                  </strong>
                </div>
                <div class="kv-item">
                  <span class="kv-label">Organización o Perfil Asociado</span>
                  <strong class="kv-value">
                    {{ usuario.fundacion_nombre ? usuario.fundacion_nombre + ' (' + usuario.fundacion_estado + ')' : '' }}
                    {{ usuario.donante_id ? 'Donante Solidario Registrado' : '' }}
                    {{ usuario.voluntario_id ? 'Voluntario Comunitario Registrado' : '' }}
                    {{ authService.tieneRol('SUPER_ADMIN') ? 'Dirección Técnica y Parametrización' : (authService.tieneRol('ADMIN') ? 'Coordinación General Sabana Norte' : '') }}
                  </strong>
                </div>
              </div>
            </article>

            <article class="cs-card sap-object-card">
              <div class="card-head">
                <h2>Actividad Reciente en la Plataforma</h2>
                <span class="sap-badge sap-badge-info">Historial</span>
              </div>

              @if (auditoria().length === 0) {
                <p class="empty-note">Cargando actividad reciente...</p>
              } @else {
                <div class="audit-table">
                  @for (evento of auditoria(); track evento.id) {
                    <div class="audit-row">
                      <div class="audit-main">
                        <span
                          class="sap-badge"
                          [class.sap-badge-ok]="!evento.accion.includes('FALLIDO') && !evento.accion.includes('RESTRINGIDO')"
                          [class.sap-badge-warn]="evento.accion.includes('FALLIDO') || evento.accion.includes('RESTRINGIDO')"
                        >
                          {{ formatearAccion(evento.accion) }}
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
        }
      </main>
    }
  `,
  styles: [`
    .header-actions { display: flex; flex-wrap: wrap; gap: 0.65rem; align-items: center; }
    .btn-logout { border-color: var(--sap-status-err-border); color: var(--sap-status-err-text); }
    .alert-ok {
      border-left: 5px solid #15803D;
      background: #DCFCE7;
      color: #14532D;
      padding: 0.9rem 1.2rem;
      border-radius: 6px;
      font-weight: 700;
      margin-bottom: 1.25rem;
    }
    .alert-err {
      border-left: 5px solid #B91C1C;
      background: #FEE2E2;
      color: #7F1D1D;
      padding: 0.9rem 1.2rem;
      border-radius: 6px;
      font-weight: 700;
      margin-bottom: 1.25rem;
    }
    .gov-tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 0.6rem;
      margin-bottom: 1.35rem;
    }
    .gov-tab {
      min-height: 44px;
      padding: 0.6rem 1.1rem;
      font-weight: 700;
      font-size: 0.9rem;
      border: 1px solid var(--sap-border-subtle);
      border-bottom: 3px solid var(--sap-border-subtle);
      background: var(--sap-bg-surface);
      color: var(--sap-text-secondary);
      border-radius: 6px;
      cursor: pointer;
    }
    .gov-tab.active {
      color: var(--sap-brand-primary);
      border-bottom-color: var(--sap-brand-primary);
      background: #F8FAFC;
    }
    .users-layout {
      display: grid;
      grid-template-columns: 1fr 1.55fr;
      gap: 1.5rem;
      align-items: start;
    }
    @media (max-width: 980px) {
      .users-layout { grid-template-columns: 1fr; }
    }
    .param-grid-3 {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
      gap: 1.25rem;
    }
    .mini-form {
      display: flex;
      flex-direction: column;
      gap: 0.55rem;
      margin-bottom: 1rem;
    }
    .chips-wrap {
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
    }
    .param-row {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      padding: 0.85rem 1rem;
      background: var(--sap-bg-canvas);
      border: 1px solid var(--sap-border-subtle);
      border-radius: 6px;
    }
    .param-controls {
      display: flex;
      gap: 0.6rem;
      align-items: center;
      min-width: 320px;
      flex: 1;
      max-width: 480px;
    }
    .role-dashboard { margin-bottom: 1.5rem; }
    .kpi-strip {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1rem;
      margin-bottom: 1.35rem;
    }
    .kpi-mini {
      border-top: 3px solid var(--sap-brand-primary);
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }
    .kpi-mini.highlight {
      border-top-color: #15803D;
      background: #F0FDF4;
    }
    .kpi-lbl { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.03em; color: var(--sap-text-secondary); font-weight: 700; }
    .kpi-mini strong { font-size: 1.3rem; color: var(--sap-text-primary); }
    .kpi-mini small { font-size: 0.8rem; color: var(--sap-text-secondary); }
    .summary-item {
      padding: 0.85rem 1rem;
      background: var(--sap-bg-canvas);
      border: 1px solid var(--sap-border-subtle);
      border-radius: 6px;
    }
    .admin-gov-card {
      border-top: 4px solid var(--sap-brand-primary);
      margin-bottom: 1.5rem;
    }
    .sub-head { margin: 0.25rem 0 0 0; font-size: 0.86rem; color: var(--sap-text-secondary); }
    .osal-approval-list { display: flex; flex-direction: column; gap: 0.85rem; }
    .osal-approval-row, .user-gov-row {
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
    .osal-title-line { display: flex; align-items: center; gap: 0.55rem; flex-wrap: wrap; margin-bottom: 0.3rem; }
    .osal-meta { margin: 0 0 0.4rem 0; font-size: 0.86rem; color: var(--sap-text-secondary); line-height: 1.4; }
    .docs-chips { display: flex; flex-wrap: wrap; gap: 0.5rem; }
    .doc-chip {
      font-size: 0.78rem;
      font-weight: 600;
      padding: 0.25rem 0.6rem;
      background: #FFFFFF;
      border: 1px solid var(--sap-border-subtle);
      border-radius: 4px;
    }
    .osal-actions, .user-actions { display: flex; gap: 0.55rem; flex-wrap: wrap; align-items: center; }
    .input-sm { max-width: 170px; min-height: 36px; padding: 0.3rem 0.6rem; font-size: 0.84rem; }
    .btn-sm { min-height: 36px; padding: 0.35rem 0.8rem; font-size: 0.82rem; }
    .btn-reject { border-color: var(--sap-status-err-border); color: var(--sap-status-err-text); }
    .form-group { margin-bottom: 0.85rem; }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.75rem; }
    .btn-full { width: 100%; margin-top: 0.4rem; }
    .sap-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
      gap: 1.5rem;
    }
    .sap-object-card { border-top: 3px solid var(--sap-brand-primary); }
    .card-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 0.85rem;
      margin-bottom: 1rem;
      border-bottom: 1px solid var(--sap-border-subtle);
    }
    .card-head h2 { margin: 0; font-size: 1.1rem; }
    .kv-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
    .kv-item { display: flex; flex-direction: column; gap: 0.2rem; }
    .kv-label { font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--sap-text-secondary); font-weight: 600; }
    .kv-value { font-size: 0.94rem; color: var(--sap-text-primary); }
    .audit-table { display: flex; flex-direction: column; gap: 0.5rem; }
    .audit-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.75rem;
      padding: 0.55rem 0.75rem;
      background: var(--sap-bg-canvas);
      border: 1px solid var(--sap-border-subtle);
      border-radius: 4px;
      font-size: 0.84rem;
    }
    .audit-main { display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap; }
    .audit-time { font-family: monospace; font-size: 0.78rem; color: var(--sap-text-secondary); white-space: nowrap; }
  `]
})
export class PanelProtegidoComponent implements OnInit {
  readonly authService = inject(AuthService);
  private readonly http = inject(HttpClient);
  private readonly route = inject(ActivatedRoute);
  private readonly offlineSync = inject(OfflineSyncService);
  readonly apiBaseUrl = getApiBaseUrl();

  pestanaAdmin = signal<'FUNDACIONES' | 'USUARIOS' | 'PARAMETRIZACION' | 'CUENTA'>('FUNDACIONES');
  catalogos = signal<CatalogosGenerales | null>(null);

  auditoria = signal<Array<{ id: number; accion: string; detalle: string; fecha_evento: string }>>([]);
  fundaciones = signal<FundacionExpediente[]>([]);
  usuariosSistema = signal<UsuarioDirectorioItem[]>([]);
  resumenVoluntario = signal<any | null>(null);
  resumenDonante = signal<any | null>(null);

  avisoRestringido = signal(false);
  mensajeExito = signal('');
  mensajeError = signal('');

  nuevasClaves: Record<number, string> = {};

  nuevoUsuarioForm = {
    rol_codigo: 'VOLUNTARIO',
    nombres: '',
    apellidos: '',
    numero_documento: '',
    telefono_contacto: '',
    correo_electronico: '',
    contrasena: '',
    municipio_id: 6,
  };

  nuevaUnidad = { simbolo: '', nombre: '' };
  nuevaCategoria = { nombre: '', descripcion: '' };
  nuevaFranja = { nombre: '', horas_sugeridas: 4 };

  ngOnInit(): void {
    this.route.queryParamMap.subscribe((params) => {
      this.avisoRestringido.set(params.get('acceso_restringido') === 'true');
    });

    if (this.authService.tieneRol('SUPER_ADMIN')) {
      this.nuevoUsuarioForm.rol_codigo = 'ADMIN';
    }

    this.cargarCatalogos();
    this.cargarPerfilYResumen();

    if (this.authService.tieneRol('ADMIN')) {
      this.cargarFundacionesParaGobernanza();
      this.cargarUsuariosSistema();
    }
  }

  cambiarPestanaAdmin(tab: 'FUNDACIONES' | 'USUARIOS' | 'PARAMETRIZACION' | 'CUENTA'): void {
    this.mensajeExito.set('');
    this.mensajeError.set('');
    this.pestanaAdmin.set(tab);
  }

  cargarCatalogos(): void {
    this.offlineSync.obtenerCatalogos().subscribe((cat) => this.catalogos.set(cat));
  }

  cargarPerfilYResumen(): void {
    this.authService.obtenerPerfilremoto().subscribe({
      next: (res) => {
        this.auditoria.set(res.auditoria_reciente);
        this.resumenVoluntario.set(res.resumen_voluntario || null);
        this.resumenDonante.set(res.resumen_donante || null);
      },
      error: () => {
        this.auditoria.set([
          {
            id: 1,
            accion: 'SESION_ACTIVA',
            detalle: 'Sesión verificada en la plataforma Conexión Solidaria.',
            fecha_evento: new Date().toISOString(),
          },
        ]);
      },
    });
  }

  cargarFundacionesParaGobernanza(): void {
    this.http.get<{ fundaciones: FundacionExpediente[] }>(`${this.apiBaseUrl}/osal`).subscribe({
      next: (res) => this.fundaciones.set(res.fundaciones),
      error: () => {},
    });
  }

  cargarUsuariosSistema(): void {
    this.http.get<{ usuarios: UsuarioDirectorioItem[] }>(`${this.apiBaseUrl}/auth/usuarios`).subscribe({
      next: (res) => this.usuariosSistema.set(res.usuarios),
      error: () => {},
    });
  }

  cambiarEstadoOsal(fundacionId: number, nuevoEstado: 'APROBADA' | 'RECHAZADA'): void {
    this.mensajeExito.set('');
    this.mensajeError.set('');
    this.http
      .put<{ mensaje_humano: string }>(`${this.apiBaseUrl}/osal/${fundacionId}/estado-validacion`, {
        estado_validacion: nuevoEstado,
        observacion: `Revisión documental: ${nuevoEstado}`,
      })
      .subscribe({
        next: (res) => {
          this.mensajeExito.set(res.mensaje_humano);
          this.cargarFundacionesParaGobernanza();
        },
        error: (err) => {
          this.mensajeError.set(err.error?.mensaje_humano || 'No se pudo actualizar el estado de la fundación.');
        },
      });
  }

  crearUsuarioDesdeAdmin(): void {
    this.mensajeExito.set('');
    this.mensajeError.set('');

    if (!this.nuevoUsuarioForm.nombres.trim() || !this.nuevoUsuarioForm.apellidos.trim() || !this.nuevoUsuarioForm.correo_electronico.trim() || !this.nuevoUsuarioForm.contrasena.trim()) {
      this.mensajeError.set('Por favor completa nombres, apellidos, correo electrónico y contraseña inicial.');
      return;
    }

    this.http.post<{ mensaje_humano: string }>(`${this.apiBaseUrl}/auth/usuarios`, this.nuevoUsuarioForm).subscribe({
      next: (res) => {
        this.mensajeExito.set(res.mensaje_humano);
        this.nuevoUsuarioForm.nombres = '';
        this.nuevoUsuarioForm.apellidos = '';
        this.nuevoUsuarioForm.numero_documento = '';
        this.nuevoUsuarioForm.telefono_contacto = '';
        this.nuevoUsuarioForm.correo_electronico = '';
        this.nuevoUsuarioForm.contrasena = '';
        this.cargarUsuariosSistema();
      },
      error: (err) => {
        this.mensajeError.set(err.error?.mensaje_humano || 'No se pudo crear la cuenta de usuario.');
      },
    });
  }

  restablecerClave(usuarioId: number): void {
    this.mensajeExito.set('');
    this.mensajeError.set('');
    const clave = (this.nuevasClaves[usuarioId] || '').trim();
    if (clave.length < 6) {
      this.mensajeError.set('Escribe una nueva contraseña de al menos 6 caracteres en la casilla junto al usuario.');
      return;
    }

    this.http
      .put<{ mensaje_humano: string }>(`${this.apiBaseUrl}/auth/usuarios/${usuarioId}/restablecer-clave`, {
        nueva_contrasena: clave,
      })
      .subscribe({
        next: (res) => {
          this.mensajeExito.set(res.mensaje_humano);
          this.nuevasClaves[usuarioId] = '';
          this.cargarUsuariosSistema();
        },
        error: (err) => {
          this.mensajeError.set(err.error?.mensaje_humano || 'No fue posible restablecer la contraseña.');
        },
      });
  }

  alternarEstadoUsuario(u: UsuarioDirectorioItem): void {
    this.mensajeExito.set('');
    this.mensajeError.set('');
    this.http
      .put<{ mensaje_humano: string }>(`${this.apiBaseUrl}/auth/usuarios/${u.id}/estado`, {
        esta_activo: !u.esta_activo,
      })
      .subscribe({
        next: (res) => {
          this.mensajeExito.set(res.mensaje_humano);
          this.cargarUsuariosSistema();
        },
        error: (err) => {
          this.mensajeError.set(err.error?.mensaje_humano || 'No fue posible cambiar el estado de la cuenta.');
        },
      });
  }

  guardarParametro(clave: string, valor: string): void {
    this.mensajeExito.set('');
    this.mensajeError.set('');
    this.http
      .put<{ mensaje_humano: string }>(`${this.apiBaseUrl}/catalogos/parametros`, { clave, valor })
      .subscribe({
        next: (res) => {
          this.mensajeExito.set(res.mensaje_humano);
          this.cargarCatalogos();
        },
        error: (err) => {
          this.mensajeError.set(err.error?.mensaje_humano || 'No se pudo actualizar el parámetro.');
        },
      });
  }

  agregarUnidadMedida(): void {
    if (!this.nuevaUnidad.simbolo.trim() || !this.nuevaUnidad.nombre.trim()) return;
    this.http.post<{ mensaje_humano: string }>(`${this.apiBaseUrl}/catalogos/unidades-medida`, this.nuevaUnidad).subscribe({
      next: (res) => {
        this.mensajeExito.set(res.mensaje_humano);
        this.nuevaUnidad = { simbolo: '', nombre: '' };
        this.cargarCatalogos();
      },
      error: (err) => this.mensajeError.set(err.error?.mensaje_humano || 'Error al agregar unidad.'),
    });
  }

  agregarCategoriaCausa(): void {
    if (!this.nuevaCategoria.nombre.trim()) return;
    this.http.post<{ mensaje_humano: string }>(`${this.apiBaseUrl}/catalogos/categorias-causas`, this.nuevaCategoria).subscribe({
      next: (res) => {
        this.mensajeExito.set(res.mensaje_humano);
        this.nuevaCategoria = { nombre: '', descripcion: '' };
        this.cargarCatalogos();
      },
      error: (err) => this.mensajeError.set(err.error?.mensaje_humano || 'Error al agregar categoría.'),
    });
  }

  agregarFranjaHoraria(): void {
    if (!this.nuevaFranja.nombre.trim()) return;
    this.http.post<{ mensaje_humano: string }>(`${this.apiBaseUrl}/catalogos/franjas-horarias`, this.nuevaFranja).subscribe({
      next: (res) => {
        this.mensajeExito.set(res.mensaje_humano);
        this.nuevaFranja = { nombre: '', horas_sugeridas: 4 };
        this.cargarCatalogos();
      },
      error: (err) => this.mensajeError.set(err.error?.mensaje_humano || 'Error al agregar franja horaria.'),
    });
  }

  formatearAccion(accion: string): string {
    const mapa: Record<string, string> = {
      INGRESO_AL_SISTEMA: 'Inicio de sesión',
      LOGIN_EXITOSO: 'Inicio de sesión',
      LOGIN_FALLIDO: 'Intento fallido',
      ACCESO_RESTRINGIDO: 'Sección restringida',
      ACCESO_DENEGADO_RBAC: 'Sección restringida',
      REGISTRO_VOLUNTARIO: 'Inscripción de voluntario',
      REGISTRO_DONANTE: 'Registro de donante',
      REGISTRO_OSAL_PENDIENTE: 'Solicitud de fundación',
      VALIDACION_OSAL_APROBADA: 'Fundación aprobada',
      VALIDACION_OSAL_RECHAZADA: 'Fundación rechazada',
      PUBLICAR_CAMPAÑA_Y_NECESIDADES: 'Campaña publicada',
      REGISTRO_DONACION_ECONOMICA: 'Donación monetaria',
      REGISTRO_DONACION_ESPECIE: 'Donación en especie',
      ENVIO_CERTIFICADO_CORREO: 'Certificado enviado por correo',
      POSTULACION_VOLUNTARIADO: 'Postulación a voluntariado',
      ACTUALIZAR_PERFIL_HABILIDADES: 'Habilidades actualizadas',
      ACTUALIZAR_TRAZABILIDAD_ESPECIE: 'Entrega actualizada',
      RESTABLECER_CONTRASENA_USUARIO: 'Contraseña restablecida',
      ACTUALIZAR_PARAMETRO_SISTEMA: 'Parámetro actualizado',
    };
    return mapa[accion] || accion.replace(/_/g, ' ');
  }
}
