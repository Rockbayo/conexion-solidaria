import { Injectable, PLATFORM_ID, inject, signal, computed } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';
import { getApiBaseUrl } from '../config/api.config';

export interface UsuarioSesion {
  id: number;
  correo_electronico: string;
  nombre_mostrar: string;
  roles: string[];
  fundacion_id: number | null;
  fundacion_nombre?: string | null;
  fundacion_estado?: string | null;
  voluntario_id: number | null;
  donante_id: number | null;
}

export interface RespuestaLogin {
  mensaje_humano: string;
  access_token: string;
  usuario: UsuarioSesion;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly platformId = inject(PLATFORM_ID);

  private readonly STORAGE_TOKEN_KEY = 'cs_jwt_token';
  private readonly STORAGE_USER_KEY = 'cs_user_session';
  private readonly STORAGE_GUEST_KEY = 'cs_guest_mode';

  readonly usuarioActual = signal<UsuarioSesion | null>(this.cargarUsuarioDesdeCache());
  readonly modoInvitado = signal<boolean>(this.cargarModoInvitadoDesdeCache());
  readonly estaAutenticado = computed(() => this.usuarioActual() !== null && !!this.obtenerToken());
  readonly tieneSesionOInvitado = computed(() => this.estaAutenticado() || this.modoInvitado());

  readonly etiquetaRolPrincipal = computed(() => {
    const u = this.usuarioActual();
    if (!u) {
      return this.modoInvitado() ? 'Visitante · Modo Invitado (Lectura)' : 'Sin Sesión Activa';
    }
    if (u.roles.includes('ADMIN')) return 'Administrador de la Plataforma';
    if (u.roles.includes('REPRESENTANTE_OSAL')) {
      return u.fundacion_nombre ? `Admin OSAL · ${u.fundacion_nombre}` : 'Administrador de OSAL';
    }
    if (u.roles.includes('VOLUNTARIO')) return 'Voluntario Rural Registrado';
    if (u.roles.includes('DONANTE')) return 'Donante Solidario Registrado';
    return u.roles.join(' · ');
  });

  private get apiUrl(): string {
    return `${getApiBaseUrl()}/auth`;
  }

  iniciarSesion(correo_electronico: string, contrasena: string): Observable<RespuestaLogin> {
    return this.http
      .post<RespuestaLogin>(`${this.apiUrl}/login`, { correo_electronico, contrasena })
      .pipe(
        tap((respuesta) => {
          this.guardarSesion(respuesta.access_token, respuesta.usuario);
        })
      );
  }

  registrarCiudadano(payload: Record<string, unknown>): Observable<RespuestaLogin> {
    return this.http
      .post<RespuestaLogin>(`${this.apiUrl}/registro-ciudadano`, payload)
      .pipe(
        tap((respuesta) => {
          this.guardarSesion(respuesta.access_token, respuesta.usuario);
        })
      );
  }

  activarModoInvitado(): void {
    this.cerrarSesionSilencioso();
    if (isPlatformBrowser(this.platformId)) {
      localStorage.setItem(this.STORAGE_GUEST_KEY, 'true');
    }
    this.modoInvitado.set(true);
    this.router.navigate(['/mapa']);
  }

  obtenerPerfilremoto(): Observable<{
    usuario: UsuarioSesion;
    auditoria_reciente: Array<{ id: number; accion: string; entidad_afectada?: string; detalle: string; direccion_ip?: string; fecha_evento: string }>;
  }> {
    return this.http.get<{
      usuario: UsuarioSesion;
      auditoria_reciente: Array<{ id: number; accion: string; entidad_afectada?: string; detalle: string; direccion_ip?: string; fecha_evento: string }>;
    }>(`${this.apiUrl}/me`);
  }

  cerrarSesion(): void {
    this.cerrarSesionSilencioso();
    this.router.navigate(['/login']);
  }

  private cerrarSesionSilencioso(): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem(this.STORAGE_TOKEN_KEY);
      localStorage.removeItem(this.STORAGE_USER_KEY);
      localStorage.removeItem(this.STORAGE_GUEST_KEY);
    }
    this.usuarioActual.set(null);
    this.modoInvitado.set(false);
  }

  obtenerToken(): string | null {
    if (isPlatformBrowser(this.platformId)) {
      return localStorage.getItem(this.STORAGE_TOKEN_KEY);
    }
    return null;
  }

  tieneRol(...rolesRequeridos: string[]): boolean {
    const usuario = this.usuarioActual();
    if (!usuario) return false;
    return usuario.roles.some((r) => rolesRequeridos.includes(r));
  }

  rutaInicioPorRol(): string {
    const u = this.usuarioActual();
    if (!u) return '/mapa';
    if (u.roles.includes('ADMIN')) return '/panel';
    if (u.roles.includes('REPRESENTANTE_OSAL')) return '/dashboard';
    if (u.roles.includes('VOLUNTARIO')) return '/voluntariado';
    if (u.roles.includes('DONANTE')) return '/donar';
    return '/mapa';
  }

  private guardarSesion(token: string, usuario: UsuarioSesion): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem(this.STORAGE_GUEST_KEY);
      localStorage.setItem(this.STORAGE_TOKEN_KEY, token);
      localStorage.setItem(this.STORAGE_USER_KEY, JSON.stringify(usuario));
    }
    this.modoInvitado.set(false);
    this.usuarioActual.set(usuario);
  }

  private cargarUsuarioDesdeCache(): UsuarioSesion | null {
    if (isPlatformBrowser(this.platformId)) {
      const raw = localStorage.getItem(this.STORAGE_USER_KEY);
      if (raw) {
        try {
          return JSON.parse(raw) as UsuarioSesion;
        } catch {
          return null;
        }
      }
    }
    return null;
  }

  private cargarModoInvitadoDesdeCache(): boolean {
    if (isPlatformBrowser(this.platformId)) {
      return localStorage.getItem(this.STORAGE_GUEST_KEY) === 'true';
    }
    return false;
  }
}
