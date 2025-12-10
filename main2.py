import json
import multiprocessing
import time
import os
from playwright.sync_api import sync_playwright

# =============================================
#  🔵 CARGAR JSON DESDE LA RUTA CORRECTA
# =============================================
def cargar_registros():
    ruta = "output/base/proceedings.json"
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 🔥 LIMPIAR RUTA PDF: quitar /app
    for d in data:
        if "ruta_pdf" in d:
            ruta_original = d["ruta_pdf"]
            ruta_limpia = ruta_original.replace("/app/", "")  # quita el /app/
            d["ruta_pdf"] = ruta_limpia

    return data


# =============================================
#  🔵 FUNCIÓN PRINCIPAL DEL SCRAPER
# =============================================
def ejecutar_scraper(args):
    usuario_json, contrasena_fija, identificador_fijo, datos = args

    print(f"\n🟦 Worker → usuario={usuario_json} identificador={identificador_fijo}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1920, "height": 1080})

            # ---------------- LOGIN ----------------
            page.goto("https://www.litigando.com/login.html", wait_until="domcontentloaded")
            page.wait_for_selector("input[name='userName']")

            page.locator("input[name='userName']").fill(usuario_json)
            page.locator("input[name='password']").fill(contrasena_fija)

            page.get_by_role("button", name="Iniciar Sesión").click()
            page.wait_for_load_state("networkidle")

            # popup
            try:
                page.wait_for_selector("div.sweet-alert.visible", timeout=3000)
                page.locator("button.confirm").click()
            except:
                pass

            # ---------------- BÚSQUEDA ----------------
            page.wait_for_selector("#identificacionInput")
            page.locator("#identificacionInput").fill(str(identificador_fijo))
            page.locator("#buscar1").click()
            time.sleep(2)

            # ---------------- IFRAME ----------------
            page.wait_for_selector("iframe[name='iframe_prin']", timeout=15000)
            frame = page.frame(name="iframe_prin")

            frame.wait_for_selector("tbody tr")
            frame.locator("tbody tr").first.locator("td img").click()
            time.sleep(1)

            # botón notificar
            frame.wait_for_selector("button.btn-notificar")
            frame.locator("button.btn-notificar").click()
            frame.wait_for_selector("#collapseOptions.show")

            frame.locator("#boton_notificar_prejuridico").click(force=True)

            # ---------------- FORMULARIO ----------------
            frame_form = page.frame(name="notificar_andes_prejuridico")
            frame_form.wait_for_selector("#formulario_agregar_instancia")

            frame_form.locator("#correoDestinatario").fill(datos["correo_destinatario"])
            frame_form.locator("#nombreDestinatario").fill(datos["nombre_destinatario"])
            frame_form.locator("#idtDestinatario").fill(identificador_fijo)

            frame_form.select_option("#ciudad_id_origen", value=datos["ciudad"])
            frame_form.select_option("#tpDocRemitente", label=datos["tp_doc_remitente"])

            frame_form.locator("#doc_remitente").fill(datos["identificacion_remitente"])
            frame_form.locator("#usuario").fill(datos["nombre_remitente"])
            frame_form.locator("#correo_remitente").fill(datos["correo_remitente"])
            frame_form.locator("#numContacto").fill(datos["telefono_remitente"])
            frame_form.locator("#dirRemitente").fill(datos["direccion_remitente"])
            frame_form.locator("#asunto").fill(datos["asunto"])
            frame_form.locator("#textArea1").fill(datos["mensaje"])

            # ---------------- PDF ----------------
            ruta_pdf = datos["ruta_pdf"]

            if not os.path.exists(ruta_pdf):
                raise Exception(f"PDF NO ENCONTRADO: {ruta_pdf}")

            frame_form.locator("#fileInput").set_input_files(ruta_pdf)

            # check
            frame_form.locator("#verificacionInfo").check()
            frame_form.locator("#buttonEnviarPrejuridico").click()

            print(f"✔ Enviado → {identificador_fijo} con usuario {usuario_json}")

            browser.close()

    except Exception as e:
        print(f"❌ ERROR con usuario {usuario_json}: {e}")


# =============================================
#  🔥 EJECUTOR DE WORKERS
# =============================================
def iniciar_workers():
    registros = cargar_registros()
    total = len(registros)

    print(f"\n🔵 Total registros cargados: {total}")

    NUM_WORKERS = 5  # puedes ajustarlo

    contraseña = "Temporal04"
    identificador = "8764361"

    print(f"🚀 Usando contraseña fija: {contraseña}")
    print(f"🚀 Usando identificador fijo: {identificador}")

    tareas = [
        (datos["user"], contraseña, identificador, datos)
        for datos in registros
    ]

    with multiprocessing.Pool(processes=NUM_WORKERS) as pool:
        pool.map(ejecutar_scraper, tareas)


# =============================================
#  🚀 EJECUTAR
# =============================================
if __name__ == "__main__":
    iniciar_workers()
