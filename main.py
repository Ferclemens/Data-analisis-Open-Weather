from datetime import datetime
import requests
import pandas as pd
from pandas import json_normalize
#import json
import os
from dotenv import load_dotenv

def get_data_from_api(city,coord):
    
    #apuntamos a las variables de entorno
    load_dotenv()
    
    #Data para realizar la busqueda en la api de Open Weather
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'
    
    #obtenemos la key desde las variables de entorno
    KEY = os.getenv('API_KEY')
    
    #Armado de la url con los datos provistos y los parametros de la función
    url = f'{BASE_URL}{coord}&q={city}&appid={KEY}'

    #Hacemos una petición (get) al end point y guardamos en una variable.
    response = requests.get(url)
    
    #Convertimos a formato Json
    data = response.json()
    #print('DATA', data)

    #Convertimos los datos almacenados en formato Json a Data Frame de pandas para su modificación
    df = json_normalize(data)
    #print(df)

    #Obtenemos la fecha del dia para armar el nombre del archivo de salida.
    date_now = datetime.now().strftime('%D').replace('/','-')
    #print(date_now)

    #sacamos los espacios de las ciudades para armar el archivo
    city_file = city.replace(' ', '-')
    #construimos el nombre del archivo
    file_path = f'data_analytics\openweather\{city_file}_{date_now}.csv'

    #guardamos los datos en un archivo csv
    with open(file_path, 'w'):
        df.to_csv(file_path, index=False)

#Ciudades y coordenadas para las busquedas
cityList = ['London', 'New York', 'Cordoba', 'Taipei', 'Buenos Aires', 'Mexico DF', 'Dublin', 'Tilfis', 'Bogota', 'Tokio']
coordList = ['lat=31&lon=64', 'lat=40&lon=-73', 'lat=-31&lon=-64', 'lat=25&lon=64', 'lat=-34&lon=-58', 'lat=19&lon=-99', 'lat=53&lon=6', 'lat=41&lon=44', 'lat=4&lon=74', 'lat=35&lon=139']

#Ejecutamos Script para cada item de los arrays (iteramos)
if __name__ == '__main__':
    for city, coord in zip(cityList, coordList):
        get_data_from_api(city,coord)