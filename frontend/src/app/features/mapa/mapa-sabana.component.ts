import { Component, OnInit, AfterViewInit, PLATFORM_ID, inject, signal } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { OfflineSyncService, CatalogosGenerales } from '../../core/services/offline-sync.service';
import { getApiBaseUrl } from '../../core/config/api.config';

export interface PinSabanaNorte {
  fundacion_id: number;
  nit: string;
  razon_social: string;
  sigla: string;
  mision: string;
  estado_validacion: string;
  telefono: string;
  municipio_id: number;
  municipio_nombre: string;
  codigo_dane: string;
  vereda_o_barrio: string;
  direccion_fisica: string;
  indicaciones_rurales: string;
  latitud: number;
  longitud: number;
  campanas_activas: string[];
  total_campanas: number;
}

const PINES_FALLBACK_SABANA: PinSabanaNorte[] = [
  {
    fundacion_id: 1,
    nit: '901458932-1',
    razon_social: 'Fundación Agroecológica Raíces de Sabana Norte',
    sigla: 'FARASAN',
    mision: 'Fortalecer la soberanía alimentaria y restaurar microcuencas en las veredas de Cogua, Zipaquirá y Tabio.',
    estado_validacion: 'APROBADA',
    telefono: '3114509876',
    municipio_id: 6,
    municipio_nombre: 'Cogua',
    codigo_dane: '25200',
    vereda_o_barrio: 'Vereda Quebrada Honda',
    direccion_fisica: 'Km 4 Vía Neusa - Escuela Vieja',
    indicaciones_rurales: 'Frente al tanque comunitario de acueducto veredal',
    latitud: 5.0785,
    longitud: -73.9891,
    campanas_activas: ['Huertas Escolares Resilientes en Veredas de Cogua y Tabio'],
    total_campanas: 1,
  },
];

