from flask import Flask, render_template, request
from flask import session, redirect, url_for, g
from datetime import timedelta
import os

app = Flask(__name__)
app.config['DEBUG'] = 1
# print(os.urandom(24))
app.config['SECRET_KEY'] = \
    b'v\xcaY\xb1]E\xb5-TS!\x89\x04\x8bC*4\xaf\\\xe0\xfb\xf9\xba\xa3'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)


@app.route("/")
def index():
    print("Index.")
    return render_template("post_get.html")


@app.route("/serach/")
def search():
    url_args = request.args
    return "Url arguments. <br>" + str(url_args)


@app.route("/login/", methods=["GET", "POST"])
def post_login():
    if request.method == "POST":
        post_data = request.form
        print(post_data)
        username = post_data["username"]
        password = post_data.get("password")
        if username == "flask" and password == "password":
            session['username'] = username
            session.permanent = True
            return "Login successfully."
        else:
            return "Login failure."
    else:
        return render_template("post_login.html")


@app.route("/edit/")
def edit():
    print(g)
    if hasattr(g, "username"):
        print(f"User {g.username}, Edit successfuly.")
        return render_template("edit.html")
    else:
        return redirect(url_for("post_login"))


# before_requsest: 在请求之前执行
# 在请求之前执行的
# 是在视图函数执行之前执行的
# 这个函数只是一个装饰器，他可以把需要设置为钩子函数的代码放到视图函数执行之前来执行


@app.before_request
def my_before_request():
    print("Brfore requests." + str(session.get("username")))
    # user_id = session.get("user_id")
    # user = User.query.filter(User.id == user_id).first()
    if session.get("username"):
        g.username = session.get("username")


@app.context_processor
def my_context_processor():
    context_dict = dict(
        username="Python",
        comefrom="context_processor",
        has_login="Has Login"
    )
    if session.get("username"):
        return context_dict
    else:
        return {}


if __name__ == "__main__":
    app.run()
