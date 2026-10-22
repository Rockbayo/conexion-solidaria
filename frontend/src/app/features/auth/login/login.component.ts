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
    <main class="login-wrapper" aria-labelledby="login-heading">
      <section class="cs-card login-card">
        <div class="brand-badge">Sabana Norte de Cundinamarca</div>
        <h1 id="login-heading">Ingreso a Conexión Solidaria</h1>
        <p class="subtitle">
          Plataforma de apoyo comunitario para fundaciones rurales, donantes y voluntarios.
        </p>

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
            <label for="correo">Correo electrónico registrado</label>
            <input
              id="correo"
              name="correo"
              type="email"
              [(ngModel)]="correoElectronico"
              placeholder="ejemplo: osal@sabananorte.org"
              required
              autocomplete="email"
            />
          </div>

          <div class="form-group">
            <label for="contrasena">Contraseña de acceso</label>
            <input
              id="contrasena"
              name="contrasena"
              type="password"
              [(ngModel)]="contrasena"
              placeholder="Escribe tu contraseña segura"
              required
              autocomplete="current-password"
            />
          </div>

          <button type="submit" class="cs-btn btn-block" [disabled]="cargando()">
            {{ cargando() ? 'Verificando tus datos...' : 'Entrar a la Plataforma' }}
          </button>
        </form>

        <hr class="divider" />

        <div class="demo-accounts" aria-label="Cuentas demostrativas para pruebas rápidas">
          <h2>Acceso Rápido Demostrativo (Sabana Norte)</h2>
          <p class="helper-text">Selecciona un perfil para autocompletar credenciales de prueba:</p>
          <div class="demo-buttons">
            <button type="button" class="btn-outline" (click)="cargarDemo('osal@sabananorte.org')">
              Perfil OSAL (Cogua)
            </button>
            <button type="button" class="btn-outline" (click)="cargarDemo('donante@conexion.org')">
              Perfil Donante (Tabio)
            </button>
            <button type="button" class="btn-outline" (click)="cargarDemo('voluntario@conexion.org')">
              Perfil Voluntario
            </button>
          </div>
        </div>
      </section>
    </main>
  `,
  styles: [`
    .login-wrapper {
      min-height: calc(100vh - 80px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }
    .login-card {
      width: 100%;
      max-width: 500px;
      border-width: 2px;
      border-color: var(--border-strong);
    }
    .brand-badge {
      display: inline-block;
      background-color: var(--status-ok-bg);
      color: var(--status-ok-text);
      font-weight: 700;
      padding: 0.25rem 0.75rem;
      border-radius: 999px;
      font-size: 0.875rem;
      margin-bottom: 0.75rem;
    }
    h1 {
      margin: 0 0 0.5rem 0;
      font-size: 1.75rem;
      color: var(--text-primary);
    }
    .subtitle {
      margin: 0 0 1.5rem 0;
      color: var(--text-secondary);
    }
    .form-group {
      margin-bottom: 1.25rem;
      display: flex;
      flex-direction: column;
    }
    label {
      font-weight: 700;
      margin-bottom: 0.5rem;
      color: var(--text-primary);
    }
    input {
      min-height: 48px;
      padding: 0.75rem 1rem;
      font-size: 1rem;
      border: 2px solid var(--border-strong);
      border-radius: 8px;
      background-color: #FFFFFF;
      color: var(--text-primary);
    }
    .btn-block {
      width: 100%;
      margin-top: 0.5rem;
    }
    .alert-error {
      border-left: 6px solid var(--status-err-text);
      background-color: var(--status-err-bg);
      color: var(--status-err-text);
      padding: 1rem;
      border-radius: 8px;
      font-weight: 600;
      margin-bottom: 1.25rem;
    }
    .divider {
      margin: 1.75rem 0;
      border: 0;
      border-top: 2px solid var(--border-subtle);
    }
    .demo-accounts h2 {
      font-size: 1.1rem;
      margin: 0 0 0.25rem 0;
    }
    .helper-text {
      font-size: 0.9rem;
      color: var(--text-secondary);
      margin: 0 0 0.75rem 0;
    }
    .demo-buttons {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 0.5rem;
    }
    .btn-outline {
      min-height: 44px;
      padding: 0.5rem;
      font-weight: 700;
      background: #FFFFFF;
      color: var(--brand-primary);
      border: 2px solid var(--brand-primary);
      border-radius: 8px;
      cursor: pointer;
    }
    .btn-outline:hover {
      background: var(--status-ok-bg);
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

