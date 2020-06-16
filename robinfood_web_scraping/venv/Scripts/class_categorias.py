import urllib.request
import re
from bs4 import BeautifulSoup
import mysql.connector as mariadb

class Categoria(object):
    def __init__(self, titulo, enlace):
        self.titulo = titulo
        self.enlace = enlace

class Categorias:
    def __init__(self, url):
        self.list_categorias = []
        self.url = url #es la url desde la que vamos a hacer el web scraping
        self.categoria = []
    #necesitamos guardar el nombre de la categoría y el enlace
    def get_categorias(self):
        req = urllib.request.Request(self.url, headers={'User-Agent': "Magic Browser"})
        con = urllib.request.urlopen(req)
        html = con.read().decode() #leemos la página web
        html = re.sub(r'[\t\r\n]', '',html) #necesario porque python tiene problemas con los backslashes
        con.close()
        page_soup = BeautifulSoup(html, "html.parser")

        #sacamos las categorias y las guardamos en un array
        container_categorias = page_soup.findAll('div', {"class":"col-lg-3 col-sm-4 col-xs-12 categoria"})
        #print(container_categorias)
        #for div in container_categorias:
        for div in container_categorias:
            titulo = div.findAll("div",{"class":"texto"})
            categoria = Categoria(titulo[0].h5.get_text(), div.a['href'])
            #print(categoria.titulo)
            #print(categoria.enlace)
            self.list_categorias.append(categoria)
            #hay que guardar la categoría en la base de datos.
            self.save_categoria_BD(categoria.titulo)
        return self.list_categorias

    def save_categoria_BD(self, name_categoria):

        mariadb_conexion = mariadb.connect(host="localhost", user="root", password="", database="robinfood")
        cursor = mariadb_conexion.cursor()
        print(name_categoria)

        try:
            sql = "INSERT INTO categoria (nombre) VALUES ('" + name_categoria + "')"
            cursor.execute(sql)
            #cursor.execute("INSERT INTO categoria (nombre) VALUES (%s)", (cat))

            mariadb_conexion.commit()  # realizamos las operaciones necesarias en la BD
            mariadb_conexion.close()  # cerramos la conexión

            return True
        except mariadb.Error as error:
            print("Error:{}".format(error))
            mariadb_conexion.rollback()
            return False


