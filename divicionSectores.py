import json
import math

def abrirJsonPaises():
    with open('divicion_pais.json', 'r') as jsonPaises:
        data = json.load(jsonPaises)
    for pais in data['paises']:
        nombre_pais = pais['nombre']
        provincias = pais['divicionTerritorial']
        if nombre_pais == 'Argentina':
            print(provincias)


def obtenerProvinciasPais(nombrePais):
    with open('divicion_pais.json', 'r') as jsonPaises:
        data = json.load(jsonPaises)
    for pais in data['paises']:
        nombre_pais = pais['nombre']
        provincias = pais['divicionTerritorial']
        if nombre_pais == nombrePais:
            return provincias

# devuelve true si la cantidad de datos a obtener se puede realizar en ese pais, sino false

def se_puede_realizar_peticion_del_pais_por_cantidad_de_datos(paisrequest, cantidadatos):
    with open('divicion_pais.json', 'r') as jsonPaises:
        data = json.load(jsonPaises)

    for pais in data['paises']:
        nombre_pais = pais['nombre']
        provincias = pais['divicionTerritorial']

        if nombre_pais == paisrequest:
            cantprovincias = len(provincias)

            if (cantprovincias * 60) > cantidadatos:
                print('se puede')
                return True
            else:
                print('no se puede')
                return False

#se_puede_realizar_peticion_del_pais_por_cantidad_de_datos('Argentina', 500)

def cantidadDePeticionesNecesariasSegunCantDatos():
    cantidad_datos_a_obtener = int(input('Ingrese el numero de cantidad de datos que deseo obtener: '))
    cantidad_peticiones = math.ceil(cantidad_datos_a_obtener / 60)
    return cantidad_peticiones

#cantidadDePeticionesxPais()

def cantidadDatosPosiblesXpaisSegunProvincias(nombre):
    with open('divicion_pais.json', 'r') as jsonPaises:
        data = json.load(jsonPaises)
    for pais in data['paises']:
        nombre_pais = pais['nombre']
        provincias = pais['divicionTerritorial']
        if nombre_pais == nombre:
            cantpeticiones = len(provincias)
            datosPosibles = cantpeticiones * 60
            print(f'Cant de peticiones posibles en {nombre} : {cantpeticiones}')
            print(f'Cant de datos posibles a obtener en {nombre} por provincias : {datosPosibles}')
            return datosPosibles

    return print('country not found')

def existeElPais(nombrepais):
    with open('divicion_pais.json', 'r') as jsonPaises:
        data = json.load(jsonPaises)
    for pais in data['paises']:
        nombre_pais = pais['nombre']
        if nombre_pais == nombrepais:

            return True
    return False


def menu():
    pais = input('Ingrese el nombre del pais: ')
    cantidadDatosNecesarios = int(input('Ingrese la cantidad de datos que necesita: '))

    if cantidadDatosNecesarios < cantidadDatosPosiblesXpaisSegunProvincias(pais):
        arrayProvincias = obtenerProvinciasPais(pais)



