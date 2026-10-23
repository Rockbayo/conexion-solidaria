import { Component, OnInit, inject, signal, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { OfflineSyncService, CatalogosGenerales } from '../../../core/services/offline-sync.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="sap-page-header">
      <div class="sap-page-header-inner">
        <div>
          <span class="sap-breadcrumb">Portal Comunitario · Sabana Norte de Cundinamarca</span>
          <h1 class="sap-page-title">Bienvenido a Conexión Solidaria</h1>
          <p class="sap-page-subtitle">
            Ingresa a tu cuenta o inscríbete para apoyar a las fundaciones y veredas de nuestra región.
          </p>
        </div>
        <div class="header-actions">
          <a routerLink="/registro-osal" class="sap-btn-secondary">
            Inscribir una Fundación (OSAL)
          </a>
          <button type="button" class="sap-btn-secondary" (click)="ingresarComoInvitado()">
            Explorar Mapa como Visitante
          </button>
        </div>
      </div>
    </div>

    <main class="sap-container auth-workspace" aria-labelledby="auth-heading">
      <div class="auth-tabs" role="tablist" aria-label="Opciones de ingreso y registro">
        <button
          type="button"
          role="tab"
          class="auth-tab"
          [class.active]="modoVista() === 'LOGIN'"
          (click)="cambiarModo('LOGIN')"
        >
          Iniciar Sesión
        </button>
        <button
          type="button"
          role="tab"
          class="auth-tab"
          [class.active]="modoVista() === 'REGISTRO_VOLUNTARIO'"
          (click)="cambiarModo('REGISTRO_VOLUNTARIO')"
        >
          Inscribirme como Voluntario
        </button>
        <button
          type="button"
          role="tab"
          class="auth-tab"
          [class.active]="modoVista() === 'REGISTRO_DONANTE'"
          (click)="cambiarModo('REGISTRO_DONANTE')"
        >
          Registrarme como Donante
        </button>
      </div>

      @if (mensajeConexionInestable()) {
        <div class="cs-alert-human" role="alert">
          {{ mensajeConexionInestable() }}
        </div>
      }

      @if (mensajeErrorHumano()) {
        <div class="alert-error" role="alert">
          {{ mensajeErrorHumano() }}
        </div>
      }

      @if (modoVista() === 'LOGIN') {
        <div class="login-split-grid">
          <section class="cs-card login-panel">
            <div class="panel-header">
              <h2 id="auth-heading">Ingresa con tu Cuenta</h2>
              <span class="sap-badge sap-badge-info">Acceso Seguro</span>
            </div>

            <form (ngSubmit)="procesarLogin()" novalidate>
              <div class="form-group">
                <label for="correo" class="sap-form-label">Correo electrónico</label>
                <input
                  id="correo"
                  name="correo"
                  type="email"
                  class="sap-input"
                  [(ngModel)]="correoElectronico"
                  placeholder="ejemplo@correo.org"
                  required
                  autocomplete="email"
                />
              </div>

              <div class="form-group">
                <label for="contrasena" class="sap-form-label">Contraseña</label>
                <input
                  id="contrasena"
                  name="contrasena"
                  type="password"
                  class="sap-input"
                  [(ngModel)]="contrasena"
                  placeholder="Escribe tu contraseña"
                  required
                  autocomplete="current-password"
                />
              </div>

              <button type="submit" class="cs-btn btn-block" [disabled]="cargando()">
                {{ cargando() ? 'Ingresando...' : 'Entrar a la Plataforma' }}
              </button>
            </form>
          </section>

          <section class="cs-card rbac-selector-panel" aria-label="Cuentas de demostración">
            <div class="panel-header">
              <h2>Acceso Rápido de Demostración</h2>
              <span class="sap-badge sap-badge-ok">Sabana Norte</span>
            </div>
            <p class="helper-desc">
              Selecciona un tipo de usuario para probar directamente sus funciones en la plataforma:
            </p>

            <div class="role-cards-list">
              <article class="role-option-card" (click)="cargarDemo('superadmin@conexion.org')">
                <div class="role-top">
                  <strong>Superusuario de la Plataforma</strong>
                  <span class="sap-badge sap-badge-info">Superusuario</span>
                </div>
                <p>Crea administradores de plataforma, gestiona usuarios y parametriza unidades, causas y catálogos.</p>
                <span class="role-cta">Probar con esta cuenta →</span>
              </article>

              <article class="role-option-card" (click)="cargarDemo('admin@conexion.org')">
                <div class="role-top">
                  <strong>Coordinación General (Administrador)</strong>
                  <span class="sap-badge sap-badge-info">Administración</span>
                </div>
                <p>Aprueba fundaciones inscritas, administra cuentas operativas y restablece contraseñas.</p>
                <span class="role-cta">Probar con esta cuenta →</span>
              </article>

              <article class="role-option-card" (click)="cargarDemo('osal@sabananorte.org')">
                <div class="role-top">
                  <strong>Representante de Fundación (OSAL)</strong>
                  <span class="sap-badge sap-badge-ok">Fundación en Cogua</span>
                </div>
                <p>Revisa los indicadores de su fundación, crea campañas y actualiza la entrega de ayudas.</p>
                <span class="role-cta">Probar con esta cuenta →</span>
              </article>

              <article class="role-option-card" (click)="cargarDemo('voluntario@conexion.org')">
                <div class="role-top">
                  <strong>Voluntario Comunitario</strong>
                  <span class="sap-badge sap-badge-ok">Voluntariado</span>
                </div>
                <p>Inscribe sus conocimientos y se postula para apoyar actividades en las veredas.</p>
                <span class="role-cta">Probar con esta cuenta →</span>
              </article>

              <article class="role-option-card" (click)="cargarDemo('donante@conexion.org')">
                <div class="role-top">
                  <strong>Donante Solidario</strong>
                  <span class="sap-badge sap-badge-info">Aportante en Tabio</span>
                </div>
                <p>Realiza aportes económicos o en especie y descarga sus certificados de donación en PDF.</p>
                <span class="role-cta">Probar con esta cuenta →</span>
              </article>
            </div>
          </section>
        </div>
      } @else {
        <section class="cs-card registro-panel">
          <div class="panel-header">
            <div>
              <h2>
                {{ modoVista() === 'REGISTRO_VOLUNTARIO'
                  ? 'Inscripción de Voluntario Comunitario'
                  : 'Registro de Donante Solidario' }}
              </h2>
              <p class="sub-note">
                Completa tus datos básicos para crear tu cuenta personal en Conexión Solidaria.
              </p>
            </div>
            <span class="sap-badge sap-badge-ok">Registro Gratuito</span>
          </div>

          <form (ngSubmit)="procesarRegistroCiudadano()" novalidate>
            <div class="grid-3">
              <div class="form-group">
                <label for="reg_nombres" class="sap-form-label">Nombres *</label>
                <input id="reg_nombres" name="reg_nombres" type="text" class="sap-input" [(ngModel)]="regForm.nombres" required />
              </div>
              <div class="form-group">
                <label for="reg_apellidos" class="sap-form-label">Apellidos *</label>
                <input id="reg_apellidos" name="reg_apellidos" type="text" class="sap-input" [(ngModel)]="regForm.apellidos" required />
              </div>
              <div class="form-group">
                <label for="reg_tel" class="sap-form-label">Teléfono / Celular *</label>
                <input id="reg_tel" name="reg_tel" type="tel" class="sap-input" [(ngModel)]="regForm.telefono_contacto" placeholder="Ej: 3158901234" required />
              </div>
            </div>

            <div class="grid-3">
              <div class="form-group">
                <label for="reg_td" class="sap-form-label">Tipo de Documento *</label>
                <select id="reg_td" name="reg_td" class="sap-input" [(ngModel)]="regForm.tipo_documento_id">
                  @for (td of catalogos()?.tipos_documento || []; track td.id) {
                    <option [ngValue]="td.id">{{ td.sigla }} · {{ td.nombre }}</option>
                  }
                </select>
              </div>
              <div class="form-group">
                <label for="reg_num_doc" class="sap-form-label">Número de Documento *</label>
                <input id="reg_num_doc" name="reg_num_doc" type="text" class="sap-input" [(ngModel)]="regForm.numero_documento" required />
              </div>
              <div class="form-group">
                <label for="reg_mun" class="sap-form-label">Municipio en Sabana Norte *</label>
                <select id="reg_mun" name="reg_mun" class="sap-input" [(ngModel)]="regForm.municipio_id">
                  @for (m of catalogos()?.municipios_sabana_norte || []; track m.id) {
                    <option [ngValue]="m.id">{{ m.nombre }}</option>
                  }
                </select>
              </div>
            </div>

            <div class="grid-2">
              <div class="form-group">
                <label for="reg_vereda" class="sap-form-label">Vereda o Barrio *</label>
                <input id="reg_vereda" name="reg_vereda" type="text" class="sap-input" [(ngModel)]="regForm.vereda_o_barrio" placeholder="Ej: Vereda Fagua / Centro" required />
              </div>
              <div class="form-group">
                <label for="reg_dir" class="sap-form-label">Dirección o Punto de Referencia *</label>
                <input id="reg_dir" name="reg_dir" type="text" class="sap-input" [(ngModel)]="regForm.direccion_fisica" required />
              </div>
            </div>

            @if (modoVista() === 'REGISTRO_VOLUNTARIO') {
              <div class="role-specific-box">
                <h3>Tus Conocimientos y Disponibilidad</h3>
                <div class="grid-3">
                  <div class="form-group">
                    <label for="reg_hab" class="sap-form-label">Área en la que deseas apoyar *</label>
                    <select id="reg_hab" name="reg_hab" class="sap-input" [(ngModel)]="regForm.habilidad_inicial_id">
                      @for (h of catalogos()?.habilidades || []; track h.id) {
                        <option [ngValue]="h.id">{{ h.nombre }}</option>
                      }
                    </select>
                  </div>
                  <div class="form-group">
                    <label for="reg_nivel" class="sap-form-label">Nivel de Experiencia *</label>
                    <select id="reg_nivel" name="reg_nivel" class="sap-input" [(ngModel)]="regForm.nivel_dominio">
                      <option value="BASICO">Básico / Aprendiz</option>
                      <option value="INTERMEDIO">Intermedio / Práctico</option>
                      <option value="AVANZADO">Avanzado / Formador</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label for="reg_horas" class="sap-form-label">Horas Disponibles por Semana *</label>
                    <input id="reg_horas" name="reg_horas" type="number" min="2" max="48" class="sap-input" [(ngModel)]="regForm.disponibilidad_horas_semana" />
                  </div>
                </div>
                <div class="form-group">
                  <label for="reg_bio" class="sap-form-label">Cuéntanos brevemente cómo te gustaría ayudar</label>
                  <input id="reg_bio" name="reg_bio" type="text" class="sap-input" [(ngModel)]="regForm.biografia_corta" placeholder="Ej: Me gustaría apoyar en huertas escolares y talleres..." />
                </div>
              </div>
            } @else {
              <div class="role-specific-box">
                <h3>Información para tus Certificados de Donación</h3>
                <div class="grid-2">
                  <div class="form-group">
                    <label for="reg_tipo_don" class="sap-form-label">Tipo de Donante *</label>
                    <select id="reg_tipo_don" name="reg_tipo_don" class="sap-input" [(ngModel)]="regForm.tipo_donante">
                      <option value="PERSONA_NATURAL">Persona Natural</option>
                      <option value="EMPRESA">Empresa u Organización</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label for="reg_emp" class="sap-form-label">Nombre de la Empresa (Opcional)</label>
                    <input id="reg_emp" name="reg_emp" type="text" class="sap-input" [(ngModel)]="regForm.empresa_organizacion" placeholder="Si donas en nombre de una empresa" />
                  </div>
                </div>
              </div>
            }

            <div class="grid-2">
              <div class="form-group">
                <label for="reg_correo" class="sap-form-label">Correo Electrónico *</label>
                <input id="reg_correo" name="reg_correo" type="email" class="sap-input" [(ngModel)]="regForm.correo_electronico" required />
              </div>
              <div class="form-group">
                <label for="reg_pass" class="sap-form-label">Crea tu Contraseña (Mínimo 6 caracteres) *</label>
                <input id="reg_pass" name="reg_pass" type="password" class="sap-input" [(ngModel)]="regForm.contrasena" required />
              </div>
            </div>

            <div class="reg-actions">
              <button type="button" class="sap-btn-secondary" (click)="cambiarModo('LOGIN')">
                Volver a Iniciar Sesión
              </button>
              <button type="submit" class="cs-btn" [disabled]="cargando()">
                {{ cargando() ? 'Creando tu cuenta...' : 'Crear mi Cuenta e Ingresar' }}
              </button>
            </div>
          </form>
        </section>
      }
    </main>
  `,
  styles: [`
    .header-actions { display: flex; flex-wrap: wrap; gap: 0.65rem; }
    .auth-tabs {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 0.75rem;
      margin-bottom: 1.5rem;
    }
    .auth-tab {
      min-height: 48px;
      padding: 0.75rem 1rem;
      font-size: 0.95rem;
      font-weight: 700;
      background: var(--sap-bg-surface);
      color: var(--sap-text-secondary);
      border: 1px solid var(--sap-border-subtle);
      border-bottom: 3px solid var(--sap-border-subtle);
      border-radius: 6px;
      cursor: pointer;
      text-align: center;
    }
    .auth-tab.active {
      color: var(--sap-brand-primary);
      border-bottom-color: var(--sap-brand-primary);
      background: #F8FAFC;
    }
    .login-split-grid {
      display: grid;
      grid-template-columns: 1fr 1.2fr;
      gap: 1.5rem;
      align-items: start;
    }
    @media (max-width: 920px) {
      .login-split-grid { grid-template-columns: 1fr; }
    }
    .login-panel, .rbac-selector-panel, .registro-panel {
      border-top: 3px solid var(--sap-brand-primary);
    }
    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 1rem;
      padding-bottom: 0.85rem;
      margin-bottom: 1.15rem;
      border-bottom: 1px solid var(--sap-border-subtle);
    }
    .panel-header h2 { margin: 0; font-size: 1.15rem; }
    .sub-note { margin: 0.25rem 0 0 0; font-size: 0.88rem; color: var(--sap-text-secondary); }
    .helper-desc { margin: 0 0 1rem 0; font-size: 0.9rem; color: var(--sap-text-secondary); }
    .role-cards-list { display: flex; flex-direction: column; gap: 0.75rem; }
    .role-option-card {
      padding: 0.85rem 1rem;
      border: 1px solid var(--sap-border-subtle);
      border-left: 4px solid var(--sap-brand-primary);
      border-radius: 6px;
      background: var(--sap-bg-canvas);
      cursor: pointer;
      transition: background 0.15s ease, transform 0.12s ease;
    }
    .role-option-card:hover {
      background: #E8F1FF;
      transform: translateX(3px);
    }
    .role-top { display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; margin-bottom: 0.3rem; }
    .role-option-card p { margin: 0 0 0.4rem 0; font-size: 0.86rem; color: var(--sap-text-secondary); }
    .role-cta { font-size: 0.82rem; font-weight: 700; color: var(--sap-brand-primary); }
    .form-group { margin-bottom: 1rem; }
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; }
    .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }
    .role-specific-box {
      padding: 1rem;
      margin-bottom: 1rem;
      background: var(--sap-bg-canvas);
      border: 1px solid var(--sap-border-subtle);
      border-radius: 6px;
    }
    .role-specific-box h3 { margin: 0 0 0.85rem 0; font-size: 0.98rem; color: var(--sap-brand-primary); }
    .reg-actions { display: flex; justify-content: space-between; align-items: center; padding-top: 1rem; border-top: 1px solid var(--sap-border-subtle); }
    .btn-block { width: 100%; margin-top: 0.5rem; }
    .alert-error {
      border-left: 4px solid var(--sap-status-err-border);
      background-color: var(--sap-status-err-bg);
      color: var(--sap-status-err-text);
      padding: 0.85rem 1rem;
      border-radius: 6px;
      font-weight: 600;
      margin-bottom: 1.15rem;
    }
  `]
})
export class LoginComponent implements OnInit {
  private readonly authService = inject(AuthService);
  private readonly offlineSync = inject(OfflineSyncService);
  private readonly router = inject(Router);
  private readonly platformId = inject(PLATFORM_ID);

  modoVista = signal<'LOGIN' | 'REGISTRO_VOLUNTARIO' | 'REGISTRO_DONANTE'>('LOGIN');
  catalogos = signal<CatalogosGenerales | null>(null);

  correoElectronico = '';
  contrasena = '';
  cargando = signal(false);
  mensajeErrorHumano = signal('');
  mensajeConexionInestable = signal('');

  regForm = {
    nombres: '',
    apellidos: '',
    telefono_contacto: '',
    tipo_documento_id: 1,
    numero_documento: '',
    municipio_id: 6,
    vereda_o_barrio: 'Vereda Centro Rural',
    direccion_fisica: 'Km 2 Vía Principal',
    correo_electronico: '',
    contrasena: '',
    disponibilidad_horas_semana: 8,
    habilidad_inicial_id: 1,
    nivel_dominio: 'INTERMEDIO',
    biografia_corta: 'Me gustaría apoyar a las comunidades rurales de la Sabana Norte.',
    tipo_donante: 'PERSONA_NATURAL',
    empresa_organizacion: '',
  };

  ngOnInit(): void {
    this.offlineSync.obtenerCatalogos().subscribe((cat) => this.catalogos.set(cat));
  }

  cambiarModo(modo: 'LOGIN' | 'REGISTRO_VOLUNTARIO' | 'REGISTRO_DONANTE'): void {
    this.modoVista.set(modo);
    this.mensajeErrorHumano.set('');
  }

  cargarDemo(correo: string): void {
    this.modoVista.set('LOGIN');
    this.correoElectronico = correo;
    this.contrasena = 'Solidaria2026*';
    this.mensajeErrorHumano.set('');
  }

  ingresarComoInvitado(): void {
    this.authService.activarModoInvitado();
  }

  procesarLogin(): void {
    this.mensajeErrorHumano.set('');
    this.mensajeConexionInestable.set('');

    if (!this.correoElectronico.trim() || !this.contrasena.trim()) {
      this.mensajeErrorHumano.set('Por favor escribe tu correo electrónico y tu contraseña antes de continuar.');
      return;
    }

    if (isPlatformBrowser(this.platformId) && !navigator.onLine) {
      this.mensajeConexionInestable.set(
        'Tu conexión en la zona rural parece estar sin señal en este momento. Conéctate brevemente para ingresar a tu cuenta.'
      );
      return;
    }

    this.cargando.set(true);
    this.authService.iniciarSesion(this.correoElectronico, this.contrasena).subscribe({
      next: () => {
        this.cargando.set(false);
        this.router.navigate([this.authService.rutaInicioPorRol()]);
      },
      error: (err) => {
        this.cargando.set(false);
        if (err.status === 0) {
          this.mensajeConexionInestable.set(
            'Tu conexión parece inestable. Guardamos tu correo en pantalla para que vuelvas a intentar apenas regrese la señal.'
          );
        } else {
          this.mensajeErrorHumano.set(
            err.error?.mensaje_humano || 'No pudimos verificar tus datos en este momento. Intenta nuevamente.'
          );
        }
      },
    });
  }

  procesarRegistroCiudadano(): void {
    this.mensajeErrorHumano.set('');
    this.cargando.set(true);

    const tipo_actor = this.modoVista() === 'REGISTRO_VOLUNTARIO' ? 'VOLUNTARIO' : 'DONANTE';
    const payload = {
      ...this.regForm,
      tipo_actor,
    };

    this.authService.registrarCiudadano(payload).subscribe({
      next: () => {
        this.cargando.set(false);
        this.router.navigate([this.authService.rutaInicioPorRol()]);
      },
      error: (err) => {
        this.cargando.set(false);
        this.mensajeErrorHumano.set(
          err.error?.mensaje_humano || 'No se pudo completar tu registro. Por favor verifica los datos ingresados.'
        );
      },
    });
  }
}
