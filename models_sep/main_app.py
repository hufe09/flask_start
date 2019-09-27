from flask import Flask
from models import Comment
from middle import db


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


@app.route("/")
def index():
    return "Models."


if __name__ == "__main__":
    app.run()
