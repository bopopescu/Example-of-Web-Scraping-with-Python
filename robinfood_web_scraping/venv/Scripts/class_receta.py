
import urllib.request
import re
import os
from bs4 import BeautifulSoup
import mysql.connector as mariadb

class Receta:
    def __init__(self, url, id_categoria):
        self.url_receta = url
        self.id_categoria = id_categoria
        self.titulo = ""
        self.ingredientes = ""
        self.preparacion = ""
        self.foto_final_file = ""
        self.enlace_video = ""

    def get_receta(self):
        req = urllib.request.Request(self.url_receta, headers={'User-Agent': "Magic Browser"})
        con = urllib.request.urlopen(req)  # contiene más datos de la conexión.
        html = con.read().decode('utf-8')  # leemos la página web y la decodificamos
        #html = re.sub(r'[\t\r\n]', '', html)
        con.close()

        page_soup = BeautifulSoup(html, "html.parser")

        # sacamos el titulo de la receta
        container_titulo = page_soup.findAll("div", {"class": "cont_recetas"})
        # filtramos el resultado y obtenemos el titulo
        for div in container_titulo:
            titulo = div.findAll("h2", {"class": "title"})
            self.titulo = titulo[0].get_text();

        # sacamos los ingredientes
        container_ingredientes = page_soup.find_all("div", {"class": "txtIngredientes"})

        for div in container_ingredientes:  # Contiene un array con los elementos encontrados
            # print(div.contents) #devuelve un array con el texto respetando los <br>
            # contenido = div.text #usando esta propiedad quita el html, pero todo lo pone junto.
            self.ingredientes = div.get_text('. ')  # Quita los elementos html y sustituye por el '. '
            # print(self.ingredientes)

        # sacamos los pasos de la preparación
        container_preparacion = page_soup.find_all("div", {"class": "txtPreparacion"})

        for div in container_preparacion:
            self.preparacion = div.get_text(' ')
            #print(self.preparacion)

        container_foto_final = page_soup.findAll("div", {"class": "noticia_card_img"})

        for div in container_foto_final:
            foto_href = div.a['href']
            #print(foto_href)
            foto_name = foto_href[foto_href.rfind(
                "/") + 1:]  # https://stackoverflow.com/questions/663171/how-do-i-get-a-substring-of-a-string-in-python
            '''Recomiendan usar esto, valido para todas las plataformas
                import ntpath
                ntpath.basename("a/b/c")'''
            dir_actual = os.getcwd()
            dir_proyecto = dir_actual[:dir_actual.rfind("\\")]
            dir_foto = dir_proyecto + '\\assets\\' + foto_name

            req_foto = urllib.request.Request(foto_href, headers={'User-Agent': "Magic Browser"})

            con_foto = urllib.request.urlopen(req_foto)  # contiene más datos de la conexión.
            foto = con_foto.read()

            if os.path.isfile(dir_foto):  # si el fichero ya existe...
                n = 1
                copia = "_" + str(n) + "."
                dir_foto = dir_foto.replace(".", copia)  # cambiamos el nombre del fichero.

                while os.path.isfile(dir_foto):  # chequeamos si existe
                    print("Ya existe la imagen")
                    n += 1
                    new_copy = "_" + str(n) + "."
                    dir_foto = dir_foto.replace(copia, new_copy)  # cambiamos el nombre del fichero. Arreglar esto
                    copia = new_copy

            with open(dir_foto, 'wb') as f:  # wb es escribir en bytes
                f.write(foto)
                self.foto_final_file = dir_foto[dir_foto.rfind("\\") + 1:]
                #print(self.foto_final_file)
            con_foto.close()

        # Buscamos ahora el enlace a youtube class="youtube3 hidden-print"
        container_video = page_soup.findAll("div", {"class": "youtube3 hidden-print"})

        for div in container_video:
            self.enlace_video = div.iframe['src']

        # Ahora solo queda guardar todo en la base de datos
        mariadb_conexion = mariadb.connect(host="localhost", user="root", password="", database="robinfood")
        cursor = mariadb_conexion.cursor()  # necesario para interactuar con la BD

        try:
            cursor.execute(
                "INSERT INTO recetas (titulo, ingredientes, preparacion, foto_final, enlace_video, categoria) VALUES (%s,%s,%s,%s,%s,%s)",
                (self.titulo, self.ingredientes, self.preparacion, self.foto_final_file, self.enlace_video, self.id_categoria))
        except mariadb.Error as error:
            print("Error:{}".format(error))

        mariadb_conexion.commit()  # realizamos las operaciones necesarias en la BD
        mariadb_conexion.close()  # cerramos la conexión
