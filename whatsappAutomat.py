import pywhatkit as kit
import datetime
import pyautogui , webbrowser
from time import sleep




def whastapp_automat():

    # Número de teléfono en el formato internacional (sin el signo +)
    numero_destino = "+54 3512583038"  # Reemplaza con el número de teléfono del destinatario
    mensaje = "Hola no me odies si queres bloqueame un rato?"

    # Obtener la hora actual y programar el envío 1 minutos después
    hora_actual = datetime.datetime.now()
    print(hora_actual)
    hora_envio = hora_actual + datetime.timedelta(minutes=1.1)
    print(hora_envio)

    # Enviar el mensaje +54 9 3512 02-7607 || +54 9 351 7658958

    kit.sendwhatmsg(numero_destino, mensaje, hora_envio.hour, hora_envio.minute, close_time=2)

def whatsapp_automat_v2(numero):
    webbrowser.open('https://web.whatsapp.com/send?phone='+numero.num)
