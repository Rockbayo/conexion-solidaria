import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from './core/services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <header class="sap-shellbar" role="banner">
      <div class="sap-shellbar-inner">
        <div class="sap-shell-brand">
          <a [routerLink]="authService.tieneSesionOInvitado() ? '/mapa' : '/login'" class="sap-logo">
            <span class="sap-logo-mark">CS</span>
            <span class="sap-logo-text">
              <strong>Conexión Solidaria</strong>
              <small>Gestión Territorial Sabana Norte</small>
            </span>
          </a>
        </div>

        <!-- NAVEGACIÓN CONDICIONADA POR MÍNIMO PRIVILEGIO (RBAC) -->
        @if (authService.tieneSesionOInvitado()) {
          <nav class="sap-shell-nav" aria-label="Navegación según privilegios del rol">
            <a routerLink="/mapa" routerLinkActive="active" class="sap-nav-item">Mapa Territorial</a>
            <a routerLink="/campanas" routerLinkActive="active" class="sap-nav-item">Causas y Necesidades</a>

            @if (authService.tieneRol('DONANTE', 'ADMIN')) {
              <a routerLink="/donar" routerLinkActive="active" class="sap-nav-item">Aportes y Certificados</a>
            }

            @if (authService.tieneRol('VOLUNTARIO', 'ADMIN')) {
              <a routerLink="/voluntariado" routerLinkActive="active" class="sap-nav-item">Postulación Voluntariado</a>
              <a routerLink="/perfil-habilidades" routerLinkActive="active" class="sap-nav-item">Mis Competencias</a>
            }

            @if (authService.tieneRol('REPRESENTANTE_OSAL', 'ADMIN')) {
              <a routerLink="/dashboard" routerLinkActive="active" class="sap-nav-item">Tablero OSAL</a>
              <a routerLink="/trazabilidad" routerLinkActive="active" class="sap-nav-item">Logística en Especie</a>
            }

            @if (authService.tieneRol('ADMIN')) {
              <a routerLink="/panel" routerLinkActive="active" class="sap-nav-item">Gobernanza OSAL</a>
            }
          </nav>
        }

        <!-- IDENTIFICADOR PERMANENTE DE SESIÓN Y ROL EN LA ESQUINA SUPERIOR DERECHA -->
        <div class="sap-identity-zone">
          @if (authService.estaAutenticado()) {
            <a routerLink="/panel" class="sap-identity-badge" title="Ver detalles de seguridad de mi cuenta">
              <span class="id-name">{{ authService.usuarioActual()?.nombre_mostrar }}</span>
              <span class="id-role">{{ authService.etiquetaRolPrincipal() }}</span>
            </a>
            <button type="button" class="sap-shell-logout" (click)="authService.cerrarSesion()">
              Salir
            </button>
          } @else if (authService.modoInvitado()) {
            <div class="sap-identity-badge guest">
              <span class="id-name">Usuario Visitante</span>
              <span class="id-role">Modo Invitado (Lectura)</span>
            </div>
            <a routerLink="/login" class="sap-shell-login">Iniciar Sesión / Registrarme</a>
          } @else {
            <span class="no-session-chip">Identificación Requerida</span>
          }
        </div>
      </div>
    </header>
    <router-outlet />
  `,
  styles: [`
    .sap-shellbar {
      background-color: var(--sap-shell-bg);
      color: var(--sap-shell-text);
      border-bottom: 1px solid #0F172A;
      position: sticky;
      top: 0;
      z-index: 1000;
    }
    .sap-shellbar-inner {
      max-width: 1280px;
      margin: 0 auto;
      padding: 0.5rem 1.5rem;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 0.85rem;
    }
    .sap-logo {
      display: flex;
      align-items: center;
      gap: 0.7rem;
      text-decoration: none;
      color: #FFFFFF;
    }
    .sap-logo-mark {
      width: 34px;
      height: 34px;
      border-radius: 6px;
      background: var(--sap-brand-primary);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 0.9rem;
    }
    .sap-logo-text {
      display: flex;
      flex-direction: column;
      line-height: 1.15;
    }
    .sap-logo-text strong { font-size: 0.98rem; font-weight: 700; }
    .sap-logo-text small { font-size: 0.72rem; color: #CBD5E1; }
    .sap-shell-nav {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.2rem;
    }
    .sap-nav-item {
      color: #E2E8F0;
      text-decoration: none;
      font-size: 0.84rem;
      font-weight: 600;
      padding: 0.45rem 0.65rem;
      border-radius: 4px;
      border-bottom: 2px solid transparent;
    }
    .sap-nav-item:hover {
      background: rgba(255, 255, 255, 0.08);
      color: #FFFFFF;
    }
    .sap-nav-item.active {
      color: #FFFFFF;
      background: rgba(255, 255, 255, 0.14);
      border-bottom-color: #60A5FA;
    }
    .sap-identity-zone {
      display: flex;
      align-items: center;
      gap: 0.55rem;
    }
    .sap-identity-badge {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      padding: 0.3rem 0.75rem;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.22);
      text-decoration: none;
      color: #FFFFFF;
      line-height: 1.2;
    }
    .sap-identity-badge.guest {
      background: rgba(231, 101, 0, 0.22);
      border-color: #F59E0B;
    }
    .id-name { font-size: 0.82rem; font-weight: 700; }
    .id-role { font-size: 0.7rem; color: #93C5FD; font-weight: 700; text-transform: uppercase; letter-spacing: 0.03em; }
    .sap-identity-badge.guest .id-role { color: #FCD34D; }
    .sap-shell-logout {
      min-height: 36px;
      padding: 0.35rem 0.75rem;
      border-radius: 4px;
      border: 1px solid #F87171;
      background: rgba(166, 28, 28, 0.25);
      color: #FECACA;
      font-weight: 700;
      font-size: 0.8rem;
      cursor: pointer;
    }
    .sap-shell-login {
      min-height: 36px;
      padding: 0.4rem 0.85rem;
      border-radius: 4px;
      background: var(--sap-brand-primary);
      color: #FFFFFF;
      font-weight: 700;
      font-size: 0.82rem;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
    }
    .no-session-chip {
      font-size: 0.78rem;
      padding: 0.3rem 0.65rem;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.1);
      color: #CBD5E1;
      font-weight: 600;
    }
  `]
})
export class App {
  readonly authService = inject(AuthService);
}
