from playwright.sync_api import sync_playwright
import time
import time
from playwright.sync_api import sync_playwright



import time
from playwright.sync_api import sync_playwright

def login_litigando(usuario, contrasena, identificador):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(
            viewport={"width": 1920, "height": 1080}
        )

        # 1️⃣ Ir al login
        page.goto("https://www.litigando.com/login.html", wait_until="domcontentloaded")

        # 2️⃣ Esperar formulario
        page.wait_for_selector("input[name='userName']")

        # 3️⃣ Usuario
        page.locator("input[name='userName']").fill(usuario)
        time.sleep(2)

        # 4️⃣ Contraseña
        page.locator("input[name='password']").fill(contrasena)
        time.sleep(2)

        # 5️⃣ Click iniciar sesión
        page.get_by_role("button", name="Iniciar Sesión").click()
        time.sleep(2)

        # 6️⃣ Esperar respuesta del servidor
        page.wait_for_load_state("networkidle")

        # ================================
        # ⚠ DETECTAR POPUP SWEETALERT
        # ================================
        try:
            page.wait_for_selector("div.sweet-alert.visible", timeout=5000)

            alert_text = page.locator("div.sweet-alert.visible h2").inner_text()

            if "Inició sesión en otro equipo" in alert_text:
                print("⚠ Popup encontrado — aceptando...")
                page.locator("button.confirm").click()
                time.sleep(2)

        except:
            print("No apareció popup SweetAlert.")

        # 7️⃣ Validar URL (login correcto)
        time.sleep(3)
        if "Liti" in page.url or "dashboard" in page.url:
            print("✔ Sesión iniciada correctamente")
        else:
            print("❌ Error iniciando sesión")
            return

        # =========================================================
        # 🔎 8️⃣ ESPERAR FORMULARIO DE BÚSQUEDA RÁPIDA
        # =========================================================
        print("⏳ Esperando formulario de búsqueda rápida...")

        page.wait_for_selector("#identificacionInput", timeout=15000)

        # 9️⃣ Escribir el número
        page.locator("#identificacionInput").fill(str(identificador))
        time.sleep(2)

        # 🔟 Dar clic al botón buscar
        page.locator("#buscar1").click()
        time.sleep(3)

        print(f"✔ Se buscó correctamente el identificador: {identificador}")


        # ============================================================
        # 🟦 ENTRAR AL IFRAME DONDE APARECE LA TABLA
        # ============================================================
        print("⏳ Esperando iframe con resultados...")

        page.wait_for_selector("iframe[name='iframe_prin']", timeout=15000)
        frame = page.frame(name="iframe_prin")

        # Esperamos la tabla
        frame.wait_for_selector("tbody tr", timeout=15000)

        # Tomar la PRIMERA FILA
        first_row = frame.locator("tbody tr").first

        print("✔ Resultado encontrado, abriendo detalle de la primera fila...")

        # Dar clic a la columna del detalle (última columna con el <img>)
        first_row.locator("td img").click()

        time.sleep(3)

        print("✔ Detalle abierto correctamente.")


            # 7️⃣ Click en botón "Notificar demandado"
        frame.wait_for_selector("button.btn-notificar", timeout=15000)
        frame.locator("button.btn-notificar").click()
        time.sleep(1)

        print("✔ Botón 'Notificar demandado' clickeado, esperando que el acordeón se abra...")

        # 8️⃣ Esperar que el acordeón esté visible (clase show)
        frame.wait_for_selector("#collapseOptions.show", timeout=15000)

        # 9️⃣ Ahora sí, click en "Correo (PreJurídico)"
        prejur = frame.locator("#boton_notificar_prejuridico")

        # Si está hidden, usamos force=True
        prejur.click(force=True)

  

        print("✔ Click en 'Correo (PreJurídico)' realizado correctamente")
        

        datos = {
    "ciudad": "BOGOTA",
    "nombre_remitente": "E-Credit SAS",
    "tp_doc_remitente": "NIT",
    "identificacion_remitente": "900097463",
    "correo_remitente": "samuel.monsalve@litigando.com",
    "telefono_remitente": "7944004",
    "direccion_remitente": "Cl 79 No. 8 - 38",
    "tipo_de_producto": "CONSUMO",
    "credito": "440003006461",
    "asunto": "Notificación Cesión de Derechos Av Villas a E-Credit SAS",


    "nombre_destinatario": "John Jairo Parada Castellano",
    "correo_destinatario": "samuel.monsalve@litigando.com",
    "identificacion_destinatario": "80048696",

    "dias_mora_historicos": "706",

    # ⬇⬇⬇ CORREGIDO: quitamos "app/"
    "ruta_pdf": "output/pdfs/memoriales ecredit/440003006461.pdf"
    }

        datos["mensaje"] = (
        f"""
        Señor {datos['nombre_destinatario']}:

        Por medio de la presente nos permitimos informarle que su obligación adquirida con Banco Av Villas
        fue cedida a la entidad E-Credit SAS con ocasión a la compra de cartera efectuada entre las mencionadas entidades.

        En ese orden de ideas y con el fin de conocer el estado de sus obligaciones y las condiciones de negociación
        disponibles para usted, lo invitamos a comunicarse a las líneas 7944004; 3183365407 o al correo
        notificacionesjudiciales@cash24-7.co.

        Lo anterior en cumplimiento de los artículos 1959 y 1961 del Código Civil y demás normas concordantes.

        Cordialmente,
        E-Credit SAS  
        Departamento de PQRS  
        notificacionesjudiciales@cash24-7.co  
        Oficina Principal - Calle 79 # 8 - 38 Bogotá
        """
        )






        
        # ============================================================
        # 🟩  AHORA VIENE EL FORMULARIO PREJURÍDICO
            # ============================================================
        print("⏳ Esperando el modal de Prejurídico...")

        # # 1) Esperar a que se abra el modal que contiene el iframe
        # page.wait_for_selector("div.modal_notificar.modal.fade.show", timeout=20000)

        # time.sleep(1)  # pequeño tiempo para que aparezca el iframe dentro

        # print("⏳ Esperando iframe notificar_andes_prejuridico...")

        # # 2) Esperar el iframe por ID
        # page.wait_for_selector("iframe#notificar_andes_prejuridico", timeout=20000)

        # 3) Obtener el iframe
        frame_form = page.frame(name="notificar_andes_prejuridico")

        if not frame_form:
            raise Exception("❌ No se pudo obtener el iframe notificar_andes_prejuridico")

        print("✔ Iframe detectado, esperando formulario interno...")

        # 4) Esperar que cargue el formulario dentro del iframe
        frame_form.wait_for_selector("#formulario_agregar_instancia", timeout=20000)

        print("✔ Formulario cargado dentro del iframe")


        # ============================================================
        # 📝  LLENAR CAMPOS DEL FORMULARIO
        # ============================================================

        frame_form.locator("#correoDestinatario").fill(datos["correo_destinatario"])
        frame_form.locator("#nombreDestinatario").fill(datos["nombre_destinatario"])
        frame_form.locator("#idtDestinatario").fill(datos["identificacion_destinatario"])

        # Ciudad
        frame_form.select_option("#ciudad_id_origen", value=datos["ciudad"])


        # Tipo documento remitente
        frame_form.select_option("#tpDocRemitente", label=datos["tp_doc_remitente"])

        # Documento remitente
        frame_form.locator("#doc_remitente").fill(datos["identificacion_remitente"])

        # Nombre remitente
        frame_form.locator("#usuario").fill(datos["nombre_remitente"])

        # Correo remitente
        frame_form.locator("#correo_remitente").fill(datos["correo_remitente"])

        # Teléfono remitente
        frame_form.locator("#numContacto").fill(datos["telefono_remitente"])

        # Dirección remitente
        frame_form.locator("#dirRemitente").fill(datos["direccion_remitente"])

        # Asunto
        frame_form.locator("#asunto").fill(datos["asunto"])

        # Mensaje del textarea
        frame_form.locator("#textArea1").fill(datos["mensaje"])

        # ============================================================
        # 📎 SUBIR ARCHIVO PDF
        # ============================================================

        print("📎 Subiendo PDF:", datos["ruta_pdf"])

        frame_form.locator("#fileInput").set_input_files(datos["ruta_pdf"])
        time.sleep(1)

        # ============================================================
        # ✔ ACEPTAR CHECK DE VERIFICACIÓN
        # ============================================================

        frame_form.locator("#verificacionInfo").check()


                # ============================================================
        # ⬇ HACER SCROLL HASTA EL FINAL DEL IFRAME (IMPORTANTE)

     

        # ============================================================
        # 🚀 HABILITAR Y ENVIAR FORMULARIO
        # ============================================================

        enviar_btn = frame_form.locator("#buttonEnviarPrejuridico")

        

        enviar_btn.click()


    

   
        

        time.sleep(10000)
    

        page.close()
        browser.close()
       

   
    

# Ejecutar:
if __name__ == "__main__":
    login_litigando("CLIENTE_PRUEBA", "Temporal09","3913953")
