# -*- coding: utf-8 -*-
"""
Script automatizado para levantar el servidor local Flask + Angular compilado (en el puerto 5055)
y recapturar las capturas de pantalla de la plataforma con el nuevo logo oficial y las fotografías
sociales reales de las fundaciones (Adulto Mayor Campesino, Niñez y Educación, Bienestar Animal y Campamentos de Vida Nueva).
"""

import os
import time
import subprocess
import sys
from playwright.sync_api import sync_playwright

BACKEND_DIR = r"c:\Users\ingor\conexion-solidaria\backend"
VENV_PYTHON = os.path.join(BACKEND_DIR, ".venv", "Scripts", "python.exe")
if not os.path.exists(VENV_PYTHON):
    VENV_PYTHON = sys.executable

CAP_DIR = r"c:\Users\ingor\conexion-solidaria\docs\capturas_mvp"
os.makedirs(CAP_DIR, exist_ok=True)

PORT = 5000
BASE_URL = f"http://127.0.0.1:{PORT}"


def capture_all_screens():
    env = os.environ.copy()
    env["PORT"] = str(PORT)
    env["FLASK_ENV"] = "production"
    server_proc = subprocess.Popen(
        [VENV_PYTHON, "run.py"],
        cwd=BACKEND_DIR,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(3.5)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="msedge", headless=True)
            context = browser.new_context(viewport={"width": 1440, "height": 1020}, device_scale_factor=1.5)
            page = context.new_page()

            # 1. Login & Vitrina Social + 5 Roles (fig_h06_login_roles.png)
            print("Capturando fig_h06_login_roles.png...")
            page.goto(f"{BASE_URL}/", wait_until="networkidle")
            page.wait_for_selector("article.role-option-card", timeout=15000)
            time.sleep(1.0)
            page.screenshot(path=os.path.join(CAP_DIR, "fig_h06_login_roles.png"), full_page=False)

            # 2. Registro OSAL Paso 1 (fig_h04_wizard_paso1.png)
            print("Capturando fig_h04_wizard_paso1.png...")
            page.click("a:has-text('Inscribir una Fundación (OSAL)')")
            page.wait_for_selector("#nit", timeout=10000)
            time.sleep(0.6)
            page.fill("#nit", "901920450-7")
            page.fill("#sigla", "FUNDSABANA")
            page.fill("#razon_social", "Fundación Campesina Semillas y Vida de la Sabana")
            page.fill("#mision", "Apoyo integral a familias campesinas, adulto mayor, niñez veredal y rescate de fauna en la Sabana Norte.")
            page.fill("#telefono", "3124567890")
            page.screenshot(path=os.path.join(CAP_DIR, "fig_h04_wizard_paso1.png"), full_page=False)

            # 3. Registro OSAL Paso 3 con Habeas Data Ley 1581 (fig_h05_wizard_paso3_habeas.png)
            print("Capturando fig_h05_wizard_paso3_habeas.png...")
            page.click("button:has-text('Continuar a Ubicación y Representación')")
            time.sleep(0.5)
            page.fill("#vereda", "Vereda Quebrada Honda")
            page.fill("#direccion", "Km 3 Vía San Jorge, junto al salón comunal")
            page.fill("#nombres_rep", "María Fernanda")
            page.fill("#apellidos_rep", "López Castro")
            page.fill("#num_doc", "52890123")
            page.fill("#correo_rep", "contacto@semillassabana.org")
            page.fill("#clave_rep", "Solidaria2026*")
            page.click("button:has-text('Continuar a Soportes Documentales')")
            time.sleep(0.6)
            page.check("input[name='habeas_data']")
            page.screenshot(path=os.path.join(CAP_DIR, "fig_h05_wizard_paso3_habeas.png"), full_page=False)

            # 4. Iniciar sesión como Voluntario para capturar Mapa, Catálogo, Voluntariado y Resumen Voluntario
            print("Iniciando sesión como Voluntario...")
            page.click("a:has-text('Volver al Inicio')")
            page.wait_for_selector("article.role-option-card", timeout=10000)
            time.sleep(0.6)
            page.click("article.role-option-card:has-text('Voluntario Comunitario')")
            page.click("button[type='submit']:has-text('Entrar a la Plataforma')")
            page.wait_for_selector("a.sap-nav-item", timeout=10000)
            time.sleep(1.0)

            # Resumen Voluntario (fig_h07_resumen_voluntario.png)
            print("Capturando fig_h07_resumen_voluntario.png...")
            page.screenshot(path=os.path.join(CAP_DIR, "fig_h07_resumen_voluntario.png"), full_page=False)

            # Postulación Voluntariado con Galería Social (fig_h08_postulacion_voluntariado.png)
            print("Capturando fig_h08_postulacion_voluntariado.png...")
            page.click("a.sap-nav-item:has-text('Postulación Voluntariado')")
            time.sleep(1.0)
            page.screenshot(path=os.path.join(CAP_DIR, "fig_h08_postulacion_voluntariado.png"), full_page=False)

            # Mapa Territorial con Fotografías de las Fundaciones (fig_h01_mapa.png)
            print("Capturando fig_h01_mapa.png...")
            page.click("a.sap-nav-item:has-text('Mapa Territorial')")
            time.sleep(2.4)
            page.screenshot(path=os.path.join(CAP_DIR, "fig_h01_mapa.png"), full_page=False)

            # Catálogo de Causas con Fotografías Sociales (fig_h02_catalogo_filtrado.png)
            print("Capturando fig_h02_catalogo_filtrado.png...")
            page.click("a.sap-nav-item:has-text('Causas y Necesidades')")
            time.sleep(1.2)
            page.screenshot(path=os.path.join(CAP_DIR, "fig_h02_catalogo_filtrado.png"), full_page=False)

            # 5. Iniciar sesión como Representante OSAL para capturar Editor de Campaña y Dashboard ODS
            print("Iniciando sesión como Representante OSAL...")
            page.click("button.sap-shell-logout")
            page.wait_for_selector("article.role-option-card", timeout=10000)
            time.sleep(0.6)
            page.click("article.role-option-card:has-text('Representante de Fundación')")
            page.click("button[type='submit']:has-text('Entrar a la Plataforma')")
            page.wait_for_selector("a.sap-nav-item", timeout=10000)
            time.sleep(1.0)

            # Publicar campaña con unidades + tarjetas sociales (fig_h03_publicar_campana_unidades.png)
            print("Capturando fig_h03_publicar_campana_unidades.png...")
            page.click("a.sap-nav-item:has-text('Causas y Necesidades')")
            time.sleep(0.8)
            btn_crear = page.locator("button:has-text('Crear Nueva Campaña')")
            if btn_crear.count() > 0:
                btn_crear.click()
                time.sleep(0.6)
            page.screenshot(path=os.path.join(CAP_DIR, "fig_h03_publicar_campana_unidades.png"), full_page=False)

            # Dashboard OSAL con Mosaico de Evidencia Territorial y ODS (fig_h11_dashboard_ods.png)
            print("Capturando fig_h11_dashboard_ods.png...")
            page.click("a.sap-nav-item:has-text('Tablero OSAL')")
            time.sleep(1.2)
            page.screenshot(path=os.path.join(CAP_DIR, "fig_h11_dashboard_ods.png"), full_page=False)

            # 6. Iniciar sesión como Donante para capturar Donaciones Transaccionales (fig_h09_donaciones_transaccional.png)
            print("Iniciando sesión como Donante...")
            page.click("button.sap-shell-logout")
            page.wait_for_selector("article.role-option-card", timeout=10000)
            time.sleep(0.6)
            page.click("article.role-option-card:has-text('Donante Solidario')")
            page.click("button[type='submit']:has-text('Entrar a la Plataforma')")
            page.wait_for_selector("a.sap-nav-item", timeout=10000)
            time.sleep(0.8)
            page.click("a.sap-nav-item:has-text('Aportes y Certificados')")
            time.sleep(1.0)
            page.screenshot(path=os.path.join(CAP_DIR, "fig_h09_donaciones_transaccional.png"), full_page=False)

            # 7. Iniciar sesión como Superusuario para capturar Gobernanza y Aprobación OSAL (fig_h12_superadmin_parametros.png)
            print("Iniciando sesión como Superusuario...")
            page.click("button.sap-shell-logout")
            page.wait_for_selector("article.role-option-card", timeout=10000)
            time.sleep(0.6)
            page.click("article.role-option-card:has-text('Superusuario de la Plataforma')")
            page.click("button[type='submit']:has-text('Entrar a la Plataforma')")
            page.wait_for_selector("a.sap-nav-item", timeout=10000)
            time.sleep(1.0)
            page.screenshot(path=os.path.join(CAP_DIR, "fig_h12_superadmin_parametros.png"), full_page=False)

            browser.close()
            print("==> ¡Todas las capturas de pantalla fueron actualizadas con éxito en docs/capturas_mvp/!")
    finally:
        server_proc.terminate()
        try:
            server_proc.wait(timeout=3)
        except Exception:
            server_proc.kill()


if __name__ == "__main__":
    capture_all_screens()
