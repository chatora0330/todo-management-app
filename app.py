from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from blueprints.auth import bp as auth_bp
from blueprints.todo import bp as todo_bp
from config import Config
from database import close_db, get_db
from models import User

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)

app.register_blueprint(auth_bp)

app.teardown_appcontext(close_db)

app.register_blueprint(todo_bp)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth.login"
login_manager.login_message = "ログインしてください"


@login_manager.user_loader
def load_user(user_id):

    db = get_db()

    row = db.execute(
        """
        SELECT * 
        FROM users 
        WHERE id = ?
        """,
        (user_id,),
    ).fetchone()

    if row:
        return User.from_row(row)

    return None


if __name__ == "__main__":
    app.run(debug=True)
