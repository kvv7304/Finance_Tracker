import config
from financial_records import FinancialRecords, FileManager
from menu import main_menu


if __name__ == "__main__":
    file_manager = FileManager(config.filename)
    financial_data = FinancialRecords(file_manager)
    financial_data.load_transactions()
    main_menu(financial_data)