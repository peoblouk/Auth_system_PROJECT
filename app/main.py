"""
 * @author [Petr Oblouk]
 * @github [https://github.com/peoblouk]
 * @create date 15-05-2022 - 18:24:13
 * @modify date 15-05-2022 - 18:24:13
 * @desc [Auth system]
"""
from grpc import Status
from settings import *


# Main program
while True:
    db.connect()

    # You are logged out or not registred!
    if not auth.isLogin():
        gui.welcome_page()

    # You are logged in!
    elif auth.isLogin():
        gui.system_page()
