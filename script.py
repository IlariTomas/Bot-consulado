import time
import datetime
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

# ==========================================
# CONFIGURACIÓN DE TELEGRAM
# ==========================================
# IMPORTANTE: Vuelve a pegar tu token completo aquí. 
TELEGRAM_TOKEN = "8568099056:AAGb-8DzVJpcCRXqgbUTiG_t4wFmYroTFaw" 
TELEGRAM_CHAT_ID = "6355970908"

# Ignorar errores de certificado SSL al descargar el motor de Chrome
os.environ['WDM_SSL_VERIFY'] = '0'

# ==========================================
# FUNCIÓN PARA ENVIAR FOTOS
# ==========================================
def enviar_foto_telegram(ruta_foto):
    """Envía un archivo de imagen a tu chat de Telegram."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        
        with open(ruta_foto, "rb") as foto:
            datos = {
                "chat_id": TELEGRAM_CHAT_ID, 
                "caption": f"📸 Captura del Consulado a las {hora_actual}"
            }
            archivos = {"photo": foto}
            respuesta = requests.post(url, data=datos, files=archivos)
            
            if respuesta.status_code == 200:
                print("✅ Screenshot enviada a Telegram.")
            else:
                print(f"⚠️ Error enviando foto: {respuesta.text}")
    except Exception as e:
        print(f"❌ Error conectando con Telegram: {e}")

# ==========================================
# LÓGICA PRINCIPAL DEL NAVEGADOR
# ==========================================
def revisar_turnos():
    opciones = Options()
    opciones.add_argument("--headless")
    opciones.add_argument("--window-size=1920,1080")
    opciones.add_argument("--disable-gpu")
    opciones.add_argument("--no-sandbox")

    driver = None # Inicializamos vacío como escudo de seguridad

    try:
        # AHORA EL DRIVER SE CREA AQUÍ ADENTRO. Si falla el internet, no rompe el programa.
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opciones)
        wait = WebDriverWait(driver, 20)

        driver.get("https://www.exteriores.gob.es/Consulados/bahiablanca/es/ServiciosConsulares/Paginas/Solicitud-de-cita-previa--Ley-de-Memoria-Democr%C3%A1tica.aspx")

        ventana_principal = driver.current_window_handle
        ventanas_antes = driver.window_handles

        boton_cita = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'citaconsular')]")))
        driver.execute_script("arguments[0].scrollIntoView();", boton_cita)
        time.sleep(1) 
        boton_cita.click()

        wait.until(EC.number_of_windows_to_be(len(ventanas_antes) + 1))
        
        ventanas_despues = driver.window_handles
        nueva_ventana = [w for w in ventanas_despues if w != ventana_principal][0]
        driver.switch_to.window(nueva_ventana)
        
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert.accept()
        except TimeoutException:
            pass

        boton_continuar = wait.until(EC.element_to_be_clickable((By.ID, "idCaptchaButton")))
        boton_continuar.click()

        # Esperamos a que cargue la página de resultados
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(15) # Pausa breve para asegurar que todo el texto/estilos terminen de renderizar

        # --- TOMAR Y ENVIAR SCREENSHOT ---
        ruta_screenshot = "estado_turno.png"
        driver.save_screenshot(ruta_screenshot)
        print("📸 Captura tomada. Enviando...")
        enviar_foto_telegram(ruta_screenshot)

    except TimeoutException:
        print("⚠️ La página tardó mucho en cargar.")
    except Exception as e:
        print(f"⚠️ Error al intentar revisar (posible fallo de red): {e}")
    finally:
        # Solo cerramos el driver si llegó a crearse exitosamente
        if driver is not None:
            driver.quit()

# ==========================================
# GESTOR DE TIEMPOS (57, 58, 59)
# ==========================================
if __name__ == "__main__":
    print("🤖 Bot iniciado. Monitoreando reloj...")
    minuto_anterior = -1

    while True:
        ahora = datetime.datetime.now()
        minuto_actual = ahora.minute

        # Si estamos en uno de los 3 minutos objetivo y aún no hemos ejecutado en ESTE minuto
        if minuto_actual in [57, 58, 59] and minuto_actual != minuto_anterior:
            print(f"\n[{ahora.strftime('%H:%M:%S')}] ¡Es el minuto {minuto_actual}! Ejecutando revisión...")
            revisar_turnos()
            minuto_anterior = minuto_actual # Guardamos el minuto para no repetir
        
        # Si ya salimos de la ventana de los minutos objetivo, reseteamos el estado
        if minuto_actual not in [57, 58, 59]:
            minuto_anterior = -1
            
        # Revisa el reloj cada 5 segundos para no consumir CPU en vano
        time.sleep(5)