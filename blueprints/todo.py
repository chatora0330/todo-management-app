from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from flask_login import (
    login_required,
    current_user,
)

from database import get_db

from datetime import datetime


bp = Blueprint(
    "todo",
    __name__,
)

@bp.route("/")
@login_required
def index():
    
    db = get_db()
    
    todos = db.execute(
        """
        SELECT *
        FROM todos
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (
            current_user.id,
        ),
    ).fetchall()
    
    return render_template(
        "todo_list.html",
        todos=todos,
    )

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        title = request.form["title"].strip()
        description = request.form["description"].strip()
        priority = request.form["priority"]
        status = request.form["status"]
        deadline = request.form["deadline"]

        if not title:
            flash("タイトルを入力してください。", "danger")
            return redirect(url_for("todo.add"))

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        db = get_db()

        db.execute(
            """
            INSERT INTO todos(
                user_id,
                title,
                description,
                status,
                priority,
                deadline,
                created_at,
                updated_at
            )
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                current_user.id,
                title,
                description,
                status,
                priority,
                deadline,
                now,
                now,
            ),
        )

        db.commit()

        flash("ToDoを追加しました。", "success")

        return redirect(url_for("todo.index"))

    return render_template("todo_add.html")