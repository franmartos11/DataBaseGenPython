import pywhatkit as kit
import datetime



def whastapp_automat():

    # Número de teléfono en el formato internacional (sin el signo +)
    numero_destino = "+54 3512583038"  # Reemplaza con el número de teléfono del destinatario
    mensaje = "Hola no me odies si queres bloqueame un rato?"

    # Obtener la hora actual y programar el envío 1 minutos después
    hora_actual = datetime.datetime.now()
    print(hora_actual)
    hora_envio = hora_actual + datetime.timedelta(minutes=1.1)
    print(hora_envio)

    # Enviar el mensaje +54 9 3512 02-7607
    kit.sendwhatmsg(numero_destino, mensaje, hora_envio.hour, hora_envio.minute, close_time=2)


whastapp_automat()

