from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def whatsapp_automat_v2(numero, mensaje):
    # Configure Chrome options to use the specified user profile
    chrome_options = Options()
    chrome_options.add_argument('--profile-directory=Profile 1')
    chrome_options.add_argument('--user-data-dir=C:\\Users\\FRANM\\AppData\\Local\\Google\\Chrome\\User Data\\')

    # Initialize the Selenium WebDriver with the specified Chrome options
    service = Service(executable_path='C:\Program Files\Google\Chrome\Application\chrome.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)


    try:
        # Open WhatsApp Web
        driver.get('https://web.whatsapp.com/send?phone=' + numero)

        # Wait for the page to load and display the input box
        time.sleep(10)

        # Find the input box element by its class name
        input_box = driver.find_element(By.CLASS_NAME, 'selectable-text')

        # Type the message and press ENTER
        input_box.send_keys(mensaje + Keys.ENTER)

        print("Mensaje enviado exitosamente.")
    except Exception as e:
        print("Ocurrió un error:", e)
    finally:
        driver.quit()



# Replace with the desired recipient's number and message
numero_destino = "54 3512583038"
mensaje_a_enviar = "Hola, esto es un mensaje automatizado."

# Call the function
whatsapp_automat_v2(numero_destino, mensaje_a_enviar)
