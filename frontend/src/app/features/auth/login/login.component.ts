import { Component, inject, signal, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="sap-page-header">
      <div class="sap-page-header-inner">
        <div>
          <span class="sap-breadcrumb">Seguridad y Control de Acceso</span>
          <h1 class="sap-page-title">Portal de Autenticación Institucional</h1>
          <p class="sap-page-subtitle">Acceso unificado para fundaciones rurales, donantes y voluntarios de la Sabana Norte.</p>
        </div>
      </div>
    </div>

    <main class="sap-container login-layout" aria-labelledby="login-heading">
      <section class="cs-card login-panel">
        <div class="panel-header">
          <h2 id="login-heading">Credenciales de Usuario</h2>
          <span class="sap-badge sap-badge-info">Sesión Cifrada JWT</span>
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

        <form (ngSubmit)="procesarLogin()" class="login-form" novalidate>
          <div class="form-group">
            <label for="correo" class="sap-form-label">Correo electrónico corporativo o personal</label>
            <input
              id="correo"
              name="correo"
              type="email"
              class="sap-input"
              [(ngModel)]="correoElectronico"
              placeholder="usuario@organizacion.org"
              required
              autocomplete="email"
            />
          </div>

          <div class="form-group">
            <label for="contrasena" class="sap-form-label">Clave de seguridad</label>
            <input
              id="contrasena"
              name="contrasena"
              type="password"
              class="sap-input"
              [(ngModel)]="contrasena"
              placeholder="••••••••••••"
              required
              autocomplete="current-password"
            />
          </div>

          <button type="submit" class="cs-btn btn-block" [disabled]="cargando()">
            {{ cargando() ? 'Validando credenciales...' : 'Iniciar Sesión' }}
          </button>
        </form>

        <div class="quick-profiles" aria-label="Perfiles preconfigurados del entorno">
          <div class="quick-header">
            <h3>Selección Rápida de Rol Operativo</h3>
            <p>Carga automática de perfiles de verificación para la Sabana Norte:</p>
          </div>
          <div class="profile-grid">
            <button type="button" class="sap-btn-secondary" (click)="cargarDemo('osal@sabananorte.org')">
              Representante OSAL · Cogua
            </button>
            <button type="button" class="sap-btn-secondary" (click)="cargarDemo('donante@conexion.org')">
              Donante · Tabio
            </button>
            <button type="button" class="sap-btn-secondary" (click)="cargarDemo('voluntario@conexion.org')">
              Voluntario Rural
            </button>
          </div>
        </div>
      </section>
    </main>
  `,
  styles: [`
    .login-layout {
      display: flex;
      justify-content: center;
      padding-top: 1rem;
    }
    .login-panel {
      width: 100%;
      max-width: 520px;
      border-top: 4px solid var(--sap-brand-primary);
    }
    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 1rem;
      margin-bottom: 1.25rem;
      border-bottom: 1px solid var(--sap-border-subtle);
    }
    .panel-header h2 {
      margin: 0;
      font-size: 1.15rem;
    }
    .form-group {
      margin-bottom: 1.15rem;
    }
    .btn-block {
      width: 100%;
      margin-top: 0.4rem;
    }
    .alert-error {
      border-left: 4px solid var(--sap-status-err-border);
      border-top: 1px solid var(--sap-status-err-border);
      border-right: 1px solid var(--sap-status-err-border);
      border-bottom: 1px solid var(--sap-status-err-border);
      background-color: var(--sap-status-err-bg);
      color: var(--sap-status-err-text);
      padding: 0.85rem 1rem;
      border-radius: 6px;
      font-weight: 600;
      margin-bottom: 1.15rem;
    }
    .quick-profiles {
      margin-top: 1.75rem;
      padding-top: 1.25rem;
      border-top: 1px solid var(--sap-border-subtle);
    }
    .quick-header h3 {
      margin: 0 0 0.2rem 0;
      font-size: 0.95rem;
    }
    .quick-header p {
      margin: 0 0 0.85rem 0;
      font-size: 0.85rem;
      color: var(--sap-text-secondary);
    }
    .profile-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
      gap: 0.6rem;
    }
  `]
})
export class LoginComponent {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);
  private readonly platformId = inject(PLATFORM_ID);

  correoElectronico = '';
  contrasena = '';
  cargando = signal(false);
  mensajeErrorHumano = signal('');
  mensajeConexionInestable = signal('');

  cargarDemo(correo: string): void {
    this.correoElectronico = correo;
    this.contrasena = 'Solidaria2026*';
    this.mensajeErrorHumano.set('');
  }

  procesarLogin(): void {
    this.mensajeErrorHumano.set('');
    this.mensajeConexionInestable.set('');

    if (!this.correoElectronico.trim() || !this.contrasena.trim()) {
      this.mensajeErrorHumano.set('Por favor completa tu correo electrónico y tu contraseña antes de continuar.');
      return;
    }

    if (isPlatformBrowser(this.platformId) && !navigator.onLine) {
      this.mensajeConexionInestable.set(
        'Tu conexión en la zona rural parece estar sin señal en este momento. Conéctate brevemente para validar tu llave de ingreso.'
      );
      return;
    }

    this.cargando.set(true);
    this.authService.iniciarSesion(this.correoElectronico, this.contrasena).subscribe({
      next: () => {
        this.cargando.set(false);
        this.router.navigate(['/panel']);
      },
      error: (err) => {
        this.cargando.set(false);
        if (err.status === 0) {
          this.mensajeConexionInestable.set(
            'Tu conexión parece inestable o el servidor comunitario no responde. Guardamos tu correo en pantalla para que reintentes apenas vuelva la señal.'
          );
        } else {
          this.mensajeErrorHumano.set(
            err.error?.mensaje_humano || 'No pudimos verificar tus datos en este momento. Intenta nuevamente.'
          );
        }
      },
    });
  }
}
