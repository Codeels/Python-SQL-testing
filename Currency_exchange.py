import sqlite3

print('Создание БД exchanger')
print('Подключение к БД')
db = sqlite3.connect('exchanger.db')
cur = db.cursor()

print('Создание таблицы users_balance')
cur.execute("""
    CREATE TABLE IF NOT EXISTS users_balance(
    UserID INTEGER PRIMARY KEY,
    Balance_RUB INTEGER,
    Balance_USD INTEGER,
    Balance_EUR INTEGER);
""")
db.commit()

print('Добавление пользователя (100000, 1000, 1000)')
user_data = [100000, 1000, 1000]
cur.execute("""
INSERT INTO users_balance(Balance_RUB, Balance_USD, Balance_EUR)
VALUES (?, ?, ?)
""", user_data)
db.commit()

# функция для получения денег на счете
def get_money(currency):
    cur.execute(f'SELECT Balance_{currency} FROM users_balance')
    db.commit()
    result = cur.fetchall()
    result = list(*result)
    return float(result[0])

# функция для ввода изменений в БД
def exchange(currency1: str, amount1: float, currency2: str, amount2: float):
    balance1 = get_money(currency1)
    balance2 = get_money(currency2)
    cur.execute(f"UPDATE users_balance SET Balance_{currency1} = {balance1 + amount1} WHERE UserID = 1")
    cur.execute(f"UPDATE users_balance SET Balance_{currency2} = {balance2 - amount2} WHERE UserID = 1")
    db.commit()

# функция для расчета конвертации валют
def convert(currency1, amount, currency2):
    total = round(rate[f'{currency1}-{currency2}']*amount, 2)
    return float(total)

# функция для проверки правильности введенных данных в шагах 1 и 2
def check_value(something):
    if something not in [1, 2, 3]:
        print('Вы ввели неверное значение')
        exit()

# функция для проверки достаточности средств на счете при проведении операции конвертации
def balance_check(currency: str, amount: float):
    balance = get_money(currency)
    if amount > balance:
        print('На счете недостаточно средств для обмена')
        return False
    else:
        return True


rate = {'USD-RUB': 70, 'RUB-USD': 0.0142857, 'EUR-RUB': 80, 'RUB-EUR': 0.0125, 'USD-EUR': 0.87, 'EUR-USD': 1.15}
current = {1: 'RUB', 2: 'USD', 3: 'EUR'}

if __name__ == "__main__":
    print('Добро пожаловать в наш обменный пункт, курс валют следующий: '
          '\n1 USD = 70 RUB'
          '\n1 EUR = 80 RUB'
          '\n1 USD = 0,87 EUR'
          '\n1 EUR = 1,15 USD\n')
    try:
        first_step = int(input('Введите какую валюту желаете получить:'
                               '\n1 - RUB'
                               '\n2 - USD'
                               '\n3 - EUR\n'))
        check_value(first_step)
        cur1 = current.get(first_step)
        second_step = float(input('Какая сумма вас интересует?\n'))
        third_step = int(input('Какую валюту готовы предложить взамен?'
                               '\n1 - RUB'
                               '\n2 - USD'
                               '\n3 - EUR\n'))
        check_value(third_step)
        cur2 = current.get(third_step)
        if first_step == third_step:
            print('Невозможно произвести обмен одинаковых валют')
            exit()
        out = convert(cur1, second_step, cur2)
        if balance_check(cur2, out):
            exchange(cur1, second_step, cur2, out)
            print('Операция прошла успешно. Спасибо за пользование нашим банкоматом!')
            print(f'На вашем счету: {get_money("RUB")} RUB, {get_money("USD")} USD и {get_money("EUR")} EUR'
                  f'\nЕсли количество денег не сходится, не волнуйтесь - это комиссия ;)')
    except ValueError:
        print('Вы ввели неправильное значение')
        exit()

