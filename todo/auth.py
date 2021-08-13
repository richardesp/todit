import functools

# Blueprint -> módulos, flash -> mensaje de error interceptado por nuestro sistema de plantillas

from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)

# Encriptacion de contraseñas que envio y recibo, para asi evitar un ManIntheMiddle (no puede leer los datos interceptados)
from werkzeug.security import check_password_hash, generate_password_hash

from todo.db import getDb

# Todas las funciones con todas las rutas que yo defina, deben tener previamente /auth para verificar los inicios de sesión
bp = Blueprint("auth", __name__, url_prefix="/auth") # Blueprint para las autenticaciones

@bp.route("/register", methods = ["GET", "POST"]) # /auth/register
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db, c = getDb() # Retorno la base de datos y el cursor 
        error = None
        c.execute(
            "SELECT id FROM User where username = %s", (username, )
        )
        if not username:
            error = "Username requerido"
        if not password:
            error = "Password requerido"
        elif c.fetchone() is not None:
            error = "El usuario {} se encuentra registrado".format(username)
        
        if error is None:
            c.execute(
                "INSERT INTO User (username, password) VALUES (%s, %s)",
                (username, generate_password_hash(password)) # Encripto la password
            )
            db.commit() # Confirmo los cambios

            return redirect(url_for("auth.login"))
        
        flash(error)
    
    # GET
    return render_template("auth/register.html") # Se devolverá en caso de petición de get

@bp.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db, c = getDb()
        error = None
        c.execute(
            "SELECT * FROM User WHERE username = %s",(username, ) # A las tuplas le tengo que pasar una , vacia al menos si le paso un elemento
        )

        user = c.fetchone()

        if user is None:
            error = "Usuario/contraseña inválida"
        elif not check_password_hash(user["password"], password):
            error = "Usuario/contraseña inválida" # No voy a dar ninguna pista del error al usuario (posibles crackers)

        if error is None:
            session.clear() # Limpio la sesión actual
            session["user_id"] = user["id"] # El id de la sesión actual corresponde al id del usuario registrado de la base de datos
            return redirect(url_for("todo.index")) # Le retorno a su página de tareas

        flash(error)

    # GET
    return render_template("auth/login.html")    

@bp.before_app_request
def loadLoggedInUser(): # Compruebo el usuario actual en la sesión
    user_id = session.get("user_id")

    if user_id is None: # Carecemos de un usuario que ha iniciado sesion
        g.user = None
    else:
        db, c = getDb()
        c.execute(
            "SELECT * FROM User WHERE id = %s", (user_id, )
        )

        g.user = c.fetchone() # Retorna una lista de un único diccionario (el usuario actual)

        

# Función que verifica que el usuario esté registrado
def loginRequired(view):
    @functools.wraps(view)
    def wrapppedView(**kwargs):
        if g.user is None: # El usuario todavía no ha iniciado sesion
            return redirect(url_for("auth.login"))

        return view(**kwargs) # El usuario está logeado y le paso la vista con todos los argumentos

    return wrapppedView

@bp.route("/logout") # Función para volver a la pantalla de inicio de sesión
def logout():
    session.clear()
    return redirect(url_for("auth.login"))