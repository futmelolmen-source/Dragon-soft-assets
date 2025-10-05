import requests
import json
import sys
import time
import socket
from colorama import init, Fore, Style

init(autoreset=True)

# --- Эффект печати ---
def print_line(text, color=Fore.WHITE, delay_char=0.015):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay_char)
    print(Style.RESET_ALL)

# --- Получение публичного IP ---
def get_my_ip():
    try:
        resp = requests.get("https://api.ipify.org", timeout=5)
        return resp.text.strip()
    except:
        return None

# --- Валидация IP ---
def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

# --- Получение данных по IP ---
def get_ip_info(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=66846719&lang=ru"
        # Поля: все основные + lang=ru для русских названий стран/регионов
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None

# --- Основная функция ---
def main():
    
    # Запрос IP
    user_input = input("Введите IP-адрес (или нажмите Enter для своего): ").strip()
    
    if not user_input:
        print_line("[AUTO] Определяю ваш публичный IP...", Fore.YELLOW)
        ip = get_my_ip()
        if not ip:
            print_line("[ERROR] Не удалось определить ваш IP.", Fore.RED)
            return
        print_line(f"[OK] Ваш IP: {ip}", Fore.GREEN)
    else:
        if not is_valid_ip(user_input):
            print_line("[ERROR] Неверный формат IP-адреса.", Fore.RED)
            return
        ip = user_input

    print()
    print_line(f"[SEARCH] Запрашиваю информацию по {ip}...", Fore.CYAN)
    data = get_ip_info(ip)

    if not data or data.get("status") != "success":
        print_line("[FAIL] Не удалось получить данные по IP.", Fore.RED)
        return

    # Вывод в стиле "столбиком", как у тебя в примерах
    print()
    print_line("ИНФОРМАЦИЯ ПО IP-АДРЕСУ", Fore.LIGHTGREEN_EX)
    print_line("=" * 40, Fore.LIGHTBLUE_EX)

    fields = {
        "IP": data.get("query", "—"),
        "Страна": data.get("country", "—"),
        "Код страны": data.get("countryCode", "—"),
        "Регион": data.get("regionName", "—"),
        "Код региона": data.get("region", "—"),
        "Город": data.get("city", "—"),
        "Почтовый индекс": data.get("zip", "—"),
        "Широта": str(data.get("lat", "—")),
        "Долгота": str(data.get("lon", "—")),
        "Часовой пояс": data.get("timezone", "—"),
        "Провайдер (ISP)": data.get("isp", "—"),
        "Организация": data.get("org", "—"),
        "AS": data.get("as", "—"),
        "Тип подключения": detect_connection_type(data),
    }

    # Печать всех полей
    for key, value in fields.items():
        if value and value != "—":
            print_line(f"{key}: {value}", Fore.WHITE)
        else:
            print_line(f"{key}: —", Fore.LIGHTBLACK_EX)

    print_line("=" * 40, Fore.LIGHTBLUE_EX)
    print_line("⚠️  Данные получены из публичных источников.", Fore.LIGHTBLACK_EX)

# --- Определение типа подключения (примерное) ---
def detect_connection_type(data):
    isp = (data.get("isp") or "").lower()
    org = (data.get("org") or "").lower()
    as_name = (data.get("as") or "").lower()

    if any(word in isp for word in ["mobile", "мобиль", "cell", "telecom", "mts", "билайн", "мегафон", "tele2"]):
        return "Мобильный"
    elif any(word in org for word in ["amazon", "google", "microsoft", "cloud", "digitalocean", "ovh", "hetzner", "hosting", "хостинг"]):
        return "Хостинг / Облако"
    elif "university" in org or "университет" in org:
        return "Образовательная сеть"
    else:
        return "Резидентский / Неизвестен"

# --- Запуск ---
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_line("\n[!] Прервано пользователем.", Fore.RED)
    except Exception as e:
        print_line(f"[ERROR] {str(e)}", Fore.RED)