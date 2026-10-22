import { Injectable, PLATFORM_ID, inject, signal, computed } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';

export interface UsuarioSesion {
  id: number;
  correo_electronico: string;
  nombre_mostrar: string;
  roles: string[];
  fundacion_id: number | null;
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
  private readonly apiUrl = 'http://localhost:5000/api/auth';

  private readonly STORAGE_TOKEN_KEY = 'cs_jwt_token';
  private readonly STORAGE_USER_KEY = 'cs_user_session';

  readonly usuarioActual = signal<UsuarioSesion | null>(this.cargarUsuarioDesdeCache());
  readonly estaAutenticado = computed(() => this.usuarioActual() !== null && !!this.obtenerToken());

  constructor() {}

  iniciarSesion(correo_electronico: string, contrasena: string): Observable<RespuestaLogin> {
    return this.http
      .post<RespuestaLogin>(`${this.apiUrl}/login`, { correo_electronico, contrasena })
      .pipe(
        tap((respuesta) => {
          this.guardarSesion(respuesta.access_token, respuesta.usuario);
        })
      );
  }

  obtenerPerfilremoto(): Observable<{ usuario: UsuarioSesion; auditoria_reciente: Array<{ id: number; accion: string; detalle: string; fecha_evento: string }> }> {
    return this.http.get<{ usuario: UsuarioSesion; auditoria_reciente: Array<{ id: number; accion: string; detalle: string; fecha_evento: string }> }>(`${this.apiUrl}/me`);
  }

  cerrarSesion(): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem(this.STORAGE_TOKEN_KEY);
      localStorage.removeItem(this.STORAGE_USER_KEY);
    }
    this.usuarioActual.set(null);
    this.router.navigate(['/login']);
  }

  obtenerToken(): string | null {
    if (isPlatformBrowser(this.platformId)) {
      return localStorage.getItem(this.STORAGE_TOKEN_KEY);
    }
    return null;
  }

  tieneRol(rolRequerido: string): boolean {
    const usuario = this.usuarioActual();
    return !!usuario && usuario.roles.includes(rolRequerido);
  }

  private guardarSesion(token: string, usuario: UsuarioSesion): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.setItem(this.STORAGE_TOKEN_KEY, token);
      localStorage.setItem(this.STORAGE_USER_KEY, JSON.stringify(usuario));
    }
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
}
