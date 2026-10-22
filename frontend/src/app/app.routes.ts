import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { LoginComponent } from './features/auth/login/login.component';
import { PanelProtegidoComponent } from './features/panel/panel-protegido.component';
import { RegistroOsalWizardComponent } from './features/osal/registro-osal-wizard.component';
import { PublicarNecesidadComponent } from './features/campanas/publicar-necesidad.component';
import { RegistrarDonacionComponent } from './features/donaciones/registrar-donacion.component';
import { TrazabilidadLogisticaComponent } from './features/donaciones/trazabilidad-logistica.component';
import { PostulacionVoluntariadoComponent } from './features/voluntariado/postulacion-voluntariado.component';
import { PerfilHabilidadesComponent } from './features/voluntariado/perfil-habilidades.component';
import { MapaSabanaComponent } from './features/mapa/mapa-sabana.component';
import { DashboardOsalComponent } from './features/dashboard/dashboard-osal.component';

export const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent,
    title: 'Control de Acceso e Identidad | Conexión Solidaria',
  },
  {
    path: 'registro-osal',
    component: RegistroOsalWizardComponent,
    title: 'Vinculación Institucional OSAL | Conexión Solidaria',
  },
  {
    path: 'mapa',
    component: MapaSabanaComponent,
    canActivate: [authGuard],
    data: { permiteInvitado: true },
    title: 'Georreferenciación Sabana Norte | Conexión Solidaria',
  },
  {
    path: 'campanas',
    component: PublicarNecesidadComponent,
    canActivate: [authGuard],
    data: { permiteInvitado: true },
    title: 'Catálogo de Causas y Necesidades | Conexión Solidaria',
  },
  {
    path: 'donar',
    component: RegistrarDonacionComponent,
    canActivate: [authGuard],
    data: { roles: ['DONANTE', 'ADMIN'] },
    title: 'Gestión de Aportes y Certificados | Conexión Solidaria',
  },
  {
    path: 'voluntariado',
    component: PostulacionVoluntariadoComponent,
    canActivate: [authGuard],
    data: { roles: ['VOLUNTARIO', 'ADMIN'] },
    title: 'Gestión de Voluntariado | Conexión Solidaria',
  },
  {
    path: 'perfil-habilidades',
    component: PerfilHabilidadesComponent,
    canActivate: [authGuard],
    data: { roles: ['VOLUNTARIO', 'ADMIN'] },
    title: 'Matriz de Competencias | Conexión Solidaria',
  },
  {
    path: 'dashboard',
    component: DashboardOsalComponent,
    canActivate: [authGuard],
    data: { roles: ['REPRESENTANTE_OSAL', 'ADMIN'] },
    title: 'Tablero de Control Operativo | Conexión Solidaria',
  },
  {
    path: 'trazabilidad',
    component: TrazabilidadLogisticaComponent,
    canActivate: [authGuard],
    data: { roles: ['REPRESENTANTE_OSAL', 'ADMIN'] },
    title: 'Cadena de Custodia Logística | Conexión Solidaria',
  },
  {
    path: 'panel',
    component: PanelProtegidoComponent,
    canActivate: [authGuard],
    title: 'Gobernanza y Seguridad de Cuenta | Conexión Solidaria',
  },
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'login',
  },
  {
    path: '**',
    redirectTo: 'login',
  },
];
