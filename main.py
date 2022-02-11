import datetime as dt


class Record:
    # так как date все равно будет обрабатываться, тут лучше не использовать "пустой" аргумент 
    # по умолчанию,, а сделать его необязательным date=None
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # такое конструкции с переносами не читабельны, их надо избегать
        # здесь лучше массивное и сложное определение даты вынести в отдельный метод класса, 
        # а аргументы присваивать уже результат, например, self.date = __get_record_date(date) 
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # стиль CamelCase используется в наименовании класса, но при работе с его объектами
        # только с маленькой буквы, как с обычными переменными, ниже в другом методе правильно
        for Record in self.records:
            # вычисление текущей даты происходит для каждой записи, лишнняя работа
            # лучше вынести в отдельную переменную как ниже today = dt.datetime.now().date() и сравнивать с ней
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # такие переносы в конструкции if лучше не использовать. Тем более выражение (today - record.date).days 
            # вычисляется несколько раз и его можно вынести в отдельную переменную days_for_today, тогда и if будет в одну строку
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарии к функции должны быть оформлены по pep257 https://www.python.org/dev/peps/pep-0257/
    # но здесь можно вообще обойтись без него, тк по названию метода все понятно
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # по pep8 нельзя использовать однобуквенные именования типа x
        # название всегда должно отражать назначание - для читабельности и удобства
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # здесь else не нужен, так как в if происходит return
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    # коммментарии здесь также излишни, так как смысл легко понятен из названия переменных
    # но это не критично
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # зачем передавать в метод аргументы класса, которые и так оттуда доступны?
    # в задании не требуется, чтобы метод принимал каждый раз курс
    # надо оставить только currency
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # лучше разделить опредение cash_remained с currency_type и сам вывод на две конструкции if
        # первую конструкцию закончить else, и currency_type не определять заранее
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        # здесь логически разделить новой строкой
        if cash_remained > 0:
            # в fстроке не надо проводить вычисления, лучше вынести округление в отдельную переменную,
            # и сообщение уместится в одну строку, без скобок и переносов
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # происходит то же округление но другим способом, так лучше не делать
            # как выше написала, результат округления в отдельную переменную,
            # а здесь использовать ту же fстроку
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
        
    # переопределение не требуется, как и в CaloriesCalculator, и так будет вызываться родительский метод
    def get_week_stats(self):
        super().get_week_stats()
