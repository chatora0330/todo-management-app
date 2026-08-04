from flask import Flask, render_template

from config import Config
from database import close_db


app = Flask(__name__)
app.config.from_object(Config)

app.teardown_appcontext(close_db)

@app.route("/")
def index():
    return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True)