import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { LoginComponent } from './features/auth/login/login.component';
import { PanelProtegidoComponent } from './features/panel/panel-protegido.component';
import { RegistroOsalWizardComponent } from './features/osal/registro-osal-wizard.component';

export const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent,
    title: 'Ingreso | Conexión Solidaria Sabana Norte',
  },
  {
    path: 'registro-osal',
    component: RegistroOsalWizardComponent,
    title: 'Registro OSAL (Wizard) | Conexión Solidaria',
  },
  {
    path: 'panel',
    component: PanelProtegidoComponent,
    canActivate: [authGuard],
    title: 'Panel Comunitario | Conexión Solidaria',
  },
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'panel',
  },
  {
    path: '**',
    redirectTo: 'panel',
  },
];
