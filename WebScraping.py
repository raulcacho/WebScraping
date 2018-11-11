from   bs4      import BeautifulSoup
import base64
import csv
import numpy    as np
from   pathlib import Path
import requests
import sys
import time
import urllib
from   WebScrapingFunctions import *

# Definición de parámetros
url        = "https://www.f1-fansite.com/f1-results/"                           # URL de la web
robots_url = "https://www.f1-fansite.com/robots.txt"  							# URL del robots.txt
delimiter  = ','                                      							# Separador de los campos del dataset
dataset    = 'datos_F1_1950_2018.csv'                 							# Nombre del dataset
update     = False

if __name__ == '__main__':

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
    robots_txt = robots_txt.split("\n")                                         # y separamos las líneas

    delay      = [x for x in robots_txt if "Crawl-delay" in x] 					# Buscamos la información del intervalo entre consultas
    delay      = float(delay[0].split(":")[-1])                					# y la convertimos a un número

    years_list, year_urls = retrieve_years_list(url)                			# y buscamos la información de los años en los que se ha disputado la F1

    for i in range(len(years_list)):                                    		# Para cada año
        year = years_list[i]
        year_url = year_urls[i]
        time.sleep(delay)                                           			# Retrasamos la consulta para no incumplir las directrices del robots.txt

        GPs_list, GPs_urls       = retrieve_GPs_list(year, year_url)            # y extraemos la información
        for i in range(len(GPs_list)):                                       	# Para cada GP
            GP = GPs_list[i]
            print("Retrieving data from " + GP + " GP " + year)        			# Informamos del paso que se está realizando
            time.sleep(delay)                                          			# Retrasamos la consulta para no incumplir las directrices del robots.txt
    
            year_GP_url = GPs_urls[i]
            Positions, Numbers, Drivers, Teams, Times, Laps, GridPos, Points = retrieve_classification(year_GP_url) # y extraemos la información
            
            for i in range(len(Positions)):
                # Adaptamos el texto para codificarlo como UTF-16
                position = str(Positions[i].encode('utf-16').decode('utf-16')).strip(" ")
                number   = str(Numbers[i].encode('utf-16').decode('utf-16')).strip(" ")
                driver   = str(Drivers[i].encode('utf-16').decode('utf-16')).strip(" ")
                team     = str(Teams[i].encode('utf-16').decode('utf-16')).strip(" ")
                racetime = str(Times[i].encode('utf-16').decode('utf-16')).strip(" ")
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
                                racetime + delimiter + \
                                lap + '\n'

                # Y la escribimos
                output_file.write(row_to_write)


