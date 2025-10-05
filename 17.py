import requests
import random
import time
import sys
import re
from colorama import init, Fore, Style

init(autoreset=True)

# --- Эффект печати ---
def print_line(text, color=Fore.WHITE, delay_char=0.015):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay_char)
    print(Style.RESET_ALL)

# --- Получение списка прокси ---
def fetch_proxy_list():
    url = "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
    try:
        print_line("[SEARCH] Ищу список прокси...", Fore.CYAN)
        response = requests.get(url, timeout=10)
        lines = response.text.strip().splitlines()
        # Фильтр: только IP:PORT
        valid = [line.strip() for line in lines if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$', line.strip())]
        print_line(f"[OK] Получено {len(valid)} прокси.", Fore.GREEN)
        random.shuffle(valid)
        return valid
    except Exception as e:
        print_line("[FAIL] Не удалось загрузить список прокси.", Fore.RED)
        return []

# --- Проверка одного прокси ---
def test_proxy(proxy, timeout=10):
    try:
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        resp = requests.get("http://ipv4.icanhazip.com", proxies=proxies, timeout=timeout)
        ip = resp.text.strip()
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            return True
    except:
        return False
    return False

# --- Основной цикл поиска ---
def find_working_proxy():
    while True:
        proxies = fetch_proxy_list()
        if not proxies:
            print_line("[FAIL] Список пуст. Жду 10 сек...", Fore.RED)
            time.sleep(10)
            continue

        print_line("[CHECK] Проверяю прокси...", Fore.YELLOW)
        for p in proxies:
            print_line(f"   Проверка: {p}", Fore.LIGHTBLACK_EX, delay_char=0.005)
            if test_proxy(p, timeout=8):
                print_line(f" → [+] РАБОЧИЙ!", Fore.GREEN)
                return p
            else:
                print_line(" [FAIL]", Fore.RED, delay_char=0.001)

        print_line("[DEAD] Ни один прокси не работает. Жду 15 сек...", Fore.RED)
        time.sleep(15)

# --- Вывод результата в стиле твоих данных ---
def show_proxy_info(proxy):
    print()
    print_line("РАБОЧИЙ HTTP-ПРОКСИ НАЙДЕН!", Fore.LIGHTGREEN_EX)
    print_line("=" * 40, Fore.LIGHTCYAN_EX)
    print_line(f"Адрес: {proxy}", Fore.YELLOW)
    print_line(f"Тип: HTTP", Fore.CYAN)
    print_line(f"Статус: Активен", Fore.GREEN)
    print_line(f"Источник: 632176355256173", Fore.LIGHTMAGENTA_EX)
    print_line("=" * 40, Fore.LIGHTCYAN_EX)
    print_line("⚠️ Все прокси взяты с открытых источников и обновляються каждый 1 час", Fore.LIGHTBLACK_EX)

# --- Запуск ---
if __name__ == "__main__":
    try:
        working = find_working_proxy()
        show_proxy_info(working)
    except KeyboardInterrupt:
        print_line("\n[!] Прервано пользователем.", Fore.RED)
    except Exception as e:
        print_line(f"[ERROR] {str(e)}", Fore.RED)