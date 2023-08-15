import math

import requests
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from divicionSectores import cantidadDatosPosiblesXpaisSegunProvincias, obtenerProvinciasPais, cantidadDePeticionesNecesariasSegunCantDatos, existeElPais

def peticionApiPorLugar(country, provincia, place_type):
    # url api , api key, array q devuelve, token para paguinar
    api_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    api_key = 'AIzaSyDIDlJPADfiNnkyieboQ0uWsziE0s4E1iI'
    places = []
    next_page_token = None

    while len(places) < 500:
        query = f"{place_type} in {provincia}, {country}"
        request_params = {
            'key': api_key,
            'query': query,
            'pagetoken': next_page_token
        }

        try:
            response = requests.get(api_url, params=request_params)
            response_data = response.json()

            if 'results' in response_data:
                places.extend(response_data['results'])

            next_page_token = response_data.get('next_page_token')

            if not next_page_token:
                break

            # Agregar un retraso de 2 segundos para esperar respuesta
            time.sleep(2)

        except requests.exceptions.RequestException as error:
            print('Error fetching data:', error)
            break

    return places

def obtenerDetalleSegunPlaceId(place_id):
    api_key = 'AIzaSyDIDlJPADfiNnkyieboQ0uWsziE0s4E1iI'
    api_url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}'

    try:
        response = requests.get(api_url)
        response_data = response.json()

        return response_data.get('result', None)

    except requests.exceptions.RequestException as error:
        print('Error fetching data:', error)
        return None

def scrapSocialMediaLinksWithSelenium(webUrl):
    # Configurar opciones para ejecutar en modo headless
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Modo headless
    chrome_options.add_argument('--ssl-version-max=tls1.2')

    # Inicializar el controlador de Selenium
    driver = webdriver.Chrome(options=chrome_options)

    # Abrir la URL
    driver.get(webUrl)

    # Diccionario para almacenar enlaces de redes sociales
    social_links = {}

    # Buscar enlaces a redes sociales utilizando XPath
    social_media_xpath = {
        'LinkedIn': "//a[contains(@href, 'linkedin')]",
        'Instagram': "//a[contains(@href, 'instagram')]",
        'Facebook': "//a[contains(@href, 'facebook')]",
        'Mail': "//*[contains(@href, 'mailto:')]"
    }

    for platform, xpath in social_media_xpath.items():
        elements = driver.find_elements(By.XPATH, xpath)
        if elements:
            social_links[platform] = elements[0].get_attribute('href')

    # Cerrar el navegador
    driver.quit()

    # Devolver el diccionario de enlaces encontrados
    return social_links

def dictionaryToExel(scrapping,homeDictionary,linkedinDictionary = None,instagramDictionary= None,facebookDictionaty= None,mailDictionary= None):
    exelName = input('Ingrese el nombre del archivo exel a generar: ')

    # Export DataFrames to Excel using ExcelWriter
    with pd.ExcelWriter(f'{exelName}.xlsx') as excel_writer:
        homeDictionary.to_excel(excel_writer, sheet_name='Home', index=False)
        if scrapping:
            facebookDictionaty.to_excel(excel_writer, sheet_name='Facebook', index=False)
            mailDictionary.to_excel(excel_writer, sheet_name='Mails', index=False)
            linkedinDictionary.to_excel(excel_writer, sheet_name='Linkedin', index=False)
            instagramDictionary.to_excel(excel_writer, sheet_name='Instagram', index=False)



