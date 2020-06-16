

import urllib.request
import re
import os
from bs4 import BeautifulSoup
import mysql.connector as mariadb

from class_categorias import Categorias
from recetas_cat import Recetas_cat
from class_receta import Receta

#primero hay que sacar las categorías desde la página principal
myurl = "https://www.robinfoodtv.com/es/inicio"

categorias_class = Categorias(myurl)
categorias = categorias_class.get_categorias()

#luego hay que ir a cada categoría y sacar todas las recetas

for cat in categorias:
    recetas_cat = Recetas_cat(cat.enlace, cat.titulo)
    #print(cat.titulo, cat.enlace)
    recetas_cat.get_recetas()
    print(vars(recetas_cat))
    #para cada receta procedemos a leerla y guardarla
    for rec in recetas_cat.list_recetas:
        if rec.enlace =="https://www.robinfoodtv.com/es/receta/rodaballo-a-la-meunière":
            rec.enlace = "https://www.robinfoodtv.com/es/receta/rodaballo-a-la-meuniere"
        receta = Receta(rec.enlace, rec.catid)
        receta.get_receta()


#Visitar cada receta y sacar los datos
#https://www.robinfoodtv.com/es/receta/rodaballo-a-la-meunière Esta url falla en la propia página. Da error en su
# en su base de datos.
# Traducido es: https://www.robinfoodtv.com/es/receta/rodaballo-a-la-meuni%C3%A8re
#receta = Receta("https://www.robinfoodtv.com/es/receta/rodaballo-a-la-meuniere", 8)
#receta = Receta("https://www.robinfoodtv.com/es/receta/sardinas-marinadas-tomate-y-albahaca", 8)
#receta.get_receta()