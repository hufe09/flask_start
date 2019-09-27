# 03 Flask 数据库

## 1. Mac 和 Windows 下数据库的安装：

1. Mysql为例
2. https://dev.mysql.com/downloads/mysql/
3. Mac上安装Mysql很简单，直接一顿下一步安装就可以了。
4. 设置初始化密码的命令是：
    ```
    mysqladmin -uroot password [password]
    ```
5. windows:
   
    * 如果没有安装.net Framework 4，就在那个提示框中，找到下载的url，下载下来，安装即可。
    * 如果没有安装Microsoft Visual C++ x64，那么就需要谷歌或者百度下载这个软件进行安装即可。

## 2. PyMSQL 中间件的介绍与安装

[PyMSQL](<<https://pymysql.readthedocs.io/en/latest/>>) 是一个Python MySQL客户端库。

**安装**

``` shell
$ pip install pymysql
```

## 3. Flask-SQLAlchemy
### 3.1 Flask-SQLAlchemy 介绍与安装

1. ORM：Object Relationship Mapping（模型关系映射）。
2. flask-sqlalchemy 是一套 ORM 框架。
3. ORM 的好处：可以让我们操作数据库跟操作对象是一样的，非常方便。因为一个表就抽象成一个类，一条数据就抽象成该类的一个对象。
4. 安装 `flask-sqlalchemy`：`sudo pip install flask-sqlalchemy`。

### 3.2 Flask-SQLAlchemy 使用
1. 初始化和设置数据库配置信息：
    * 使用 flask_sqlalchemy 中的 SQLAlchemy 进行初始化：
        ```
        from flask_sqlalchemy import SQLAlchemy
        app = Flask(__name__)
        db = SQLAlchemy(app)
        ```
2. 设置配置信息：在 `config.py` 文件中添加以下配置信息：
    ```
    # dialect+driver://username:password@host:port/database
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = 'root'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'flask_demo'

    SQLALCHEMY_DATABASE_URI = f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ```
    
3. 在主 `sql_app.py` 文件中，添加配置文件：
    ```
    app = Flask(__name__)
    app.config.from_object('config')
    db = SQLAlchemy(app)
    ```
4. 做测试，看有没有问题：
    ```
    db.create_all()
    ```
    如果没有报错，说明配置没有问题，如果有错误，可以根据错误进行修改。



### 3.3 使用 Flask-SQLAlchemy 创建模型与表的映射

1. 模型需要继承自 `db.Model`，然后需要映射到表中的属性，必须写成 `db.Column` 的数据类型。
2. 数据类型：
    * `db.Integer` 代表的是整形。
    * `db.String` 代表的是 `varchar`，需要指定最长的长度。
    * `db.Text` 代表的是 `text`。
3. 其他参数：
    * `primary_key`：代表的是将这个字段设置为主键。
    * `autoincrement`：代表的是这个主键为自增长的。
    * `nullable`：代表的是这个字段是否可以为空，默认可以为空，可以将这个值设置为 `False`，在数据库中，这个值就不能为空了。
4. 最后需要调用 `db.create_all()` 来将模型真正的创建到数据库中。

    *sql_app.py*

    ``` python
    # artical 表：
    # create table artical(
    #     id int primary key autoincrement,
    #     title varchar(100) not null,
    #     content text not null,
    # )

    class Article(db.Model):
        __tablename__ = "article"
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        title = db.Column(db.String(100), nullable=False)
        content = db.Column(db.Text, nullable=False)

    db.create_all()
    ```

    进入数据库查看建表结果：

    ```
    mysql> show tables;
    +----------------------+
    | Tables_in_flask_demo |
    +----------------------+
    | article              |
    +----------------------+
    1 row in set (0.00 sec)

    mysql> desc article;
    +---------+--------------+------+-----+---------+----------------+
    | Field   | Type         | Null | Key | Default | Extra          |
    +---------+--------------+------+-----+---------+----------------+
    | id      | int(11)      | NO   | PRI | NULL    | auto_increment |
    | title   | varchar(100) | NO   |     | NULL    |                |
    | content | text         | NO   |     | NULL    |                |
    +---------+--------------+------+-----+---------+----------------+
    3 rows in set (0.03 sec)
    ```



### 3.4 Flask-SQLAlchemy 数据的增、删、改、查：

1. 增：
    ```
    @app.route('/add/')
    def add_article():
        # add
        title = "Flask Start"
        content = "知了课堂，黄勇老师讲解。"
        article = Article(title=title, content=content)
        # 增加：
        db.session.add(article)
        # 事务
        db.session.commit()
    ```
2. 查：
    ```
    @app.route('/query/<id>')
    def query_article(id):
        result = Article.query.filter(Article.id == int(id)).all()
        if result:
            articles = f'Title: {result[0].title}, Content: {result[0].content}'
        return "<h1>Query.</h1>" + articles
    ```
3. 改：
    ```
    @app.route('/edit/<id>')
    def edit_article(id):
        # 1. 先把你要更改的数据查找出来
        result = Article.query.filter(Article.id == int(id)).first()
        if result:
            # 2. 把这条数据，你需要修改的地方进行修改
            result.title = "New flask start"
            # 3. 做事务的提交
            db.session.commit()
            articles = 'Edit success.'
            return "<h1>Edit.</h1>" + articles
    ```
4. 删：
    ```
    @app.route('/delete/<id>')
    def delete_article(id):
        # 1. 把需要删除的数据查找出来
        result = Article.query.filter(Article.id == int(id)).first()
        if result:
            # 2. 把这条数据删除掉
            db.session.delete(result)
            # 3. 做事务提交
            db.session.commit()
            articles = 'Delete success.'
            return "<h1>Delete.</h1>" + articles
    ```

### 3.5 Flask-SQLAlchemy 外键及其关系
1. 外键：
    ```
    class User(db.Model):
        __tablename__ = 'user'
        id = db.Column(db.Integer,primary_key=True,autoincrement=True)
        username = db.Column(db.String(100),nullable=False)

    class Article(db.Model):
        __tablename__ = 'article'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        title = db.Column(db.String(100),nullable=False)
        content = db.Column(db.Text,nullable=False)
        author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

        author = db.relationship('User',backref=db.backref('articles'))
    ```
2. `author = db.relationship('User',backref=db.backref('articles'))` 解释：
   
    * 给  `Article` 这个模型添加一个 `author` 属性，可以访问这篇文章的作者的数据，像访问普通模型一样。
* `backref` 是定义反向引用，可以通过 `User.articles` 访问这个模型所写的所有文章。
3. 多对多：
   
    *article_tag* ，此为文章和标签的中间表，进行关联文章和标签直接多对对的关系
    
    ``` python
    article_tag = db.Table('article_tag',
                           db.Column('article_id',
                                     db.Integer,
                                     db.ForeignKey("article.id"),
                                 ),
                           db.Column('tag_id',
                                     db.Integer,
                                 db.ForeignKey("tag.id"),
                                     )
                           )
    ```
    
    *artical Table*

    ``` python
    class Article(db.Model):
    __tablename__ = "article"
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
        author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
        
        author = db.relationship('User', backref=db.backref('articles'))
    
        tags = db.relationship('Tag', secondary=article_tag,
                               backref=db.backref('articles'))
    ```

    *tag Table*
    
    ``` python
    class Tag(db.Model):
        __tablename__ = 'tag'
        id = db.Column(db.Integer, primary_key=True, nullable=False)
        name = db.Column(db.String(100), nullable=False)
    ```

    * 多对多的关系，要通过一个中间表进行关联。
    * 中间表，不能通过 `class` 的方式实现，只能通过 `db.Table()` 的方式实现。
    * 设置关联：`tags = db.relationship('Tag',secondary=article_tag,backref=db.backref('articles'))` 需要使用一个关键字参数 `secondary=中间表` 来进行关联。
    * 访问和数据添加可以通过以下方式进行操作：
        - 添加数据：
            ```
            title = "Flask Start"
            content = "知了课堂，黄勇老师讲解。"
    
            article1 = Article(title=title, content=content, author_id=1)
            article2 = Article(title=title, content=content, author_id=2)
    
            tag1 = Tag(name='111')
            tag2 = Tag(name='222')
    
            article1.tags.append(tag1)
            article1.tags.append(tag2)
    
            article2.tags.append(tag1)
            article2.tags.append(tag2)
    
            db.session.add(article1)
            db.session.add(article2)
    
            db.session.add(tag1)
            db.session.add(tag2)
            
            db.session.commit()
            ```
        - 访问数据：
            ```
            @app.route('/query_tag/<id>')
            def query_tags(id):
                article1 = Article.query.filter(Article.id == int(id)).first()
                tags = article1.tags
                for tag in tags:
                    print(tag.name)
            ```



## 4. Flask-Script 的介绍与安装

1. Flask-Script：Flask-Script 的作用是可以通过命令行的形式来操作 Flask。例如通过命令跑一个开发版本的服务器、设置数据库，定时任务等。

2. 安装：首先进入到虚拟环境中，然后 `pip install flask-script` 来进行安装。

3. 如果直接在主 `manage.py` 中写命令，那么在终端就只需要 `python manage.py command_name` 就可以了。

4. 如果把一些命令集中在一个文件中，那么在终端就需要输入一个父命令，比如 `python manage.py db init`。

5. 例子：
   
    *manager.py*
    
    ```
    from flask_script import Manager
    from app import app
    from db_scripts import DBManager
    
    manager = Manager(app)
    
    @manager.command
    def runserver():
        print("Run Server.")
    
    if __name__ == "__main__":
        manager.run()
    ```
    
    执行效果：
    ```
    (flask_start) E:\Dropbox\flask_start>python manager.py runserver
    Run Server.
    ```
    
6. 有子命令的例子：

    *db_scripts.py*

    ```
    from flask_script import Manager
    
    DBManager = Manager()
    
    @DBManager.command
    def init():
    print("The database has been inited.")
    
    @DBManager.command
    def migrate():
        print("Databse migration successfuly.")
    ```

    在 *manager.py* 中加入下面两句

    ```
    from db_scripts import DBManage
    
    manager.add_command('db', DBManager)
    ```

    执行效果：

    ```
    (flask_start) E:\Dropbox\flask_start>python manager.py db init
    The database has been inited.
    
    (flask_start) E:\Dropbox\flask_start>python manager.py db migrate
    Databse migration successfuly.
    ```



## 5. 分开 `models` 以及解决循环引用

1. 分开 model s的目的：为了让代码更加方便的管理。
2. 如何解决循环引用：把 `db` 放在一个单独的文件中，切断循环引用的线条就可以了。

>本章节代码都在文件夹 *models_sep* 下面。

*models_sep/main_app.py*
``` python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Comment

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

db.create_all

@app.route("/")
def index():
    return "Models."

if __name__ == "__main__":
    app.run(
```

*models_sep/models.py*

```python
from main_app import db

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
```
执行 *models_sep/models_sep.py*，会有如下报错：
```
ImportError: cannot import name 'Comment' from 'models' (e:\Dropbox\flask_start\models_sep\models.py)
```

此问题由循环引用引起。

![image](https://raw.githubusercontent.com/hufe09/GitNote-Images/master/image_hosting/1569492526045.iun7mf36dn.png)

解决方式，将 db 放入第三方组件，供两者来调用。

![image](https://raw.githubusercontent.com/hufe09/GitNote-Images/master/image_hosting/1569492537456.om1uit31v7c.png)



新建 *models_sep/middle.py*

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

修改 *models_sep/main_app.py* ，移除 `from flask_sqlalchemy import SQLAlchemy`, 新增 `from middle import db` 以及初始化 db，`db.init_app(app)`

``` python
from flask import Flask
from models import Comment
from middle import db

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
```

修改 *models_sep/models.py*， 将 `db` 从 `main_app` 引入替换为从第三方 `middle` 引入。

```python
from middle import db

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
```

执行 *models_sep/main_app.py* 运行正常。



## 6. Flask-Migrate 的介绍与安装

1. 介绍：因为采用 `db.create_all()` 在后期修改字段的时候，不会自动的映射到数据库中，必须删除表，然后重新运行 `db.craete_all()` 才会重新映射，这样不符合我们的需求。因此 flask-migrate 就是为了解决这个问题，它可以在每次修改模型后，可以将修改的部分映射到数据库中。

2. 首先进入到你的虚拟环境中，然后使用 `pip install flask-migrate` 进行安装就可以了。

3. 使用 `flask_migrate` 必须借助 `flask_scripts`，这个包的 `MigrateCommand` 中包含了所有和数据库相关的命令。

4. `flask_migrate` 相关的命令：
   
    * `python manage.py db init`：初始化一个迁移脚本的环境，只需要执行一次。
    * `python manage.py db migrate`：将模型生成迁移文件，只要模型更改了，就需要执行一遍这个命令。
    * `python manage.py db upgrade`：将迁移文件真正的映射到数据库中。每次运行了 `migrate` 命令后，就记得要运行这个命令。
    * 模型  ->  迁移文件  ->  表
    
5. 注意点：需要将你想要映射到数据库中的模型，都要导入到 `manage.py` 文件中，如果没有导入进去，就不会映射到数据库中。如：`from models import Article`

6. 示例代码：
   
    > 本章节代码都在文件夹 *migrate_demo* 下面。
    
    *migrate_demo/manage.py*
    
    ```
    from flask_script import Manager
    from migrate_demo import app
    from flask_migrate import Migrate, MigrateCommand
    from exts import db
    from models import Article
    
    manager = Manager(app)
    
    # 1. 要使用flask_migrate，必须绑定app和db
    migrate = Migrate(app,db)
    
    # 2. 把MigrateCommand命令添加到manager中
    manager.add_command('db',MigrateCommand)
    
    if __name__ == '__main__':
        manager.run()
    ```
    
    *migrate_demo/migrate_demo.py*
    
    ``` python
    from flask import Flask
    from middle import db

    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)

    # 新建一个article模型，采用models分开的方式
    # flask-scrpts的方式
    
    #db.create_all()
    
    @app.route('/')
    def hello_world():
    return 'Hello World!'
    
    if __name__ == '__main__':
        app.run()
    ```
    
    如果运行 *migrate_demo/migrate_demo.py* 会有如下报错：
    
    ```
    RuntimeError: No application found. Either work inside a view function or push an application context. See http://flask-sqlalchemy.pocoo.org/contexts/.
    找不到应用程序。 在视图函数内部工作或推送应用上下文里面。
    ```
    这是因为应用程序未注册到实例里面。改为下面这样：
    
    ``` python
    with app.app_context():
        db.create_all()
    ```

    正如第一点所说，采用 `db.create_all()` 不方便修改数据库字段，必须删除表，才会重新映射所以采用 flask-migrate 解决这个问题。

7. 打开虚拟环境所在终端执行 `flask_migrate` 命令

    **python manage.py db init**

    ```
    (flask_start) E:\Dropbox\flask_start\migrate_demo>python manage.py db init
    Creating directory E:\Dropbox\flask_start\migrate_demo\migrations ...  done
    Creating directory E:\Dropbox\flask_start\migrate_demo\migrations\versions ...  done
    Generating E:\Dropbox\flask_start\migrate_demo\migrations\alembic.ini ...  done
    Generating E:\Dropbox\flask_start\migrate_demo\migrations\env.py ...  done
    Generating E:\Dropbox\flask_start\migrate_demo\migrations\README ...  done
    Generating E:\Dropbox\flask_start\migrate_demo\migrations\script.py.mako ...  done
    Please edit configuration/connection/logging settings in 'E:\\Dropbox\\flask_start\\migrate_demo\\migrations\\alembic.ini' before proceeding.
    ```

    **python manage.py db migrate**

    ```
    (flask_start) E:\Dropbox\flask_start\migrate_demo>python manage.py db migrate
    INFO  [alembic.runtime.migration] Context impl MySQLImpl.
    INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
    INFO  [alembic.autogenerate.compare] Detected added table 'article'
    Generating E:\Dropbox\flask_start\migrate_demo\migrations\versions\c63d9a39a8a3_.py ...  done
    ```

    多了一张 alembic_version 表。

    **python manage.py db upgrade**

    ```
    (flask_start) E:\Dropbox\flask_start\migrate_demo>python manage.py db upgrade
    INFO  [alembic.runtime.migration] Context impl MySQLImpl.
    INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
    INFO  [alembic.runtime.migration] Running upgrade  -> c63d9a39a8a3, empty message
    ```

    此时，article 表创建成功。

    在 Article 中添加字段 tag 后，执行 migrate 和 upgrade 后，数据库中就可以同步。

    ```
    # migrate 
    INFO  [alembic.autogenerate.compare] Detected added column 'article.tags'
    ...
    # upgrade 
    INFO  [alembic.runtime.migration] Running upgrade c63d9a39a8a3 -> bb5f4f515d1a, empty message
    ```

    alembic_version 表中，version_num列增加数据 bb5f4f515d1a。



