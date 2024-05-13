from utils import clear_screen, exit_program
from financial_records import UserInput, TransactionDisplay


class MenuItem:
    def __init__(self, text, action):
        self.text = text
        self.action = action

class Menu:
    def __init__(self, title, clear_func, financial_records):
        self.title = title
        self.menu_items = {}
        self.clear_screen = clear_func
        self.financial_records = financial_records
        self.user_input = UserInput()
        self.transaction_display = TransactionDisplay(financial_records)


    def display_balance(self):
        self.display_balance = self.transaction_display.display_balance()

    def display_transactions(self):
        self.display_transactions = self.transaction_display.display_transactions()

    def search_transactions(self, search_term):
        return self.financial_records.search_transactions(search_term)

    def validate_date(self):
        return self.UserInput.validate_date()

    def choose_category(self):
        return self.UserInput.choose_category()

    def validate_amount(self):
        return self.UserInput.validate_amount()

    def add_transaction(self, date, category, amount, description):
        self.add_or_edit_transaction = \
            self.financial_records.add_or_edit_transaction(date, category, amount, description)

    def edit_transaction(self, date, category, amount, description, index):
        self.add_or_edit_transaction = \
            self.financial_records.add_or_edit_transaction(date, category, amount, description, index)


    def add_transaction_menu(self):
        date = self.validate_date()
        category = self.choose_category()
        amount = self.validate_amount()
        description = input("Введите описание: ")
        self.add_transaction(date, category, amount, description)
        print("Запись добавлена.")

    def edit_transaction_menu(self):
        self.display_transactions()
        index = input("Введите номер записи для редактирования: ")
        date = self.validate_date()
        category = self.choose_category()
        amount = self.validate_amount()
        description = input("Введите новое описание: ")
        self.edit_transaction(date, category, amount, description, int(index) - 1)
        print("Запись обновлена.")

    def search_transactions_menu(self):
        """Поиск транзакций по заданным критериям."""
        search_term = input("Введите критерий поиска (дата, категория, сумма или описание): ")
        results = self.search_transactions(search_term)
        if results.transactions:
            print("\nНайденные записи:")
            transaction_display = TransactionDisplay(results)  # Создаем экземпляр для отображения результатов
            transaction_display.display_transactions()
        else:
            print("Записи не найдены.")

    def add_item(self, key, menu_item):
        self.menu_items[key] = menu_item

    def run(self):
        while True:
            print(f'\n{self.title}')
            for key, item in self.menu_items.items():
                print(f"{key}. {item.text}")
            choice = input("Выберите действие: ")
            if choice in self.menu_items:
                self.menu_items[choice].action()
            else:
                self.clear_screen()
                print("Неверный ввод. Пожалуйста, попробуйте снова.")

    def validate_date(self):
        return self.user_input.validate_date()

    def validate_amount(self):
        return self.user_input.validate_amount()

    def choose_category(self):
        return self.user_input.choose_category()

def main_menu(data):
    menu = Menu('Консольное приложение "Личный финансовый кошелек"', clear_screen, data)

    menu.add_item("1", MenuItem("Вывод баланса", menu.display_balance))
    menu.add_item("2", MenuItem("Добавление записи", menu.add_transaction_menu))
    menu.add_item("3", MenuItem("Редактирование записи", menu.edit_transaction_menu))
    menu.add_item("4", MenuItem("Поиск по записям", menu.search_transactions_menu))
    menu.add_item("5", MenuItem("Выход", exit_program))

    menu.run()
