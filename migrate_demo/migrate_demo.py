from flask import Flask
from exts import db
# from models import Article

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

# 新建一个article模型，采用models分开的方式
# flask-scrpts的方式

# with app.app_context():
#     db.create_all()


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
