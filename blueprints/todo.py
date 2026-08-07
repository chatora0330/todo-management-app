from flask import (
    Blueprint,
    render_template,
)

from flask_login import (
    login_required,
    current_user,
)

from database import get_db

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
        WHERE user_id=?
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
    