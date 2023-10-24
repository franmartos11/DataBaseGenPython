import math
import requests
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from divicionSectores import cantidadDatosPosiblesXpaisSegunProvincias, obtenerProvinciasPais, cantidadDePeticionesNecesariasSegunCantDatos, existeElPais
from emailsAutomat import cleanEmailFormat, sendEmail, sendEmailsToEverione
import tkinter as tk

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
    # Diccionario para almacenar enlaces de redes sociales
    social_links = {}
    # Filtro contra webs mal puestas
    if 'facebook' in webUrl.lower() or 'instagram' in webUrl.lower() or 'linkedin' in webUrl.lower() :
        return social_links
    try:
        # Configurar opciones para ejecutar en modo headless
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Modo headless
        chrome_options.add_argument('--ssl-version-max=tls1.2')

        # Inicializar el controlador de Selenium
        driver = webdriver.Chrome(options=chrome_options)

        # Abrir la URL
        driver.get(webUrl)

        # Buscar enlaces a redes sociales utilizando XPath
        social_media_xpath = {
            'LinkedIn': "//a[contains(@href, 'linkedin')]",
            'Instagram': "//a[contains(@href, 'instagram')]",
            'Facebook': "//a[contains(@href, 'facebook')]",
            'Mail': "//*[contains(@href, 'mailto:')]"
        }

        for platform, xpath in social_media_xpath.items():
            try:
                elements = driver.find_elements(By.XPATH, xpath)
                if elements:
                    social_links[platform] = elements[0].get_attribute('href')

            except Exception as e:
                print(f"Error while scraping {platform} link: {e}")

    except Exception as e:
        print(f"Error during scraping: {e}")

    finally:
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

def dictionaryToExelTkinder(exel_name,scrapping,homeDictionary,linkedinDictionary = None,instagramDictionary= None,facebookDictionaty= None,mailDictionary= None):

    # Export DataFrames to Excel using ExcelWriter
    with pd.ExcelWriter(f'{exel_name}.xlsx') as excel_writer:
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
        mailDictionary = generadorDictionaryConFiltro(arrayName, arrayAddress, arrayPhone, cleanEmailFormat(arrayMail), 'Mail')

        # creo los dataframes de los datos extraidos con selenium
        linkedin_df = pd.DataFrame(linkedinDictionary)
        instagram_df = pd.DataFrame(instagramDictionary)
        facebook_df = pd.DataFrame(facebookDictionary)
        mail_df = pd.DataFrame(mailDictionary)

        # crear el exel si hay datos extraidos de selenium
        dictionaryToExel(scrap, home_df, linkedin_df, instagram_df, facebook_df, mail_df)
        print('Exel Creado')
    else:
        # crear el exel si NO hay datos extraidos de selenium
        dictionaryToExel(scrap, home_df)
        print('Exel Creado')

    menu_envio_mails_scrapp(scrap, arrayMail)

    return print('#########Done########')

def menu_envio_mails_scrapp(scrap, arrayMail):
    if scrap:
        print('##############################################')
        print('Envio de emails')
        emailSend = int(input('Deseas enviar un email a cada uno de los encontrados en el scrapping'
                              '1-si'
                              '2-no'))
        if emailSend == 1:
            sendEmailsToEverione(arrayMail)
            print('##############################################')
            print('Envio De Emails Finalizado Con exito')


def generadorDictionaryConFiltro(arrayName, arrayAddress, arrayPhone, arrayFiltro,nameFilter):

    filteredArraysDictionary = {'Name': [], 'Address': [], 'Phone': [], f'{nameFilter}': []}

    for i in range(len(arrayFiltro)):
        if arrayFiltro[i] != 'No encontrado':
            filteredArraysDictionary['Name'].append(arrayName[i])
            filteredArraysDictionary['Address'].append(arrayAddress[i])
            filteredArraysDictionary['Phone'].append(arrayPhone[i])
            filteredArraysDictionary[f'{nameFilter}'].append(arrayFiltro[i])

    return filteredArraysDictionary

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

    #seleccion de si deseo scrappear o no
    scrap = int(input('Desea realizar scrapping de webs 1 = si , 0 = no: '))
    scrapping = False
    if scrap == 1:
        scrapping = True

    places = []
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

def menuPlanDatosDeseados():
    print('###### Menu Para Datos Deseados ######')
    print('')
    scrap = int(input('Desea realizar scrapping de webs 1 = si , 0 = no: '))
    scrapping = False
    if scrap == 1:
        scrapping = True

    cantidadRequests = int(input('Ingrese la cantidad de requests que desea cada una trae 60 datos: '))
    places = []

    for i in range(cantidadRequests):
        print(f'Request numero {i + 1}')
        country = input('Ingrese el país: ')
        provincia = input('Ingrese la provincia: ')
        place_type = input('Ingrese el tipo de lugar: ')
        data = peticionApiPorLugar(country, provincia, place_type)
        places.extend(data)
    placesToDictionary(places, scrapping)


