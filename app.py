import traceback
import dbconnect


def user_login(alias, password):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    while True:
        try:
            # this ensures the username and password match in the database for a valid login
            cursor.execute(
                "SELECT alias FROM hackers h WHERE alias = ? and password=?", [alias, password])
            # if user comes back empty, that means the password/alias didn't match in DB
            user = cursor.fetchall()
            if user == []:
                print("Sorry, that username/password combo is incorrect \n")
                return False
                # continue
            # if not empty, there was a match. this greets them
            else:
                for name in user:
                    print(f"Hello {name[0]}!")
                return True
        except KeyboardInterrupt:
            traceback.print_exc()
            break
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)


def user_signup(alias, password):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    cursor.execute(
        "SELECT * FROM hackers h WHERE h.alias = ? AND h.password = ?", [alias, password])
    selected_data = cursor.fetchall()
    if selected_data != []:
        print("That username is unavailable. Try again")
        return False
    else:
        print("New account created!")
        cursor.execute("INSERT INTO hackers(alias, password) VALUES(?, ?)", [
            alias, password])
        conn.commit()

    # print("New account created!")
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)


def new_exploit(user_id):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    content = input("Write your new post here: ")
    # user_id = cursor.execute(
    #     "SELECT id FROM hackers WHERE alias = ?", [alias, ])
    cursor.execute(
        "INSERT INTO exploits (content, user_id) VALUES(?, ?)", [content, user_id])
    conn.commit()
    print("You did it! That was mean and you should be ashamed of yourself \n")
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)

# def mod_exploit(user_id):


def see_your_exploits(user_id):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    # where user_id in the system is the same as current user's id
    cursor.execute(
        "SELECT content FROM exploits e WHERE user_id = ?", [user_id, ])
    print("Your exploits: ")
    # prints out the tuples nicely
    for exploits in cursor.fetchall():
        print(f"    - {exploits[0]}")
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)


def see_all_exlpoits(user_id):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    # where user_id is not current user's user_id
    cursor.execute(
        "SELECT h.alias, e.content FROM exploits e INNER JOIN hackers h on h.id = e.user_id WHERE e.user_id != ?", [
            user_id, ]
    )

    for exploits in cursor.fetchall():
        print(f"Alias: {exploits[0]}\nContent: {exploits[1]} \n")
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)


while True:
    welcome_selection = int(input(
        "Welcome! Choose from the following options: \n 1. Login \n 2. Sign Up \n Selection: "))
    # login info
    alias = input("Please enter your alias: ")
    password = input("Please enter your password: ")
    # want to make this only prompt for alias/password not selection again?
    if welcome_selection == 1:
        if user_login(alias, password) == False:
            continue
        else:
            break
    elif welcome_selection == 2:
        if user_signup(alias, password) == False:
            continue
        else:
            break
    else:
        print("Invalid selection")
        continue
    break

while True:
    try:
        # need these to access user_id
        conn = dbconnect.get_db_connection()
        cursor = dbconnect.get_db_cursor(conn)

        # this is just to get the user_id to use in other functions later on
        cursor.execute(
            "SELECT h.id FROM hackers h WHERE h.alias = ?", [alias, ])
        for user_id in cursor.fetchall():
            user_id = user_id[0]

        selection = int(input(
            "Please select from the following options: \n1. Exploit someone lol \n2. View your exploits \n3. View others' exploits \n4. Exit \nSelection: "))
        if selection == 1:
            new_exploit(user_id)
            continue
        elif selection == 2:
            see_your_exploits(user_id)
            continue
        elif selection == 3:
            see_all_exlpoits(user_id)
            continue
        elif selection == 4:
            print("Later gator!")
            break
        else:
            print("Please select a valid number \n")
            continue
    except KeyboardInterrupt:
        break
    except:
        print("Sorry, something went wrong")
        traceback.print_exc()
        dbconnect.close_db_cursor(cursor)
        dbconnect.close_db_connection(conn)
