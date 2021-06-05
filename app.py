import traceback
import dbconnect


def new_exploit():
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_connection(conn)
    content = input("Write your new post here: ")
    cursor.execute("INSERT INTO exploits(content) VALUES(?)", [content, ])
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)


def user_login():
    while True:
        try:
            conn = dbconnect.get_db_connection()
            cursor = dbconnect.get_db_cursor(conn)
            username = input("Please enter your username: ")
            password = input("Please enter your password: ")
            cursor.execute(
                "SELECT alias FROM hackers WHERE alias = ? and password=?", [username, password])
            user = cursor.fetchall()
            if user == []:
                print("Sorry, that username/password combo is incorrect")
                continue
            else:
                for name in user:
                    print(f"Welcome {name[0]}!")
            break
        except:
            traceback.print_exc()
        dbconnect.close_db_cursor(cursor)
        dbconnect.close_db_connection(conn)


user_login()
