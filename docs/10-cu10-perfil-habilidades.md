# Documento 10: CU10 - Perfil de Habilidades del Voluntario (5FN)

**Caso de Uso:** CU10 - Perfil de Habilidades  
**Módulo de Base de Datos Principal:** Voluntariado (`voluntarios`, `categorias_habilidades`, `habilidades`, `perfil_habilidades_voluntario`)

---

## 1. Descripción Funcional

El módulo **CU10** permite a cada voluntario administrar su matriz de competencias comunitarias sin duplicar catálogos, respetando la **Quinta Forma Normal (5FN)** mediante la tabla asociativa `perfil_habilidades_voluntario` (que vincula `voluntario_id` y `habilidad_id` con `nivel_dominio` y `anos_experiencia`).

---

## 2. Rutas de la API (Backend Flask)

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/voluntariado/perfil-habilidades` | Retorna los datos del voluntario (`disponibilidad_horas_semana`, `dispuesto_desplazamiento_rural`) y sus competencias cruzadas con `habilidades` y `categorias_habilidades`. |
| `POST / PUT` | `/api/voluntariado/perfil-habilidades` | Inserta o actualiza una competencia en `perfil_habilidades_voluntario` y actualiza la disponibilidad del voluntario. |
| `DELETE` | `/api/voluntariado/perfil-habilidades/<id>` | Desvincula una competencia específica del perfil del voluntario. |

---

## 3. Componente UI (Frontend Angular)

- **`PerfilHabilidadesComponent` (`src/app/features/voluntariado/perfil-habilidades.component.ts`)**:
  - Interfaz accesible para agregar/actualizar competencias (Agroecología, Pedagogía Rural, Logística Veredal), configurar horas semanales y disposición de desplazamiento rural.
