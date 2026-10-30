# Borrador 4 (Anexo G): Fragmentos de Código Relevantes y Evidencia de Construcción del MVP

> **Propósito de este documento:** Constituir el **Anexo G (Fragmentos de código relevantes)** y sustentar técnicamente los apartados `5.4.4 (Desarrollo de módulos y funcionalidades)` y `5.4.7 (Evidencias del desarrollo del software)` del documento entregable (`conexion_solidaria_v3 (1).docx`).

---

## 1. Control de Acceso Basado en Roles (RBAC) y Jerarquía de Superusuario (`backend/app/security.py`)

Este decorador intercepta cada petición HTTP en los endpoints protegidos, verifica la firma criptográfica del token **JWT (`HS256`)**, extrae la lista de roles asignados en Quinta Forma Normal y aplica herencia automática de privilegios para el rol **`SUPER_ADMIN`**, manteniendo exclusivos aquellos endpoints marcados únicamente para gobierno maestro (`@requiere_roles("SUPER_ADMIN")`):

```python
# Archivo: backend/app/security.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def requiere_roles(*roles_permitidos: str):
    """
    Decorador de autorización RBAC.
    Verifica el JWT en la cabecera Authorization y valida que el usuario posea al menos
    uno de los roles requeridos. El rol SUPER_ADMIN hereda automáticamente los permisos
    operativos de ADMIN, pero las rutas exclusivas de SUPER_ADMIN permanecen restringidas.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            roles_usuario = set(claims.get("roles", []))
            roles_objetivo = set(roles_permitidos)
            if "ADMIN" in roles_objetivo:
                roles_objetivo.add("SUPER_ADMIN")

            if not roles_usuario.intersection(roles_objetivo):
                return jsonify({
                    "error": "Acceso denegado por permisos insuficientes (RBAC)",
                    "mensaje_humano": (
                        f"Tu perfil actual no cuenta con los permisos necesarios para esta acción. "
                        f"Se requiere uno de los siguientes roles: {', '.join(roles_permitidos)}."
                    ),
                    "roles_requeridos": list(roles_permitidos),
                    "roles_usuario": list(roles_usuario)
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
```

---

## 2. Validación de Radicación Documental Obligatoria y Habeas Data Ley 1581 (`backend/app/blueprints/osal.py`)

Implementación del protocolo de acreditación jurídica (`CU02`), que impide radicar solicitudes de vinculación sin los dos soportes legales obligatorios (**RUT DIAN** y **Certificado de Existencia y Representación Legal de Cámara de Comercio**) y sin la aceptación expresa de la **Ley Estatutaria 1581 de 2012**:

```python
# Archivo: backend/app/blueprints/osal.py (Extracto de POST /api/osal/registro)
documentos_legales = data.get("documentos_legales") or []
acepta_tratamiento_datos = data.get("acepta_tratamiento_datos", True)

if not acepta_tratamiento_datos:
    return jsonify({
        "error": "Autorización de Habeas Data requerida",
        "mensaje_humano": (
            "De conformidad con la Ley Estatutaria 1581 de 2012 (Habeas Data), "
            "debes autorizar el tratamiento de datos personales e institucionales para radicar la solicitud."
        )
    }), 400

# Validación estricta de Soportes Documentales obligatorios (RUT y Cámara de Comercio)
docs_validos = [
    d for d in documentos_legales
    if isinstance(d, dict) and (d.get("nombre_archivo") or "").strip()
]
if len(docs_validos) < 2:
    return jsonify({
        "error": "Soportes documentales obligatorios faltantes",
        "mensaje_humano": (
            "Para radicar la solicitud es obligatorio adjuntar tanto el Registro Único Tributario (RUT) "
            "como el Certificado de Existencia y Representación Legal."
        )
    }), 400
```

---

## 3. Reglas Antifraude en Donaciones Monetarias y Generación de Certificado Tributario PDF (`backend/app/blueprints/donaciones.py`)

Este fragmento evidencia: (1) el control estricto de importes enteros en pesos colombianos sin decimales y mayores o iguales a **`$10.000 COP`**, (2) la obligatoriedad de adjuntar el comprobante y la referencia bancaria, y (3) la generación del **Comprobante Fiscal / Certificado de Donación en PDF (`ReportLab`)** con citación expresa del **Estatuto Tributario Nacional (Arts. 125 y 257)** y huella criptográfica **SHA-256**:

