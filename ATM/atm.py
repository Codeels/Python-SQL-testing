from sql_query import SQL_atm


class ATM():

    def atm_logic(self):

        SQL_atm.create_table()

        # создаются пользователи для проверки программы
        SQL_atm.add_user((1234, 1111, 10000))
        SQL_atm.add_user((2345, 2222, 10000))

        number_card = str(input('Введите номер карты: '))

        while True:
            if SQL_atm.input_card(number_card):
                if SQL_atm.input_code(number_card):
                    SQL_atm.input_operation(number_card)
                    break
                else:
                    break
            else:
                break


if __name__ == "__main__":
    start = ATM()
    start.atm_logic()
