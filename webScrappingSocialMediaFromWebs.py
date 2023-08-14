from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def scrapSocialMediaLinksWithSelenium(webUrl):
    # Configurar opciones para ejecutar en modo headless
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Modo headless

    # Inicializar el controlador de Selenium con las opciones configuradas
    driver = webdriver.Chrome(options=chrome_options)

    # Abrir la URL en el navegador
    driver.get(webUrl)

    # Diccionario para almacenar los enlaces de las redes sociales
    social_links = {}

    # Buscar enlaces a redes sociales utilizando XPath
    social_media_xpath = {
        'LinkedIn': "//a[contains(@href, 'linkedin')]",
        'Instagram': "//a[contains(@href, 'instagram')]",
        'Facebook': "//a[contains(@href, 'facebook')]",
        'Twitter': "//a[contains(@href, 'twitter')]"
    }

    # Iterar a través de los enlaces encontrados y almacenarlos en el diccionario
    for platform, xpath in social_media_xpath.items():
        elements = driver.find_elements(By.XPATH, xpath)
        if elements:
            social_links[platform] = elements[0].get_attribute('href')

    # Cerrar el navegador
    driver.quit()

    # Devolver el diccionario de enlaces encontrados
    return social_links

# Llamada a la función con la URL y convertir el diccionario en un array
social_media_array = list(scrapSocialMediaLinksWithSelenium('https://aspa-web-app.vercel.app').items())

# Imprimir el array
print(social_media_array)
# Llamada a la función con la URL


