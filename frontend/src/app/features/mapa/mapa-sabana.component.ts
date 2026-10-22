import { Component, OnInit, AfterViewInit, PLATFORM_ID, inject, signal } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { OfflineSyncService, CatalogosGenerales } from '../../core/services/offline-sync.service';

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
    <main class="container" aria-labelledby="cu06-heading">
      <header class="cs-card header-banner">
        <div>
          <span class="tag-pill">CU06 · Mapa Georreferenciado con Leaflet.js (5FN)</span>
          <h1 id="cu06-heading">Territorio Solidario: Sabana Norte de Cundinamarca</h1>
          <p>
            Cruza en tiempo real las tablas <code>fundaciones_osal</code>, <code>direcciones</code> y <code>municipios</code> para ubicar cada organización comunitaria y sus veredas.
          </p>
        </div>

        <div class="filter-box">
          <label for="mun_filter">Filtrar por Municipio:</label>
          <select id="mun_filter" [(ngModel)]="municipioFiltro" (ngModelChange)="filtrarPorMunicipio()">
            <option [ngValue]="0">Todos los municipios (Sabana Norte)</option>
            @for (m of catalogos()?.municipios_sabana_norte || []; track m.id) {
              <option [ngValue]="m.id">{{ m.nombre }}</option>
            }
          </select>
        </div>
      </header>

      <div class="map-layout">
        <!-- LIENZO INTERACTIVO LEAFLET.JS -->
        <section class="cs-card map-card" aria-label="Mapa interactivo de fundaciones en la Sabana Norte">
          <div id="leaflet-sabana-map" class="leaflet-canvas"></div>
        </section>

        <!-- TARJETAS LATERALES ACCESIBLES (WCAG 2.2 ALTERNATIVA TEXTUAL AL MAPA) -->
        <section class="pins-sidebar" aria-label="Listado accesible de fundaciones en el mapa">
          <h2>Fundaciones Georreferenciadas ({{ pines().length }})</h2>
          @for (p of pines(); track p.fundacion_id) {
            <article class="cs-card pin-card" (click)="centrarPinEnMapa(p)" tabindex="0">
              <div class="pin-top">
                <span class="mun-tag">📍 {{ p.municipio_nombre }} · {{ p.vereda_o_barrio }}</span>
                <span class="val-tag">{{ p.estado_validacion }}</span>
              </div>
              <h3>{{ p.razon_social }}</h3>
              <p class="dir-text">{{ p.direccion_fisica }} ({{ p.indicaciones_rurales || 'Zona rural' }})</p>
              <p class="coords-text">Coordenadas: {{ p.latitud }}, {{ p.longitud }}</p>
              <div class="pin-actions">
                <a routerLink="/campanas" class="btn-link">Ver Campañas ({{ p.total_campanas }})</a>
                <a routerLink="/donar" class="btn-link">Apoyar OSAL</a>
              </div>
            </article>
          }
        </section>
      </div>
    </main>
  `,
  styles: [`
    .container { max-width: 1140px; margin: 2rem auto; padding: 0 1.5rem; }
    .header-banner { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1.5rem; border-color: var(--brand-primary); }
    .header-banner h1 { margin: 0.4rem 0; font-size: 1.7rem; }
    .tag-pill { display: inline-block; background: var(--status-ok-bg); color: var(--status-ok-text); font-weight: 800; padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.85rem; }
    .filter-box { display: flex; flex-direction: column; min-width: 250px; }
    .filter-box label { font-weight: 700; margin-bottom: 0.35rem; }
    .filter-box select { min-height: 48px; padding: 0.6rem 0.85rem; border: 2px solid var(--border-strong); border-radius: 8px; font-size: 1rem; }
    .map-layout { display: grid; grid-template-columns: 1.6fr 1fr; gap: 1.5rem; align-items: start; }
    @media (max-width: 900px) { .map-layout { grid-template-columns: 1fr; } }
    .map-card { padding: 0.75rem; border-color: var(--border-strong); }
    .leaflet-canvas { width: 100%; height: 520px; border-radius: 8px; border: 2px solid var(--border-subtle); }
    .pins-sidebar { display: flex; flex-direction: column; gap: 1rem; }
    .pins-sidebar h2 { margin: 0; font-size: 1.25rem; }
    .pin-card { cursor: pointer; border-color: var(--border-strong); transition: transform 0.15s ease; }
    .pin-card:hover { transform: translateY(-2px); border-color: var(--brand-primary); }
    .pin-top { display: flex; justify-content: space-between; gap: 0.5rem; margin-bottom: 0.4rem; }
    .mun-tag { background: var(--status-warn-bg); color: var(--status-warn-text); font-weight: 800; padding: 0.2rem 0.55rem; border-radius: 6px; font-size: 0.8rem; }
    .val-tag { background: var(--status-ok-bg); color: var(--status-ok-text); font-weight: 800; padding: 0.2rem 0.55rem; border-radius: 6px; font-size: 0.78rem; }
    .pin-card h3 { margin: 0.25rem 0; font-size: 1.1rem; }
    .dir-text { margin: 0.25rem 0; font-size: 0.9rem; color: var(--text-secondary); }
    .coords-text { margin: 0.2rem 0 0.6rem 0; font-size: 0.8rem; font-family: monospace; color: var(--brand-primary); }
    .pin-actions { display: flex; gap: 1rem; }
    .btn-link { font-weight: 800; color: var(--brand-primary); text-decoration: underline; }
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
    const url =
      this.municipioFiltro > 0
        ? `http://localhost:5000/api/mapa/pines?municipio_id=${this.municipioFiltro}`
        : 'http://localhost:5000/api/mapa/pines';

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
        radius: 11,
        fillColor: '#14532D',
        color: '#FFFFFF',
        weight: 3,
        opacity: 1,
        fillOpacity: 0.92,
      });

      marker.bindPopup(`
        <div style="font-family: system-ui; min-width: 210px;">
          <strong style="color:#14532D; font-size:14px;">${p.razon_social}</strong><br/>
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
