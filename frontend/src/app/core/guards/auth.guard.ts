import { inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (route) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const platformId = inject(PLATFORM_ID);

  // Durante SSR permitimos hidratación inicial en cliente antes de redirigir
  if (!isPlatformBrowser(platformId)) {
    return true;
  }

  if (!authService.estaAutenticado()) {
    return router.createUrlTree(['/login']);
  }

  const rolesPermitidos = route.data?.['roles'] as string[] | undefined;
  if (rolesPermitidos && rolesPermitidos.length > 0) {
    const usuario = authService.usuarioActual();
    const poseePermiso = usuario?.roles.some((rol) => rolesPermitidos.includes(rol));
    if (!poseePermiso) {
      return router.createUrlTree(['/panel'], {
        queryParams: { acceso_restringido: 'true' },
      });
    }
  }

  return true;
};
