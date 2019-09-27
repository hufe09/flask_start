from flask_script import Manager

DBManager = Manager()


@DBManager.command
def init():
    print("The database has been inited.")


@DBManager.command
def migrate():
    print("Databse migration successfuly.")