def placesToDictionaryTkinter(exel_name,data,scrap):
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
        mailDictionary = generadorDictionaryConFiltro(arrayName, arrayAddress, arrayPhone, cleanEmailFormat(arrayMail), 'Mail')

        # creo los dataframes de los datos extraidos con selenium
        linkedin_df = pd.DataFrame(linkedinDictionary)
        instagram_df = pd.DataFrame(instagramDictionary)
        facebook_df = pd.DataFrame(facebookDictionary)
        mail_df = pd.DataFrame(mailDictionary)

        # crear el exel si hay datos extraidos de selenium
        dictionaryToExelTkinder(exel_name,scrap, home_df, linkedin_df, instagram_df, facebook_df, mail_df)
        print('Exel Creado')
    else:
        # crear el exel si NO hay datos extraidos de selenium
        dictionaryToExelTkinder(exel_name,scrap, home_df)
        print('Exel Creado')

    menu_envio_mails_scrapp(scrap, arrayMail)

    return print('#########Done########')


def menuVisual():
    places = []
    def buscar():
        country = country_entry.get()
        provincia = provincia_entry.get()
        place_type = place_type_entry.get()
        scrapp_option = scrapp_option_var.get()
        exel_name = exel_name_entry.get()

        #linkedin_scrapp = linkedin_scrapp_var.get()
        #phone_scrapp = phone_scrapp_var.get()
        #email_scrapp  = email_scrapp_var.get()
        #facebook_scrapp  = facebook_scrapp_var.get()

        data = peticionApiPorLugar(country,provincia,place_type)
        places.extend(data)
        placesToDictionaryTkinter(exel_name,places, scrapp_option)

    # Crear una ventana
    ventana = tk.Tk()
    ventana.title("Liquid Leeds")
    ventana.configure(bg="#f0f0f0")  # Cambiar el color de fondo de la ventana
    ventana.geometry("720x400")  # Ancho x Alto en píxeles

    fuente_personalizada = ("Arial", 10)
    fuente_personalizada2 = ("Arial", 12)

    # Etiqueta y entrada para Pais
    country_label = tk.Label(ventana, text="Pais:", font=fuente_personalizada2)
    country_label.pack()
    country_entry = tk.Entry(ventana, font=fuente_personalizada)
    country_entry.pack(pady=10)
    country_label.configure(bg="#F0F0F0")  # Cambiar el color de fondo de la etiqueta

    # Etiqueta y entrada para Provincia
    provincia_label = tk.Label(ventana, text="Provincia:", font=fuente_personalizada2)
    provincia_label.pack()
    provincia_entry = tk.Entry(ventana, font=fuente_personalizada)
    provincia_entry.pack(pady=10)


    # Etiqueta y entrada para Tipo de Negocio
    place_type_label = tk.Label(ventana, text="Tipo de Negocio:", font=fuente_personalizada2)
    place_type_label.pack()
    place_type_entry = tk.Entry(ventana, font=fuente_personalizada)
    place_type_entry.pack(pady=10)

    # Checkbox para hacer scrapping web
    scrapp_option_var = tk.IntVar()
    scrapp_option_checkbox = tk.Checkbutton(ventana, text="Realizar scrapping web", variable=scrapp_option_var, font=fuente_personalizada2)
    scrapp_option_checkbox.pack(pady=10)

    # Etiqueta y entrada nombre de exel
    exel_name_label = tk.Label(ventana, text="Nombre de exel a generar:", font=fuente_personalizada2)
    exel_name_label.pack()
    exel_name_entry = tk.Entry(ventana, font=fuente_personalizada)
    exel_name_entry.pack(pady=10)

    # Checkbox para mostrar Linkedin
    #linkedin_scrapp_var = tk.IntVar()
    #linkedin_scrapp_checkbox = tk.Checkbutton(ventana, text="Scrappear linkedin", variable=linkedin_scrapp_var)
    #linkedin_scrapp_checkbox.pack()

    # Checkbox para mostrar todos los email
    #email_scrapp_var = tk.IntVar()
    #email_scrapp_checkbox = tk.Checkbutton(ventana, text="Scrappear emails", variable=email_scrapp_var)
    #email_scrapp_checkbox.pack()

    # Checkbox para mostrar todos los tel
    #phone_scrapp_var = tk.IntVar()
    #phone_scrapp_checkbox = tk.Checkbutton(ventana, text="Scrappear telefonos", variable=phone_scrapp_var)
    #phone_scrapp_checkbox.pack()

    # Checkbox para mostrar todos los facebook
    #facebook_scrapp_var = tk.IntVar()
    #facebook_scrapp_checkbox = tk.Checkbutton(ventana, text="Scrappear facebook", variable=facebook_scrapp_var)
    #facebook_scrapp_checkbox.pack()

    # Botón de búsqueda
    buscar_button = tk.Button(ventana, text="Buscar", command=buscar, font=fuente_personalizada2)
    buscar_button.pack(pady=10)
    buscar_button.configure(bg="#008CBA", fg="white")  # Cambiar el color de fondo y el color del texto del botón

    # Iniciar la aplicación
    ventana.mainloop()

def menu():
    print('Inicio de scrap de leeds')
    print('')
    print('Selecciona un plan')
    print('')
    print('1: Plan 250 Datos ')
    print('')
    print('2: Plan 500 Datos ')
    print('')
    print('3: Plan 1000 Datos ')
    print('')
    print('4: Plan Obtencion de datos x divicion geografica ')
    print('')
    print('5: Plan Obtencion de cantidad de datos deseada  ')
    print('')
    print('5: Menu visual  ')
    print('')
    print('')

    plan = 0
    while plan != 1 and plan != 2 and plan != 3 and plan != 4 and plan !=5 and plan !=6:
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
        if plan == 5:
            menuPlanDatosDeseados()
        if plan == 6:
            menuVisual()

menu()










