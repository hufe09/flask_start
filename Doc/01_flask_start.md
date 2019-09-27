# 01 Python Web 框架 Flask 学习

## 1. 创建 Flask Project

使用 Pychram 编辑器可以很方便的创建一个Flask项目，推荐新建一个虚拟环境来运行此项目。我新建了一个与项目名称 flask_start 同名的  Anaconda 虚拟环境。

![title](https://i.loli.net/2019/09/24/G6R9tzhy1xoFXg8.png)

创建完项目看下 Python 以及 Flask 版本。

```
(flask_start) E:\Dropbox\flask_start>flask --version
Python 3.7.4
Flask 1.1.1
Werkzeug 0.16.0
```

创建项目之后，目录如下：

```
(flask_start) E:\Dropbox\flask_start>tree /f
│  app.py
│
├─static
└─templates
```

*app.py* 中内容如下：

``` python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
```



## 2. 第一个 Flask 程序讲解

*app.py* 修改如下

```
# 从flask这个框架中导入Flask这个类
from flask import Flask

# 初始化一个Flask对象
# Flask()
# 需要传递一个参数 __name__
# 1. 方便flask框架去寻找资源
# 2. 方便flask插件比如Flask-Sqlalchemy出现错误的时候，好去寻找问题所在的位置
app = Flask(__name__)



# @app.route是一个装饰器
# @开头，并且在函数的上面，说明是装饰器
# 这个装饰器的作用，是做一个url与视图函数的映射
# 127.0.0.1:5000/   ->  去请求hello_world这个函数，然后将结果返回给浏览器
@app.route('/')
def hello_world():
    return '第一个 Flask 程序。'


# 如果当前这个文件是作为入口程序运行，那么就执行app.run()
if __name__ == '__main__':
    # app.run()
    # 启动一个应用服务器，来接受用户的请求
    # while True:
    #   listen()
    app.run()
```

运行后，在浏览器中打开 `http://127.0.0.1:5000/`。

```
(flask_start) E:\Dropbox\flask_start>flask run
 * Environment: development
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

![image](https://raw.githubusercontent.com/hufe09/GitNote-Images/master/image_hosting/image.ssupasunz7e.png)

## 3. 开启 Debug 模式

### Debug 模式的两大功能

- 当程序出现问题的时候，可以在页面中看到错误信息和出错的位置。
- 只要修改了项目中的 `python` 文件，程序会自动加载，不需要手动重新启动服务器。
### 如何设置
- 1.0 版本之前

在 `app.run()` 中传入一个关键字参数 debug，就设置当前项目为 debug 模式。
```
if __name__ == '__main__':
    app.run(debug=True)
```

- 1.0 版本之后，使用环境变量来配置

要进入调试模式就要修改环境的环境变量，修改`FLASK_ENV=development` 或者 `FLASK_DEBUG=1`，才能进入调试。
Unix Bash (Linux, Mac, etc.):

```
$ export FLASK_ENV=development
$ export FLASK_DEBUG=1
```

Windows CMD:

```
> set FLASK_ENV=development
> set FLASK_DEBUG=1
```

Windows PowerShell:

```
> $env:FLASK_ENV = "development"
> $env:FLASK_DEBUG = 1
```

**设置 FLASK_ENV=development**

```
(flask_start) E:\Dropbox\flask_start>set FLASK_ENV=development

(flask_start) E:\Dropbox\flask_start>flask run
 * Environment: development
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 125-285-744
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
**设置 FLASK_DEBUG=1**

```
(flask_start) E:\Dropbox\flask_start>set FLASK_DEBUG=1

(flask_start) E:\Dropbox\flask_start>flask run
 * Environment: development
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 125-285-744
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
运行中的调试器截图：
![image](https://raw.githubusercontent.com/hufe09/GitNote-Images/master/image_hosting/image.4i8bxzqby5.png)

**WIN 如何设置环境变量：**
```
1. 查看所有环境变量：set
2. 设置环境变量：set MyEnvTest=D:\res
3.查看某个或某类环境变量：set MyEnvTest
4.修改环境变量值：set MyEnvTest=%MyEnvTest%;D:\apk
5.删除某个环境变量：set MyEnvTest=
```
所有的在cmd命令行下对环境变量的修改只对**当前窗口**有效，不是永久性的修改。

如果是在 Pychram 中，可以这样设置，也是只针对当前运行。
![title](https://i.loli.net/2019/09/24/sFIXDnLvM9g5wxB.png)



## 4. 使用配置文件

[Flask 文档 配置管理](<https://dormousehole.readthedocs.io/en/latest/config.html>)

1. 新建一个 `config.py` 文件，文件名可以任意取。

*config.py*

``` python
# Example configuration
DEBUG = True
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
```
2. 在主 app 文件中导入这个文件，并且配置到 *app.py* 文件中，示例代码如下：
    - 1.0 版本之前，需要先 `import config`

    ``` python
    import config

    app = Flask(__name__)
    app.config.from_object(config)
    ```
    - 1.0 版本之后，不再需要 `import`。注意！！只需要配置名称，无需填入文件路径。

    ``` python
    app = Flask(__name__)
    app.config.from_object('config')
    ```
3. 还有许多的其他参数，都是放在这个配置文件中，比如 `SECRET_KEY` 和 `SQLALCHEMY` 这些配置，都是在 *config.py* 这个文件中。

## 5. URL 传参数

1. 参数的作用：可以在相同的 URL，但是指定不同的参数，来加载不同的数据。
2. 在 Flask 中如何使用参数：
``` python
@app.route('/article/<id>')
def article(id):
    return f'您请求的参数是：{id}'
```
* 参数需要放在两个尖括号中。
* 视图函数中需要放和 url 中的参数同名的参数。

``` python
@app.route("/movie/<id>/<islogin>/")
def movie_detail(id, islogin):
    login_url = url_for("login")
    if islogin == '0':
        return redirect(login_url)
    else:
        return f"This movie id is {id}."
```



## 6. 反转 URL
1. 什么叫做反转 url：从视图函数到 url 的转换叫做反转 url

2. 反转 url 的用处：
    * 在页面重定向的时候，会使用url反转。
    * 在模板中，也会使用url反转。
    
    ``` python
    from flask import url_for
    
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
    ```
    
    

## 7. 页面跳转和重定向
1. 用处：在用户访问一些需要登录的页面的时候，如果用户没有登录，那么可以让她重定向到登录页面。
2. 代码实现：
    ``` python
    from flask import redirect
    redirect(url_for('login'))
    ```

    ``` python
    @app.route("/movie/<id>/<islogin>/")
    def movie_detail(id, islogin):
        login_url = url_for("login")
        if islogin == '0':
            return redirect(login_url)
        else:
            return f"This movie id is {id}."
    ```
