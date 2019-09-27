from flask import Flask, render_template, request, g
from utils import login_ip_log, login_log


app = Flask(__name__)
app.config['DEBUG'] = 1


@app.route("/")
def index():
    return render_template("post_get.html")


@app.route("/serach")
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
        g.username = username
        login_log()
        g.ip = "192.168.0.1"
        login_ip_log()
        if username == "flask" and password == "password":
            return "Login successfully."
        else:
            return "Login failure."
    else:
        return render_template("post_login.html")


# before_requsest: 在请求之前执行
# 在请求之前执行的
# 是在视图函数执行之前执行的
# 这个函数只是一个装饰器，他可以把需要设置为钩子函数的代码放到视图函数执行之前来执行


@app.before_request
def my_before_request():
    print("Brfore requests.")


if __name__ == "__main__":
    app.run()
