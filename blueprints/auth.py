from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from werkzeug.security import (
    generate_password_hash, 
    check_password_hash
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from database import get_db
from models import User


bp = Blueprint(
    "auth", 
    __name__, 
    url_prefix="/auth",
)


@bp.route("/login")
def login():
    return render_template("login.html")

@bp.route("/signup", methods=["GET", "POST"])
def signup():
    
    if request.method == "POST":
        
        username = request.form["username"].strip()
        password = request.form["password"]
        
        if not username or not password:
            flash("ユーザー名とパスワードを入力してください。", "danger")
            return redirect(url_for("auth.signup"))
        
        db = get_db()
        
        user = db.execute(
            """
            SELECT id
            FROM users 
            WHERE username=?
            """,
            (username,),
        ).fetchone()
        
        if user:
            flash("ユーザー名は既に使用されています。", "warning")
            return redirect(url_for("auth.signup"))
        
        password_hash = generate_password_hash(password)
        
        db.execute(
            """
            INSERT INTO users (
                username, 
                password
            )
            VALUES(?, ?)
            """,
            (
                username, 
                password_hash
            ),
        )
        
        db.commit()
        
        flash("ユーザー登録が完了しました。ログインしてください。", "success")
        
        return redirect(url_for("auth.login"))

    return render_template("signup.html")