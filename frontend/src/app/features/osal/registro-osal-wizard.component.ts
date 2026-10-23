import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { OfflineSyncService, CatalogosGenerales } from '../../core/services/offline-sync.service';
import { getApiBaseUrl } from '../../core/config/api.config';

interface BorradorOsalWizard {
  nit: string;
  razon_social: string;
  sigla: string;
  mision: string;
  telefono_institucional: string;
  fecha_constitucion: string;
  municipio_id: number;
  vereda_o_barrio: string;
  direccion_fisica: string;
  indicaciones_rurales: string;
  latitud: number;
  longitud: number;
  nombres_representante: string;
  apellidos_representante: string;
  tipo_documento_id: number;
  numero_documento_representante: string;
  correo_electronico: string;
  contrasena: string;
  nombre_rut: string;
  nombre_camara: string;
}

@Component({
  selector: 'app-registro-osal-wizard',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div class="sap-page-header">
      <div class="sap-page-header-inner">
        <div>
          <span class="sap-breadcrumb">Directorio Institucional · Sabana Norte</span>
          <h1 class="sap-page-title">Vinculación de Organización Sin Ánimo de Lucro (OSAL)</h1>
          <p class="sap-page-subtitle">Asistente estructurado de registro institucional, localización rural y radicación de soportes legales.</p>
        </div>
        <div class="header-right">
          <span class="sap-badge sap-badge-info">Etapa {{ pasoActual() }} de 3</span>
          <a routerLink="/login" class="sap-btn-secondary">← Volver al Inicio</a>
        </div>
      </div>
    </div>

    <main class="sap-container">
      <div class="sap-wizard-steps" role="list" aria-label="Etapas del proceso de vinculación">
        <div class="sap-step" [class.active]="pasoActual() === 1" [class.completed]="pasoActual() > 1" role="listitem">
          <span class="step-num">1</span>
          <div class="step-info">
            <strong>Datos Institucionales</strong>
            <small>Identificación jurídica y misión</small>
          </div>
        </div>
        <div class="sap-step" [class.active]="pasoActual() === 2" [class.completed]="pasoActual() > 2" role="listitem">
          <span class="step-num">2</span>
          <div class="step-info">
            <strong>Ubicación y Representación</strong>
            <small>Georreferencia veredal y contacto</small>
          </div>
        </div>
        <div class="sap-step" [class.active]="pasoActual() === 3" role="listitem">
          <span class="step-num">3</span>
          <div class="step-info">
            <strong>Soportes Documentales</strong>
            <small>RUT y Certificado de Existencia (Obligatorios)</small>
          </div>
        </div>
      </div>

      @if (mensajeGuardadoOffline()) {
        <div class="cs-alert-human" role="alert">
          {{ mensajeGuardadoOffline() }}
        </div>
      }

      @if (mensajeExito()) {
        <section class="cs-card success-card" role="status">
          <div class="success-head">
            <span class="sap-badge sap-badge-ok">Radicación Completada</span>
            <h2>Expediente en Estado: Pendiente de Validación</h2>
          </div>
          <p>{{ mensajeExito() }}</p>
          <div class="success-actions">
            <a routerLink="/login" class="cs-btn">
              Finalizar Proceso y Volver al Inicio
            </a>
            <button type="button" class="sap-btn-secondary" (click)="reiniciarWizard()">
              Radicar otra organización
            </button>
          </div>
        </section>
      } @else {
        <form class="cs-card sap-wizard-card" (ngSubmit)="enviarRegistroOsal()" novalidate>
          @if (mensajeError()) {
            <div class="alert-error" role="alert">{{ mensajeError() }}</div>
          }

          @if (pasoActual() === 1) {
            <fieldset class="step-fieldset">
              <legend>Información Jurídica e Institucional</legend>

              <div class="grid-2">
                <div class="form-group">
                  <label for="nit" class="sap-form-label">NIT (con dígito de verificación) *</label>
                  <input id="nit" name="nit" type="text" class="sap-input" [(ngModel)]="form.nit" (ngModelChange)="persistirBorrador()" placeholder="Ej: 901540210-3" required />
                </div>
                <div class="form-group">
                  <label for="sigla" class="sap-form-label">Sigla o acrónimo institucional</label>
                  <input id="sigla" name="sigla" type="text" class="sap-input" [(ngModel)]="form.sigla" (ngModelChange)="persistirBorrador()" placeholder="Ej: FUNDASABANA" />
                </div>
              </div>

              <div class="form-group">
                <label for="razon_social" class="sap-form-label">Razón Social Completa *</label>
                <input id="razon_social" name="razon_social" type="text" class="sap-input" [(ngModel)]="form.razon_social" (ngModelChange)="persistirBorrador()" placeholder="Ej: Fundación Campesina Semillas del Neusa" required />
              </div>

              <div class="form-group">
                <label for="mision" class="sap-form-label">Objeto Social y Misión Territorial *</label>
                <textarea id="mision" name="mision" rows="3" class="sap-input" [(ngModel)]="form.mision" (ngModelChange)="persistirBorrador()" placeholder="Describe la población rural o el ecosistema beneficiado en la Sabana Norte..." required></textarea>
              </div>

              <div class="grid-2">
                <div class="form-group">
                  <label for="telefono" class="sap-form-label">Teléfono de Contacto Institucional *</label>
                  <input id="telefono" name="telefono" type="tel" class="sap-input" [(ngModel)]="form.telefono_institucional" (ngModelChange)="persistirBorrador()" placeholder="Ej: 3124567890" required />
                </div>
                <div class="form-group">
                  <label for="fecha_const" class="sap-form-label">Fecha de Constitución Legal</label>
                  <input id="fecha_const" name="fecha_const" type="date" class="sap-input" [(ngModel)]="form.fecha_constitucion" (ngModelChange)="persistirBorrador()" />
                </div>
              </div>

              <div class="wizard-actions">
                <a routerLink="/login" class="sap-btn-secondary">Cancelar y Volver al Inicio</a>
                <button type="button" class="cs-btn" (click)="irAlPaso(2)">
                  Continuar a Ubicación y Representación
                </button>
              </div>
            </fieldset>
          }

          @if (pasoActual() === 2) {
            <fieldset class="step-fieldset">
              <legend>Localización Rural y Representante Legal</legend>

              <div class="grid-2">
                <div class="form-group">
                  <label for="municipio" class="sap-form-label">Municipio de Jurisdicción *</label>
                  <select id="municipio" name="municipio" class="sap-input" [(ngModel)]="form.municipio_id" (ngModelChange)="actualizarCoordenadasMunicipio($event)">
                    @for (m of catalogos()?.municipios_sabana_norte || []; track m.id) {
                      <option [ngValue]="m.id">{{ m.nombre }}</option>
                    }
                  </select>
                </div>
                <div class="form-group">
                  <label for="vereda" class="sap-form-label">Vereda o Sector Rural *</label>
                  <input id="vereda" name="vereda" type="text" class="sap-input" [(ngModel)]="form.vereda_o_barrio" (ngModelChange)="persistirBorrador()" placeholder="Ej: Vereda Río Frío Occidental" required />
                </div>
              </div>

              <div class="form-group">
                <label for="direccion" class="sap-form-label">Dirección Física e Indicaciones de Acceso *</label>
                <input id="direccion" name="direccion" type="text" class="sap-input" [(ngModel)]="form.direccion_fisica" (ngModelChange)="persistirBorrador()" placeholder="Ej: Km 3 Vía San Jorge, junto al salón comunal" required />
              </div>

              <div class="grid-2">
                <div class="form-group">
                  <label for="latitud" class="sap-form-label">Latitud Geográfica</label>
                  <input id="latitud" name="latitud" type="number" step="0.0001" class="sap-input" [(ngModel)]="form.latitud" (ngModelChange)="persistirBorrador()" />
                </div>
                <div class="form-group">
                  <label for="longitud" class="sap-form-label">Longitud Geográfica</label>
                  <input id="longitud" name="longitud" type="number" step="0.0001" class="sap-input" [(ngModel)]="form.longitud" (ngModelChange)="persistirBorrador()" />
                </div>
              </div>

              <hr class="divider" />

              <div class="grid-2">
                <div class="form-group">
                  <label for="nombres_rep" class="sap-form-label">Nombres del Representante Legal *</label>
                  <input id="nombres_rep" name="nombres_rep" type="text" class="sap-input" [(ngModel)]="form.nombres_representante" (ngModelChange)="persistirBorrador()" required />
                </div>
                <div class="form-group">
                  <label for="apellidos_rep" class="sap-form-label">Apellidos del Representante Legal *</label>
                  <input id="apellidos_rep" name="apellidos_rep" type="text" class="sap-input" [(ngModel)]="form.apellidos_representante" (ngModelChange)="persistirBorrador()" required />
                </div>
              </div>

              <div class="grid-2">
                <div class="form-group">
                  <label for="num_doc" class="sap-form-label">Documento de Identidad del Representante *</label>
                  <input id="num_doc" name="num_doc" type="text" class="sap-input" [(ngModel)]="form.numero_documento_representante" (ngModelChange)="persistirBorrador()" required />
                </div>
                <div class="form-group">
                  <label for="correo_rep" class="sap-form-label">Correo Electrónico Institucional *</label>
                  <input id="correo_rep" name="correo_rep" type="email" class="sap-input" [(ngModel)]="form.correo_electronico" (ngModelChange)="persistirBorrador()" placeholder="contacto@fundacion.org" required />
                </div>
              </div>

              <div class="form-group">
                <label for="clave_rep" class="sap-form-label">Contraseña para la Cuenta de la Fundación *</label>
                <input id="clave_rep" name="clave_rep" type="password" class="sap-input" [(ngModel)]="form.contrasena" (ngModelChange)="persistirBorrador()" placeholder="Define una contraseña segura para ingresar al portal" required />
              </div>

              <div class="wizard-actions">
                <button type="button" class="sap-btn-secondary" (click)="irAlPaso(1)">
                  Regresar
                </button>
                <button type="button" class="cs-btn" (click)="irAlPaso(3)">
                  Continuar a Soportes Documentales
                </button>
              </div>
            </fieldset>
          }

          @if (pasoActual() === 3) {
            <fieldset class="step-fieldset">
              <legend>Anexos Legales Obligatorios y Radicación</legend>
              <p class="helper-note">
                Para evitar rechazos en la revisión administrativa, <strong>es obligatorio adjuntar ambos documentos vigentes</strong>. Al confirmar, la entidad quedará en estado <strong>Pendiente de Validación</strong>.
              </p>

              <div class="doc-upload-grid">
                <div class="doc-box" [class.doc-ready]="!!form.nombre_rut">
                  <label for="rut_file" class="sap-form-label">1. Registro Único Tributario (RUT - DIAN) *</label>
                  <input id="rut_file" type="file" class="sap-input" accept=".pdf,.png,.jpg" (change)="seleccionarArchivo($event, 'rut')" required />
                  @if (form.nombre_rut) {
                    <span class="file-tag ok">✅ Archivo cargado: {{ form.nombre_rut }}</span>
                  } @else {
                    <span class="file-tag pending">⚠️ Pendiente por adjuntar archivo</span>
                  }
                </div>

                <div class="doc-box" [class.doc-ready]="!!form.nombre_camara">
                  <label for="camara_file" class="sap-form-label">2. Certificado de Existencia y Representación Legal *</label>
                  <input id="camara_file" type="file" class="sap-input" accept=".pdf,.png,.jpg" (change)="seleccionarArchivo($event, 'camara')" required />
                  @if (form.nombre_camara) {
                    <span class="file-tag ok">✅ Archivo cargado: {{ form.nombre_camara }}</span>
                  } @else {
                    <span class="file-tag pending">⚠️ Pendiente por adjuntar archivo</span>
                  }
                </div>
              </div>

              <div class="wizard-actions">
                <button type="button" class="sap-btn-secondary" (click)="irAlPaso(2)">
                  Regresar
                </button>
                <button type="submit" class="cs-btn" [disabled]="enviando()">
                  {{ enviando() ? 'Procesando radicación...' : 'Radicar Solicitud de Vinculación' }}
                </button>
              </div>
            </fieldset>
          }
        </form>
      }
    </main>
  `,
  styles: [`
    .header-right { display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; }
    .sap-wizard-steps {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
    }
    .sap-step {
      display: flex;
      align-items: center;
      gap: 0.85rem;
      padding: 0.9rem 1.15rem;
      background: var(--sap-bg-surface);
      border: 1px solid var(--sap-border-subtle);
      border-bottom: 3px solid var(--sap-border-subtle);
      border-radius: 6px;
    }
    .sap-step.active {
      border-bottom-color: var(--sap-brand-primary);
      background: #F8FAFC;
    }
    .sap-step.completed {
      border-bottom-color: var(--sap-status-ok-border);
    }
    .step-num {
      width: 30px;
      height: 30px;
      border-radius: 50%;
      background: var(--sap-bg-subtle);
      color: var(--sap-text-primary);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 0.88rem;
    }
    .sap-step.active .step-num {
      background: var(--sap-brand-primary);
      color: #FFFFFF;
    }
    .sap-step.completed .step-num {
      background: var(--sap-accent-rural);
      color: #FFFFFF;
    }
    .step-info {
      display: flex;
      flex-direction: column;
    }
    .step-info strong {
      font-size: 0.92rem;
    }
    .step-info small {
      font-size: 0.78rem;
      color: var(--sap-text-secondary);
    }
    .sap-wizard-card {
      border-top: 3px solid var(--sap-brand-primary);
    }
    .step-fieldset {
      border: none;
      padding: 0;
      margin: 0;
    }
    legend {
      font-size: 1.15rem;
      font-weight: 700;
      margin-bottom: 1.25rem;
      padding-bottom: 0.65rem;
      width: 100%;
      border-bottom: 1px solid var(--sap-border-subtle);
    }
    .grid-2 {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1.15rem;
    }
    .form-group {
      margin-bottom: 1.1rem;
    }
    .doc-upload-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.15rem;
      margin-bottom: 1.25rem;
    }
    .doc-box {
      padding: 1rem;
      background: var(--sap-bg-canvas);
      border: 1px solid var(--sap-border-subtle);
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }
    .doc-box.doc-ready {
      border-color: var(--sap-status-ok-border);
      background: #F0FDF4;
    }
    .file-tag {
      font-size: 0.83rem;
      font-weight: 700;
    }
    .file-tag.ok { color: var(--sap-status-ok-text); }
    .file-tag.pending { color: var(--sap-status-err-text); }
    .wizard-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 1.5rem;
      padding-top: 1rem;
      border-top: 1px solid var(--sap-border-subtle);
    }
    .alert-error {
      border-left: 4px solid var(--sap-status-err-border);
      background: var(--sap-status-err-bg);
      color: var(--sap-status-err-text);
      padding: 0.85rem 1rem;
      border-radius: 6px;
      font-weight: 600;
      margin-bottom: 1rem;
    }
    .success-card {
      border-top: 4px solid var(--sap-status-ok-border);
    }
    .success-head h2 {
      margin: 0.5rem 0;
    }
    .success-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 0.85rem;
      margin-top: 1.25rem;
    }
    .divider {
      margin: 1.25rem 0;
      border: 0;
      border-top: 1px solid var(--sap-border-subtle);
    }
  `]
})
export class RegistroOsalWizardComponent implements OnInit {
  private readonly http = inject(HttpClient);
  private readonly offlineSync = inject(OfflineSyncService);
  private readonly DRAFT_KEY = 'cu02_registro_osal';

  pasoActual = signal(1);
  catalogos = signal<CatalogosGenerales | null>(null);
  enviando = signal(false);
  mensajeError = signal('');
  mensajeExito = signal('');
  mensajeGuardadoOffline = signal('');

  form: BorradorOsalWizard = this.crearFormularioPorDefecto();

  ngOnInit(): void {
    this.offlineSync.obtenerCatalogos().subscribe((cat) => {
      this.catalogos.set(cat);
    });

    const borrador = this.offlineSync.cargarBorradorFormulario<BorradorOsalWizard>(this.DRAFT_KEY);
    if (borrador) {
      if (borrador.nombre_rut === 'RUT_Fundacion_SabanaNorte.pdf') borrador.nombre_rut = '';
      if (borrador.nombre_camara === 'Certificado_Existencia_OSAL.pdf') borrador.nombre_camara = '';
      this.form = borrador;
      this.mensajeGuardadoOffline.set(
        'Restauramos automáticamente el avance de tu solicitud para que continúes donde ibas.'
      );
    }
  }

  crearFormularioPorDefecto(): BorradorOsalWizard {
    return {
      nit: '',
      razon_social: '',
      sigla: '',
      mision: '',
      telefono_institucional: '',
      fecha_constitucion: '2021-06-15',
      municipio_id: 6,
      vereda_o_barrio: '',
      direccion_fisica: '',
      indicaciones_rurales: '',
      latitud: 5.0617,
      longitud: -73.9806,
      nombres_representante: '',
      apellidos_representante: '',
      tipo_documento_id: 1,
      numero_documento_representante: '',
      correo_electronico: '',
      contrasena: '',
      nombre_rut: '',
      nombre_camara: '',
    };
  }

  persistirBorrador(): void {
    this.offlineSync.guardarBorradorFormulario(this.DRAFT_KEY, this.form);
  }

  actualizarCoordenadasMunicipio(municipioId: number): void {
    const mun = this.catalogos()?.municipios_sabana_norte.find((m) => m.id === Number(municipioId));
    if (mun) {
      this.form.latitud = mun.latitud_centro;
      this.form.longitud = mun.longitud_centro;
    }
    this.persistirBorrador();
  }

  seleccionarArchivo(event: Event, tipo: 'rut' | 'camara'): void {
    const input = event.target as HTMLInputElement;
    const archivo = input.files?.[0];
    if (archivo) {
      if (tipo === 'rut') {
        this.form.nombre_rut = archivo.name;
      } else {
        this.form.nombre_camara = archivo.name;
      }
      this.mensajeError.set('');
      this.persistirBorrador();
    }
  }

  irAlPaso(paso: number): void {
    this.mensajeError.set('');
    if (paso === 2 && (!this.form.nit.trim() || !this.form.razon_social.trim() || !this.form.mision.trim() || !this.form.telefono_institucional.trim())) {
      this.mensajeError.set('Por favor completa el NIT, la razón social, la misión y el teléfono antes de continuar.');
      return;
    }
    if (paso === 3 && (!this.form.vereda_o_barrio.trim() || !this.form.direccion_fisica.trim() || !this.form.nombres_representante.trim() || !this.form.apellidos_representante.trim() || !this.form.numero_documento_representante.trim() || !this.form.correo_electronico.trim() || !this.form.contrasena.trim())) {
      this.mensajeError.set('Completa la vereda, dirección, documento, correo y contraseña del representante legal antes de continuar.');
      return;
    }
    this.pasoActual.set(paso);
    this.persistirBorrador();
  }

  enviarRegistroOsal(): void {
    this.mensajeError.set('');

    if (!this.form.nombre_rut.trim() || !this.form.nombre_camara.trim()) {
      this.mensajeError.set(
        'No es posible radicar la solicitud sin los soportes legales. Por favor adjunta tanto el archivo del RUT (DIAN) como el Certificado de Existencia y Representación Legal.'
      );
      return;
    }

    this.enviando.set(true);

    const payload = {
      ...this.form,
      documentos_legales: [
        { tipo_soporte: 'RUT_DIAN', nombre_archivo: this.form.nombre_rut },
        { tipo_soporte: 'CERTIFICADO_EXISTENCIA_CAMARA', nombre_archivo: this.form.nombre_camara },
      ],
    };

    this.http.post<{ mensaje_humano: string }>(`${getApiBaseUrl()}/osal/registro`, payload).subscribe({
      next: (res) => {
        this.enviando.set(false);
        this.offlineSync.limpiarBorradorFormulario(this.DRAFT_KEY);
        this.mensajeGuardadoOffline.set('');
        this.mensajeExito.set(res.mensaje_humano);
      },
      error: (err) => {
        this.enviando.set(false);
        this.persistirBorrador();
        if (err.status === 0) {
          this.mensajeGuardadoOffline.set(
            'Tu conexión parece inestable en la vereda. Hemos guardado todos los pasos del registro de tu fundación en este dispositivo para que lo envíes apenas recuperes la señal.'
          );
        } else {
          this.mensajeError.set(err.error?.mensaje_humano || 'Ocurrió un inconveniente al registrar la fundación.');
        }
      },
    });
  }

  reiniciarWizard(): void {
    this.form = this.crearFormularioPorDefecto();
    this.pasoActual.set(1);
    this.mensajeExito.set('');
  }
}
