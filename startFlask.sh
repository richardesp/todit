MAIN=todo # Carpeta de produccion

. venv/bin/activate
export FLASK_APP=$MAIN
export FLASK_ENV=development
flask run
exit 0
