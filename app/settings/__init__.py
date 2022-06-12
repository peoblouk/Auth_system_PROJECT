"""
 * @author [Petr Oblouk]
 * @github [https://github.com/peoblouk]
 * @create date 15-05-2022 - 18:23:21
 * @modify date 15-05-2022 - 18:23:21
 * @desc [Functions for managing accounts]
"""
import hashlib
import os
from pickle import TRUE
import sqlite3
import time as t

#########################################################################################
class Database:
    # This function will connect you to database and set cursor
    def connect(self):
        # Control if file exists
        global c
        global conn
        if os.path.exists("app/settings/accounts.db"):
            conn = sqlite3.connect("app/settings/accounts.db")
            c = conn.cursor()

        else:
            conn = sqlite3.connect("app/settings/accounts.db")
            c = conn.cursor()
            c.execute(
                """CREATE TABLE accounts
                    (username text, hash_user text, firstname text, lastname text, num text, role text) """
            )


#########################################################################################
class Auth:
    status = False
    admin = False

    #######################################################################
    def isLogin(self):
        return self.status

    #######################################################################
    def isAdmin(self):
        return self.admin

    #######################################################################
    # This function create new login for new user
    def register(self):
        global username
        try:
            username = input("Enter your username > ")
        except SyntaxError:
            print("In your name there are spaces which aren't allowed!")

        password = input("Enter your password > ")
        confirm_password = input("Enter your password again > ")

        if password == confirm_password:
            encode = password.encode()
            hash_user = hashlib.md5(encode).hexdigest()

            # Another informations about user
            role = "user"

            user_fname = input("Enter your first name > ")
            user_lname = input("Enter your last name > ")
            try:
                user_num = int(input("Add your number > "))
            except ValueError:
                print("Telephone number must contain numbers !")
                user_num = "-"
            finally:
                # save this information to database
                c.execute(
                    "INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?)",
                    [
                        username,
                        hash_user,
                        user_fname,
                        user_lname,
                        user_num,
                        role,
                    ],
                )
                conn.commit()

                print("You've registered successfully!")
                self.status = True

        else:
            print("Password isn't same as above! \n")
            self.status = False
        return self.status

    #######################################################################
    # This function will logout you from system
    def logout(self):
        print("You've sucessfully logout")
        self.status = False
        print("######################")
        return self.status

    #######################################################################
    # This function help you to change your password
    def change_password(self):
        password = input("Enter your new password > ")
        confirm_password = input("Enter your password again > ")
        if password == confirm_password:
            encode = password.encode()
            hash_user = hashlib.md5(encode).hexdigest()
            c.execute(
                """UPDATE accounts SET hash_user = ? WHERE username = ?""",
                [hash_user, username],
            )
            conn.commit()
        else:
            print("Try again, new password isn't match")

    #######################################################################
    # This function control admin permissions
    def control_role(self):
        c.execute("""SELECT * FROM accounts WHERE username = ? """, [username])
        items = c.fetchall()
        for item in items:
            if item[5] == "admin":
                print("You're logged in as admin")
                self.admin = True
                auth.isAdmin = True
            else:
                print("You're logged in as user")
                self.admin = False
                auth.isAdmin = False

        return self.admin

    #######################################################################
    # This function helps to user to login to system
    def login(self):
        global username
        try:
            username = input("Enter your username > ")
        except SyntaxError:
            print("In your name there are spaces, which aren't allowed!")

        password = input("Enter your password > ")

        auth = password.encode()
        auth_hash = hashlib.md5(auth).hexdigest()
        # take a look into database
        c.execute(
            "SELECT * FROM accounts WHERE username = ? and hash_user = ?",
            [username, auth_hash],
        )
        # if username and password was found in database login
        if c.fetchone() == None:
            print("Incorrect credentials")
            self.status = False

        else:
            print("Logged in!")
            self.status = True
        return self.status


