# Todit

Gestor de tareas creado con el framework de Flask y MySQL

![Preview Image](https://raw.githubusercontent.com/richardesp/todit/master/todo/resources/img/login.png)

![Preview Image](https://raw.githubusercontent.com/richardesp/todit/master/todo/resources/img/index.png)

Antes de clonar el repositorio, debes crear el entorno virtual de python:
```bash
python3 -m venv venv
```

Ahora debes activar el entorno virtual:
```bash
. venv/bin/activate
```

Una vez creado, debes instalar las siguientes depedencias:
```bash
pip3 install werkzeug
```
```bash
pip3 install mysql-connector-python
```
```bash
pip3 install flask
```

Debes completar las variables del fichero ```exportDb.sh```. Recuerda haber creado previamente tanto el usuario como la base de datos en tu servidor de mysql:
```bash
PASSWORD= # Tu contraseña del usuario de acceso
USER= # Usuario de acceso
HOST= # En el caso de querer probarla de forma local, poner "localhost"
DATABASE= # El nombre que le hayas asignado a tu base de datos

export FLASK_DATABASE_PASSWORD=$PASSWORD
export FLASK_DATABASE_USER=$USER
export FLASK_DATABASE_HOST=$HOST
export FLASK_DATABASE=$DATABASE
export FLASK_APP=todo
```
Ejecutas el fichero (recuerda asignar previamente permisos de ejecución):
```bash
sh exportDb.sh
```

Ahora debes ejecutar el siguiente comando para generar el modelo lógico de la base de datos:
```bash
flask init-db
```
Si el comando ha sido exitoso deberá imprimirse ```Data base initialized correctly!```.

Finalmente ejecutar el siguiente script:
```bash
sh startFlask.sh
```

![Preview Image](https://raw.githubusercontent.com/richardesp/todit/master/todo/resources/img/shell.png)

¡Ya estaría todo listo!

