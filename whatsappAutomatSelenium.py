from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time



def whatsapp_automat_v2(numero, mensaje):
    # Configurar la ubicación del perfil de usuario de Chrome


    # Configurar opciones para utilizar el perfil de usuario
    chrome_options = Options()
    chrome_options.add_argument('--profile-directory=Profile 1')
    chrome_options.add_argument('--user-data-dir=C:\\Users\\FRANM\\AppData\\Local\\Google\\Chrome\\User Data\\')

    # Inicializar el controlador de Selenium con las opciones de usuario
    print('a')
    driver = uc.Chrome(executable_path='C:\Program Files\Google\Chrome\Application\chrome.exe', options=chrome_options)
    print('a')
    try:
        print('b')
        driver.get('https://web.whatsapp.com/send?phone=' + numero)
        # Esperar hasta que aparezca el cuadro de entrada de texto
        time.sleep(10)

        input_box = driver.find_elements(By.CLASS_NAME, 'selectable-text copyable-text iq0m558w g0rxnol2')
        print(input_box)

        input_box.send_keys(mensaje + Keys.ENTER)

        print("Mensaje enviado exitosamente.")
    except Exception as e:
        print("Ocurrió un error:", e)
    finally:
        driver.quit()


# Llamada a la función
numero_destino = "54 3512583038"  # Reemplaza con el número al que deseas enviar el mensaje
mensaje_a_enviar = "Hola, esto es un mensaje automatizado."  # Mensaje que deseas enviar
whatsapp_automat_v2(numero_destino, mensaje_a_enviar)
