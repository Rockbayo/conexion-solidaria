import { Injectable, PLATFORM_ID, inject, signal } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Observable, of, tap, catchError } from 'rxjs';
import { getApiBaseUrl } from '../config/api.config';

export interface CatalogosGenerales {
  municipios_sabana_norte: Array<{ id: number; codigo_dane: string; nombre: string; latitud_centro: number; longitud_centro: number }>;
  tipos_documento: Array<{ id: number; sigla: string; nombre: string }>;
  ods_objetivos: Array<{ id: number; numero_ods: number; titulo: string; descripcion: string }>;
  categorias_causas: Array<{ id: number; nombre: string; descripcion: string }>;
  tipos_necesidad: Array<{ id: number; codigo: string; nombre: string }>;
  unidades_medida: Array<{ id: number; simbolo: string; nombre: string }>;
  metodos_pago: Array<{ id: number; codigo: string; nombre: string }>;
  categorias_habilidades: Array<{ id: number; nombre: string; descripcion: string }>;
  habilidades: Array<{ id: number; categoria_id: number; nombre: string; descripcion: string }>;
  franjas_horarias: Array<{ id: number; codigo: string; nombre: string; horas_sugeridas: number }>;
  parametros_sistema: Array<{ id: number; clave: string; valor: string; descripcion: string; tipo_dato: string }>;
}

const CATALOGOS_FALLBACK_SABANA: CatalogosGenerales = {
  municipios_sabana_norte: [
    { id: 1, codigo_dane: '25175', nombre: 'Chía', latitud_centro: 4.8616, longitud_centro: -74.0325 },
    { id: 2, codigo_dane: '25126', nombre: 'Cajicá', latitud_centro: 4.9186, longitud_centro: -74.0279 },
    { id: 3, codigo_dane: '25899', nombre: 'Zipaquirá', latitud_centro: 5.0221, longitud_centro: -74.0042 },
    { id: 4, codigo_dane: '25785', nombre: 'Tabio', latitud_centro: 4.9173, longitud_centro: -74.0936 },
    { id: 5, codigo_dane: '25799', nombre: 'Tenjo', latitud_centro: 4.8722, longitud_centro: -74.1439 },
    { id: 6, codigo_dane: '25200', nombre: 'Cogua', latitud_centro: 5.0617, longitud_centro: -73.9806 },
    { id: 7, codigo_dane: '25758', nombre: 'Sopó', latitud_centro: 4.9089, longitud_centro: -73.9403 },
    { id: 8, codigo_dane: '25817', nombre: 'Tocancipá', latitud_centro: 4.9658, longitud_centro: -73.9136 },
    { id: 9, codigo_dane: '25295', nombre: 'Gachancipá', latitud_centro: 4.9911, longitud_centro: -73.8736 },
    { id: 10, codigo_dane: '25486', nombre: 'Nemocón', latitud_centro: 5.0678, longitud_centro: -73.8778 },
  ],
  tipos_documento: [
    { id: 1, sigla: 'CC', nombre: 'Cédula de Ciudadanía' },
    { id: 2, sigla: 'CE', nombre: 'Cédula de Extranjería' },
    { id: 3, sigla: 'NIT', nombre: 'Número de Identificación Tributaria' },
  ],
  ods_objetivos: [
    { id: 1, numero_ods: 1, titulo: 'Fin de la Pobreza', descripcion: 'Erradicar la pobreza rural extrema' },
    { id: 2, numero_ods: 2, titulo: 'Hambre Cero', descripcion: 'Seguridad alimentaria y agricultura campesina sostenible' },
    { id: 3, numero_ods: 4, titulo: 'Educación de Calidad', descripcion: 'Educación rural inclusiva y equitativa' },
    { id: 4, numero_ods: 15, titulo: 'Vida de Ecosistemas Terrestres', descripcion: 'Restauración de páramos y cuencas en Sabana Norte' },
  ],
  categorias_causas: [
    { id: 1, nombre: 'Soberanía Alimentaria y Huertas', descripcion: 'Apoyo a familias campesinas y comedores veredales' },
    { id: 2, nombre: 'Educación y Conectividad Veredal', descripcion: 'Escuelas rurales, bibliotecas y formación' },
    { id: 3, nombre: 'Conservación de Páramos y Agua', descripcion: 'Reforestación nativa en cuencas altas' },
  ],
  tipos_necesidad: [
    { id: 1, codigo: 'ECONOMICA', nombre: 'Apoyo Económico Monetario' },
    { id: 2, codigo: 'ESPECIE', nombre: 'Donación en Especie (Insumos / Alimentos / Herramientas)' },
    { id: 3, codigo: 'TIEMPO_VOLUNTARIADO', nombre: 'Tiempo y Talento de Voluntariado' },
  ],
  unidades_medida: [
    { id: 1, simbolo: 'COP', nombre: 'Pesos Colombianos ($ COP)' },
    { id: 2, simbolo: 'KG', nombre: 'Kilogramos (kg)' },
    { id: 3, simbolo: 'LT', nombre: 'Litros (L)' },
    { id: 4, simbolo: 'UND', nombre: 'Unidades (und)' },
    { id: 5, simbolo: 'KIT', nombre: 'Kits / Paquetes' },
    { id: 6, simbolo: 'HORAS', nombre: 'Horas de Voluntariado (h)' },
  ],
  metodos_pago: [
    { id: 1, codigo: 'TRANSFERENCIA', nombre: 'Transferencia Bancaria / PSE' },
    { id: 2, codigo: 'BILLETERA_MOVIL', nombre: 'Nequi / DaviPlata Rural' },
  ],
  categorias_habilidades: [
    { id: 1, nombre: 'Agroecología y Campo', descripcion: 'Conocimientos técnicos agrícolas y ambientales' },
    { id: 2, nombre: 'Pedagogía y Salud Comunitaria', descripcion: 'Acompañamiento educativo y psicosocial' },
    { id: 3, nombre: 'Logística y Gestión', descripcion: 'Transporte veredal, acopio y contabilidad' },
  ],
  habilidades: [
    { id: 1, categoria_id: 1, nombre: 'Manejo de Huertas Orgánicas', descripcion: 'Compostaje y siembra sin agroquímicos' },
    { id: 2, categoria_id: 1, nombre: 'Reforestación de Especies Nativas', descripcion: 'Viverismo y plantación en alta montaña' },
    { id: 3, categoria_id: 2, nombre: 'Tutoría Escolar Primaria Rural', descripcion: 'Refuerzo en lectura, matemáticas y tecnología' },
    { id: 4, categoria_id: 3, nombre: 'Transporte y Distribución en Veredas', descripcion: 'Conducción 4x4 y entrega de acopios' },
  ],
  franjas_horarias: [
    { id: 1, codigo: 'FIN_SEMANA_MANANA', nombre: 'Fines de semana en la mañana (Sábados y Domingos 7:00 a.m. - 12:00 m.)', horas_sugeridas: 5 },
    { id: 2, codigo: 'FIN_SEMANA_TARDE', nombre: 'Fines de semana en la tarde (Sábados y Domingos 1:00 p.m. - 5:00 p.m.)', horas_sugeridas: 4 },
    { id: 3, codigo: 'SABADO_COMPLETO', nombre: 'Jornada completa de sábado (7:00 a.m. - 3:00 p.m.)', horas_sugeridas: 8 },
    { id: 4, codigo: 'ENTRE_SEMANA_MANANA', nombre: 'Entre semana en la mañana (Lunes a Viernes 8:00 a.m. - 12:00 m.)', horas_sugeridas: 4 },
    { id: 5, codigo: 'ENTRE_SEMANA_TARDE', nombre: 'Entre semana en la tarde (Lunes a Viernes 2:00 p.m. - 6:00 p.m.)', horas_sugeridas: 4 },
  ],
  parametros_sistema: [
    { id: 1, clave: 'MONTO_MINIMO_DONACION_COP', valor: '10000', descripcion: 'Importe mínimo permitido para aportes monetarios ($ COP)', tipo_dato: 'NUMERO' },
    { id: 2, clave: 'MAX_INTENTOS_LOGIN', valor: '5', descripcion: 'Número máximo de intentos fallidos antes de bloquear una cuenta', tipo_dato: 'NUMERO' },
    { id: 3, clave: 'NORMA_TRIBUTARIA_VIGENTE', valor: 'Artículos 125, 125-1, 125-2, 125-3 y 257 del Estatuto Tributario Nacional y Decreto 2150 de 2017', descripcion: 'Marco normativo impreso en los certificados de donación', tipo_dato: 'TEXTO' },
  ],
};

