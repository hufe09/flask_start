from flask import g


def login_log():
    print(f"The user is {g.username}")


def login_ip_log():
    print(f"The login ip is {g.ip}")