@Component({
  selector: 'app-mapa-sabana',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="sap-page-header">
      <div class="sap-page-header-inner">
        <div>
          <span class="sap-breadcrumb">Sistema de Información Geográfica · Sabana Norte</span>
          <h1 class="sap-page-title">Visor Georreferenciado de Organizaciones Rurales</h1>
          <p class="sap-page-subtitle">Monitoreo espacial de sedes operativas, jurisdicciones municipales y cobertura veredal en Cundinamarca.</p>
        </div>

        <div class="filter-bar">
          <label for="mun_filter" class="sap-form-label">Filtrar por Municipio</label>
          <select id="mun_filter" class="sap-input" [(ngModel)]="municipioFiltro" (ngModelChange)="filtrarPorMunicipio()">
            <option [ngValue]="0">Todos los municipios (Sabana Norte)</option>
            @for (m of catalogos()?.municipios_sabana_norte || []; track m.id) {
              <option [ngValue]="m.id">{{ m.nombre }}</option>
            }
          </select>
        </div>
      </div>
    </div>

    <main class="sap-container">
      <div class="map-layout">
        <section class="cs-card map-card" aria-label="Cartografía interactiva de Sabana Norte">
          <div class="map-toolbar">
            <strong>Cartografía Base OpenStreetMap · Cobertura Rural</strong>
            <span class="sap-badge sap-badge-info">{{ pines().length }} Sedes Localizadas</span>
          </div>
          <div id="leaflet-sabana-map" class="leaflet-canvas"></div>
        </section>

        <section class="pins-sidebar" aria-label="Directorio de sedes georreferenciadas">
          <div class="sidebar-header">
            <h2>Directorio de Sedes en el Territorio</h2>
          </div>

          @for (p of pines(); track p.fundacion_id) {
            <article class="cs-card pin-card" (click)="centrarPinEnMapa(p)" tabindex="0">
              <div class="pin-top">
                <span class="sap-badge sap-badge-info">{{ p.municipio_nombre }} · {{ p.vereda_o_barrio }}</span>
                <span class="sap-badge sap-badge-ok">{{ p.estado_validacion === 'APROBADA' ? 'Verificada' : p.estado_validacion }}</span>
              </div>
              <h3>{{ p.razon_social }}</h3>
              <p class="dir-text">{{ p.direccion_fisica }} — {{ p.indicaciones_rurales || 'Sector rural' }}</p>
              <div class="meta-strip">
                <span>NIT: {{ p.nit }}</span>
                <span>Tel: {{ p.telefono || 'Sin registro' }}</span>
              </div>
              <div class="pin-actions">
                <a routerLink="/campanas" class="cs-btn btn-sm">Ver Causas Activas ({{ p.total_campanas }})</a>
              </div>
            </article>
          }
        </section>
      </div>
    </main>
  `,
  styles: [`
    .filter-bar { min-width: 280px; }
    .map-layout { display: grid; grid-template-columns: 1.65fr 1fr; gap: 1.5rem; align-items: start; }
    @media (max-width: 920px) { .map-layout { grid-template-columns: 1fr; } }
    .map-card { padding: 1rem; border-top: 3px solid var(--sap-brand-primary); }
    .map-toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; font-size: 0.88rem; }
    .leaflet-canvas { width: 100%; height: 540px; border-radius: 6px; border: 1px solid var(--sap-border-subtle); }
    .pins-sidebar { display: flex; flex-direction: column; gap: 0.9rem; }
    .sidebar-header h2 { margin: 0; font-size: 1.05rem; text-transform: uppercase; letter-spacing: 0.03em; color: var(--sap-text-secondary); }
    .pin-card { cursor: pointer; border-left: 4px solid var(--sap-brand-primary); padding: 1.15rem; transition: box-shadow 0.15s ease, transform 0.15s ease; }
    .pin-card:hover { transform: translateY(-2px); }
    .pin-top { display: flex; justify-content: space-between; gap: 0.5rem; margin-bottom: 0.5rem; }
    .pin-card h3 { margin: 0.2rem 0; font-size: 1.05rem; }
    .dir-text { margin: 0.25rem 0 0.6rem 0; font-size: 0.88rem; color: var(--sap-text-secondary); }
    .meta-strip { display: flex; justify-content: space-between; font-size: 0.78rem; font-family: monospace; color: var(--sap-text-secondary); padding: 0.4rem 0.6rem; background: var(--sap-bg-canvas); border-radius: 4px; margin-bottom: 0.8rem; }
    .pin-actions { display: flex; gap: 0.6rem; }
    .btn-sm { min-height: 36px; padding: 0.35rem 0.85rem; font-size: 0.84rem; }
  `]
})
export class MapaSabanaComponent implements OnInit, AfterViewInit {
  private readonly http = inject(HttpClient);
  private readonly offlineSync = inject(OfflineSyncService);
  private readonly platformId = inject(PLATFORM_ID);

  catalogos = signal<CatalogosGenerales | null>(null);
  pines = signal<PinSabanaNorte[]>([]);
  municipioFiltro = 0;

  private mapInstance: any = null;
  private leafletLib: any = null;
  private markersLayer: any = null;

  ngOnInit(): void {
    this.offlineSync.obtenerCatalogos().subscribe((cat) => this.catalogos.set(cat));
    this.cargarPines();
  }

  async ngAfterViewInit(): Promise<void> {
    if (!isPlatformBrowser(this.platformId)) {
      return;
    }
    const L = await import('leaflet');
    this.leafletLib = L.default || L;

    this.mapInstance = this.leafletLib.map('leaflet-sabana-map').setView([4.965, -74.01], 11);
    this.leafletLib
      .tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors · Sabana Norte de Cundinamarca',
        maxZoom: 18,
      })
      .addTo(this.mapInstance);

    this.markersLayer = this.leafletLib.layerGroup().addTo(this.mapInstance);
    this.renderizarMarcadores();
  }

  cargarPines(): void {
    const base = getApiBaseUrl();
    const url =
      this.municipioFiltro > 0
        ? `${base}/mapa/pines?municipio_id=${this.municipioFiltro}`
        : `${base}/mapa/pines`;

    this.http.get<{ pines: PinSabanaNorte[] }>(url).subscribe({
      next: (res) => {
        this.pines.set(res.pines.length > 0 ? res.pines : PINES_FALLBACK_SABANA);
        this.renderizarMarcadores();
      },
      error: () => {
        this.pines.set(PINES_FALLBACK_SABANA);
        this.renderizarMarcadores();
      },
    });
  }

  filtrarPorMunicipio(): void {
    this.cargarPines();
  }

  renderizarMarcadores(): void {
    if (!this.mapInstance || !this.leafletLib || !this.markersLayer) {
      return;
    }
    this.markersLayer.clearLayers();

    for (const p of this.pines()) {
      const marker = this.leafletLib.circleMarker([p.latitud, p.longitud], {
        radius: 10,
        fillColor: '#0057D2',
        color: '#FFFFFF',
        weight: 3,
        opacity: 1,
        fillOpacity: 0.92,
      });

      marker.bindPopup(`
        <div style="font-family: 'Segoe UI', system-ui; min-width: 210px;">
          <strong style="color:#0057D2; font-size:14px;">${p.razon_social}</strong><br/>
          <span><b>Municipio:</b> ${p.municipio_nombre} (${p.vereda_o_barrio})</span><br/>
          <span><b>Dirección:</b> ${p.direccion_fisica}</span><br/>
          <span><b>Estado:</b> ${p.estado_validacion}</span>
        </div>
      `);

      marker.addTo(this.markersLayer);
    }
  }

  centrarPinEnMapa(pin: PinSabanaNorte): void {
    if (this.mapInstance) {
      this.mapInstance.setView([pin.latitud, pin.longitud], 14);
    }
  }
}
