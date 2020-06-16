import urllib.request
import re
from bs4 import BeautifulSoup
import mysql.connector as mariadb

class Receta_cat(object):
    def __init__(self, titulo, enlace, cat_id):
        self.titulo = titulo
        self.enlace = enlace
        self.catid = cat_id

class Recetas_cat:
    def __init__(self, url, nombre_cat):
        self.url = url
        self.nombre_cat = nombre_cat
        self.list_recetas = []

    def get_recetas(self):
        req = urllib.request.Request(self.url, headers={'User-Agent': "Magic Browser"})
        con = urllib.request.urlopen(req)
        html = con.read().decode() #leemos la página web
        html = re.sub(r'[\t\r\n]', '',html) #necesario porque python tiene problemas con los backslashes
        con.close()
        page_soup = BeautifulSoup(html, "html.parser")

        #sacamos el id de la categoria de la receta
        id_cat_recetas = self.get_id_categoria(self.nombre_cat)
        print(id_cat_recetas)
        #sacamos las recetas
        container_recetas = page_soup.findAll("div",{"class":"receta col-lg-3 col-sm-4 col-xs-12 recetas"})

        for div in container_recetas:
            #el div tiene dos enlaces hay que coger el segundo que es el que tiene el enlace a la receta y el titulo.
            titulo = div.a.h5.get_text()
            enlace = div.a["href"]
            receta = Receta_cat(titulo, enlace, id_cat_recetas)
            print(receta.titulo, receta.enlace, receta.catid)
            self.list_recetas.append(receta)

        #return self.list_recetas

    def get_id_categoria(self, name_categoria):
        mariadb_conexion = mariadb.connect(host="localhost", user="root", password="", database="robinfood")
        cursor = mariadb_conexion.cursor()  # necesario para interactuar con la BD

        try:
            sql = "SELECT * FROM categoria WHERE nombre = '" + name_categoria + "'"
            #cursor.execute("SELECT * FROM categoria WHERE nombre = %s", (name_categoria))
            cursor.execute(sql)
            cat = cursor.fetchone()
            #print(cat[0]) #(1,'sopas, caldos y cremas'). La librería de gestión de BD no devuelve el nombre de las columnas
            return cat[0]

        except mariadb.Error as error:
            print("Error:{}".format(error))

        mariadb_conexion.commit()  # realizamos las operaciones necesarias en la BD
        mariadb_conexion.close()  # cerramos la conexión


                