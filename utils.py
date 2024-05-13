import os
import platform
import sys
from datetime import datetime

def clear_screen() -> None:
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def exit_program() -> None:
    print('Вы вышли из консольного приложения "Личный финансовый кошелек".')
    sys.exit()
