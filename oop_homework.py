import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date == None:
            self.date = dt.date.today()
        else:
            date_format = "%d.%m.%Y"
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.date.today()
        self.week = self.today - dt.timedelta(days=7)

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        stats_today = []
        for record in self.records:
            if record.date == self.today:
                stats_today.append(record.amount)
        return sum(stats_today)

    def get_week_stats(self):
        stats_week = []
        for record in self.records:
            if self.week <= record.date <= self.today:
                stats_week.append(record.amount)
        return sum(stats_week)

    def get_today_limit_balance(self):
        limit_balance = self.limit - self.get_today_stats()
        return limit_balance


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        calories_remained = self.get_today_limit_balance()
        if calories_remained > 0:
            message = (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                       f'калорийностью не более {calories_remained} кКал')
        else:
            message = 'Хватит есть!'
        return message


class CashCalculator(Calculator):

    EURO_RATE = 87.12
    USD_RATE = 76.05
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency='rub'):

        currencies = {
            'eur': ('Euro', CashCalculator.EURO_RATE),
            'usd': ('USD', CashCalculator.USD_RATE),
            'rub': ('RUB', CashCalculator.RUB_RATE)
        }
        currensy_name = currencies[currency][0]
        currensy_rate = currencies[currency][1]
        remained_cash = self.get_today_limit_balance()
        remained_cash_in_currency = round(remained_cash / currensy_rate, 2)

        if remained_cash == 0:
            return f"Денег нет, держись!"
        elif currency not in currencies:
            return f'Валюта {currency} не поддерживается'
        elif remained_cash_in_currency > 0:
            return f"На сегодня осталось {remained_cash_in_currency} {currensy_name}"
        else:
            return f"Денег нет, держись: твой долг - {remained_cash_in_currency} {currensy_name}"