def placesToDictionary(data,scrap):
    # arrays de datos para el diccionario
    arrayCantidadDatos = []
    arrayName = []
    arrayAddress = []
    arrayPhone = []
    arrayUrlMaps = []
    arrayWebsite = []
    arrayRating = []
    arrayCantidadReviews = []
    arrayLinkedin = []
    arrayFacebook = []
    arrayInstagram = []
    arrayMail = []

    for place in data:
        place_id = place.get('place_id')
        lugar = obtenerDetalleSegunPlaceId(place_id)

        if lugar:
            name = lugar.get('name', 'Nombre no disponible')
            address = lugar.get('formatted_address', 'Dirección no disponible')
            phone = lugar.get('international_phone_number', 'Teléfono no disponible')
            urlMaps = lugar.get('url', 'url no disponible')
            website = lugar.get('website', 'Sitio web no disponible')
            rating = lugar.get('rating', 'no hay rating')
            cantidadReviews = lugar.get('user_ratings_total', 'No tiene reviews')

            # Actualizar las listas correspondientes en esta única iteración
            arrayCantidadDatos.append(len(arrayCantidadDatos) + 1)
            arrayName.append(name)
            arrayAddress.append(address)
            arrayPhone.append(phone)
            arrayUrlMaps.append(urlMaps)
            arrayWebsite.append(website)
            arrayRating.append(rating)
            arrayCantidadReviews.append(cantidadReviews)

            # si deseo realizar scrap analizo los websites q se extrajeron
            if scrap:
                if website and website != 'Sitio web no disponible':
                    social_media_links = scrapSocialMediaLinksWithSelenium(website)

                    linkedin = social_media_links.get('LinkedIn', 'No encontrado')
                    instagram = social_media_links.get('Instagram', 'No encontrado')
                    facebook = social_media_links.get('Facebook', 'No encontrado')
                    mail = social_media_links.get('Mail', 'No encontrado')

                    # Agregar los enlaces al array correspondiente
                    arrayLinkedin.append(linkedin)
                    arrayInstagram.append(instagram)
                    arrayFacebook.append(facebook)
                    arrayMail.append(mail)
                else:
                    # Si no hay enlace de sitio web, llenar con 'No encontrado'
                    arrayLinkedin.append('No encontrado')
                    arrayInstagram.append('No encontrado')
                    arrayFacebook.append('No encontrado')
                    arrayMail.append('No encontrado')

    dataDictionary = {
        'Id': arrayCantidadDatos,
        'Name': arrayName,
        'Address': arrayAddress,
        'Phone': arrayPhone,
        'URL Maps': arrayUrlMaps,
        'Website': arrayWebsite,
        'Rating': arrayRating,
        'Quantity of Reviews': arrayCantidadReviews,
    }

    # pasar los dictioonary a dataframes usando panda para poder crear las sheets + filtro para limpiar datos q no contangan la info q necesito
    home_df = pd.DataFrame(dataDictionary)
    # genero diccionarios segun un filtro si es que scrappeo
    if scrap:
        linkedinDictionary = generadorDictionaryConFiltro(arrayName, arrayAddress, arrayPhone, arrayLinkedin, 'Linkedin')
        instagramDictionary = generadorDictionaryConFiltro(arrayName, arrayAddress, arrayPhone, arrayInstagram, 'Instagram')
        facebookDictionary = generadorDictionaryConFiltro(arrayName, arrayAddress, arrayPhone, arrayFacebook, 'Facebook')
        mailDictionary = generadorDictionaryConFiltro(arrayName, arrayAddress, arrayPhone, arrayMail, 'Mail')

        # creo los dataframes de los datos extraidos con selenium
        linkedin_df = pd.DataFrame(linkedinDictionary)
        instagram_df = pd.DataFrame(instagramDictionary)
        facebook_df = pd.DataFrame(facebookDictionary)
        mail_df = pd.DataFrame(mailDictionary)

        # crear el exel si hay datos extraidos de selenium
        dictionaryToExel(scrap, home_df, linkedin_df, instagram_df, facebook_df, mail_df)

    else:
        # crear el exel si NO hay datos extraidos de selenium
        dictionaryToExel(scrap, home_df)

    return print('Exel Creado')



def generadorDictionaryConFiltro(arrayName, arrayAddress, arrayPhone, arrayFiltro,nameFilter):

    filteredArraysDictionary = {'Name': [], 'Address': [], 'Phone': [], f'{nameFilter}': []}

    for i in range(len(arrayFiltro)):
        if arrayFiltro[i] != 'No encontrado':
            filteredArraysDictionary['Name'].append(arrayName[i])
            filteredArraysDictionary['Address'].append(arrayAddress[i])
            filteredArraysDictionary['Phone'].append(arrayPhone[i])
            filteredArraysDictionary[f'{nameFilter}'].append(arrayFiltro[i])

    return filteredArraysDictionary

#...........................automatizacion de mandado de emails ..................................