@Injectable({
  providedIn: 'root',
})
export class OfflineSyncService {
  private readonly http = inject(HttpClient);
  private readonly platformId = inject(PLATFORM_ID);
  private readonly CATALOGOS_CACHE_KEY = 'cs_catalogos_5fn_cache';

  readonly modoOfflineActivo = signal(false);

  obtenerCatalogos(): Observable<CatalogosGenerales> {
    return this.http.get<CatalogosGenerales>(`${getApiBaseUrl()}/catalogos/general`).pipe(
      tap((datos) => {
        this.modoOfflineActivo.set(false);
        if (isPlatformBrowser(this.platformId)) {
          localStorage.setItem(this.CATALOGOS_CACHE_KEY, JSON.stringify(datos));
        }
      }),
      catchError(() => {
        this.modoOfflineActivo.set(true);
        if (isPlatformBrowser(this.platformId)) {
          const guardado = localStorage.getItem(this.CATALOGOS_CACHE_KEY);
          if (guardado) {
            try {
              return of(JSON.parse(guardado) as CatalogosGenerales);
            } catch {
              return of(CATALOGOS_FALLBACK_SABANA);
            }
          }
        }
        return of(CATALOGOS_FALLBACK_SABANA);
      })
    );
  }

  guardarBorradorFormulario<T>(clave: string, datos: T): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.setItem(`cs_draft_${clave}`, JSON.stringify(datos));
    }
  }

  cargarBorradorFormulario<T>(clave: string): T | null {
    if (isPlatformBrowser(this.platformId)) {
      const raw = localStorage.getItem(`cs_draft_${clave}`);
      if (raw) {
        try {
          return JSON.parse(raw) as T;
        } catch {
          return null;
        }
      }
    }
    return null;
  }

  limpiarBorradorFormulario(clave: string): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem(`cs_draft_${clave}`);
    }
  }
}
