from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from werkzeug.exceptions import abort
from todo.auth import loginRequired
from todo.db import getDb

bp = Blueprint("todo", __name__)

@bp.route("/")
@loginRequired
def index():
    db, c = getDb()
    c.execute(
        "SELECT t.id, t.description, u.username, t.completed, t.created_at FROM Task t, User u WHERE t.created_by = %s AND u.id = %s ORDER BY created_at DESC", (session["user_id"], session["user_id"]) # inner join 
    )

    tasks = c.fetchall()

    return render_template("index.html", tasks = tasks)

@bp.route("/create", methods = ["GET", "POST"])
@loginRequired
def create():
    if request.method == "POST":
        description = request.form["description"]
        error = None

        if not description:
            error = "La descripción es requerida"
        
        if error is not None:
            flash(error)
        else:
            db, c = getDb()
            c.execute(
                "INSERT INTO Task (description, completed, created_by) "
                "values(%s, %s, %s)",
                (description, False, g.user["id"])
            )
            db.commit()
            return redirect(url_for("todo.index"))

    return render_template("tasks/create.html")

def getTask(id):
    db, c = getDb()
    c.execute(
        "SELECT t.id, t.description, t.created_by, t.created_at, u.username FROM Task t, User u where t.created_by = u.id and t.id = %s", 
        (id, )
    )

    task = c.fetchone()

    if task is None:
        abort(404, f"La tarea cuyo id {id} no existe.")

    return task

@bp.route("/<int:id>/update", methods = ["GET", "POST"])
@loginRequired
def update(id):
    task = getTask(id)

    if request.method == "POST":
        description = request.form["description"]
        completed = True if request.form.get("completed") == "on" else False
        error = None

        if not description:
            error = "La descripción es necesaria"
        
        if error is not None:
            flash(error)
        
        else:
            db, c = getDb()
            c.execute(
                "UPDATE Task SET description = %s, completed = %s WHERE id = %s",
                (description, completed, id)
            )
            db.commit()
            return redirect(url_for("todo.index"))

    return render_template("tasks/update.html", task = task)

@bp.route("/<int:id>/delete", methods = ["POST"])
@loginRequired
def delete(id):
    db, c = getDb()
    c.execute(
        "DELETE FROM Task WHERE id = %s", (id, )
    )
    
    db.commit()
    return redirect(url_for("todo.index"))