#########################################################################################
class Gui(Auth):
    # This function generate menu
    def welcome_page(self):
        print("Type in log - for login\n or reg - for register\n")
        user_select = input("Enter select > ")
        user_select.strip()
        if user_select == "reg":
            auth.register()
        elif user_select == "log":
            auth.login()
        elif user_select == "exit":
            raise SystemExit()
        else:
            print("There is no function for this! Try to select another one")

    #######################################################################
    def wait(self):
        t.sleep(0.5)

    #######################################################################
    def system_page(self):
        print("###################")
        gui.wait()
        print("\nWelcome in system")
        auth.control_role()
        print("select from menu >\n")
        print("logout - to logout from system")
        print("chpassword - to change password\n")

        # If you will login as Admin this will print
        if auth.isAdmin == True:
            gui.wait()
            print("##################")
            print("Admins permissions")
            print("view - print everything database")
            print("chrole - change admin to user")
            print("setpasswordfor - set passworrd for somebody")

        user_select = input("select > ")
        if user_select == "view":
            admin.view()

        elif user_select == "chrole":
            admin.change_role()

        elif user_select == "chpassword":
            auth.change_password()

        elif user_select == "setpasswordfor":
            admin.set_for_user()

        elif user_select == "logout":
            auth.logout()

        elif user_select == "exit":
            raise SystemExit()
        else:
            print("Try it again !")


#########################################################################################
class Admin:
    # This function is to view accounts, while you are logged in as admin
    def view(self):
        if auth.isAdmin:
            c.execute("SELECT * FROM accounts")
            items = c.fetchall()
            print("¦ username ¦ hash_user ¦ firstname ¦ lastname ¦ number ¦ role ¦")

            for item in items:
                print(
                    f"¦{item[0]} ¦ {item[1]} ¦ {item[2]} ¦ {item[3]} ¦ {item[4]} ¦ {item[5]}¦ "
                )
        else:
            print("You don't have permissions !")

    #######################################################################
    # This function is to change role
    def change_role(self):
        if auth.isAdmin == True:
            #
            username = input("Enter username > ")
            c.execute("SELECT * FROM accounts WHERE username = ?", [username])
            # if username and password was found in database login
            gui.wait()
            if c.fetchone() == None:
                print("User isn't in database !")

            else:
                #
                # Print informations about user, which you select
                c.execute("""SELECT * FROM accounts WHERE username = ? """, [username])
                items = c.fetchall()
                print(
                    "¦ username ¦ hash_user ¦ firstname ¦ lastname ¦ number ¦ role ¦ "
                )
                for item in items:
                    print(
                        f"¦{item[0]} ¦ {item[1]} ¦ {item[2]} ¦ {item[3]} ¦ {item[4]} ¦ {item[5]}¦ "
                    )
                user_select = input("change role to > ")

                if user_select == "admin":
                    role = "admin"
                    c.execute(
                        """UPDATE accounts SET role = ? WHERE username = ?""",
                        [role, username],
                    )
                    conn.commit()

                elif user_select == "user":
                    role = "user"
                    c.execute(
                        """UPDATE accounts SET role = ? WHERE username = ?""",
                        [role, username],
                    )
                    conn.commit()

                else:
                    print("You select inccorect role !")
            #
        else:
            print("You don't have permissions !")
        ##

    #######################################################################
    # This function help you to change your password (you msut have admin permissions)
    def set_for_user(self):
        if auth.isAdmin == True:
            username = input("Enter username > ")
            c.execute("SELECT * FROM accounts WHERE username = ?", [username])
            # if username and password was found in database login
            gui.wait()
            if c.fetchone() == None:
                print("User isn't in database !")

            else:
                #
                # Print informations about user, which you select
                c.execute("""SELECT * FROM accounts WHERE username = ? """, [username])
                items = c.fetchall()
                print(
                    "¦ username ¦ hash_user ¦ firstname ¦ lastname ¦ number ¦ role ¦ "
                )

                for item in items:
                    print(
                        f"¦{item[0]} ¦ {item[1]} ¦ {item[2]} ¦ {item[3]} ¦ {item[4]} ¦ {item[5]}¦ "
                    )
                password = input("Enter your new password > ")
                confirm_password = input("Enter your password again > ")
                if password == confirm_password:
                    encode = password.encode()
                    hash_user = hashlib.md5(encode).hexdigest()
                    c.execute(
                        """UPDATE accounts SET hash_user = ? WHERE username = ?""",
                        [hash_user, username],
                    )
                    conn.commit()
                else:
                    print("Try it again, new password isn't match")
        else:
            print("You don't have permissions for that !")


#########################################################################################


# Define macros
auth = Auth()
admin = Admin()
gui = Gui()
db = Database()
