import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { OfflineSyncService, CatalogosGenerales } from '../../core/services/offline-sync.service';

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
  imports: [CommonModule, FormsModule],
  template: `
    <main class="wizard-container" aria-labelledby="osal-wizard-title">
      <header class="cs-card wizard-header">
        <span class="step-badge">CU02 · Paso {{ pasoActual() }} de 3</span>
        <h1 id="osal-wizard-title">Registro de Fundación (OSAL) en Sabana Norte</h1>
        <p>
          Formulario asistido paso a paso con guardado automático Offline-First para evitar pérdida de datos en veredas con baja señal.
        </p>

        <div class="progress-steps" role="list" aria-label="Progreso del registro">
          <div class="step-pill" [class.active]="pasoActual() === 1" [class.done]="pasoActual() > 1" role="listitem">
            1. Datos Institucionales
          </div>
          <div class="step-pill" [class.active]="pasoActual() === 2" [class.done]="pasoActual() > 2" role="listitem">
            2. Ubicación Rural y Representante
          </div>
          <div class="step-pill" [class.active]="pasoActual() === 3" role="listitem">
            3. Documentos Legales y Envío
          </div>
        </div>
      </header>

      @if (mensajeGuardadoOffline()) {
        <div class="cs-alert-human" role="alert">
          {{ mensajeGuardadoOffline() }}
        </div>
      }

      @if (mensajeExito()) {
        <section class="cs-card success-card" role="status">
          <h2>¡Registro Recibido! Estado: PENDIENTE DE VALIDACIÓN</h2>
          <p>{{ mensajeExito() }}</p>
          <button type="button" class="cs-btn" (click)="reiniciarWizard()">
            Registrar otra organización
          </button>
        </section>
      } @else {
        <form class="cs-card wizard-body" (ngSubmit)="enviarRegistroOsal()" novalidate>
          @if (mensajeError()) {
            <div class="alert-error" role="alert">{{ mensajeError() }}</div>
          }

          <!-- PASO 1: DATOS INSTITUCIONALES -->
          @if (pasoActual() === 1) {
            <fieldset class="step-fieldset">
              <legend>Paso 1: Identidad de la Fundación u Organización Solidaria</legend>

              <div class="grid-2">
                <div class="form-group">
                  <label for="nit">NIT (con dígito de verificación) *</label>
                  <input id="nit" name="nit" type="text" [(ngModel)]="form.nit" (ngModelChange)="persistirBorrador()" placeholder="Ej: 901540210-3" required />
                </div>
                <div class="form-group">
                  <label for="sigla">Sigla o nombre corto</label>
                  <input id="sigla" name="sigla" type="text" [(ngModel)]="form.sigla" (ngModelChange)="persistirBorrador()" placeholder="Ej: FUNDASABANA" />
                </div>
              </div>

              <div class="form-group">
                <label for="razon_social">Razón Social Completa *</label>
                <input id="razon_social" name="razon_social" type="text" [(ngModel)]="form.razon_social" (ngModelChange)="persistirBorrador()" placeholder="Ej: Fundación Campesina Semillas del Neusa" required />
              </div>

              <div class="form-group">
                <label for="mision">Misión Comunitaria en la Sabana Norte *</label>
                <textarea id="mision" name="mision" rows="3" [(ngModel)]="form.mision" (ngModelChange)="persistirBorrador()" placeholder="Describe brevemente a qué población rural o ecosistema beneficia la fundación..." required></textarea>
              </div>

              <div class="grid-2">
                <div class="form-group">
                  <label for="telefono">Teléfono / WhatsApp Comunitario *</label>
                  <input id="telefono" name="telefono" type="tel" [(ngModel)]="form.telefono_institucional" (ngModelChange)="persistirBorrador()" placeholder="Ej: 3124567890" required />
                </div>
                <div class="form-group">
                  <label for="fecha_const">Fecha de Constitución Legal</label>
                  <input id="fecha_const" name="fecha_const" type="date" [(ngModel)]="form.fecha_constitucion" (ngModelChange)="persistirBorrador()" />
                </div>
              </div>

              <div class="wizard-actions">
                <span></span>
                <button type="button" class="cs-btn" (click)="irAlPaso(2)">
                  Siguiente: Ubicación Rural →
                </button>
              </div>
            </fieldset>
          }

          <!-- PASO 2: UBICACIÓN RURAL Y REPRESENTANTE -->
          @if (pasoActual() === 2) {
            <fieldset class="step-fieldset">
              <legend>Paso 2: Georreferenciación en Sabana Norte y Representante Legal</legend>

              <div class="grid-2">
                <div class="form-group">
                  <label for="municipio">Municipio (Sabana Norte) *</label>
                  <select id="municipio" name="municipio" [(ngModel)]="form.municipio_id" (ngModelChange)="actualizarCoordenadasMunicipio($event)">
                    @for (m of catalogos()?.municipios_sabana_norte || []; track m.id) {
                      <option [ngValue]="m.id">{{ m.nombre }}</option>
                    }
                  </select>
                </div>
                <div class="form-group">
                  <label for="vereda">Vereda o Sector Rural *</label>
                  <input id="vereda" name="vereda" type="text" [(ngModel)]="form.vereda_o_barrio" (ngModelChange)="persistirBorrador()" placeholder="Ej: Vereda Río Frío Occidental" required />
                </div>
              </div>

              <div class="form-group">
                <label for="direccion">Dirección Física o Punto de Referencia *</label>
                <input id="direccion" name="direccion" type="text" [(ngModel)]="form.direccion_fisica" (ngModelChange)="persistirBorrador()" placeholder="Ej: Km 3 Vía San Jorge, junto al salón comunal" required />
              </div>

              <div class="grid-2">
                <div class="form-group">
                  <label for="latitud">Latitud Geográfica (Sabana Norte)</label>
                  <input id="latitud" name="latitud" type="number" step="0.0001" [(ngModel)]="form.latitud" (ngModelChange)="persistirBorrador()" />
                </div>
                <div class="form-group">
                  <label for="longitud">Longitud Geográfica</label>
                  <input id="longitud" name="longitud" type="number" step="0.0001" [(ngModel)]="form.longitud" (ngModelChange)="persistirBorrador()" />
                </div>
              </div>

              <hr class="divider" />

              <div class="grid-2">
                <div class="form-group">
                  <label for="nombres_rep">Nombres del Representante Legal *</label>
                  <input id="nombres_rep" name="nombres_rep" type="text" [(ngModel)]="form.nombres_representante" (ngModelChange)="persistirBorrador()" required />
                </div>
                <div class="form-group">
                  <label for="apellidos_rep">Apellidos del Representante Legal *</label>
                  <input id="apellidos_rep" name="apellidos_rep" type="text" [(ngModel)]="form.apellidos_representante" (ngModelChange)="persistirBorrador()" required />
                </div>
              </div>

              <div class="grid-2">
                <div class="form-group">
                  <label for="num_doc">Número de Documento del Representante *</label>
                  <input id="num_doc" name="num_doc" type="text" [(ngModel)]="form.numero_documento_representante" (ngModelChange)="persistirBorrador()" required />
                </div>
                <div class="form-group">
                  <label for="correo_rep">Correo Institucional de Acceso *</label>
                  <input id="correo_rep" name="correo_rep" type="email" [(ngModel)]="form.correo_electronico" (ngModelChange)="persistirBorrador()" required />
                </div>
              </div>

              <div class="wizard-actions">
                <button type="button" class="btn-secondary" (click)="irAlPaso(1)">
                  ← Volver al Paso 1
                </button>
                <button type="button" class="cs-btn" (click)="irAlPaso(3)">
                  Siguiente: Documentos Legales →
                </button>
              </div>
            </fieldset>
          }

          <!-- PASO 3: DOCUMENTOS LEGALES Y ENVÍO -->
          @if (pasoActual() === 3) {
            <fieldset class="step-fieldset">
              <legend>Paso 3: Soportes Legales (documentos_legales_osal)</legend>
              <p class="helper-note">
                Adjunta o confirma los nombres de los certificados legales de tu organización. Tu fundación quedará en estado <strong>PENDIENTE</strong> mientras un auditor verifica la documentación.
              </p>

              <div class="form-group">
                <label for="rut_file">1. Copia del RUT actualizado (DIAN) *</label>
                <input id="rut_file" type="file" accept=".pdf,.png,.jpg" (change)="seleccionarArchivo($event, 'rut')" />
                <small>Archivo registrado: <strong>{{ form.nombre_rut }}</strong></small>
              </div>

              <div class="form-group">
                <label for="camara_file">2. Certificado de Existencia y Representación Legal (Cámara de Comercio / Gobernación) *</label>
                <input id="camara_file" type="file" accept=".pdf,.png,.jpg" (change)="seleccionarArchivo($event, 'camara')" />
                <small>Archivo registrado: <strong>{{ form.nombre_camara }}</strong></small>
              </div>

              <div class="wizard-actions">
                <button type="button" class="btn-secondary" (click)="irAlPaso(2)">
                  ← Volver al Paso 2
                </button>
                <button type="submit" class="cs-btn" [disabled]="enviando()">
                  {{ enviando() ? 'Enviando registro...' : 'Finalizar y Enviar para Validación' }}
                </button>
              </div>
            </fieldset>
          }
        </form>
      }
    </main>
  `,
  styles: [`
    .wizard-container {
      max-width: 860px;
      margin: 2rem auto;
      padding: 0 1.5rem;
    }
    .wizard-header {
      margin-bottom: 1.5rem;
      border-color: var(--brand-primary);
    }
    .step-badge {
      display: inline-block;
      background: var(--status-ok-bg);
      color: var(--status-ok-text);
      font-weight: 800;
      padding: 0.25rem 0.75rem;
      border-radius: 999px;
      font-size: 0.875rem;
    }
    .progress-steps {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 0.75rem;
      margin-top: 1rem;
    }
    .step-pill {
      padding: 0.75rem;
      border-radius: 8px;
      border: 2px solid var(--border-subtle);
      font-weight: 700;
      text-align: center;
      background: #F3F4F6;
    }
    .step-pill.active {
      border-color: var(--brand-primary);
      background: var(--status-ok-bg);
      color: var(--status-ok-text);
    }
    .step-pill.done {
      border-color: var(--brand-primary);
      background: #FFFFFF;
    }
    .step-fieldset {
      border: none;
      padding: 0;
      margin: 0;
    }
    legend {
      font-size: 1.3rem;
      font-weight: 800;
      margin-bottom: 1.25rem;
      color: var(--text-primary);
    }
    .grid-2 {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1rem;
    }
    .form-group {
      display: flex;
      flex-direction: column;
      margin-bottom: 1.15rem;
    }
    label {
      font-weight: 700;
      margin-bottom: 0.4rem;
    }
    input, select, textarea {
      min-height: 48px;
      padding: 0.7rem 0.9rem;
      font-size: 1rem;
      border: 2px solid var(--border-strong);
      border-radius: 8px;
      background: #FFFFFF;
      color: var(--text-primary);
    }
    .wizard-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 1.5rem;
      gap: 1rem;
    }
    .btn-secondary {
      min-height: 48px;
      padding: 0.75rem 1.25rem;
      font-weight: 700;
      background: #FFFFFF;
      color: var(--text-primary);
      border: 2px solid var(--border-strong);
      border-radius: 8px;
      cursor: pointer;
    }
    .alert-error {
      border-left: 6px solid var(--status-err-text);
      background: var(--status-err-bg);
      color: var(--status-err-text);
      padding: 1rem;
      border-radius: 8px;
      font-weight: 700;
      margin-bottom: 1rem;
    }
    .success-card {
      border-color: var(--brand-primary);
      background: var(--status-ok-bg);
      color: var(--status-ok-text);
    }
    .divider {
      margin: 1.25rem 0;
      border: 0;
      border-top: 2px solid var(--border-subtle);
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
      this.form = borrador;
      this.mensajeGuardadoOffline.set(
        'Recuperamos automáticamente los datos que estabas escribiendo antes en este formulario.'
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
      municipio_id: 6, // Cogua por defecto
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
      contrasena: 'Solidaria2026*',
      nombre_rut: 'RUT_Fundacion_SabanaNorte.pdf',
      nombre_camara: 'Certificado_Existencia_OSAL.pdf',
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
      this.persistirBorrador();
    }
  }

  irAlPaso(paso: number): void {
    this.mensajeError.set('');
    if (paso === 2 && (!this.form.nit.trim() || !this.form.razon_social.trim() || !this.form.mision.trim() || !this.form.telefono_institucional.trim())) {
      this.mensajeError.set('Por favor completa el NIT, la razón social, la misión y el teléfono antes de pasar al Paso 2.');
      return;
    }
    if (paso === 3 && (!this.form.vereda_o_barrio.trim() || !this.form.direccion_fisica.trim() || !this.form.nombres_representante.trim() || !this.form.correo_electronico.trim())) {
      this.mensajeError.set('Completa la vereda, dirección y los datos del representante legal antes de continuar al Paso 3.');
      return;
    }
    this.pasoActual.set(paso);
    this.persistirBorrador();
  }

  enviarRegistroOsal(): void {
    this.mensajeError.set('');
    this.enviando.set(true);

    const payload = {
      ...this.form,
      documentos_legales: [
        { tipo_soporte: 'RUT_DIAN', nombre_archivo: this.form.nombre_rut },
        { tipo_soporte: 'CERTIFICADO_EXISTENCIA_CAMARA', nombre_archivo: this.form.nombre_camara },
      ],
    };

    this.http.post<{ mensaje_humano: string }>('http://localhost:5000/api/osal/registro', payload).subscribe({
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

