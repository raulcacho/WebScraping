from   bs4      import BeautifulSoup
import numpy as np
import requests
import sys

def retrieve_classification(year_GP_url):
    page              = requests.get(year_GP_url)                   # cargamos la información de esta URL
    page_data         = BeautifulSoup(page.content, 'html.parser')  # buscamos la información del GP
    
    # Los datos que nos interesan están en forma de tabla, con diferentes etiquetas de clase        
    Numbers_data      = page_data.find_all("th", class_="msr_col2")
    Drivers_data      = page_data.find_all("td", class_="msr_col3")
    Teams_data        = page_data.find_all("td", class_="msr_col4")
    Times_data        = page_data.find_all("td", class_="msr_col5")
    Laps_data         = page_data.find_all("td", class_="msr_col6")
    GridPos_data      = page_data.find_all("td", class_="msr_col8")
    Points_data       = page_data.find_all("td", class_="msr_col9")

    # Creamos listas para almacenar los datos
    Positions         = []
    Numbers           = []
    Drivers           = []
    Teams             = []
    Times             = []
    Laps              = []
    GridPos           = []
    Points            = []
    
    # Buscamos el texto en cada etiqueta encontrada y lo almacenamos en la lista correspondiente
    if len(Drivers_data) >= 35: # Nunca ha habido mas de 34 pilotos en la F1. En funcion de la web del GP, se leen o no datos de clasificacion
        n_Drivers = int(len(Drivers_data)/2)
    else:
        n_Drivers = len(Drivers_data)
    for i in range(n_Drivers):
        Positions.append(str(i+1))
        Numbers.append(str(Numbers_data[i+1].get_text()))
        Drivers.append(str(Drivers_data[i].get_text()))
        Teams.append(str(Teams_data[i].get_text()))
        Times.append(str(Times_data[i].get_text()))
        Laps.append(str(Laps_data[i].get_text()))
        GridPos.append(str(GridPos_data[i].get_text()))
        Points.append(str(Points_data[i].get_text()))
    return Positions, Numbers, Drivers, Teams, Times, Laps, GridPos, Points

def retrieve_GPs_list(year, url):
    # Solicitamos la información de esta URL,
    page      = requests.get(url)                     
    page_data = BeautifulSoup(page.content, 'html.parser')

    GPs_data  = page_data.find_all("a")                     # Buscamos las etiquetas de hipervínculo
    urls_data = page_data.find_all("a", href=True)

    GPs_list  = []                                          # Creamos una lista que almacene los datos
    urls_list  = []                                         # Creamos una lista que almacene los datos
    for data in urls_data:                                  # Recorremos todas las etiquetas
        link = data.find_all("a", href=True)
        dummy = data['href']
        # Buscamos aquellas direcciones que dirigen a los resultados de cada GP 
        if ("/f1-result/result" in dummy) or ("/f1-results/result" in dummy) or ("/f1-results/race" in dummy) or ("/f1-result/race" in dummy):
            if dummy not in set(urls_list):                 # Evitamos repetir urls
                urls_list.append(dummy)                     # y las añadimos a la lista
                
                # De esta URL extraemos el nombre del GP y lo añadimos a la lista
                dummy = str(dummy)
                dummy = dummy.split(year)[-1]
                dummy = dummy.strip('/')
                dummy = dummy.replace('formula-1', '')
                dummy = dummy.replace('of-', '')
                dummy = dummy.replace('grand-prix', '')
                dummy = dummy.replace('-', ' ')
                dummy = dummy.strip(' ')
                GPs_list.append(dummy)
    return GPs_list, urls_list

def retrieve_years_list(url):
    # Solicitamos la información de esta URL,
    page       = requests.get(url)                          
    page_data  = BeautifulSoup(page.content, 'html.parser')

    year_data  = page_data.find_all("option")               # Buscamos las etiquetas "option"
    urls_data  = page_data.find_all("a", href=True)

    years_list = []
    urls_list  = []                                         # Creamos una lista que almacene los datos
    for data in urls_data:                                  # Recorremos todas las etiquetas
        link = data['href']                                 # Obtenemos el texto de la etiqueta y lo separamos según los espacios en blanco
        try:
            dummy = link.split('/')
            dummy = dummy[-2].split('-')
            if (dummy[-1] == 'standings'):
                if dummy[0] not in set(years_list):
                    years_list.append(dummy[0])
                    urls_list.append(link)
        except:
            pass
    return years_list, urls_list

