import pywhatkit as kit
import datetime
import pyautogui, webbrowser
from time import sleep
from pywhatkit import sendwhats_image

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

def whatsapp_automat_v2(numero,mensaje):
    webbrowser.open('https://web.whatsapp.com/send?phone='+numero)
    sleep(10)
    pyautogui.typewrite(f'{mensaje}')
    pyautogui.press('enter')

#whatsapp_automat_v2('54 9 351 7658958')

def envio_multiple_whatsapp(arrayNumeros,mensaje):
    for numero in arrayNumeros:
        whatsapp_automat_v2(numero,mensaje)
        sleep(5)


def envio_multiple_whatsapp_imge(arrayNumeros,arrayTalleres):
    ruta_imagen = 'images/carcheck.png'
    for i, numero in enumerate(arrayNumeros):
      mensaje = f"Hola {arrayTalleres[i]},\n\n" \
                "Soy Agustín, encargado comercial de Aspa Software. Somos una empresa cordobesa de desarrollo de Software a medida.\n\n" \
                "Me comunico con ustedes para presentarles nuestra app multiplataforma de gestión integral para talleres mecánicos, Aspa Car Check.\n\n" \
                "Aspa Car Check le permitirá:\n\n" \
                "- Ahorrar tiempo y mejorar la eficiencia de su taller.\n" \
                "- Brindar una atención más personalizada a sus clientes.\n" \
                "- Tomar decisiones estratégicas para su negocio.\n" \
                "- Gestionar su equipo de trabajo.\n" \
                "- Centralizar toda su información olvidándose de carpetas, hojas y excels.\n\n" \
                "¿Tendrán 5 minutos para hacer un llamado y comentarles un poco más de nuestra solución?\n"

      sendwhats_image(numero, ruta_imagen, mensaje)
      sleep(5)
arraynumtest = ['+54 9 3512 58-3038', '+54 9 3513 84-2751']
arraynomtest = ['agus', 'santi']
envio_multiple_whatsapp_imge(arraynumtest,arraynomtest)