```python
# Archivo: backend/app/blueprints/donaciones.py (Extracto de validación y emisión PDF)
try:
    monto_decimal = Decimal(str(monto_raw))
except (InvalidOperation, ValueError):
    return jsonify({
        "error": "Monto inválido",
        "mensaje_humano": "Ingresa un importe numérico entero en pesos colombianos sin decimales."
    }), 400

if monto_decimal != monto_decimal.to_integral_value():
    return jsonify({
        "error": "Decimales no permitidos en COP",
        "mensaje_humano": "El importe en pesos colombianos ($ COP) no debe contener centavos ni decimales."
    }), 400

monto_entero = int(monto_decimal)
if monto_entero < 10000:
    return jsonify({
        "error": "Importe inferior al mínimo permitido",
        "mensaje_humano": "El monto mínimo para registrar un aporte monetario es de $10.000 COP."
    }), 400

if not url_comprobante:
    return jsonify({
        "error": "Comprobante obligatorio faltante",
        "mensaje_humano": "Es obligatorio adjuntar el archivo de soporte o comprobante de pago antes de registrar la donación."
    }), 400

# Generación de huella criptográfica única SHA-256 para el Recibo Tributario (Art. 125 y 257 E.T.)
consecutivo = f"CERT-{anio_actual}-{uuid.uuid4().hex[:6].upper()}"
semilla_hash = f"{consecutivo}|{campana.id}|{donante.id}|{monto_entero}|{datetime.now(timezone.utc).isoformat()}"
hash_sha256 = hashlib.sha256(semilla_hash.encode("utf-8")).hexdigest()

recibo = ReciboTributario(
    donacion_economica_id=donacion_eco.id,
    numero_consecutivo=consecutivo,
    anio_gravable=anio_actual,
    hash_verificacion=hash_sha256
)
db.session.add(recibo)
```

---

## 4. Control de Disponibilidad Horaria y Privacidad por Rol en Voluntariado (`backend/app/blueprints/voluntariado.py`)

Evidencia técnica de la validación que impide a un voluntario comprometer más horas semanales de las que tiene configuradas en su perfil (`disponibilidad_horas_semana`), bloquea postulaciones duplicadas (`HTTP 409`) y filtra las asignaciones para que cada voluntario visualice exclusivamente sus propios registros:

```python
# Archivo: backend/app/blueprints/voluntariado.py (Extracto de POST /api/voluntariado/postular)
horas_disponibles_perfil = int(voluntario.disponibilidad_horas_semana or 4)
try:
    horas_comprometidas = int(data.get("horas_comprometidas") or 4)
except (ValueError, TypeError):
    horas_comprometidas = 4

if horas_comprometidas < 1:
    return jsonify({
        "error": "Horas inválidas",
        "mensaje_humano": "Debes comprometer al menos 1 hora semanal para postularte."
    }), 400

if horas_comprometidas > horas_disponibles_perfil:
    return jsonify({
        "error": "Excede disponibilidad horaria registrada",
        "mensaje_humano": (
            f"Las horas a comprometer ({horas_comprometidas} h) no pueden superar las horas que "
            f"registraste como disponibles en tu inscripción ({horas_disponibles_perfil} h/semana)."
        )
    }), 400

# Verificación de restricción única 5FN (uq_voluntario_necesidad)
existente = PostulacionVoluntariado.query.filter_by(
    voluntario_id=voluntario.id,
    necesidad_campana_id=necesidad.id
).first()
if existente:
    return jsonify({
        "error": "Postulación duplicada",
        "mensaje_humano": (
            f"Registro duplicado: Ya cuentas con una postulación activa en la labor "
            f"'{necesidad.descripcion_item}' ({existente.disponibilidad_propuesta})."
        )
    }), 409
```

---

## 5. Motor de Resiliencia a Baja Conectividad Rural (`frontend/src/app/core/services/offline-sync.service.ts`)

Componente de innovación ingenieril (`RNF01`) en el frontend Angular que monitorea el estado del enlace de red en veredas, almacena en caché los catálogos maestros de la Sabana, guarda borradores de formularios extensos y encola transacciones realizadas sin conexión para su despacho automático cuando retorna la cobertura móvil:

```typescript
// Archivo: frontend/src/app/core/services/offline-sync.service.ts (Extracto)
@Injectable({ providedIn: 'root' })
export class OfflineSyncService {
  private readonly http = inject(HttpClient);
  private readonly CATALOG_CACHE_KEY = 'cs_catalogos_sabana_cache_v1';
  private readonly QUEUE_KEY = 'cs_offline_tx_queue_v1';

  estaEnLinea = signal<boolean>(typeof navigator !== 'undefined' ? navigator.onLine : true);
  pendientesSincronizar = signal<number>(0);

  constructor() {
    if (typeof window !== 'undefined') {
      window.addEventListener('online', () => {
        this.estaEnLinea.set(true);
        this.sincronizarColaPendiente();
      });
      window.addEventListener('offline', () => {
        this.estaEnLinea.set(false);
      });
    }
  }

  guardarBorradorFormulario<T>(formId: string, datos: T): void {
    if (typeof localStorage === 'undefined') return;
    localStorage.setItem(`cs_draft_${formId}`, JSON.stringify({
      actualizado: new Date().toISOString(),
      datos
    }));
  }
}
```

