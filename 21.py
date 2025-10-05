import random
import time
import sys
from datetime import datetime, timedelta
from colorama import init, Fore, Style

init(autoreset=True)

# --- Эффект печати ---
def print_line(text, color=Fore.WHITE, delay_char=0.015):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay_char)
    print(Style.RESET_ALL)

# --- Генерация валидного номера карты (алгоритм Луна) ---
def generate_luhn_digit(card_number_without_check):
    digits = [int(d) for d in card_number_without_check]
    # Удваиваем каждую вторую цифру справа
    for i in range(len(digits) - 1, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    total = sum(digits)
    check_digit = (10 - (total % 10)) % 10
    return str(check_digit)

def generate_card_number(prefix, length=16):
    number = prefix + ''.join(str(random.randint(0, 9)) for _ in range(length - len(prefix) - 1))
    check_digit = generate_luhn_digit(number)
    return number + check_digit

# --- Данные для генерации ---
card_types = {
    "Visa": {"prefixes": ["4"], "length": 16},
    "MasterCard": {"prefixes": [str(i) for i in range(51, 56)] + [str(i) for i in range(2221, 2721)], "length": 16},
    "American Express": {"prefixes": ["34", "37"], "length": 15},
    "Discover": {"prefixes": ["6011"] + [f"65{i}" for i in range(0, 10)] + [str(i) for i in range(644, 650)], "length": 16},
    "Мир": {"prefixes": ["2200", "2201", "2202", "2203", "2204"], "length": 16}
}

banks = [
    "Сбербанк", "ВТБ", "Альфа-Банк", "Тинькофф", "Газпромбанк", "Росбанк",
    "Открытие", "Райффайзен", "ЮMoney", "Почта Банк", "Ренессанс Кредит"
]

countries = [
    "Россия", "США", "Германия", "Франция", "Великобритания", "Канада",
    "Япония", "Бразилия", "Индия", "Австралия"
]

currencies = ["RUB", "USD", "EUR", "GBP", "JPY", "CAD", "CHF", "CNY"]

# --- Имена для карты ---
first_names = [
    "Александр", "Дмитрий", "Мария", "Екатерина", "Иван", "Анна",
    "Сергей", "Ольга", "Максим", "Татьяна", "Артём", "Наталья"
]

last_names = [
    "Иванов", "Смирнов", "Кузнецов", "Попов", "Соколов", "Лебедев",
    "Козлов", "Новиков", "Морозов", "Петров", "Волков", "Соловьёв"
]

# --- Основная функция ---
def generate_fake_card():
    # Выбор типа карты
    card_name = random.choice(list(card_types.keys()))
    config = card_types[card_name]
    prefix = random.choice(config["prefixes"])
    length = config["length"]

    # Генерация номера
    card_number = generate_card_number(prefix, length)

    # Срок действия (+2-5 лет от текущей даты)
    now = datetime.now()
    exp_year = now.year + random.randint(2, 5)
    exp_month = random.randint(1, 12)
    expiry = f"{exp_month:02d}/{exp_year}"

    # CVV (3 или 4 цифры)
    cvv_length = 4 if card_name == "American Express" else 3
    cvv = ''.join(str(random.randint(0, 9)) for _ in range(cvv_length))

    # PIN
    pin = ''.join(str(random.randint(0, 9)) for _ in range(4))

    # Владелец
    first = random.choice(first_names)
    last = random.choice(last_names)
    owner = f"{first.upper()} {last.upper()}"

    # Банк, страна, валюта
    bank = random.choice(banks)
    country = random.choice(countries)
    currency = random.choice(currencies)

    # Вывод в стиле "столбиком"
    print_line("ВЫМЫШЛЕННАЯ БАНКОВСКАЯ КАРТА", Fore.LIGHTCYAN_EX)
    print_line("=" * 40, Fore.LIGHTBLUE_EX)
    print_line(f"Тип карты: {card_name}", Fore.YELLOW)
    print_line(f"Номер карты: {card_number}", Fore.LIGHTGREEN_EX)
    print_line(f"Срок действия: {expiry}", Fore.MAGENTA)
    print_line(f"CVV/CVC: {cvv}", Fore.RED)
    print_line(f"PIN: {pin}", Fore.LIGHTRED_EX)
    print_line(f"Владелец: {owner}", Fore.WHITE)
    print_line(f"Банк-эмитент: {bank}", Fore.CYAN)
    print_line(f"Страна выпуска: {country}", Fore.LIGHTYELLOW_EX)
    print_line(f"Валюта: {currency}", Fore.LIGHTMAGENTA_EX)
    print_line("=" * 40, Fore.LIGHTBLUE_EX)
    print_line("⚠️  Эта карта НЕ РЕАЛЬНА!", Fore.LIGHTBLACK_EX)

# --- Запуск ---
if __name__ == "__main__":
    print()
    generate_fake_card()
