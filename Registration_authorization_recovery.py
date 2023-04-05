import os
import sqlite3


# функция для создания таблицы users_data
def create_table():
    print('Создание таблицы users_data')
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users_data(
        UserID INTEGER PRIMARY KEY,
        Login TEXT,
        Password TEXT,
        Code INTEGER);
    """)
    db.commit()


# функция для добавления пользователя Ivan
def add_ivan():
    print('Добавление пользователя Ivan')
    user_credentials_ivan = ['Ivan', 'qwer1234', '1234']
    cur.execute("""
        INSERT INTO users_data(Login, Password, Code)
        VALUES (?, ?, ?);
    """, user_credentials_ivan)
    db.commit()


# функция для получения списка пользователей
def get_logins_list():
    cur.execute("""
    SELECT Login
    FROM users_data;
    """)
    result = cur.fetchall()
    result = list(set(result))
    result_norm = []
    for res in result:
        result_norm.extend(list(res))
    return result_norm


# функция для проверки корректности логина при регистрации
def check_login_registration(login):
    cur.execute(f"""SELECT Login FROM users_data WHERE Login = '{login}'""")
    if cur.fetchone() is not None:
        print('Логин уже используется')
        exit()
    elif len(login) == 0:
        print('Некорректный логин')
        exit()
    elif not isinstance(login, str):
        print('Некорректный логин')
        exit()
    else:
        print('Логин ОК')


# функция для проверки корректности логина при авторизации
def check_login_auth(login):
    cur.execute(f"""SELECT Login FROM users_data WHERE Login = '{login}'""")
    result = cur.fetchone()
    if len(login) == 0:
        print('Некорректный логин')
        exit()
    elif result is None:
        print('Пользователь с указанным логином не существует')
        exit()
    else:
        print('Логин ОК')


# функция для проверки корректности пароля
def check_password(password):
    if len(password) == 0:
        print('Некорректный пароль')
        exit()
    else:
        print('Пароль ОК')


# функция для проверки корректности кода при регистрации
def check_code_registration(code):
    if len(str(code)) == 0:
        print('Некорректный код')
        exit()
    elif not isinstance(code, int):
        print('Некорректный код')
        exit()
    else:
        print('Код ОК')


# функция для проверки корректности кода при смене пароля
def check_code_change(login, code):
    cur.execute(f"""SELECT Code FROM users_data WHERE Login = '{login}'""")
    result = cur.fetchone()[0]
    if len(code) == 0:
        print('Некорректный код')
        exit()
    elif int(result) != int(code):
        print('Код не подходит')
        exit()
    else:
        print('Код ОК')


# функция для регистрации
def registration(Login: str, Password: str, Code):
    user_credentials = [Login, Password, Code]
    if Login not in get_logins_list():
        cur.execute("""
            INSERT INTO users_data(Login, Password, Code)
            VALUES (?, ?, ?);
            """, user_credentials)
        db.commit()
        print('Регистрация прошла успешно')
    else:
        print('Данный логин уже используется')


# функция для авторизации
def login(Login: str, Password: str):
    user_credentials = [Login, Password]
    cur.execute("""
    SELECT *
    FROM users_data
    WHERE Login = ? and Password = ?;
    """, user_credentials)
    result = cur.fetchone()
    # print(result)
    if result is None:
        print('Комбинация логин/пароль некорректная')
    else:
        print('Авторизация прошла успешно')


# функция для смены пароля
def password_change(Login: str, Code, New_password: str):
    user_credentials = [New_password, Login, Code]
    if Login in get_logins_list():
        cur.execute("""
        UPDATE users_data
        SET Password = ?
        WHERE Login = ? and Code = ?;   
        """, user_credentials)
        db.commit()
        print('Пароль успешно изменен')
    else:
        print('Такого пользователя не существует')

def main_func():
    try:
        choice = int(input("Выберите желаемое действие по его номеру:"
                               "\n1 - регистрация нового пользователя"
                               "\n2 - авторизация в системе"
                               "\n3 - восстановление пароля по кодовому слову с заменой пароля\n"))
        if choice == 1:
            Login = str(input('Введите логин: '))
            check_login_registration(Login)
            Password = str(input('Введите пароль: '))
            check_password(Password)
            Code = int(input('Введите код для восстановления пароля (число): '))
            check_code_registration(Code)
            registration(Login, Password, Code)

        elif choice == 2:
            Login = str(input('Введите логин: '))
            check_login_auth(Login)
            Password = str(input('Введите пароль: '))
            login(Login, Password)

        elif choice == 3:
            Login = str(input('Введите логин: '))
            check_login_auth(Login)
            if Login in get_logins_list():
                Code = input('Введите код для восстановления пароля (число): ')
                check_code_change(Login, Code)
                New_password = str(input('Введите новый пароль: '))
                password_change(Login, Code, New_password)
            else:
                print('Такого пользователя не существует')

        else:
            print('Вы ввели неверный номер')

    except ValueError:
        print('Введено неверное значение')


if __name__ == "__main__":
    # вызов функций для создания и заполнения таблицы и запуска основой логики, если файл с БД не создан
    if os.path.isfile('registration.db') is False:
        print('Создание БД registration.db')
        print('Подключение к БД')
        db = sqlite3.connect('registration.db')
        cur = db.cursor()
        create_table()
        add_ivan()
        main_func()
    else:
        # если файл с БД есть, то происходит подключение к существующей БД
        print('Подключение к БД')
        db = sqlite3.connect('registration.db')
        cur = db.cursor()
        main_func()
