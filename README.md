Bot de Turnos para el Consulado

Este script monitorea automáticamente la página de citas del consulado y envía una alerta a Telegram (junto con una captura de pantalla) cuando detecta cambios en la disponibilidad de turnos.

🛠️ Requisitos e Instalación

Antes de ejecutar el script, asegúrate de tener instalado Python en tu computadora. Luego, debes instalar las librerías necesarias.

Abre tu terminal (o la consola de Visual Studio Code) y ejecuta el siguiente comando:

pip install requests selenium webdriver-manager


(Nota: Si usas Windows y te da error el comando anterior, prueba usando python -m pip install requests selenium webdriver-manager o py -m pip install requests selenium webdriver-manager).

📱 Configuración del Bot de Telegram

Para que el script pueda enviarte alertas y capturas de pantalla a tu celular, necesitas crear un bot en Telegram y obtener tus credenciales de acceso. Sigue estos sencillos pasos:

1. Crear el Bot y obtener el TOKEN

Abre la aplicación de Telegram y busca al usuario @BotFather (asegúrate de que tenga el tilde azul de cuenta verificada).

Inicia el chat y envíale el comando: /newbot

Elige un nombre para tu bot (ej. Bot Turnos Consulado).

Elige un nombre de usuario para tu bot. Debe terminar obligatoriamente con la palabra "bot" (ej. TurnosBahia_bot).

@BotFather te enviará un mensaje confirmando la creación. Busca en ese texto la clave que dice "Use this token to access the HTTP API".

Copia y guarda ese TOKEN (se verá parecido a esto: 1234567890:AAExR...).

2. Obtener tu CHAT ID personal

El script necesita saber a qué usuario de Telegram debe enviarle los mensajes. Para averiguar tu ID único:

En el buscador de Telegram, busca al usuario @userinfobot (o @getmyid_bot).

Inicia el chat (o envíale cualquier mensaje, como "Hola").

El bot te responderá con tu información. Cópia el número que aparece al lado de Id (ej. 123456789).

3. Autorizar al bot (¡Paso crucial!)

Por motivos de seguridad, los bots de Telegram no pueden enviarte mensajes si tú no les hablas primero.

Busca en Telegram el nombre de usuario de tu bot (el que creaste en el paso 1.4).

Entra al chat y presiona el botón "Iniciar" (o envía el comando /start).

4. Configurar el código

Abre el archivo script.py y reemplaza las variables de configuración en las primeras líneas con los datos que acabas de obtener:

# ==========================================
# CONFIGURACIÓN DE TELEGRAM
# ==========================================
TELEGRAM_TOKEN = "PEGA_TU_TOKEN_AQUÍ"
TELEGRAM_CHAT_ID = "PEGA_TU_ID_AQUÍ"


⚠️ Advertencia de seguridad: Nunca compartas tu TELEGRAM_TOKEN ni lo subas a repositorios públicos en GitHub, ya que cualquiera podría controlar tu bot.

🚀 Cómo ejecutar el bot

Una vez instaladas las librerías y configurado Telegram, puedes iniciar el bot desde la terminal con:

python script.py
