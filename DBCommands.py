import sqlite3


def tabular_output_rating(table):
    string_output = ''
    for element in table:
        string_output += f'[{element[0]}] {element[1]:20}{element[2]}\n'
    return string_output


def clear_SRV(server_id, message_id):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    query = f"""DELETE FROM Surveys WHERE server_id = {server_id} and message_id = {message_id}"""
    cursor.execute(query)
    DB.commit()
    DB.close()
    return 0


def set_SRV(server_id, server_name, message_id, message_text, results):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    query = f"""
                INSERT INTO Surveys(server_id, server_name, message_id, message_text, results)                            
                SELECT {server_id}, "{server_name}", {message_id}, "{message_text}", "{results}"
             """
    cursor.execute(query)
    DB.commit()
    DB.close()
    return 0


def show_SRV(server_id):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    try:
        query = f"""SELECT message_id FROM Surveys WHERE server_id = {server_id}"""
        cursor.execute(query)
        array = cursor.fetchall()

        output = []

        for element in array:
            output.append(element[0])
        return output
    except:
        return "Error in database"


def add_SRV(server_id, message_id, results):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    try:
        query = f"""UPDATE Surveys SET results = "{results}" WHERE server_id = {server_id} and message_id = {message_id}"""
        cursor.execute(query)
        DB.commit()
        DB.close()
        return 0
    except:
        return 1


def get_SRV(server_id, message_id):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    try:
        query = f"""SELECT results FROM Surveys WHERE server_id = {server_id} and message_id = {message_id}"""
        cursor.execute(query)
        array = cursor.fetchall()

        return array[0][0]
    except:
        return []


def get_BigBrother(server_id):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    try:
        query = f"""SELECT user_id, rating FROM BigBrother WHERE server_id = {server_id}"""
        cursor.execute(query)
        array = cursor.fetchall()

        rating = {}

        for element in array:
            rating.update({int(element[0]): int(element[1])})

        DB.commit()
        DB.close()
        return rating
    except:
        return 1


def get_Ranks(server_id):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    try:
        query = f"""SELECT role_id, rating_lower, rating_upper FROM Ranks WHERE server_id = {server_id}"""
        cursor.execute(query)
        array = cursor.fetchall()

        roles = {}

        for element in array:
            roles.update({int(element[0]): (int(element[1]), int(element[2]))})

        DB.commit()
        DB.close()
        return roles
    except:
        return 1


def db_create():
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    script_create_R = """
                        CREATE TABLE IF NOT EXISTS BigBrother(
                            user_id INTEGER,
                            user_name TEXT,
                            server_id INTEGER,
                            server_name TEXT,
                            rating INTEGER)
                      """
    cursor.execute(script_create_R)

    script_create_L = """ 
                        CREATE TABLE IF NOT EXISTS RatingLogs(
                            type TEXT,
                            time REAL,
                            date TEXT,
                            user_id INTEGER,
                            user_name TEXT,
                            server_id INTEGER,
                            server_name TEXT,
                            value INTEGER)
                      """
    cursor.execute(script_create_L)

    script_create_C = """
                        CREATE TABLE IF NOT EXISTS WorkingDirectory(
                            server_id INTEGER,
                            server_name TEXT,
                            console_id INTEGER,
                            log_id INTEGER,
                            info_id INTEGER)    
    """
    cursor.execute(script_create_C)

    script_create_D = """
                        CREATE TABLE IF NOT EXISTS Ranks(
                            server_id INTEGER,
                            server_name TEXT,
                            key INTEGER,
                            role_id INTEGER,
                            role_name INTEGER,
                            rating_lower INTEGER,
                            rating_upper INTEGER)
                      """
    cursor.execute(script_create_D)

    script_create_S = """
                        CREATE TABLE IF NOT EXISTS Surveys(
                            server_id INTEGER,
                            server_name TEXT,
                            message_id INTEGER,
                            message_text TEXT,
                            results TEXT)
                        """
    cursor.execute(script_create_S)

    DB.commit()
    DB.close()


def RatingModule_SetAutoRoles(server_id, server_name, key, role_id, role_name, rating_lower, rating_upper):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    try:
        query = f"""INSERT INTO Ranks(server_id, server_name, key, role_id, role_name, rating_lower, rating_upper)
                    SELECT {server_id}, '{server_name}', {key}, {role_id}, '{role_name}', {rating_lower}, {rating_upper}
                    WHERE NOT EXISTS(SELECT 1 FROM Ranks WHERE server_id = {server_id} and key = {key});
                 """
        cursor.execute(query)

        query = f"""UPDATE Ranks 
                    SET server_name = '{server_name}', role_id = {role_id}, role_name = '{role_name}', rating_lower = {rating_lower}, rating_upper = {rating_upper} 
                    WHERE server_id = {server_id} and key = {key};
                 """
        cursor.execute(query)

        DB.commit()
        DB.close()
        return 0
    except:
        with Exception as error:
            print(error)
        return 1


