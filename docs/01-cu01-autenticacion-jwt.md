# Documento 01: CU01 - Autenticación con JWT, Auditoría Relacional y Enrutamiento Protegido

**Caso de Uso:** CU01 - Autenticación  
**Módulo de Base de Datos Principal:** Seguridad (`usuarios`, `roles`, `usuarios_roles`, `logs_auditoria`) + Perfiles (`personas`, `fundaciones_osal`)

---

## 1. Descripción Funcional

El flujo **CU01** gestiona el ingreso seguro de los actores comunitarios de la Sabana Norte (Representantes de OSAL, Donantes, Voluntarios y Administradores). Al autenticarse:
1. Verifica las credenciales cifradas (`hash_contrasena` con `pbkdf2/scrypt` de Werkzeug).
2. Consulta la relación muchos-a-muchos normalizada en 5FN entre `usuarios`, `usuarios_roles` y `roles`.
3. Registra cada evento de acceso (exitoso o fallido) en la tabla `logs_auditoria` con fecha UTC, dirección IP y detalle.
4. Emite un **JSON Web Token (JWT)** firmado que incluye como *claims* los roles del usuario y las llaves foráneas de su perfil (`fundacion_id`, `donante_id`, `voluntario_id`).

---

## 2. Rutas de la API (Backend Flask)

Blueprint registrado en `backend/app/blueprints/auth.py` bajo el prefijo `/api/auth`:

| Método | Ruta | Protección | Descripción |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/login` | Pública | Recibe `correo_electronico` y `contrasena`. Valida credenciales, inserta registro en `logs_auditoria` y retorna `access_token` (JWT) + objeto `usuario` + `mensaje_humano`. |
| `GET` | `/api/auth/me` | `@jwt_required()` | Verifica el token JWT en la cabecera `Authorization: Bearer <token>`, retorna el estado del usuario y sus últimos 5 eventos en `logs_auditoria`. |

---

## 3. Lógica de Base de Datos (5FN)

- **`usuarios`**: Almacena exclusivamente credenciales y metadatos de estado (`correo_electronico`, `hash_contrasena`, `esta_activo`, `ultimo_acceso`).
- **`roles` y `usuarios_roles`**: Desacoplan los permisos del usuario mediante llave compuesta única (`uq_usuario_rol`), permitiendo que una misma persona en una vereda pueda ser simultáneamente Donante y Voluntario sin duplicar registros en `usuarios` ni en `personas`.
- **`logs_auditoria`**: Garantiza trazabilidad inmutable de seguridad (`LOGIN_EXITOSO`, `LOGIN_FALLIDO`) referenciando `usuario_id`.
- **Seeder Inicial (`backend/app/seed.py`)**: Incluye el comando `flask init-db` que inicializa los 10 municipios de la Sabana Norte (Chía, Cajicá, Zipaquirá, Tabio, Tenjo, Cogua, Sopó, Tocancipá, Gachancipá, Nemocón), catálogos 5FN y tres cuentas de prueba (`osal@sabananorte.org`, `donante@conexion.org`, `voluntario@conexion.org`).

---

## 4. Componentes UI y Enrutamiento Protegido (Frontend Angular)

1. **`AuthService` (`src/app/core/services/auth.service.ts`)**:
   - Gestiona el estado reactivo con Angular Signals (`usuarioActual`, `estaAutenticado`).
   - Persiste el JWT y la sesión en `localStorage` protegiendo la ejecución en SSR mediante `isPlatformBrowser`.
2. **`jwtInterceptor` (`src/app/core/interceptors/jwt.interceptor.ts`)**:
   - Interceptor funcional conectado a `provideHttpClient(withFetch(), withInterceptors([jwtInterceptor]))` que adjunta automáticamente la cabecera `Authorization: Bearer <token>`.
3. **`authGuard` (`src/app/core/guards/auth.guard.ts`)**:
   - Guardián de rutas (`CanActivateFn`) que bloquea el acceso no autenticado redirigiendo a `/login` y valida autorización por rol (`route.data['roles']`).
4. **`LoginComponent` (`src/app/features/auth/login/login.component.ts`)**:
   - Tarjeta minimalista de **Alto Contraste WCAG 2.2** con controles táctiles de mínimo `48px`, detección de desconexión rural (`navigator.onLine`) y mensajes de error humanos contextualizados.
5. **`PanelProtegidoComponent` (`src/app/features/panel/panel-protegido.component.ts`)**:
   - Vista protegida por `authGuard` que despliega en tarjetas los vínculos relacionales del usuario y su bitácora de auditoría en tiempo real.

