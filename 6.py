import os
import sys
import sqlite3
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.platform == "win32":
    try:
        from colorama import init
        init()
    except ImportError:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def type_print(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

print_lock = threading.Lock()

def search_in_db(db_path, query):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            try:
                cursor.execute(f"PRAGMA table_info(`{table}`);")
                columns = [col[1] for col in cursor.fetchall()]
                if not columns:
                    continue

                safe_columns = [f"`{col}`" for col in columns]
                like_conditions = [f"{col} LIKE ?" for col in safe_columns]
                sql = f"SELECT * FROM `{table}` WHERE " + " OR ".join(like_conditions)
                params = [f"%{query}%"] * len(columns)

                cursor.execute(sql, params)
                rows = cursor.fetchall()

                if rows:
                    with print_lock:
                        type_print(f"\n\033[93m[+] Найдено в {db_path} → таблица `{table}`:\033[0m")
                        for row in rows:
                            type_print(f"    📌 {row}")
            except sqlite3.Error as e:
                with print_lock:
                    type_print(f"\033[91m[!] Ошибка в таблице {table} ({db_path}): {e}\033[0m")
        conn.close()
    except Exception as e:
        with print_lock:
            type_print(f"\033[91m[!] Не удалось открыть БД {db_path}: {e}\033[0m")

def search_in_text_file(file_path, query):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()

        found = False
        for i, line in enumerate(lines, 1):
            if query.lower() in line.lower():
                if not found:
                    with print_lock:
                        type_print(f"\n\033[93m[+] Найдено в {file_path}:\033[0m")
                    found = True
                with print_lock:
                    type_print(f"    📌 Строка {i}: {line.strip()}")
    except Exception as e:
        with print_lock:
            type_print(f"\033[91m[!] Ошибка чтения {file_path}: {e}\033[0m")

def main():
    db_folder = os.path.join(os.getcwd(), "DataBase")
    
    if not os.path.exists(db_folder):
        type_print(f"\033[93m[!] Папка 'DataBase' не найдена. Создаём...\033[0m")
        os.makedirs(db_folder)
        type_print(f"\033[92m[✓] Папка 'DataBase' создана. Положите туда свои файлы.\033[0m")

    supported_exts = (
        '.db', '.sqlite', '.sqlite3', '.txt', '.csv', '.json', '.html', '.xml',
        '.log', '.md', '.sql', '.yml', '.yaml', '.ini', '.cfg', '.dat'
    )

    while True:
        type_print("\n" + "="*60)
        query = input("\033[96m🔍 Введите строку для поиска (или 'exit' для выхода): \033[0m").strip()

        if query.lower() in ('exit', 'quit', 'выход'):
            type_print("\033[92m[✓] До встречи! 👋\033[0m")
            break

        if not query:
            type_print("\033[91m[-] Запрос не может быть пустым.\033[0m")
            input("\nНажмите Enter, чтобы продолжить...")
            continue

        if not os.path.exists(db_folder):
            type_print("\033[91m[-] Папка DataBase исчезла!\033[0m")
            input("\nНажмите Enter...")
            continue

        files = []
        for file in os.listdir(db_folder):
            full_path = os.path.join(db_folder, file)
            if os.path.isfile(full_path) and file.endswith(supported_exts):
                files.append(full_path)

        if not files:
            type_print(f"\033[91m[-] В папке 'DataBase' нет файлов с поддерживаемыми расширениями.\033[0m")
            type_print(f"    Поддерживаемые: {', '.join(supported_exts)}")
            input("\nНажмите Enter, чтобы продолжить...")
            continue

        type_print(f"\n\033[92m[+] Найдено {len(files)} файл(ов) в папке 'DataBase'. Ищем '{query}'...\033[0m")

        with ThreadPoolExecutor(max_workers=32) as executor:
            futures = []
            for file_path in files:
                if file_path.endswith(('.db', '.sqlite', '.sqlite3')):
                    futures.append(executor.submit(search_in_db, file_path, query))
                else:
                    futures.append(executor.submit(search_in_text_file, file_path, query))

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    with print_lock:
                        type_print(f"\033[91m[!] Ошибка в потоке: {e}\033[0m")

        type_print("\n\033[92m[✓] Поиск завершён.\033[0m")
        input("\nНажмите Enter, чтобы начать новый поиск...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        type_print("\n\n\033[93m[!] Программа прервана пользователем.\033[0m")
    finally:
        input("\nНажмите Enter, чтобы выйти...")