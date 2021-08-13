PASSWORD= # Tu contraseña del usuario de acceso
USER= # Usuario de acceso
HOST= # En el caso de querer probarla de forma local, poner "localhost"
DATABASE= # El nombre que le hayas asignado a tu base de datos

export FLASK_DATABASE_PASSWORD=$PASSWORD
export FLASK_DATABASE_USER=$USER
export FLASK_DATABASE_HOST=$HOST
export FLASK_DATABASE=$DATABASE