def RatingModule_ClearAutoRoles(server_id, key):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    try:
        query = f"""DELETE FROM Ranks WHERE server_id = {server_id} and key = {key}"""
        cursor.execute(query)

        DB.commit()
        DB.close()
        return 0
    except:
        return 1


def RatingModule_ShowAutoRoles(server_id):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    try:
        query = f"""SELECT * FROM Ranks WHERE server_id = {server_id}"""
        cursor.execute(query)
        array = cursor.fetchall()

        output = ""

        for element in array:
            output += f"{element[2]}) [{element[3]}| {element[4]}] [{element[5]}:{element[6]}]\n"

        return output
    except:
        return "Error in database"


def RatingModule_NewUser(user_id, user_name, server_id, server_name, value):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    try:
        query = f"""INSERT INTO BigBrother(user_id, user_name, server_id, server_name, rating)
                    SELECT {user_id}, '{user_name}', {server_id}, '{server_name}', {value}
                    WHERE NOT EXISTS(SELECT 1 FROM BigBrother WHERE user_id = {user_id} and server_id = {server_id});"""
        cursor.execute(query)

        query = f"""UPDATE BigBrother SET user_name = '{user_name}', server_name = '{server_name}' WHERE user_id = {user_id} and server_id = {server_id};"""
        cursor.execute(query)

        DB.commit()
        DB.close()
        return 0
    except:
        with Exception as error:
            print(error)
        return 1


def DirectoryModule_SetDirectory(server_id, server_name, console_id, log_id, info_id):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    try:
        query = f"""INSERT INTO WorkingDirectory(server_id, server_name, console_id, log_id, info_id)
                    SELECT {server_id}, '{server_name}', {console_id}, {log_id}, {info_id}
                    WHERE NOT EXISTS(SELECT 1 FROM WorkingDirectory WHERE server_id = {server_id})"""
        cursor.execute(query)

        query = f"""UPDATE WorkingDirectory SET console_id = {console_id}, log_id = {log_id}, info_id = {info_id} WHERE server_id = {server_id};"""
        cursor.execute(query)

        DB.commit()
        DB.close()
    except:
        with Exception as error:
            print(error)
        return 1


def DirectoryModule_ShowDirectory(server_id):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    try:
        query = f"""SELECT console_id, log_id, info_id FROM WorkingDirectory WHERE server_id = '{server_id}';"""
        cursor.execute(query)
        ids = cursor.fetchall()[0]

        return ids
    except:
        with Exception as error:
            print(error)
        return 1


def RatingModule_SetRating(user_id, server_id, value):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    try:
        query = f"""UPDATE BigBrother SET rating = {value} WHERE user_id = {user_id} and server_id = {server_id};"""
        cursor.execute(query)

        DB.commit()
        DB.close()
        return 0
    except:
        with Exception as error:
            print(error)
        return 1


def RatingModule_AddRating(user_id, server_id, value):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    try:
        query = f"""SELECT rating FROM BigBrother WHERE user_id = {user_id} and server_id = {server_id};"""
        cursor.execute(query)
        current_rating = cursor.fetchall()[0][0]

        query = f"""UPDATE BigBrother SET rating = {current_rating + value} WHERE user_id = {user_id} and server_id = {server_id};"""
        cursor.execute(query)

        DB.commit()
        DB.close()
        return 0
    except:
        with Exception as error:
            print(error)
        return 1


def RatingModule_ShowServerRating(user_id, server_id):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    try:
        if user_id == '*':
            query = f"""SELECT user_id, user_name, rating FROM BigBrother WHERE server_id = {server_id};"""
            cursor.execute(query)
            current_rating = cursor.fetchall()
            DB.commit()
            DB.close()
            return tabular_output_rating(current_rating)
        else:
            query = f"""SELECT rating FROM BigBrother WHERE user_id = {user_id} and server_id = {server_id};"""
            cursor.execute(query)
            current_rating = cursor.fetchall()[0][0]
            DB.commit()
            DB.close()
            return f"{user_id}: {current_rating}"
    except:
        with Exception as error:
            print(error)
        return f'Пользователя с [{user_id}] не найдено'


def RatingModule_ShowUserRating(server_id, user_id):
    DB = sqlite3.connect('server.db')
    cursor = DB.cursor()

    try:
        query = f"""SELECT rating FROM BigBrother WHERE user_id = {user_id} and server_id = {server_id};"""
        cursor.execute(query)
        current_rating = cursor.fetchall()[0][0]
        DB.commit()
        DB.close()
        return current_rating
    except:
        with Exception as error:
            print(error)
        return -1000


if __name__ == "__main__":
    pass
