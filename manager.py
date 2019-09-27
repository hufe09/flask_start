from flask_script import Manager
from app import app
from db_scripts import DBManager


manager = Manager(app)


@manager.command
def runserver():
    print("Run Server.")


manager.add_command('db', DBManager)


if __name__ == "__main__":
    manager.run()
