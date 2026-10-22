import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from './core/services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <header class="top-nav" role="banner">
      <div class="nav-inner">
        <a routerLink="/mapa" class="brand-title">
          🌱 Conexión Solidaria · Sabana Norte
        </a>
        <nav class="nav-links" aria-label="Menú principal de casos de uso">
          <a routerLink="/mapa" routerLinkActive="active-link" class="nav-link">Mapa (CU06)</a>
          <a routerLink="/campanas" routerLinkActive="active-link" class="nav-link">Campañas (CU03)</a>
          <a routerLink="/registro-osal" routerLinkActive="active-link" class="nav-link">Registro OSAL (CU02)</a>
          <a routerLink="/donar" routerLinkActive="active-link" class="nav-link">Donar + PDF (CU04/07)</a>
          <a routerLink="/voluntariado" routerLinkActive="active-link" class="nav-link">Voluntariado (CU05)</a>
          @if (authService.estaAutenticado()) {
            <a routerLink="/dashboard" routerLinkActive="active-link" class="nav-link">Dashboard (CU08)</a>
            <a routerLink="/trazabilidad" routerLinkActive="active-link" class="nav-link">Logística (CU09)</a>
            <a routerLink="/perfil-habilidades" routerLinkActive="active-link" class="nav-link">Habilidades (CU10)</a>
            <a routerLink="/panel" routerLinkActive="active-link" class="nav-link">Sesión (CU01)</a>
          } @else {
            <a routerLink="/login" routerLinkActive="active-link" class="nav-link btn-nav-login">Ingresar (CU01)</a>
          }
        </nav>
      </div>
    </header>
    <router-outlet />
  `,
  styles: [`
    .top-nav {
      background-color: var(--brand-primary);
      color: #FFFFFF;
      padding: 0.75rem 1.25rem;
      border-bottom: 3px solid var(--border-strong);
    }
    .nav-inner {
      max-width: 1180px;
      margin: 0 auto;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 0.75rem;
    }
    .brand-title {
      color: #FFFFFF;
      font-weight: 800;
      font-size: 1.15rem;
      text-decoration: none;
    }
    .nav-links {
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem;
      align-items: center;
    }
    .nav-link {
      color: #FFFFFF;
      font-weight: 700;
      font-size: 0.9rem;
      text-decoration: none;
      padding: 0.45rem 0.7rem;
      border-radius: 6px;
      border: 2px solid transparent;
    }
    .nav-link:hover, .active-link {
      background-color: rgba(255, 255, 255, 0.16);
      border-color: #FFFFFF;
    }
    .btn-nav-login {
      background-color: #FFFFFF;
      color: var(--brand-primary);
    }
  `]
})
export class App {
  readonly authService = inject(AuthService);
}
