"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

import os
import unicodedata

from flask import Flask
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

## nombre del fichero donde se guarda las frases y realizan las consultas
nombre_archivo = "frases.txt"


## función para quitar las tildes
def quitar_tildes(texto):
    resultado = texto.replace("á","a").replace("Á","a").replace("é","e").replace("É","e").replace("í","i").replace("Í","i")
    resultado = resultado.replace("ó","o").replace("Ó","o").replace("ú","u").replace("Ú","u").replace("Ñ","ñ").lower()
    return resultado

## endpoint raiz --> explica que endpoint se implemente
@app.route('/')
def hello():
    resultado = "<p>Servicio de almacenaje de frases y consulta de palabras</p>"
    resultado += "<p>Para realizar el almacenamiento de frase se ha de añadir a la URI /almacena/ y la frase a introducir</p>"
    resultado += "<p>Para realizar la consulta de palabras se añade a la URI /consulta/ y la palabra a buscar</p>"
    return resultado


## endpoint almacenamiento
## Este endpoint coge el parametro pasado en el URI y lo guarda el fichero incorporando un salto de linea.
## Si existe el archivo a�ade el parametro, si no existe crea el fichero y a�ade el parametro 
@app.route('/almacena/<key>')
def almacena(key):

    if os.path.exists(nombre_archivo):
        archivo = open(nombre_archivo, "a")
    else:
        archivo = open(nombre_archivo, "w")

    archivo.write(key + os.linesep)

    archivo.close()
    return ''


# endpoint de consulta
# Si no existe el archivo donde se almacena las frases no se puede encontrar la palabra pasada como parametro
# por lo que se devuelve un 0 indicando que no hay coincidencias.
# Si existe el archivo trae las lineas en un array.
# Luego se convierte en minusculas y se quita las tildes y se sustituye la � y la � por caracteres tanto del parametro
# de la URI como de las lineas.
# Por �ltimo buscamos el parametro transformado con las las lineas contando las lineas que lo poseen
# y retornarmos ese conteo.
@app.route('/consulta/<key>')
def consulta(key):

    if os.path.exists(nombre_archivo) == False:
        return "0";

    archivo = open(nombre_archivo, "r")
    lineas = archivo.readlines()
    archivo.close()

    contador = 0
    palabra = quitar_tildes(key)
    for linea in lineas:
        frase = quitar_tildes(linea)
        if frase.find(palabra) > -1:
            contador = contador + 1

            
    return str(contador)


# asignamos el puerto 12345 al servicio
if __name__ == '__main__':    
    app.run(port=12345)
