import random
import time
import sys
from datetime import datetime, timedelta
from colorama import init, Fore, Style

init(autoreset=True)

# --- Транслитерация для email ---
def translit_rus_to_eng(name):
    # Поддержка только заглавных букв, остальное — через lower()
    trans = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh',
        'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
        'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts',
        'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ы': 'Y', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }
    result = ""
    for char in name:
        if char.upper() in trans:
            result += trans[char.upper()]
        else:
            result += char
    return result

# --- Списки имён ---
male_names = ["Александр", "Дмитрий", "Максим", "Иван", "Артём", "Михаил", "Сергей", "Андрей",
              "Николай", "Владимир", "Евгений", "Павел", "Роман", "Олег", "Виктор", "Станислав",
              "Глеб", "Лев", "Тимофей", "Добромысл", "Ярослав", "Всеволод", "Богдан", "Игнат"]

female_names = ["Анна", "Мария", "Екатерина", "Алёна", "Дарья", "Полина", "Виктория", "София",
                "Елизавета", "Вероника", "Анастасия", "Ксения", "Милана", "Арина", "Валерия",
                "Ульяна", "Светлана", "Таисия", "Злата", "Мирослава"]

male_patronymics = ["Александрович", "Дмитриевич", "Максимович", "Иванович", "Артёмович", "Михайлович",
                    "Сергеевич", "Андреевич", "Николаевич", "Владимирович", "Евгеньевич", "Павлович",
                    "Романович", "Олегович", "Викторович", "Станиславович", "Глебович", "Львович",
                    "Тимофеевич", "Добромыслович", "Ярославович", "Всеволодович", "Богданович", "Игнатьевич"]

female_patronymics = ["Александровна", "Дмитриевна", "Максимовна", "Ивановна", "Артёмовна", "Михайловна",
                      "Сергеевна", "Андреевна", "Николаевна", "Владимировна", "Евгеньевна", "Павловна",
                      "Романовна", "Олеговна", "Викторовна", "Станиславовна", "Глебовна", "Львовна",
                      "Тимофеевна", "Добромысловна", "Ярославовна", "Всеволодовна", "Богдановна", "Игнатьевна"]

last_names_male = ["Иванов", "Смирнов", "Кузнецов", "Попов", "Соколов", "Лебедев", "Козлов", "Новиков",
                   "Морозов", "Петров", "Волков", "Соловьёв", "Васильев", "Зайцев", "Павлов", "Крылов",
                   "Фёдоров", "Морозов", "Никитин", "Алексеев", "Степанов", "Григорьев", "Богданов"]

last_names_female = ["Иванова", "Смирнова", "Кузнецова", "Попова", "Соколова", "Лебедева", "Козлова", "Новикова",
                     "Морозова", "Петрова", "Волкова", "Соловьёва", "Васильева", "Зайцева", "Павлова", "Крылова",
                     "Фёдорова", "Морозова", "Никитина", "Алексеева", "Степанова", "Григорьева", "Богданова"]

streets = ["ул. Ленина", "ул. Советская", "ул. Пушкина", "ул. Гагарина", "ул. Кирова",
           "пер. Макаренко", "пер. Чехова", "ул. Лермонтова", "ул. Калинина", "пер. Октябрьский"]

cities = ["г. Петрозаводск", "с. Валдай", "г. Кондопога", "пгт. Сегежа", "г. Костомукша",
          "с. Медвежьегорск", "г. Питкяранта", "пгт. Лахденпохья", "с. Пудож", "г. Сортавала"]

regions = ["респ. Карелия", "Ленинградская обл.", "Мурманская обл.", "Архангельская обл."]

# --- Генераторы ---
def generate_inn(): return ''.join(str(random.randint(0,9)) for _ in range(12))
def generate_snils(): return ''.join(str(random.randint(0,9)) for _ in range(11))
def generate_passport_series(): return str(random.randint(1000, 9999))
def generate_passport_number(): return str(random.randint(100000, 999999))

def generate_phone():
    code = random.choice(["848", "911", "921", "953", "964", "981"])
    num = ''.join(str(random.randint(0,9)) for _ in range(7))
    return f"8 ({code}) {num[:3]}-{num[3:]}"

def generate_email(first_name, year):
    first_eng = translit_rus_to_eng(first_name).lower()
    year_short = str(year)[-2:]
    domain = random.choice(["@mail.ru", "@yandex.ru", "@gmail.com", "@example.com"])
    return f"{first_eng}_{year_short}{domain}"

def generate_address():
    street = random.choice(streets)
    house = random.randint(1, 200)
    city = random.choice(cities)
    region = random.choice(regions)
    postal = str(random.randint(185000, 187999))
    return f"{street}, д. {house}, {city}, {region} {postal}"

# --- Печать с эффектом (по строке, не по символу в одну строку!) ---
def print_line(text, color=Fore.WHITE, delay_char=0.015):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay_char)
    print(Style.RESET_ALL)  # Перевод на новую строку после каждой строки

# --- Генерация ---
def generate_person(gender_input):
    gender = gender_input.strip().upper()
    if gender not in ("М", "Ж"):
        print_line("❌ Ошибка: введите 'М' или 'Ж'", Fore.RED)
        return

    today = datetime.today()
    age = random.randint(18, 70)
    birth_date = today - timedelta(days=age * 365 + random.randint(-180, 180))
    birth_str = birth_date.strftime("%d %B %Y")

    if gender == "М":
        first = random.choice(male_names)
        patronymic = random.choice(male_patronymics)
        last = random.choice(last_names_male)
    else:
        first = random.choice(female_names)
        patronymic = random.choice(female_patronymics)
        last = random.choice(last_names_female)

    full_name = f"{last} {first} {patronymic}"
    email = generate_email(first, birth_date.year)
    phone = generate_phone()
    address = generate_address()
    inn = generate_inn()
    snils = generate_snils()
    passport_series = generate_passport_series()
    passport_number = generate_passport_number()

    # Вывод ТОЛЬКО данных, как в твоём примере — без лишних слов!
    print_line(f"ФИО: {full_name}", Fore.GREEN)
    print_line(f"Пол: {gender}", Fore.YELLOW)
    print_line(f"Дата рождения: {birth_str}", Fore.MAGENTA)
    print_line(f"Возраст: {age} лет", Fore.CYAN)
    print_line(f"Адрес: {address}", Fore.LIGHTBLACK_EX)
    print_line(f"Email: {email}", Fore.LIGHTGREEN_EX)
    print_line(f"Телефон: {phone}", Fore.LIGHTCYAN_EX)
    print_line(f"ИНН: {inn}", Fore.LIGHTYELLOW_EX)
    print_line(f"СНИЛС: {snils}", Fore.LIGHTMAGENTA_EX)
    print_line(f"Паспорт серия: {passport_series} номер: {passport_number}", Fore.WHITE)

# --- Запуск ---
if __name__ == "__main__":
    gender = input("Введите пол (М - мужской, Ж - женский): ").strip()
    print()  # пустая строка перед выводом
    generate_person(gender)