# 02 Flask 渲染 Jinja2 模板和传参
1. 如何渲染模板：
    * 模板放在 `templates` 文件夹下
    * 从 `flask` 中导入 `render_template` 函数。
    * 在视图函数中，使用 `render_template` 函数，渲染模板。注意：只需要填写模板的名字，不需要填写 `templates` 这个文件夹的路径。
2. 模板传参：
    * 如果只有一个或者少量参数，直接在 `render_template` 函数中添加关键字参数就可以了。
    * 如果有多个参数的时候，那么可以先把所有的参数放在字典中，然后在 `render_template` 中，
    使用两个星号，把字典转换成关键参数传递进去，这样的代码更方便管理和使用。
3. 在模板中，如果要使用一个变量，语法是：`{{params}}`
4. 访问模型中的属性或者是字典，可以通过 `{{params.property}}` 的形式，或者是使用 `{{params['age']}}` 

## 1. if 判断
1. 语法：  
    ```
    {% if if_condition %}
    {% else %}
    {% endif %}
    ```
    
2. if的使用，可以和python中相差无几。

3. Example
    *templates/if_use.html*

    ``` html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title></title>
    </head>
    <body>
        {% if user and user.age > 18 %}
            <a href="#">{{ user.username }}</a>
            <a href="#">注销</a>
        {% else %}
            <a href="#">登录</a>
            <a href="#">注册</a>
        {% endif %}
    </body>
    </html>
    ```

    *app.py*

    ``` python
    from flask import Flask, url_for, redirect, render_template
    
    app = Flask(__name__)
    
    @app.route('/if/<islogin>/')
    def if_use(islogin):
        if islogin == '1':
            user = {
                'username': 'Flask',
                'age':  20
            }
            return render_template('if_use.html', user=user)
        else:
            return render_template('if_use.html')
    
    if __name__ == '__main__':
        app.run()
    ```

