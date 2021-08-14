import os

from flask import Flask

def create_app(): # Funcion para crear varias instancias de la app y hacer testing (obligatorio en Flask)
    app = Flask(__name__) # Instancia de la clasde de Flask

    app.config.from_mapping( # Variables de entorno de configuración
        # Cambiar por algo mas complicado con una funcion de hash
        # Variables de entorno para configurar y obtener todas las claves desde las variables de entorno
        SECRET_KEY ="aG45h%&ahjk2$5anm&", # Clave para el cliente (cookie, id unico para saber que usuario es y que datos tiene asociados)
        DATABASE_HOST = os.environ.get("FLASK_DATABASE_HOST"),
        DATABASE_PASSWORD = os.environ.get("FLASK_DATABASE_PASSWORD"),
        DATABASE_USER = os.environ.get("FLASK_DATABASE_USER"),
        DATABASE = os.environ.get("FLASK_DATABASE")
    )

    from . import db # Importo de la carpeta actual db

    db.initApp(app)

    from . import auth
    from . import todo

    app.register_blueprint(auth.bp) # Creo el módulo de auth en el framework de flask
    app.register_blueprint(todo.bp) # Creo el módulo de todo en el framework de flask

    # Una ruta de ejemplo para testear 
    @app.route("/hello")
    def hola():
        return "Hello world!"

    return app