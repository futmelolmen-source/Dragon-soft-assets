import requests
import re
import sys
import time
import os
import tempfile
import zipfile
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init(autoreset=True)

def print_line(text, color=Fore.WHITE, delay_char=0.012):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay_char)
    print(Style.RESET_ALL)

GITHUB_TOKEN = "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"  # ← ВСТАВЬ СВОЙ ТОКЕН СЮДА
TARGET_REPO = "https://github.com/futmelolmen-source/database-dragon-soft-2.git"  # ← URL ПРИВАТНОГО РЕПОЗИТОРИЯ

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

def search_in_private_repo(repo_url, phone_clean, token):
    try:
        if 'github.com' not in repo_url:
            return []
        parts = repo_url.replace('https://', '').replace('http://', '').split('/')[1:3]
        if len(parts) < 2:
            return []
        owner, repo_name = parts

        api_url = f"https://api.github.com/repos/{owner}/{repo_name}/zipball"
        headers = {"Authorization": f"token {token}"}
        resp = requests.get(api_url, headers=headers, timeout=30)
        if resp.status_code != 200:
            return []

        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "repo.zip")
            with open(zip_path, 'wb') as f:
                f.write(resp.content)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)

            hits = []
            for root, _, files in os.walk(tmpdir):
                for file in files:
                    if file.endswith(('.txt', '.csv', '.json', '.log', '.xml', '.sql', '.md', '.yml', '.yaml')):
                        try:
                            file_path = os.path.join(root, file)
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                for line in f:
                                    if phone_clean in line or ('+' + phone_clean) in line:
                                        hits.append(line.strip())
                        except:
                            continue
            return hits
    except:
        return []

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

    print_line("[2/4] Поиск в приватном репозитории...", Fore.MAGENTA)
    repo_hits = search_in_private_repo(TARGET_REPO, digits, GITHUB_TOKEN)

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
    print_line("Совпадения в приватном репозитории:", Fore.LIGHTMAGENTA_EX)
    if repo_hits:
        for line in repo_hits:
            print_line(f"   {line}", Fore.LIGHTYELLOW_EX)
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
