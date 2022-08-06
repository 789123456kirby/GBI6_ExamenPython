# NOMBRE (Kirby, Guillermo):

# Carga de librerías necesarias
    
from Bio import Entrez
import pandas as pd
import re
import matplotlib.pyplot as plt
def download_pudmed(keyword):
    """Esta funcion busca una palabra clave en la bace de datos PubMed usando el paquete Entrez de Biopython
    Para usarlo, se debe especificar lo siguiente download_pudmed(keyword)
    La funcion devuelve un diccionario con los IDs de las publicaciones, un conteo de cuantas publicaciones 
    y demas informacion en un diccionario"""
    pudmed_salida = open('data/' +keyword,'w' )
    Entrez.email = 'A.N.Other@example.com'
    result = Entrez.esearch(db='pubmed',
                            term=keyword, 
                            retmax = 1000, usehistory = 'y')
    data = Entrez.read(result)
    id_list = data['IdList']
    webenv = data['WebEnv']
    query_key = data['QueryKey']
    handle = Entrez.efetch(db = 'pubmed',
                           rettype = 'medline',
                           retmode = 'text', 
                           retmax = 1000, 
                           webenv = webenv, 
                           query_key = query_key)
    texto = handle.read() 
    pudmed_salida.write(texto)
    pudmed_salida.close()
    texto = texto.split('\nPMID- ')
    years = []
    num_autors = []
    paises = []
    for articulo in texto[1:]:
        
        year = re.findall(r'DP\s\s-\s(\d\d\d\d)', articulo)[0]
        num_autor = len(re.findall(r'AU  - ', articulo))
        pais = re.findall(r'PL\s\s-\s(.*)', articulo)[0]
        if pais == 'England':
            pais = 'United Kingdom'
        years.append(year)
        paises.append(pais)
        num_autors.append(num_autor)
    pmtable = pd.DataFrame({'ID':id_list, 
                           'Year':years,
                           'Autores':num_autors,
                           'Pais':paises})
        
    return pmtable
def scince_plots (dowload_pudmed):

    """se utiliza download_pubmed y oredena los conteos por autores por pais en orden acendente y selecciona los 5 mas abundantes"""
    dowload_pudmed2 = dowload_pudmed.groupby('Pais').sum()
    dowload_pudmed2 = dowload_pudmed2.sort_values('Autores',ascending=False).head(5)
    plt.pie(dowload_pudmed2['Autores'],labels =dowload_pudmed2.index)
    plt.savefig("img/publicaciones.pdf")
    
    
    
