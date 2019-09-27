from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

#  # article_tag Table
#  create table article_tag(
#      article_tag int,
#      tag_id int ,
#      primary key (`article_id`, `tag_id`),
#      foreigin key `article_id` references `article.id`,
#      foreigin key `tage_id` references `tag.id`,

#  )

# 中间表，实现多对多
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


# artical Table：
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
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 反向引用
    author = db.relationship('User', backref=db.backref('articles'))
    # 通过这条语句，查询该作者写过的所有文章。
    # author.articles

    tags = db.relationship('Tag', secondary=article_tag,
                           backref=db.backref('articles'))

# user Table
# create table user(
#     id int primary key autoincrement,
#     user_name verchar(100) not null,
# )


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # # tag Table
    # create table tag(
    #     id int primary key autoincrement,
    #     name varchar(50) not null,
    #  )


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)


db.create_all()


# 增
@app.route('/add_article/')
def add_article():
    # add
    title = "Flask Start"
    content = "知了课堂，黄勇老师讲解。"
    article_1 = Article(title=title, content=content, author_id=1)
    db.session.add(article_1)
    # transaction
    db.session.commit()
    article_1 = f'Title: {title}, Content: {content}'
    return "<h1>Add</h1> An article has been added to the database.<br>" \
        + article_1


# 查
@app.route('/query/<id>')
def query_article(id):
    result = Article.query.filter(Article.id == int(id)).all()
    if result:
        article_1 = f'Title: {result[0].title}, Content: {result[0].content}'
    else:
        article_1 = 'No result.'
    return "<h1>Query.</h1>" + article_1


# 改
@app.route('/edit/<id>')
def edit_article(id):
    result = Article.query.filter(Article.id == int(id)).first()
    if result:
        result.title = "New flask start"
        db.session.commit()
        article_1 = 'Edit success.'
        return "<h1>Edit.</h1>" + article_1
    else:
        article_1 = 'Edit failed.'
    return "<h1>Edit.</h1>" + article_1


# 删
@app.route('/delete/<id>')
def delete_article(id):
    result = Article.query.filter(Article.id == int(id)).first()
    print(result)
    if result:
        db.session.delete(result)
        db.session.commit()
        article_1 = 'Delete success.'
        return "<h1>Delete.</h1>" + article_1
    else:
        article_1 = 'Delete failed.'
    return "<h1>Delete.</h1>" + article_1


@app.route('/add_user/<name>')
def add_user(name):
    # add
    user_name = name
    password = "flask password"
    user = User(user_name=user_name, password=password)
    db.session.add(user)
    # transaction
    db.session.commit()
    return f"<h1>Add User</h1> {name}"


@app.route('/query_user/<id>')
def query_user(id):
    result = Article.query.filter(Article.id == int(id)).first()
    if result:
        # 这样写步骤很多，很麻烦
        # author_id = result.author_id
        # query_user = User.query.filter(User.id == user_id).first()
        # user_name = query_user.user_name

        # 反向引用，会简洁很多
        user_name = result.author.user_name
        user_id = result.author.id

        # 通过作者找到他的所有文章
        user = User.query.filter(User.id == user_id).first()
        articles = user.articles
        pots = '<br>'
        for article in articles:
            pots += article.title + "&nbsp" * 4
            pots += article.content + '<br>'

    else:
        user_name = 'No result.'
    return f"<h1>Query user.</h1> User Name: {user_name} {pots}"


@app.route('/add_article_tag/')
def add_article_tag():
    # add
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

    return 'Success.'


@app.route('/query_tag/<id>')
def query_tags(id):
    result = Article.query.filter(Article.id == int(id)).first()
    if result:
        tags = result.tags
        str = '<br>'
        for tag in tags:
            str += tag.name + "&nbsp" * 4
    return f"<h1>Query tags.</h1> Tags: {str}"


if __name__ == '__main__':
    app.run()
