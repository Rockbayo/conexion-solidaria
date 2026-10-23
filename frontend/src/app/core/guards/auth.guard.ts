import { inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (route) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const platformId = inject(PLATFORM_ID);

  if (!isPlatformBrowser(platformId)) {
    return true;
  }

  const permiteInvitado = route.data?.['permiteInvitado'] === true;
  const rolesPermitidos = route.data?.['roles'] as string[] | undefined;

  if (permiteInvitado && authService.tieneSesionOInvitado()) {
    return true;
  }

  if (!authService.estaAutenticado()) {
    return router.createUrlTree(['/login']);
  }

  if (rolesPermitidos && rolesPermitidos.length > 0) {
    const poseePermiso = authService.tieneRol(...rolesPermitidos);
    if (!poseePermiso) {
      return router.createUrlTree(['/panel'], {
        queryParams: { acceso_restringido: 'true' },
      });
    }
  }

  return true;
};
