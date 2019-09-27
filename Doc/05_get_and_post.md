# 05 GET 请求和 POST 请求

## 1. GET 请求和 POST 请求介绍
1. GET请求：
    * 使用场景：如果只对服务器获取数据，并没有对服务器产生任何影响，那么这时候使用 GET 请求。
    * 传参：GET 请求传参是放在 url 中，并且是通过 `?` 的形式来指定 key 和 value 的。
2.  POST 请求：
    * 使用场景：如果要对服务器产生影响，那么使用 POST 请求。
    * 传参： POST 请求传参不是放在 url 中，是通过 `form data` 的形式发送给服务器的。

##  2. GET 和 POST 请求获取参数
1.  GET 请求是通过 `flask.request.args` 来获取。

2.  POST 请求是通过 `flask.request.form` 来获取。

3.  POST 请求在模板中要注意几点：
    * input 标签中，要写 name 来标识这个 value 的 key ，方便后台获取。
    * 在写 form 表单的时候，要指定 `method='post'`，并且要指定 `action='/login/'`。
    
4. 示例代码：
   
    *templates/post_login.html*
    
    ```html
    <form action="{{ url_for('post_login') }}" method="post">
        <table>
            <tbody>
                <tr>
                    <td>用户名：</td>
                    <td><input type="text" placeholder="请输入用户名" name="username"></td>
                </tr>
                <tr>
                    <td>密码：</td>
                    <td><input type="password" placeholder="请输入密码" name="password"></td>
               </tr>
               <tr>
                   <td></td>
                   <td><input type="submit" value="登录"></td>
                </tr>
            </tbody>
        </table>
    </form>
    ```

    

    *templates/post_get.html*

    ``` html
    <li><a href="{{ url_for('search', q='flask') }}">搜索</a></li>
    <li><a href="{{ url_for('post_login') }}">登录</a></li>
    ```
    
    *utils.py*
    
    ``` ptython
    from flask import g
    
    def login_log():
        print(f"The user is {g.username}")
    
    def login_ip_log():
        print(f"The login ip is {g.ip}"
    ```
    
    
    
    *post_get.py*
    
    ``` python
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
    
    @app.route("/login", methods=["GET", "POST"])
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
    
    if __name__ == "__main__":
        app.run()
    ```



## 3. 保存全局变量的 g 属性

`g`：global

1. `g` 对象是专门用来保存用户的数据的。
2. `g` 对象在一次请求中的所有的代码的地方，都是可以使用的。

## 4. 钩子函数（hook）
1. before_request：
    * 在请求之前执行的
    * 是在视图函数执行之前执行的
    * 这个函数只是一个装饰器，他可以把需要设置为钩子函数的代码放到视图函数执行之前来执行
    
    ``` python
    @app.route("/")
    def index():
        print("Index.")
        return render_template("index.html")
    
    @app.before_request
    def my_before_request():
        print("Brfore requests.")
    ```
    
    输出：
    
    ```
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    Brfore requests.
    Index.
    127.0.0.1 - - [27/Sep/2019 15:39:18] "GET / HTTP/1.1" 200 -
    ```
    
    在发送请求之前，先执行 ` my_before_request` ，请求之后才执行 `index` 。
    
2. context_processor：
    * 上下文处理器应该返回一个字典。字典中的 `key` 会被模板中当成变量来渲染。
    * 上下文处理器中返回的字典，在所有页面中都是可用的。
    * 被这个装饰器修饰的钩子函数，必须要返回一个字典，即使为空也要返回。
    
    ``` python
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
    ```
    
    

## 5. 认识 URL

1. 如果使用的是 HTTP 协议，那么浏览器就会使用80端口去请求这个服务器的资源。
2. 如果使用的是 HTTPS 协议，那么浏览器会使用443端口去请求这个服务器的资源。

```
http://www.jianshu.com/
https://www.baidu.com/
https://www.baidu.com/s?ie=utf-8&f=8

http://baike.baidu.com/link?url=ELcglgxAgFQ9WlMytXEhxu-WBtI7mTlDj3TJ-Ht6ZSecAYt0hgqY0euqaB60opaEEZ7JChin5vUd_YkOgMi7BT5kc3E85ZXeoVL2iVfKZu_jHMcNabK8NXilqnfJknKs

http://baike.baidu.com/link?url=ELcglgxAgFQ9WlMytXEhxu-WBtI7mTlDj3TJ-Ht6ZSecAYt0hgqY0euqaB60opaEEZ7JChin5vUd_YkOgMi7BT5kc3E85ZXeoVL2iVfKZu_jHMcNabK8NXilqnfJknKs#3

http://baike.baidu.com/link?url=ELcglgxAgFQ9WlMytXEhxu-WBtI7mTlDj3TJ-Ht6ZSecAYt0hgqY0euqaB60opaEEZ7JChin5vUd_YkOgMi7BT5kc3E85ZXeoVL2iVfKZu_jHMcNabK8NXilqnfJknKs#5
```

## 6. URL 详解

URL 是 Uniform Resource Locator 的简写，统一资源定位符。

一个 URL 由以下几部分组成：

```
scheme://host:port/path/?query-string=xxx#anchor
```

scheme：代表的是访问的协议，一般为 http 或者 https 以及 ftp 等。
host：主机名，域名，比如 www.baidu.com。
port：端口号。当你访问一个网站的时候，浏览器默认使用80端口。
path：查找路径。比如：www.jianshu.com/trending/now，后面的 `trending/now` 就是 path。
query-string：查询字符串，比如：www.baidu.com/s?wd=python，后面的 `wd=python` 就是查询字符串。
anchor：锚点，后台一般不用管，前端用来做页面定位的。

## 7. WEB 服务器和应用服务器以及 WEB 应用框架

web 服务器：负责处理 http 请求，响应静态文件，常见的有 Apache，Nginx 以及微软的 IIS.
应用服务器：负责处理逻辑的服务器。比如 php、python 的代码，是不能直接通过 nginx 这种 web 服务器来处理的，只能通过应用服务器来处理，常见的应用服务器有 uwsgi、tomcat 等。
web 应用框架：一般使用某种语言，封装了常用的 web 功能的框架就是 web 应用框架 Flask、Django以及 Java 中的 SSH(Structs2 + Spring3 + Hibernate3) 框架都是 web 应用框架。