def sendEmail(mailDestinatario):
    # Configuración del servidor SMTP y credenciales
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    mi_correo = 'usafyabot2.4@gmail.com'
    password = 'mfoubsxgpnovkjbx'

    # Crear objeto para el correo electrónico
    msg = MIMEMultipart()
    msg['From'] = mi_correo
    msg['To'] = mailDestinatario
    msg['Subject'] = 'Asunto del correo'

    # Cuerpo del correo
    mensaje = "Este es el contenido del correo."
    msg.attach(MIMEText(mensaje, 'plain'))

    # Establecer conexión con el servidor SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(mi_correo, password)

    # Enviar el correo electrónico
    server.sendmail(mi_correo, mailDestinatario, msg.as_string())

    # Cerrar la conexión
    server.quit()


#...............................Menu............................................................

def menuPlan250Datos():
    print('######Menu Para 250 datos######')
    print('')
    scrap = int(input('Desea realizar scrapping de webs 1 = si , 0 = no: '))
    scrapping = False
    if scrap == 1:
        scrapping = True

    cantidadRequests = 5
    places = []
    for i in range(cantidadRequests):
        print(f'Request numero {i + 1}')
        country = input('Ingrese el país: ')
        provincia = input('Ingrese la provincia: ')
        place_type = input('Ingrese el tipo de lugar: ')
        data = peticionApiPorLugar(country, provincia, place_type)
        places.extend(data)
    placesToDictionary(places, scrapping)

def menuPlan500Datos():
    print('######Menu Para 250 datos######')
    print('')
    scrap = int(input('Desea realizar scrapping de webs 1 = si , 0 = no: '))
    scrapping = False
    if scrap == 1:
        scrapping = True

    cantidadRequests = 9
    places = []
    for i in range(cantidadRequests):
        print(f'Request numero {i + 1}')
        country = input('Ingrese el país: ')
        provincia = input('Ingrese la provincia: ')
        place_type = input('Ingrese el tipo de lugar: ')
        data = peticionApiPorLugar(country, provincia, place_type)
        places.extend(data)
    placesToDictionary(places, scrapping)

def menuPlan1000Datos():
    print('######Menu Para 250 datos######')
    print('')
    scrap = int(input('Desea realizar scrapping de webs 1 = si , 0 = no: '))
    scrapping = False
    if scrap == 1:
        scrapping = True

    cantidadRequests = 17
    places = []
    for i in range(cantidadRequests):
        print(f'Request numero {i + 1}')
        country = input('Ingrese el país: ')
        provincia = input('Ingrese la provincia: ')
        place_type = input('Ingrese el tipo de lugar: ')
        data = peticionApiPorLugar(country, provincia, place_type)
        places.extend(data)
    placesToDictionary(places, scrapping)


def testSectores():
    print('######Busqueda x divicion territorial######')
    print('')
    pais = 'null'

    while existeElPais(pais) == False:
        pais = input('Ingrese el nombre del pais: ')
        existeElPais(pais)

    cantidadDatosNecesarios = int(input('Ingrese la cantidad de datos que necesita: '))
    places = []

    #seleccion de si deseo scrappear o no
    scrap = int(input('Desea realizar scrapping de webs 1 = si , 0 = no: '))
    scrapping = False
    if scrap == 1:
        scrapping = True

    if cantidadDatosNecesarios < cantidadDatosPosiblesXpaisSegunProvincias(pais):
        arrayProvincias = obtenerProvinciasPais(pais)
        place_type = input('Ingrese el tipo de lugar: ')
        cantPeticionesNecesarias = math.ceil(cantidadDatosNecesarios / 60)
        print(cantPeticionesNecesarias)
        cont = 0
        for prov in arrayProvincias:
            data = peticionApiPorLugar(pais, prov, place_type)
            places.extend(data)
            cont += 1
            print(cont)
            if cont >= cantPeticionesNecesarias:
                placesToDictionary(places, scrapping)
                break




def menu():
    print('Inicio de scrapper de Datos x Google Maps')
    print('')
    print('Selecciona uno de los planes')
    print('')
    print('1: Plan 250 Datos ')
    print('')
    print('2: Plan 500 Datos ')
    print('')
    print('3: Plan 1000 Datos ')
    print('')
    print('4: Plan Obtencion de datos x divicion geografica ')
    print('')
    print('')

    plan = 0
    while plan != 1 and plan != 2 and plan != 3 and plan != 4:
        plan = int(input('Ingrese el Numero de plan: '))
        print('')
        if plan == 1:
            menuPlan250Datos()
        if plan == 2:
            menuPlan500Datos()
        if plan == 3:
            menuPlan1000Datos()
        if plan == 4:
            testSectores()



menu()