![image](https://raw.githubusercontent.com/hufe09/GitNote-Images/master/image_hosting/image.25aosqz2nut.png)

## 2. for 循环遍历列表和字典

1. 字典的遍历，语法和 `python` 一样，可以使用 `items()`、`keys()`、`values()`、`iteritems()`、`iterkeys()`、`itervalues()`
    ```
    {% for k, v in user.items() %}
        <p>{{ k }}：{{ v }}</p>
    {% endfor %}
    ```
    
2. 列表的遍历：语法和 `python` 一样。
    ```
    {% for website in websites %}
        <p>{{ website }}</p>
    {% endfor %}
    ```

3. Example 

    *templates/for_use.html*
    
    ``` html
    <body>
        <table>
            <thead>
                <th>书名</th>
                <th>作者</th>
                <th>价格</th>
            </thead>
            <tbody>
                {% for book in books %}
                <tr>
                    <td>{{ book.name }}</td>
                    <td>{{ book.author }}</td>
                    <td>{{ book.price }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    ```

    *app.py*
    
    ``` python
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
    ```

![image](https://raw.githubusercontent.com/hufe09/GitNote-Images/master/image_hosting/image.mnhawfwtx.png)

## 3. 过滤器

1. 介绍和语法：

   - 介绍：过滤器可以处理变量，把原始的变量经过处理后再展示出来。作用的对象是变量。

   - 语法：

     ```
     {{ avatar|default('xxx') }}
     ```

2. `default` 过滤器：如果当前变量不存在，这时候可以指定默认值。

3. `length` 过滤器：求列表、字符串、字典或者元组的长度。

   *templates/filter.html*

   ``` html
   <body>
       <h1>Flask Start.</h1>
       imges_empty <img src="{{ imgaes_empty }}"><br>
       imges_empty default filter. <img
           src="{{ imgaes_empty|default('https://dormousehole.readthedocs.io/en/latest/_static/flask-icon.png') }}"><br>
       imges<br> <img src="{{ images }}">
   </body>
   ```

   

   *app.py*

   ``` python
   @app.route('/filter/')
   def filter():
   
       params = dict(
           images="https://dormousehole.readthedocs.io/en/latest/_images/flask-logo.png",
           flask_str='This is Flask Filter.',
           iter_list=['defaule', 'length', 'last', 'join'],
           str_number='520.1314',
           number=520,
           content_html="<span>HTML Span Tag.</span><img src='https://dormousehole.readthedocs.io/en/latest/_static/flask-icon.png'>   Flask logo.",
           )
   
       return render_template('filter.html', **params)
   ```

   ![image](https://raw.githubusercontent.com/hufe09/GitNote-Images/master/image_hosting/image.p1gvkwrpps.png)
4. 常用的过滤器：
   - `abs(value)`：返回一个数值的绝对值。示例：`-1|abs`
   
   - `default(value,default_value,boolean=false)`：如果当前变量没有值，则会使用参数中的值来代替。示例：`name|default('xiaotuo')` ——如果 name 不存在，则会使用xiaotuo 来替代。`boolean=False` 默认是在只有这个变量为 `undefined` 的时候才会使用 `default` 中的值，如果想使用 python 的形式判断是否为 `false`，则可以传递`boolean=true`。也可以使用 `or` 来替换。
   
   - `escape(value)` 或 `e` ：转义字符，会将`<`、`>`等符号转义成 HTML 中的符号。示例：`content|escape` 或 `content|e`。

   - `first(value)`：返回一个序列的第一个元素。示例：`names|first`
   
   - `format(value,*arags,**kwargs)`：格式化字符串。比如：
     ``` html
     {{ "%s - %s"|format('Hello?',"Foo!") }}
     将输出：Helloo? - Foo!
     ```
   - `last(value)`：返回一个序列的最后一个元素。示例：`names|last`。
   
   - `length(value)`：返回一个序列或者字典的长度。示例：`names|length`。
   
   - `join(value,d=u'')`：将一个序列用 `d` 这个参数的值拼接成字符串。
   
   - `safe(value)`：如果开启了全局转义，那么 `safe` 过滤器会将变量关掉转义。示例：`content_html|safe`。
   
   - `int(value)`：将值转换为 `int` 类型。
   
   - `float(value)`：将值转换为 `float` 类型。
   
   - `lower(value)`：将字符串转换为小写。
   
   - `upper(value)`：将字符串转换为小写。
   
   - `replace(value,old,new)`： 替换将 `old` 替换为 `new` 的字符串。
   
   - `truncate(value,length=255,killwords=False)`：截取 `length` 长度的字符串。
   
   - `striptags(value)`：删除字符串中所有的 HTML 标签，如果出现多个空格，将替换成一个空格。
   
   - `trim`：截取字符串前面和后面的空白字符。
   
   - `string(value)`：将变量转换成字符串。
   
   - `wordcount(s)`：计算一个长字符串中单词的个数。
   
    ![image](https://raw.githubusercontent.com/hufe09/GitNote-Images/master/image_hosting/image.qhi6vj9wu9.png)



## 4. 继承和 block

1. 继承作用和语法：

   - 作用：可以把一些公共的代码放在父模板中，避免每个模板写同样的代码。

   - 语法：

     ```
     {% extends 'base.html' %}
     ```

2. block 实现：

   - 作用：可以让子模板实现一些自己的需求。父模板需要提前定义好。
   - 注意点：字模板中的代码，必须放在 block 块中。
   
   *templates/base.html*
   
   ```html
   <!DOCTYPE html>
   <html lang="en">
   
   <head>
       <meta charset="UTF-8">
       <title>{% block title %} {{ title }} {% endblock %}</title>
   </head>
   
   <body>
       <div class="nav">
           <ul>
               <li><a href="{{ url_for('base') }}">Base</a></li>
               <li><a href="{{ url_for('picture') }}">Picture</a></li>
               <li><a href="{{ url_for('music') }}">Music</a></li>
           </ul>
       </div>
       {% block main %}
       <h1>这是 Base 。</h1>
       {% endblock %}
   </body>
   
   </html>
   ```
   
   
   
   *templates/inherited.html*
   
   ``` html
   {% extends "base.html"%}
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       {% block title %} {{ title }} {% endblock %}
   </head>
   <body>
   {% block main %}
   <h1>这是 {{ name }} , 继承了 Base。</h1>
   {% endblock%}
   </body>
   </html>
   ```
   
   
   
   *app.py*
   
   ``` python
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
   ```
   
   ![image](https://raw.githubusercontent.com/hufe09/GitNote-Images/master/image_hosting/image.uri41s90i6d.png)


## 5. 加载静态文件
**url 链接：使用 `url_for(视图函数名称)` 可以反转成 url。**

1. 语法：`url_for('static',filename='路径')`
2. 静态文件，flask 会从 `static` 文件夹中开始寻找，所以不需要再写`static`这个路径了。
3. 可以加载 `css` 文件，可以加载 `js` 文件，还有 `image` 文件。
    ```html
    第一个：加载css文件
    <link rel="stylesheet" href="{{ url_for('static',filename='css/index.css') }}">
    第二个：加载js文件
    <script src="{{ url_for('static',filename='js/index.js') }}"></script>
    第三个：加载图片文件
    <img src="{{ url_for('static',filename='images/flask-icon.png') }}" alt="flask-icon">
    ```