import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink } from '@angular/router';
import { AuthService } from './core/services/auth.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink],
  template: `
    <header class="top-nav" role="banner">
      <div class="nav-inner">
        <a routerLink="/panel" class="brand-title">
          Conexión Solidaria · Sabana Norte
        </a>
        <nav aria-label="Navegación principal">
          @if (authService.estaAutenticado()) {
            <a routerLink="/panel" class="nav-link">Mi Panel</a>
          } @else {
            <a routerLink="/login" class="nav-link">Iniciar Sesión</a>
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
      padding: 0.85rem 1.5rem;
      border-bottom: 3px solid var(--border-strong);
    }
    .nav-inner {
      max-width: 1080px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .brand-title {
      color: #FFFFFF;
      font-weight: 800;
      font-size: 1.2rem;
      text-decoration: none;
    }
    .nav-link {
      color: #FFFFFF;
      font-weight: 700;
      text-decoration: underline;
      padding: 0.5rem 0.75rem;
    }
  `]
})
export class App {
  readonly authService = inject(AuthService);
}
