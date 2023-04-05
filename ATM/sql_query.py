import csv
import datetime
import os
import sqlite3

now_date = datetime.datetime.utcnow().strftime('%H:%M:%S-%d.%m.%Y')


class SQL_atm:
    """Создание таблицы Users_data"""

    @staticmethod
    def create_table():
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Users_data(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Number_card INTEGER NOT NULL,
            Pin_code INTEGER NOT NULL,
            Balance INTEGER NOT NULL);""")
            print('Создание таблицы Users_data')

    """Создание нового пользователя"""

    @staticmethod
    def add_user(data_users):
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute("""INSERT INTO Users_data (Number_card, Pin_code, Balance)
                        VALUES(?, ?, ?)""", data_users)
            print('Создание нового пользователя')

    """Ввод и проверка карты"""

    @staticmethod
    def input_card(number_card):
        try:
            with sqlite3.connect('atm.db') as db:
                cur = db.cursor()
                cur.execute(f"""SELECT Number_card FROM Users_data WHERE Number_card = {number_card}""")
                result_card = cur.fetchone()
                if result_card is None:
                    print('Введен неизвестный номер карты')
                    return False
                else:
                    print(f'Введен номер карты: {number_card}')
                    return True
        except:
            print('Введен неизвестный номер карты')

    """Ввод и проверка пин-кода"""

    @staticmethod
    def input_code(number_card):
        pin_code = input('Введите пин-код карты: ')
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Pin_code FROM Users_data WHERE Number_card = {number_card}""")
            result_code = cur.fetchone()
            input_pin = result_code[0]
            try:
                if int(input_pin) == int(pin_code):
                    print('Введен верный пин-код')
                    return True
                else:
                    print('Введен неверный пин-код')
                    return False
            except:
                print('Введен неверный пин-код')
                return False

    """Вывод на экран баланса карты"""

    @staticmethod
    def info_balance(number_card):
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {number_card}""")
            result_info_balance = cur.fetchone()
            balance_card = result_info_balance[0]
            # print(f'Баланс вашей карты: {balance_card}')
            return balance_card

    """Снятие денежных средств с баланса карты"""

    @staticmethod
    def withdraw_money(number_card):
        amount = input('Введите сумму, которую желаете снять: ')

        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {number_card}""")
            result_info_balance = cur.fetchone()
            balance_card = result_info_balance[0]
            try:
                if int(amount) <= 0:
                    print('Некорректная сумма')
                    return False
                if int(amount) > balance_card:
                    print('На вашей карте недостаточно средств')
                    return False
                else:
                    cur.execute(f"""UPDATE Users_data SET Balance = Balance - {amount} WHERE Number_card = {number_card};""")
                    db.commit()
                    print(f'Баланс вашей карты: {SQL_atm.info_balance(number_card)}')
                    SQL_atm.report_operation_1(now_date, number_card, '1', amount, '')
                    return True
            except:
                print('Некорректное действие')
                return False


    """Внесение денежных средств"""

    @staticmethod
    def deposition_money(number_card):
        amount = input('Введите сумму, которую желаете внести: ')
        with sqlite3.connect('atm.db') as db:
            try:
                if int(amount) <= 0:
                    print('Некорректная сумма')
                    return False
                cur = db.cursor()
                cur.execute(f"""UPDATE Users_data SET Balance = Balance + {amount} WHERE Number_card = {number_card};""")
                db.commit()
                print(f'Баланс вашей карты: {SQL_atm.info_balance(number_card)}')
                SQL_atm.report_operation_1(now_date, number_card, '2', amount, '')
            except:
                print('Некорректное действие')
                return False

    """Перевод денег между счетами"""
    @staticmethod
    def transfer_money(number_card):
        receiver_card = input('Введите номер карты получателя: ')
        if receiver_card == number_card:
            print('Вы не можете перевести деньги самому себе')
            return False


        with sqlite3.connect('atm.db') as db:
            try:
                cur = db.cursor()
                cur.execute(f"""SELECT Number_card FROM Users_data WHERE Number_card = {receiver_card}""")
                result = cur.fetchone()
                if result is None:
                    print('Введен неизвестный номер карты')
                    return False
                else:
                    amount = input('Введите сумму, которую желаете перевести: ')
                    try:
                        amount = int(amount)
                    except ValueError:
                        print('Неверно введена сумма')
                    if int(amount) <= 0:
                        print('Некорректная сумма')
                        return False
                    if int(amount) <= int(SQL_atm.info_balance(number_card)) and (int(amount)>0):

                        cur.execute(
                            f"""UPDATE Users_data SET Balance = Balance - {amount} WHERE Number_card = {number_card};""")
                        cur.execute(
                            f"""UPDATE Users_data SET Balance = Balance + {amount} WHERE Number_card = {receiver_card};""")
                        db.commit()
                        print(f'Баланс вашей карты: {SQL_atm.info_balance(number_card)}')
                        SQL_atm.report_operation_1(now_date, number_card, '3', amount, '')
                        SQL_atm.report_operation_2(now_date, receiver_card, '3', amount, number_card)
                    else:
                        print('Недостаточно средств для совершения операции')
            except:
                print('Некорректное действие')
                return False


    """Выбор операции"""

    @staticmethod
    def input_operation(number_card):
        while True:
            operation = input('\nВведите желаемое действие:'
                              '\n1 - Узнать баланс'
                              '\n2 - Снять денежные средства'
                              '\n3 - Внести денежные средства'
                              '\n4 - Завершить работу'
                              '\n5 - Перевести денежные средства\n')
            if operation == '1':
                print(f'Баланс вашей карты: {SQL_atm.info_balance(number_card)}')
            elif operation == '2':
                SQL_atm.withdraw_money(number_card)
            elif operation == '3':
                SQL_atm.deposition_money(number_card)
            elif operation == '4':
                print('Работа завершена')
                # return False
                exit()
            elif operation == '5':
                SQL_atm.transfer_money(number_card)
            else:
                print('Неверный ввод. Попробуйте ещё раз')

    """Отчет об операциях"""

    @staticmethod
    def report_operation_1(now_date, number_card, type_operation, amount, payee):
        rows_name = [('Date', 'Number_card', 'Type_operation', 'Amount', 'Payee')]
        user_data = [(now_date, number_card, type_operation, amount, payee)]

        # если операция совершается впервые (файла с отчетом до этого не было),
        # то создается файл с необходимыми названиями столбцов и данными
        if os.path.isfile('report_1.csv') is False:
            with open('report_1.csv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerows(
                    rows_name
                )
                writer.writerows(
                    user_data
                )
        # если файл с отчетом уже есть, то производится запись только данных
        else:
            with open('report_1.csv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerows(
                    user_data
                )

        print('Данные внесены в отчет')


    """Отчет об операциях для 7.11"""

    @staticmethod
    def report_operation_2(now_date, payee, type_operation, amount, number_card):
        rows_name = [('Date', 'Payee', 'Type_operation', 'Amount', 'Sender')]
        user_data = [(now_date, payee, '3', amount, number_card)]

        # если операция совершается впервые (файла с отчетом до этого не было),
        # то создается файл с необходимыми названиями столбцов и данными
        if os.path.isfile('report_2.csv') is False:
            with open('report_2.csv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerows(
                    rows_name
                )
                writer.writerows(
                    user_data
                )
        # если файл с отчетом уже есть, то производится запись только данных
        else:
            with open('report_2.csv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerows(
                    user_data
                )


"""
Type_operation

1 - снятие денег
2 - внесение денег
3 - перевод денег

"""

