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
          <a routerLink="/mapa" class="sap-logo">
            <span class="sap-logo-mark">CS</span>
            <span class="sap-logo-text">
              <strong>Conexión Solidaria</strong>
              <small>Gestión Territorial Sabana Norte</small>
            </span>
          </a>
        </div>

        <nav class="sap-shell-nav" aria-label="Navegación corporativa">
          <a routerLink="/mapa" routerLinkActive="active" class="sap-nav-item">Mapa Territorial</a>
          <a routerLink="/campanas" routerLinkActive="active" class="sap-nav-item">Causas y Necesidades</a>
          <a routerLink="/registro-osal" routerLinkActive="active" class="sap-nav-item">Vinculación OSAL</a>
          <a routerLink="/donar" routerLinkActive="active" class="sap-nav-item">Aportes y Certificados</a>
          <a routerLink="/voluntariado" routerLinkActive="active" class="sap-nav-item">Voluntariado</a>
          @if (authService.estaAutenticado()) {
            <a routerLink="/dashboard" routerLinkActive="active" class="sap-nav-item">Indicadores</a>
            <a routerLink="/trazabilidad" routerLinkActive="active" class="sap-nav-item">Logística</a>
            <a routerLink="/perfil-habilidades" routerLinkActive="active" class="sap-nav-item">Competencias</a>
            <a routerLink="/panel" routerLinkActive="active" class="sap-nav-item sap-user-pill">
              {{ authService.usuarioActual()?.nombre_mostrar }}
            </a>
          } @else {
            <a routerLink="/login" routerLinkActive="active" class="sap-nav-item sap-login-cta">Iniciar Sesión</a>
          }
        </nav>
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
      max-width: 1240px;
      margin: 0 auto;
      padding: 0.55rem 2rem;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
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
      letter-spacing: 0.03em;
    }
    .sap-logo-text {
      display: flex;
      flex-direction: column;
      line-height: 1.15;
    }
    .sap-logo-text strong {
      font-size: 1rem;
      font-weight: 700;
    }
    .sap-logo-text small {
      font-size: 0.74rem;
      color: #CBD5E1;
    }
    .sap-shell-nav {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.25rem;
    }
    .sap-nav-item {
      color: #E2E8F0;
      text-decoration: none;
      font-size: 0.86rem;
      font-weight: 600;
      padding: 0.45rem 0.75rem;
      border-radius: 4px;
      border-bottom: 2px solid transparent;
      transition: background 0.15s ease, color 0.15s ease;
    }
    .sap-nav-item:hover {
      background: rgba(255, 255, 255, 0.08);
      color: #FFFFFF;
    }
    .sap-nav-item.active {
      color: #FFFFFF;
      background: rgba(255, 255, 255, 0.12);
      border-bottom-color: #60A5FA;
    }
    .sap-login-cta {
      background: var(--sap-brand-primary);
      color: #FFFFFF;
      margin-left: 0.35rem;
    }
    .sap-user-pill {
      background: rgba(255, 255, 255, 0.14);
      color: #FFFFFF;
      margin-left: 0.35rem;
    }
  `]
})
export class App {
  readonly authService = inject(AuthService);
}