nombresTalleresTotal= [
  "Katz Service Taller Integral del Automotor",
  "Taller Roberto S.R.L.",
  "Taller integral para el automotor R&R",
  "Taller Malvinas",
  "Mecánica Integral del Automotor Franco",
  "Taller Mecánico Integral Samurai Automotive",
  "Medrano Automotores",
  "Talleres Rosedal S.R.L.",
  "Mecánico Autos (Taller Bogado)",
  "Automotores Giangreco",
  "TALLER MECÁNICO BOEDO",
  "Taller Adriano",
  "GPS Taller - Eco Electrónica Automotriz",
  "Taller Mecánico Eagle",
  "Taller JR",
  "Taller Silva Motors",
  "Mecánica Integral MAHLU",
  "Car-Centro Centro de Belleza Automotor , Chapa , Pintura y Mecánica",
  "Taller Mecánico Automotor Julián",
  "Lyon's Servicio Integral del Automotor - Taller mecánico",
  "GPS Taller - Local German Cars",
  "Taller Mecanico ALBERTO",
  "Ar-Go Taller Integral Del Automotor",
  "Taller Mecanico - Jota",
  "GPS Taller - D. Riesco Service Integral del Automotor",
  "Taller Integral del Automóvil",
  "Taller Mecánico Coiroz Vargas",
  "GPS Taller - Taller Tweety",
  "Taller Mecánico Mecatec",
  "Car-Centro Centro de Belleza Automotor , Chapa , Pintura y Mecánica"
]
nombresTalleres1 = [
  "Katz Service Taller Integral del Automotor",
  "Taller Roberto S.R.L.",
  "Taller integral para el automotor R&R",
  "Taller Malvinas",
  "Mecánica Integral del Automotor Franco",
  "Taller Mecánico Integral Samurai Automotive",
  "Medrano Automotores",
  "Talleres Rosedal S.R.L.",

]
nombresTalleres2= [
  "Mecánico Autos (Taller Bogado)",
  "Automotores Giangreco",
  "TALLER MECÁNICO BOEDO",
  "Taller Adriano",
  "GPS Taller - Eco Electrónica Automotriz",
  "Taller Mecánico Eagle",
  "Taller JR",
  "Taller Silva Motors",
]
nombresTalleres3= [
  "Mecánica Integral MAHLU",
  "Car-Centro Centro de Belleza Automotor , Chapa , Pintura y Mecánica",
  "Taller Mecánico Automotor Julián",
  "Lyon's Servicio Integral del Automotor - Taller mecánico",
  "GPS Taller - Local German Cars",
  "Taller Mecanico ALBERTO",
  "Ar-Go Taller Integral Del Automotor",
  "Taller Mecanico - Jota",
  "GPS Taller - D. Riesco Service Integral del Automotor",
  "Taller Integral del Automóvil",
  "Taller Mecánico Coiroz Vargas",
  "GPS Taller - Taller Tweety",
  "Taller Mecánico Mecatec",
  "Car-Centro Centro de Belleza Automotor , Chapa , Pintura y Mecánica"
]
nombresTalleres4= [
  "GPS Taller - D. Riesco Service Integral del Automotor",
  "Taller Integral del Automóvil",
  "Taller Mecánico Coiroz Vargas",
  "GPS Taller - Taller Tweety",
  "Taller Mecánico Mecatec",
  "Car-Centro Centro de Belleza Automotor , Chapa , Pintura y Mecánica"
]
numerosTelefonicosTotal = [
  "+54 9 11 5027-5555",
  "+54 43078109",
  "+54 11 7560-1065",
  "+54 11 4432-0544",
  "+54 9 11 3572-1774",
  "+54 11 3921-6833",
  "+54 11 4867-3736",
  "+54 11 4771-6638",
  "+54 11 2658-1520",
  "+54 11 4305-8212",
  "+54 11 4957-1428",
  "+54 11 4961-4847",
  "+54 11 4855-4146",
  "+54 11 5808-0321",
  "+54 11 2177-0171",
  "+54 11 3980-5150",
  "+54 11 6874-7595",
  "+54 11 3570-7744",
  "+54 11 4555-6062",
  "+54 11 4611-2137",
  "+54 11 4961-8619",
  "+54 11 5148-8870",
  "+54 9 11 2353-8510",
  "+54 11 4706-2658",
  "+54 9 11 4786-1620",
  "+54 9 11 3075-2922",
  "+54 11 2454-4243",
  "+54 11 4866-4996",
  "+54 11 3570-7744"
]
numerosTelefonicos1 = [
  "+54 9 11 5027-5555",
  "+54 43078109",
  "+54 11 7560-1065",
  "+54 11 4432-0544",
  "+54 9 11 3572-1774",
  "+54 11 3921-6833",
  "+54 11 4867-3736",
  "+54 11 4771-6638",
]
numerosTelefonicos2 = [
  "+54 11 2658-1520",
  "+54 11 4305-8212",
  "+54 11 4957-1428",
  "+54 11 4961-4847",
  "+54 11 4855-4146",
  "+54 11 5808-0321",
  "+54 11 2177-0171",
  "+54 11 3980-5150",
]
numerosTelefonicos3 = [
  "+54 11 6874-7595",
  "+54 11 3570-7744",
  "+54 11 4555-6062",
  "+54 11 4611-2137",
  "+54 11 4961-8619",
  "+54 11 5148-8870",
  "+54 9 11 2353-8510",
  "+54 11 4706-2658",
]
numerosTelefonicos4 = [
  "+54 9 11 4786-1620",
  "+54 9 11 3075-2922",
  "+54 11 2454-4243",
  "+54 11 4866-4996",
  "+54 11 3570-7744"
]