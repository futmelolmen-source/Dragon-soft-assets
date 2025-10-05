import requests
import re
import sys
import time
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init(autoreset=True)

def print_line(text, color=Fore.WHITE, delay_char=0.012):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay_char)
    print(Style.RESET_ALL)

TARGET_URLS = [
    "https://raw.githubusercontent.com/futmelolmen-source/database-dragon-soft-2/refs/heads/main/sdek-database-31234?token=GHSAT0AAAAAADMQJKMBAHKUPTOHLMWHGNOS2HCM6LQ",
    "",
    ""
]

def get_russian_operator_region(digits):
    abc = digits[1:4]
    op_map = {
        "900": ("Мегафон", "Россия"), "903": ("МТС", "Москва и МО"), "915": ("МТС", "Москва"),
        "925": ("МТС", "Москва"), "961": ("Билайн", "Южный ФО"), "962": ("Билайн", "СЗ ФО"),
        "963": ("Билайн", "Центр"), "964": ("Билайн", "Урал"), "965": ("Билайн", "Сибирь"),
        "967": ("Билайн", "ДВ"), "926": ("МТС", "Москва"), "985": ("МТС", "Москва"),
        "999": ("Теле2", "Москва"), "958": ("Теле2", "Центр"), "959": ("Теле2", "Сибирь")
    }
    if abc in op_map:
        return op_map[abc]
    if abc.startswith("90"): return "Мегафон", "Россия"
    if abc.startswith(("91", "92", "98")): return "МТС", "Россия"
    if abc.startswith("96"): return "Билайн", "Россия"
    if abc.startswith(("95", "99")): return "Теле2", "Россия"
    return "Неизвестен", "Неизвестен"

def search_vk(phone):
    try:
        url = f"https://vk.com/search?c%5Bq%5D={phone}&c%5Bsection%5D=people"
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'lxml')
        profiles = []
        for link in soup.find_all('a', href=re.compile(r'^/id\d+')):
            name_tag = link.find_next('div')
            name = name_tag.get_text(strip=True) if name_tag else "Без имени"
            profiles.append((f"https://vk.com{link['href']}", name))
        return profiles[:3]
    except:
        return []

def search_in_urls(urls, phone_clean):
    all_hits = []
    for url in urls:
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            for line in resp.text.splitlines():
                if phone_clean in line or ('+' + phone_clean) in line:
                    all_hits.append((url, line.strip()))
        except:
            continue
    return all_hits

def check_spam(phone_clean):
    try:
        resp = requests.get("https://antiscam.org/blacklist.txt", timeout=5)
        return phone_clean in resp.text
    except:
        return False

def main():
    phone_input = input("Введите номер (89123456789): ").strip()
    digits = re.sub(r'\D', '', phone_input)
    if len(digits) == 10:
        digits = '7' + digits
    elif len(digits) == 11 and digits.startswith('8'):
        digits = '7' + digits[1:]
    if len(digits) != 11 or not digits.startswith('7'):
        print_line("[!] Только российские номера", Fore.RED)
        return

    full_number = '+' + digits
    operator, region = get_russian_operator_region(digits)

    print_line("[1/4] Поиск во ВКонтакте...", Fore.CYAN)
    vk_profiles = search_vk(full_number)

    print_line("[2/4] Поиск по ссылкам...", Fore.MAGENTA)
    url_hits = search_in_urls(TARGET_URLS, digits)

    print_line("[3/4] Проверка спам-баз...", Fore.YELLOW)
    is_spam = check_spam(digits)

    print_line("[4/4] Формирование отчёта...", Fore.GREEN)

    print()
    print_line("ОТЧЁТ ПО НОМЕРУ", Fore.LIGHTGREEN_EX)
    print_line("=" * 50, Fore.LIGHTBLUE_EX)
    print_line(f"Номер: {full_number}", Fore.WHITE)
    print_line(f"Оператор: {operator}", Fore.CYAN)
    print_line(f"Регион: {region}", Fore.YELLOW)

    print_line("-" * 50, Fore.LIGHTBLACK_EX)
    print_line("ВКонтакте:", Fore.LIGHTCYAN_EX)
    if vk_profiles:
        for url, name in vk_profiles:
            print_line(f"   {name} → {url}", Fore.LIGHTGREEN_EX)
    else:
        print_line("   Не найдено", Fore.LIGHTBLACK_EX)

    print_line("-" * 50, Fore.LIGHTBLACK_EX)
    print_line("Совпадения по ссылкам:", Fore.LIGHTMAGENTA_EX)
    if url_hits:
        for url, line in url_hits:
            print_line(f"   Источник: {url}", Fore.LIGHTBLACK_EX)
            print_line(f"   Строка: {line}", Fore.LIGHTYELLOW_EX)
            print_line("", Fore.WHITE)
    else:
        print_line("   Совпадений нет", Fore.LIGHTBLACK_EX)

    print_line("-" * 50, Fore.LIGHTBLACK_EX)
    print_line("Спам-базы:", Fore.LIGHTRED_EX)
    print_line("   В чёрном списке" if is_spam else "   Чист", 
               Fore.RED if is_spam else Fore.LIGHTGREEN_EX)

    print_line("=" * 50, Fore.LIGHTBLUE_EX)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_line("\n[!] Прервано.", Fore.RED)
    except Exception as e:
        print_line(f"[ERROR] {str(e)}", Fore.RED)
