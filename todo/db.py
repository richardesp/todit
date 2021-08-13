import mysql.connector

import click # Módulo para ejecutar comandos en la terminal, asi no uso sql-workbench, todo desde terminal
from flask import current_app, g
from flask.cli import with_appcontext # Contexto de la configuración de la aplicacion en la bd, para mantener el login y psw de la bd
from .schema import instructions # Carpeta con los scipts para crear la base de datos (módulo propio)

def getDb():
    if "db" not in g:
        g.db = mysql.connector.connect(
            host = current_app.config["DATABASE_HOST"],
            user = current_app.config["DATABASE_USER"],
            password = current_app.config["DATABASE_PASSWORD"],
            database = current_app.config["DATABASE"]
        )
        g.c = g.db.cursor(dictionary = True) # Acceso a los índices de las tuplas por valor alfanumérico del campo
    return g.db, g.c # Retorno la base de datos y el cursor

def closeDb(e = None):
    db = g.pop("db", None) # Quitamos la propiedad de db a g

    if db is not None: # Compruebo si llamé previamente a db para cerrar la conexión
        db.close()

def initDb():
    db, c = getDb()

    # Lista de strings con instrucciones del DDL
    for instruction in instructions:
        c.execute(instruction)
    
    db.commit()

@click.command("init-db") # Flask init-db -> Ejecutara la función de initDb al escribirlo en terminal (formatea la base de datos por completo)
@with_appcontext # Accederemos a las variables de entorno para asignar los valores de conexión

def initDbCommand():
    initDb()
    click.echo("Data base inicialized correctly!") # Se imprime en la terminal una vez inicializada la bd

def initApp(app):
    app.teardown_appcontext(closeDb) # Cada vez que termine la petición cortaré la conexión con la bd
    app.cli.add_command(initDbCommand)