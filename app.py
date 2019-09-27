from flask import Flask, url_for, redirect, render_template

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def index():
    print(url_for("movie_detail", id=20, islogin=1))
    print(url_for("movies_list"))
    context = dict(
        user_name="hufe",
        gender="男",
        age=18,
    )
    return render_template("index.html", **context)


@app.route('/movie/')
def movies_list():
    return "Maoyan top 100 movies lists."


@app.route("/movie/<id>/<islogin>/")
def movie_detail(id, islogin):
    login_url = url_for("login")
    if islogin == '0':
        return redirect(login_url)
    else:
        return f"This movie id is {id}."


@app.route("/login/")
def login():
    return "Please login."


@app.route('/if/<islogin>/')
def if_use(islogin):
    if islogin == '1':
        user = {
            'username': 'Flask',
            'age': 20
        }
        return render_template('if_use.html', user=user)
    else:
        return render_template('if_use.html')


@app.route('/for/')
def for_use():
    books_list = [['西游记', '吴承恩', 100], ['红楼梦', '曹雪芹', 89],
                  ['三国演义', '罗贯中', 59], ['水浒传', '施耐庵', 90]]
    books = []
    for book in books_list:
        detail = {}
        detail['name'] = book[0]
        detail['author'] = book[1]
        detail['price'] = book[2]
        books.append(detail)
    return render_template('for_use.html', books=books)


@app.route('/filter/')
def filter():
    params = dict(
        images="https://dormousehole.readthedocs.io/en/latest/_images/flask-logo.png",
        flask_str='This is Flask Filter.',
        iter_list=['default', 'length', 'last', 'join'],
        str_number='520.1314',
        number=520,
        content_html="<span>HTML Span Tag.</span> \
        <img src='https://dormousehole.readthedocs.io/en/latest/_static/flask-icon.png'> \
           Flask logo.",
    )

    return render_template('filter.html', **params)


@app.route('/base/')
def base():
    title = "Base"
    return render_template('base.html', title=title)


@app.route('/picture/')
def picture():
    title = "Picture"
    return render_template('inherited.html', title=title)


@app.route('/music/')
def music():
    title = "Music"
    return render_template('inherited.html', title=title)


@app.route('/load_static/')
def load_static():
    title = "Load Static"
    return render_template('load_static.html', title=title)


if __name__ == '__main__':
    app.run()
