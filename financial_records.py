import config
from transactions import Transaction
from utils import clear_screen, exit_program
from datetime import datetime

class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def file_manager_load_transactions(self):
        transactions = []
        try:
            with open(self.filename, 'r', encoding="utf-8") as file:
                content = file.read().strip()
                entries = content.split('\n\n')
                for entry in entries:
                    data = entry.split('\n')
                    transaction_data = {
                        line.split(':')[0].strip(): line.split(':')[1].strip()
                        for line in data if ':' in line
                    }
                    transactions.append(Transaction(
                        transaction_data['Дата'], transaction_data['Категория'],
                        float(transaction_data['Сумма']), transaction_data['Описание']
                    ))
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден.")
        return transactions

    def file_manager_save_transactions(self, transactions):
        with open(self.filename, 'w', encoding="utf-8") as file:
            for transaction in transactions:
                file.write(str(transaction) + '\n\n')


class UserInput:
    def __init__(self):
        self.categories = ['Доход', 'Расход']

    def validate_date(self):
        """Просит пользователя ввести дату и возвращает её в формате 'YYYY-MM-DD', если дата корректна."""
        from datetime import datetime

        while True:
            day = input("Введите число (dd): ")
            month = input("Введите месяц (mm): ")
            year = input("Введите год (YYYY): ")
            date_input = f"{year}-{month}-{day}"
            try:
                valid_date = datetime.strptime(date_input, "%Y-%m-%d")
                return valid_date.strftime("%Y-%m-%d")
            except ValueError:
                print("Введена некорректная дата. Пожалуйста, убедитесь, что все компоненты даты введены правильно.")

    def validate_amount(self):
        """Проверяет и возвращает корректно введенную сумму как положительное целое число."""
        while True:
            amount_input = input("Введите сумму: ")
            if amount_input.isdigit():
                return int(amount_input)
            print("Введите корректную сумму (целое число).")

    def choose_category(self):
        """Позволяет пользователю выбрать категорию из списка и возвращает выбранную категорию."""
        print("Выберите категорию:")
        for idx, category in enumerate(self.categories, 1):
            print(f"{idx}. {category}")
        while True:
            try:
                choice = int(input("Введите номер категории: "))
                if 1 <= choice <= len(self.categories):
                    return self.categories[choice - 1]
                else:
                    print("Выберите номер из списка.")
            except ValueError:
                print("Пожалуйста, введите числовое значение.")

class TransactionDisplay:
    def __init__(self, financial_records):
        self.financial_records = financial_records

    def display_transactions(self):
        clear_screen()
        transactions = self.financial_records.transactions
        if not transactions:
            print("Список транзакций пуст.")
        else:
            print("\nСписок всех транзакций:")
            print(f"{'№':<5}{'Дата':<12} {'Категория':<10} {'Сумма':<10} {'Описание':<30}")
            for index, transaction in enumerate(transactions, start=1):
                print(f"{index:<5}"
                      f"{transaction.date:<12} "
                      f"{transaction.category:<10} "
                      f"{transaction.amount:<10} "
                      f"{transaction.description:<30}")

    def display_balance(self):
        self.display_transactions()
        balance, income, expense = self.financial_records.get_balance()
        print(f"\nТекущий баланс: {balance}")
        print(f"Доходы: {income}")
        print(f"Расходы: {expense}")

class FinancialRecords:
    def __init__(self, file_manager=None, menu=None):
        self.transactions = []
        self.file_manager = file_manager
        self.menu = menu

    def load_transactions(self):
        self.transactions = self.file_manager.file_manager_load_transactions()

    def save_transactions(self):
        self.file_manager.file_manager_save_transactions(self.transactions)

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def add_or_edit_transaction(self, date, category, amount, description, index=None):
        if index is not None and 0 <= index < len(self.transactions):
            self.transactions[index] = Transaction(date, category, amount, description)
        else:
            self.add_transaction(Transaction(date, category, amount, description))
        self.save_transactions()

    def get_balance(self):
        income = sum(t.amount for t in self.transactions if t.category == 'Доход')
        expense = sum(t.amount for t in self.transactions if t.category == 'Расход')
        balance = income - expense
        return balance, income, expense


    def search_transactions(self, search_term: str) -> 'FinancialRecords':
        """Поиск транзакций по заданным критериям и возвращает новый экземпляр FinancialRecords."""
        new_data_file = FinancialRecords()  # Создаем новый экземпляр для найденных транзакций
        for t in self.transactions:
            if search_term.lower() in t.date.lower() or \
                    search_term.lower() in t.category.lower() or \
                    search_term.lower() in t.description.lower() or \
                    search_term == str(t.amount):
                new_data_file.add_transactions(t)
        return new_data_file

    def add_transactions(self, transactions):
        """Добавляет одну транзакцию или список транзакций в список."""
        if isinstance(transactions, list):
            self.transactions.extend(transactions)
        else:
            self.transactions.append(transactions)