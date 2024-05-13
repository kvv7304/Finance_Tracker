class Transaction:
    def __init__(self, date: str, category: str, amount: float, description: str) -> None:
        self.date: str = date
        self.category: str = category
        self.amount: float = amount
        self.description: str = description

    def __str__(self) -> str:
        return (f"Дата: {self.date}\n"
                f"Категория: {self.category}\n"
                f"Сумма: {self.amount}\n"
                f"Описание: {self.description}\n")
