from   bs4      import BeautifulSoup
import base64
import csv
import numpy    as np
import requests
import sys
import time
import urllib
from   WebScrapingFunctions import *

# Definición de parámetros
url        = "https://www.f1-fansite.com/f1-results/" # URL de la web
robots_url = "https://www.f1-fansite.com/robots.txt"  # URL del robots.txt
delimiter  = ','                                      # Separador de los campos del dataset
dataset    = 'datos_F1_1950_2018.csv'                 # Nombre del dataset


if __name__ == '__main__':

    # Creamos el fichero que contendrá el dataset y lo abrimos para escritura
    output_file = open(dataset, 'w', encoding='utf-16')

    # Escribimos la cabecera de datos
    header      = '# Year' + delimiter + \
                  'GP' + delimiter + \
                  'Driver' + delimiter + \
                  'Number' + delimiter + \
                  'Team' + delimiter + \
                  'Grid position' + delimiter + \
                  'Final position' + delimiter + \
                  'Points' + delimiter + \
                  'Finish' + delimiter + \
                  'Laps' + '\n'
    output_file.write(header)

    robots_txt = str(BeautifulSoup(requests.get(robots_url).content, "html.parser")) # Leemos el contenido del robots.txt
    robots_txt = robots_txt.split("\n")                                              # y separamos las líneas

    delay      = [x for x in robots_txt if "Crawl-delay" in x] # Buscamos la información del intervalo entre consultas
    delay      = float(delay[0].split(":")[-1])                # y la convertimos a un número

    page       = requests.get(url)                             # Solicitamos la información de la web,
    page_data  = BeautifulSoup(page.content, 'html.parser')    # cargamos su contenido
    years_list = retrieve_years_list(page_data)                # y buscamos la información de los años en los que se ha disputado la F1

    for year in years_list[0:1]:                                    # Para cada año
        time.sleep(delay)                                           # Retrasamos la consulta para no incumplir las directrices del robots.txt

        year_url       = url + year + "-f1-championship-standings/" # Definimos la URL con la información del año,
        page           = requests.get(year_url)                     # cargamos la información de esta URL,
        page_year_data = BeautifulSoup(page.content, 'html.parser') # buscamos la información de los GPs del año,
        GPs_list       = retrieve_GPs_list(page_year_data)          # y la extraemos.

        for GP in GPs_list[0:1]:                                       # Para cada GP
            print("Retrieving data from " + GP + " GP " + year)        # Informamos del paso que se está realizando
            time.sleep(delay)                                          # Retrasamos la consulta para no incumplir las directrices del robots.txt
    
            year_GP_url       = url + "race-results-" + year + \
                                "-" + GP.replace(" ", "-").lower() + \
                                "-f1-grand-prix/"                      # Definimos la URL con la información del GP,       

            page              = requests.get(year_GP_url)              # cargamos la información de esta URL
            page_GP_data = BeautifulSoup(page.content, 'html.parser')  # buscamos la información del GP
            Positions, Numbers, Drivers, Teams, Times, Laps, GridPos, Points    = retrieve_classification(page_GP_data) # y la extraemos.
            
            for i in range(len(Positions)):
                # Adaptamos el texto para codificarlo como UTF-16
                position = str(Positions[i].encode('utf-16').decode('utf-16')).strip(" ")
                number   = str(Numbers[i].encode('utf-16').decode('utf-16')).strip(" ")
                driver   = str(Drivers[i].encode('utf-16').decode('utf-16')).strip(" ")
                team     = str(Teams[i].encode('utf-16').decode('utf-16')).strip(" ")
                time     = str(Times[i].encode('utf-16').decode('utf-16')).strip(" ")
                lap      = str(Laps[i].encode('utf-16').decode('utf-16')).strip(" ")
                gridpos  = str(GridPos[i].encode('utf-16').decode('utf-16')).strip(" ")
                point    = str(Points[i].encode('utf-16').decode('utf-16')).strip(" ")

                # Creamos la siguiente fila a introducir en el dataset
                row_to_write  = year + delimiter + \
                                GP + delimiter + \
                                driver + delimiter + \
                                number + delimiter + \
                                team + delimiter + \
                                gridpos + delimiter + \
                                position + delimiter + \
                                point + delimiter + \
                                time + delimiter + \
                                lap + '\n'

                # Y la escribimos
                output_file.write(row_to_write)


