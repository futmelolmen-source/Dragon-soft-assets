import random
import string
import time
import sys
from colorama import init, Fore, Style

init(autoreset=True)

# --- Эффект печати по строке ---
def print_line(text, color=Fore.WHITE, delay_char=0.015):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay_char)
    print(Style.RESET_ALL)

# --- Генерация пароля ---
def generate_password(length=16):
    if length < 8:
        length = 8  # Минимум 8 символов для "сложного" пароля

    # Обязательные компоненты
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    # Гарантируем наличие всех типов символов
    password = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
        random.choice(symbols)
    ]

    # Добавляем остальные символы из полного набора
    all_chars = lower + upper + digits + symbols
    for _ in range(length - 4):
        password.append(random.choice(all_chars))

    # Перемешиваем
    random.shuffle(password)
    return ''.join(password)

# --- Оценка надёжности ---
def get_strength(length):
    if length < 8:
        return "Слабый"
    elif length < 12:
        return "Хороший"
    elif length < 16:
        return "Сильный"
    else:
        return "Очень сильный"

# --- Основная функция ---
def generate_secure_password():
    # Можно сделать длину случайной (от 12 до 24)
    length = random.randint(12, 24)
    password = generate_password(length)
    strength = get_strength(length)

    # Вывод в стиле твоего формата — только данные, без лишнего
    print_line(f"Длина пароля: {length} символов", Fore.CYAN)
    print_line(f"Надёжность: {strength}", Fore.GREEN)
    print_line(f"Пароль: {password}", Fore.LIGHTYELLOW_EX)

# --- Запуск ---
if __name__ == "__main__":
    print()  # пустая строка для красоты
    generate_secure_password()