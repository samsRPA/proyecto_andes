import asyncio
import logging
import time
#from playwright.async_api import async_playwright
from app.domain.interfaces.IScrapperAndes import IScrapperAndes
from app.application.dto.ProceedingsDto import ProceedingsDto

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException
)
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
import time
import os
import logging
class ScrapperAndes(IScrapperAndes):



   
    def __init__(self,body:ProceedingsDto):
        self.body= body
        self.logger= logging.getLogger(__name__)

    CHROME_MAJOR = 143




    def crear_driver(self):


        # Opciones de Chrome
        opts = uc.ChromeOptions()
        opts.add_argument("--start-maximized")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-popup-blocking")
        opts.add_argument("--disable-notifications")
        opts.add_argument("--window-size=1200,900")
        opts.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        )

        opts.add_argument("--headless=new")  # 🔥 IMPORTANTE en Docker Linux

        # ⚙️ Preferencias para descargas automáticas
        prefs = {            # Ruta donde guardar
            "download.prompt_for_download": False,                   # No preguntar dónde guardar
            "download.directory_upgrade": True,                      # Permitir sobrescribir
            "safebrowsing.enabled": True,                            # Permitir descargas sin alerta
            "profile.default_content_settings.popups": 0,            # Bloquear popups
        }
        opts.add_experimental_option("prefs", prefs)

        # Crear el driver
        driver = uc.Chrome(options=opts, version_main=self.CHROME_MAJOR)

        # Ocultar bandera "webdriver"
        try:
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception:
            pass

        return driver

     


    # async def scrapper_andes(self, usuario, contrasena, identificador, datos):
    #     driver = None

    #     self.logger.info("🟦 Iniciando scrapper_andes() con SELENIUM")

  

    #     try:
    #         driver = self.crear_driver()
    #         # 1️⃣ LOGIN
    #         self.logger.info("➡️ Cargando login...")
    #         driver.get("https://www.litigando.com/login.html")
    #         time.sleep()

    #         wait = WebDriverWait(driver, 20)
    #         actions = ActionChains(driver)

    #         wait.until(EC.presence_of_element_located((By.NAME, "userName")))

    #         self.logger.info(f"⌨️ Ingresando usuario {usuario}")
    #         driver.find_element(By.NAME, "userName").send_keys(usuario)
    #         time.sleep(1)

    #         self.logger.info("🔐 Ingresando contraseña...")
    #         driver.find_element(By.NAME, "password").send_keys(contrasena)
    #         time.sleep(1)

    #         self.logger.info("➡️ Click en iniciar sesión")
    #         driver.find_element(By.XPATH, "//button[contains(text(),'Iniciar Sesión')]").click()

    #         time.sleep(1)

    #         # ===============================================
    #         # 🟡 POPUP SWEETALERT
    #         # ===============================================
    #         try:
    #             self.logger.info("🔍 Verificando SweetAlert...")

    #             popup = wait.until(
    #                 EC.visibility_of_element_located((By.CSS_SELECTOR, "div.sweet-alert.visible"))
    #             )

    #             alert_text = popup.find_element(By.TAG_NAME, "h2").text
    #             self.logger.warning(f"⚠ Popup detectado: {alert_text}")

    #             if "Inició sesión en otro equipo" in alert_text:
    #                 self.logger.warning("⚠ Sesión duplicada! Aceptando alerta...")
    #                 popup.find_element(By.CSS_SELECTOR, "button.confirm").click()
    #                 time.sleep(1)

    #         except Exception:
    #             self.logger.info("✔ No apareció SweetAlert")

    #         # 7️⃣ Validar URL
    #         if "Liti" in driver.current_url or "dashboard" in driver.current_url:
    #             self.logger.info(f"✔ Sesión iniciada correctamente: {driver.current_url}")
    #         else:
    #             self.logger.error(f"❌ Error de login, URL: {driver.current_url}")
    #             driver.quit()
    #             return

    #         # ===============================================
    #         # 🔎 FORMULARIO DE BÚSQUEDA RÁPIDA
    #         # ===============================================
    #         self.logger.info("⏳ Esperando formulario de búsqueda...")
    #         wait.until(EC.presence_of_element_located((By.ID, "identificacionInput")))

    #         self.logger.info(f"⌨️ Ingresando identificador {identificador}")
    #         driver.find_element(By.ID, "identificacionInput").send_keys(str(identificador))
    #         time.sleep(1)

    #         self.logger.info("➡️ Ejecutando búsqueda...")
    #         driver.find_element(By.ID, "buscar1").click()
    #         time.sleep(1)

    #         # ===============================================
    #         # 🟦 ENTRAR A IFRAME
    #         # ===============================================
    #         self.logger.info("⏳ Esperando iframe iframe_prin...")
    #         wait.until(EC.frame_to_be_available_and_switch_to_it("iframe_prin"))

    #         wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr")))
    #         self.logger.info("✔ Resultados encontrados")

    #         first_row = driver.find_element(By.CSS_SELECTOR, "tbody tr")
    #         first_row.find_element(By.CSS_SELECTOR, "td img").click()
    #         time.sleep(1)

    #         self.logger.info("✔ Detalle del expediente abierto")

    #         # Notificar demandado
    #         wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-notificar")))
    #         driver.find_element(By.CSS_SELECTOR, "button.btn-notificar").click()

    #         self.logger.info("✔ Botón 'Notificar demandado' clickeado")

        
    #         self.logger.info("➡️ Click en PreJurídico")
    #         # Esperar a que el acordeón se despliegue
    #         self.logger.info("⏳ Esperando que se abra el acordeón de 'Notificar demandado'...")

    #         # 1️⃣ Esperar a que el contenedor del acordeón sea visible
    #         wait.until(EC.visibility_of_element_located(
    #             (By.CSS_SELECTOR, ".accordion-content")
    #         ))

    #         # 2️⃣ Esperar a que el botón "Correo (PreJurídico)" sea clickeable
    #         self.logger.info("⏳ Esperando botón 'Correo (PreJurídico)'...")
    #         prejur = wait.until(EC.element_to_be_clickable(
    #             (By.ID, "boton_notificar_prejuridico")
    #         ))


    #         prejur.click()
    #         self.logger.info("➡️ Click en 'Correo (PreJurídico)'")
    #         screenshot_path = f"/app/output/img.png"

    #         time.sleep(2)
          


    #         wait.until(EC.frame_to_be_available_and_switch_to_it(
    #             (By.CSS_SELECTOR, "iframe[src*='notificarAndesPrejuridico.jsp']")
    #         ))

    #         # ============================================================
    #         # 📝 LLENAR FORMULARIO
    #         # ============================================================

    #         self.logger.info("📝 Llenando formulario con datos del ProceedingsDto...")

    #         driver.find_element(By.ID, "correoDestinatario").send_keys(datos.correo_destinatario)
    #         driver.find_element(By.ID, "nombreDestinatario").send_keys(datos.nombre_destinatario)
    #         driver.find_element(By.ID, "idtDestinatario").send_keys(datos.identificacion_destinatario)

    #         # selects
    #         Select(driver.find_element(By.ID, "ciudad_id_origen")).select_by_value(datos.ciudad)
    #         Select(driver.find_element(By.ID, "tpDocRemitente")).select_by_visible_text(datos.tp_doc_remitente)

    #         # remitente
    #         driver.find_element(By.ID, "doc_remitente").send_keys(datos.identificacion_remitente)
    #         driver.find_element(By.ID, "usuario").send_keys(datos.nombre_remitente)
    #         driver.find_element(By.ID, "correo_remitente").send_keys(datos.correo_remitente)
    #         driver.find_element(By.ID, "numContacto").send_keys(datos.telefono_remitente)
    #         driver.find_element(By.ID, "dirRemitente").send_keys(datos.direccion_remitente)
    #         driver.find_element(By.ID, "asunto").send_keys(datos.asunto)
    #         driver.find_element(By.ID, "textArea1").send_keys(datos.mensaje)


    #         # ============================================================
    #         # 📎 SUBIR ARCHIVO PDF
    #         # ============================================================

    #         self.logger.info(f"📎 Subiendo archivo PDF: {datos.ruta_pdf}")

    #         file_input = driver.find_element(By.ID, "fileInput")
    #         file_input.send_keys(datos.ruta_pdf)

    #         self.logger.info("✔ PDF anexado al formulario.")


    #         # ============================================================
    #         # ☑ CHECKBOX
    #         # ============================================================

    #         checkbox = driver.find_element(By.ID, "verificacionInfo")

    #         driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
    #         time.sleep(1)

    #         checkbox.click()
    #         self.logger.info("✔ Checkbox verificación marcado.")


    #         # ============================================================
    #         # ⬇ SCROLL PARA VER BOTÓN DE ENVÍO
    #         # ============================================================

    #         self.logger.info("⬇ Haciendo scroll para visualizar el botón de envío...")

    #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         time.sleep(1)


    #         # ============================================================
    #         # 🚀 ENVIAR FORMULARIO
    #         # ============================================================

    #         self.logger.info("🚀 Enviando formulario PreJurídico...")

    #         btn_enviar = wait.until(EC.element_to_be_clickable(
    #             (By.ID, "buttonEnviarPrejuridico")
    #         ))

    #         btn_enviar.click()

    #         self.logger.info("✔ Formulario enviado correctamente.")

    #         time.sleep(8)  # permite que cargue el Swal2 o respuesta final


    #         # ===============================================
    #         # 🗑 BORRAR PDF
    #         # ===============================================
    #         self.logger.info(f"🗑 Eliminando PDF: {datos.ruta_pdf}")

    #         try:
    #             if os.path.exists(datos.ruta_pdf):
    #                 os.remove(datos.ruta_pdf)
    #                 self.logger.info("🟩 PDF eliminado")
    #             else:
    #                 self.logger.warning("⚠ PDF no existe")
    #         except Exception as e:
    #             self.logger.error(f"❌ Error eliminando PDF: {e}")

    #     except Exception as e:
    #         self.logger.error(f"❌ Error en el scrapper: {e}")

    #     finally:
    #         if driver:
    #             driver.quit()
    #             self.logger.info("🟩 scrapper_andes() Selenium finalizó.")



    async def scrapper_andes(self, usuario, contrasena, identificador, datos: ProceedingsDto):

        self.logger.info("🟦 Iniciando scrapper_andes() ")

        async with async_playwright() as p:
            self.logger.info("🌐 Lanzando navegador Playwright en modo headless...")
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                viewport={"width": 1920, "height": 1080}
            )

            # 1️⃣ Ir al login
            self.logger.info("➡️ Navegando a página de login...")
            await page.goto("https://www.litigando.com/login.html", wait_until="domcontentloaded")
            await asyncio.sleep(4)

            # 2️⃣ Esperar formulario
            self.logger.info("⏳ Esperando formulario de login...")
            await page.wait_for_selector("input[name='userName']")

            # 3️⃣ Usuario
            self.logger.info(f"⌨️ Ingresando usuario {usuario}")
            await page.locator("input[name='userName']").fill(usuario)
            await asyncio.sleep(2)

            # 4️⃣ Contraseña
            self.logger.info("🔐 Ingresando contraseña...")
            await page.locator("input[name='password']").fill(contrasena)
            await asyncio.sleep(2)

            # 5️⃣ Click iniciar sesión
            self.logger.info("➡️ Enviando formulario de login...")
            await page.get_by_role("button", name="Iniciar Sesión").click()
            await asyncio.sleep(2)

            # 6️⃣ Esperar respuesta
            await page.wait_for_load_state("networkidle")

            # ================================
            # ⚠ POPUP SWEETALERT
            # ================================
            try:
                self.logger.info("🔍 Verificando si hay popup SweetAlert...")
                await page.wait_for_selector("div.sweet-alert.visible", timeout=60000)
                alert_text = await page.locator("div.sweet-alert.visible h2").inner_text()

                self.logger.warning("⚠ Popup detectado: %s", alert_text)

                if "Inició sesión en otro equipo" in alert_text:
                    self.logger.warning("⚠ Sesión duplicada detectada - aceptando alerta...")
                    await page.locator("button.confirm").click()
                    await asyncio.sleep(2)

            except Exception:
                self.logger.info("✔ No apareció popup SweetAlert.")

            # 7️⃣ Validar URL
            await asyncio.sleep(3)
            if "Liti" in page.url or "dashboard" in page.url:
                self.logger.info("✔ Sesión iniciada correctamente. URL actual: %s", page.url)
            else:
                self.logger.error("❌ Error iniciando sesión. URL actual: %s", page.url)
                return

            # =========================================================
            # 🔎 8️⃣ FORMULARIO DE BÚSQUEDA RÁPIDA
            # =========================================================
            self.logger.info("⏳ Esperando formulario de búsqueda rápida...")

            await page.wait_for_selector("#identificacionInput", timeout=60000)

            # 9️⃣ Escribir el número
            self.logger.info("⌨️ Ingresando identificador %s", identificador)
            await page.locator("#identificacionInput").fill(str(identificador))
            await asyncio.sleep(2)

            # 🔟 Buscar
            self.logger.info("➡️ Ejecutando búsqueda...")
            await page.locator("#buscar1").click()
            await asyncio.sleep(3)

            self.logger.info("✔ Búsqueda completada con identificador %s", identificador)

            # ============================================================
            # 🟦 ENTRAR AL IFRAME
            # ============================================================
            self.logger.info("⏳ Esperando iframe con resultados...")

            await page.wait_for_selector("iframe[name='iframe_prin']", timeout=60000)
            frame = page.frame(name="iframe_prin")

            await frame.wait_for_selector("tbody tr", timeout=60000)

            self.logger.info("✔ Resultados encontrados, entrando al detalle...")

            first_row = frame.locator("tbody tr").first
            await first_row.locator("td img").click()
            await asyncio.sleep(3)

            self.logger.info("✔ Detalle del expediente abierto correctamente.")

            # Notificar demandado
            self.logger.info("➡️ Buscando botón 'Notificar demandado'...")
            await frame.wait_for_selector("button.btn-notificar", timeout=60000)
            await frame.locator("button.btn-notificar").click()
            await asyncio.sleep(1)

            self.logger.info("✔ Botón 'Notificar demandado' clickeado.")

            # Acordeón visible
            await frame.wait_for_selector("#collapseOptions.show", timeout=60000)

            # Prejurídico
            self.logger.info("➡️ Click en botón 'Correo (PreJurídico)'...")
            prejur = frame.locator("#boton_notificar_prejuridico")
            await prejur.click(force=True)

            self.logger.info("✔ Opción PreJurídico seleccionada.")

            # Iframe interno
            frame_form = page.frame(name="notificar_andes_prejuridico")

            if not frame_form:
                self.logger.error("❌ No se pudo obtener iframe interno notificar_andes_prejuridico")
                raise Exception("Iframe no encontrado")

            self.logger.info("✔ Iframe interno detectado. Cargando formulario...")

            await frame_form.wait_for_selector("#formulario_agregar_instancia", timeout=60000)

            self.logger.info("✔ Formulario interno cargado correctamente.")

            # ============================================================
            # 📝 LLENAR FORMULARIO
            # ============================================================
            self.logger.info("📝 Llenando formulario con datos del ProceedingsDto...")
            print(datos)
            await frame_form.locator("#correoDestinatario").fill(datos.correo_destinatario)
          
            await frame_form.locator("#nombreDestinatario").fill(datos.nombre_destinatario)
            await frame_form.locator("#idtDestinatario").fill(datos.identificacion_destinatario)

            await frame_form.select_option("#ciudad_id_origen", value=datos.ciudad)
            await frame_form.select_option("#tpDocRemitente", label=datos.tp_doc_remitente)

            await frame_form.locator("#doc_remitente").fill(datos.identificacion_remitente)
            await frame_form.locator("#usuario").fill(datos.nombre_remitente)
            await frame_form.locator("#correo_remitente").fill(datos.correo_remitente)
            await frame_form.locator("#numContacto").fill(datos.telefono_remitente)
            await frame_form.locator("#dirRemitente").fill(datos.direccion_remitente)
            await frame_form.locator("#asunto").fill(datos.asunto)
            await frame_form.locator("#textArea1").fill(datos.mensaje)

            # ============================================================
            # 📎 SUBIR ARCHIVO PDF
            # ============================================================
            self.logger.info("📎 Subiendo archivo PDF: %s", datos.ruta_pdf)

            await frame_form.locator("#fileInput").set_input_files(datos.ruta_pdf)
            await asyncio.sleep(1)

            self.logger.info("✔ PDF anexado al formulario.")

            # Check
            await frame_form.locator("#verificacionInfo").check()

            # ============================================================
            # ⬇ SCROLL
            # ============================================================
            self.logger.info("⬇ Realizando scroll para visualizar botón de envío...")

            try:
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                self.logger.info("⬇ Scroll realizado correctamente.")
                await asyncio.sleep(1)
            except Exception as e:
                self.logger.warning("⚠ No se pudo hacer scroll: %s", str(e))

            # ============================================================
            # 🚀 ENVIAR FORMULARIO
            # ============================================================
            self.logger.info("🚀 Enviando formulario PreJurídico...")

            enviar_btn = frame_form.locator("#buttonEnviarPrejuridico")
            await enviar_btn.click()
            await asyncio.sleep(10)

            self.logger.info("✔ Formulario enviado correctamente.")


            # self.logger.info("🗑 Intentando eliminar PDF: %s", datos.ruta_pdf)

            # try:
            
            #     if os.path.exists(datos.ruta_pdf):
            #         os.remove(datos.ruta_pdf)
            #         self.logger.info("🟩 PDF eliminado correctamente.")
            #     else:
            #         self.logger.warning("⚠ El PDF no existe o ya fue eliminado: %s", datos.ruta_pdf)

            # except Exception as e:
            #     self.logger.error("❌ Error eliminando PDF: %s", str(e))


            await page.close()
            await browser.close()

            self.logger.info("🟩 scrapper_andes() finalizó exitosamente.")


 

    async def runScrapper(self):
            
        try:
            # Construir el DTO que espera run_multi (AHORA usando TU DTO REAL)
            dto = ProceedingsDto(
                ciudad=self.body.ciudad,
                nombre_remitente=self.body.nombre_remitente,
                tp_doc_remitente=self.body.tp_doc_remitente,
                identificacion_remitente=self.body.identificacion_remitente,
                correo_remitente=self.body.correo_remitente,
                telefono_remitente=self.body.telefono_remitente,
                direccion_remitente=self.body.direccion_remitente,
                tipo_de_producto=self.body.tipo_de_producto,
                credito=self.body.credito,

                asunto=self.body.asunto,
                mensaje=self.body.mensaje,

                nombre_destinatario=self.body.nombre_destinatario,
                correo_destinatario=self.body.correo_destinatario,
                identificacion_destinatario=self.body.identificacion_destinatario,

                nombre_del_destinatario=self.body.nombre_del_destinatario,
                dias_mora_historicos=self.body.dias_mora_historicos,
                ruta_pdf=self.body.ruta_pdf,
                user=self.body.user
            )
            
            usuario = dto.user
            datos = dto

            resultado = await self.scrapper_andes(
                usuario,
                "Temporal04",
                "8764361",
                datos
            )

        except Exception as e:
            raise e




