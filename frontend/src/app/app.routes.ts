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
    title: 'CU01 · Ingreso | Conexión Solidaria Sabana Norte',
  },
  {
    path: 'registro-osal',
    component: RegistroOsalWizardComponent,
    title: 'CU02 · Registro OSAL (Wizard) | Conexión Solidaria',
  },
  {
    path: 'campanas',
    component: PublicarNecesidadComponent,
    title: 'CU03 · Publicar Necesidad y Campañas | Conexión Solidaria',
  },
  {
    path: 'donar',
    component: RegistrarDonacionComponent,
    title: 'CU04 y CU07 · Donaciones y Certificados PDF | Conexión Solidaria',
  },
  {
    path: 'voluntariado',
    component: PostulacionVoluntariadoComponent,
    title: 'CU05 · Postulación Voluntariado | Conexión Solidaria',
  },
  {
    path: 'mapa',
    component: MapaSabanaComponent,
    title: 'CU06 · Mapa Georreferenciado Sabana Norte | Conexión Solidaria',
  },
  {
    path: 'dashboard',
    component: DashboardOsalComponent,
    canActivate: [authGuard],
    title: 'CU08 · Dashboard OSAL | Conexión Solidaria',
  },
  {
    path: 'trazabilidad',
    component: TrazabilidadLogisticaComponent,
    canActivate: [authGuard],
    title: 'CU09 · Trazabilidad Logística | Conexión Solidaria',
  },
  {
    path: 'perfil-habilidades',
    component: PerfilHabilidadesComponent,
    canActivate: [authGuard],
    title: 'CU10 · Perfil de Habilidades | Conexión Solidaria',
  },
  {
    path: 'panel',
    component: PanelProtegidoComponent,
    canActivate: [authGuard],
    title: 'Mi Panel Seguro | Conexión Solidaria',
  },
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'mapa',
  },
  {
    path: '**',
    redirectTo: 'mapa',
  },
];
