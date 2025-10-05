import requests
import socket
import ssl
import json
import re
import time
import sys
import subprocess
from urllib.parse import urlparse
from colorama import init, Fore, Style

# Попытка импорта опциональных модулей
try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

from bs4 import BeautifulSoup

init(autoreset=True)

# --- Эффект печати ---
def print_line(text, color=Fore.WHITE, delay_char=0.012):
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay_char)
    print(Style.RESET_ALL)

# --- Нормализация URL ---
def normalize_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

# --- Получение базовой инфы ---
def get_site_info(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    return url, domain

# --- WHOIS ---
def get_whois_info(domain):
    if not WHOIS_AVAILABLE:
        return "Модуль 'whois' не установлен"
    try:
        w = whois.whois(domain)
        return {
            "Регистратор": str(w.registrar) if w.registrar else "—",
            "Создан": str(w.creation_date) if w.creation_date else "—",
            "Истекает": str(w.expiration_date) if w.expiration_date else "—",
            "Владелец": str(w.org) if w.org else "—",
            "Страна": str(w.country) if w.country else "—"
        }
    except Exception as e:
        return f"Ошибка WHOIS: {str(e)}"

# --- DNS-записи ---
def get_dns_info(domain):
    if not DNS_AVAILABLE:
        return {"Ошибка": "Модуль 'dnspython' не установлен"}
    records = {}
    types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
    for qtype in types:
        try:
            answers = dns.resolver.resolve(domain, qtype)
            records[qtype] = [str(rdata) for rdata in answers]
        except:
            records[qtype] = ["—"]
    return records

# --- HTTP-заголовки и технологии ---
def get_http_info(url):
    try:
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        headers = dict(resp.headers)
        tech = []

        # Определение CMS и технологий
        if 'wordpress' in resp.text.lower():
            tech.append("WordPress")
        if 'drupal' in resp.text.lower():
            tech.append("Drupal")
        if 'x-powered-by' in headers:
            tech.append(headers['x-powered-by'])
        if 'server' in headers:
            tech.append(headers['server'])

        return {
            "Статус": resp.status_code,
            "Заголовки": headers,
            "Технологии": tech if tech else ["Не обнаружены"]
        }
    except Exception as e:
        return {"Ошибка": str(e)}

# --- SSL-сертификат ---
def get_ssl_info(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                subject = dict(x[0] for x in cert['subject'])
                issuer = dict(x[0] for x in cert['issuer'])
                return {
                    "Субъект": subject.get('commonName', '—'),
                    "Издатель": issuer.get('commonName', '—'),
                    "Действителен до": cert.get('notAfter', '—')
                }
    except:
        return {"Ошибка": "SSL недоступен"}

# --- Robots.txt и Sitemap ---
def check_robots_sitemap(url):
    results = {}
    for path in ['/robots.txt', '/sitemap.xml']:
        try:
            r = requests.get(url.rstrip('/') + path, timeout=5)
            results[path] = "Доступен" if r.status_code == 200 else "Недоступен"
        except:
            results[path] = "Ошибка"
    return results

# --- Поиск поддоменов (базовый) ---
def find_subdomains(domain):
    subdomains = []
    common = ['www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'dev', 'test', 'admin', 'api']
    for sub in common:
        try:
            socket.gethostbyname(f"{sub}.{domain}")
            subdomains.append(f"{sub}.{domain}")
        except:
            pass
    return subdomains if subdomains else ["Не найдены"]

# --- Сканирование портов (только 80, 443, 21, 22, 25, 53, 110, 143, 993, 995) ---
def scan_common_ports(domain):
    open_ports = []
    common_ports = [21, 22, 25, 53, 80, 110, 143, 443, 993, 995]
    for port in common_ports:
        try:
            with socket.create_connection((domain, port), timeout=3):
                open_ports.append(port)
        except:
            pass
    return open_ports if open_ports else ["Закрыты"]

# --- Основная функция ---
def main():

    target = input("Введите URL или домен (например, example.com): ").strip()
    if not target:
        print_line("[!] Не указан домен.", Fore.RED)
        return

    url, domain = get_site_info(target)
    print_line(f"[OK] Цель: {domain}", Fore.GREEN)
    print()

    # === Сбор данных ===
    print_line("[1/7] Получение WHOIS...", Fore.YELLOW)
    whois_data = get_whois_info(domain)

    print_line("[2/7] Запрос DNS-записей...", Fore.YELLOW)
    dns_data = get_dns_info(domain)

    print_line("[3/7] Анализ HTTP/HTTPS...", Fore.YELLOW)
    http_data = get_http_info(url)

    print_line("[4/7] Проверка SSL-сертификата...", Fore.YELLOW)
    ssl_data = get_ssl_info(domain)

    print_line("[5/7] Поиск robots.txt и sitemap.xml...", Fore.YELLOW)
    robots_sitemap = check_robots_sitemap(url)

    print_line("[6/7] Поиск поддоменов...", Fore.YELLOW)
    subdomains = find_subdomains(domain)

    print_line("[7/7] Сканирование общих портов...", Fore.YELLOW)
    ports = scan_common_ports(domain)

    # === Вывод результатов ===
    print()
    print_line("РЕЗУЛЬТАТЫ РАЗВЕДКИ", Fore.LIGHTGREEN_EX)
    print_line("=" * 50, Fore.LIGHTBLUE_EX)

    # WHOIS
    if isinstance(whois_data, dict):
        for k, v in whois_data.items():
            print_line(f"{k}: {v}", Fore.CYAN)
    else:
        print_line(f"WHOIS: {whois_data}", Fore.LIGHTBLACK_EX)

    print_line("-" * 50, Fore.LIGHTBLACK_EX)

    # DNS
    for rec_type, values in dns_data.items():
        if isinstance(values, list):
            val_str = ", ".join(values) if values[0] != "—" else "—"
        else:
            val_str = str(values)
        print_line(f"DNS {rec_type}: {val_str}", Fore.MAGENTA)

    print_line("-" * 50, Fore.LIGHTBLACK_EX)

    # HTTP
    if "Ошибка" not in str(http_data):
        print_line(f"HTTP Статус: {http_data['Статус']}", Fore.LIGHTGREEN_EX)
        print_line(f"Технологии: {', '.join(http_data['Технологии'])}", Fore.LIGHTYELLOW_EX)
    else:
        print_line(f"HTTP: {http_data.get('Ошибка', 'Неизвестно')}", Fore.RED)

    print_line("-" * 50, Fore.LIGHTBLACK_EX)

    # SSL
    if "Ошибка" not in str(ssl_data):
        for k, v in ssl_data.items():
            print_line(f"SSL {k}: {v}", Fore.LIGHTMAGENTA_EX)
    else:
        print_line("SSL: недоступен", Fore.LIGHTBLACK_EX)

    print_line("-" * 50, Fore.LIGHTBLACK_EX)

    # Robots & Sitemap
    for path, status in robots_sitemap.items():
        print_line(f"{path}: {status}", Fore.LIGHTCYAN_EX)

    print_line("-" * 50, Fore.LIGHTBLACK_EX)

    # Поддомены
    print_line(f"Поддомены: {', '.join(subdomains)}", Fore.LIGHTYELLOW_EX)

    # Порты
    print_line(f"Открытые порты: {', '.join(map(str, ports))}", Fore.LIGHTRED_EX)

    print_line("=" * 50, Fore.LIGHTBLUE_EX)
    print_line("⚠️  Используйте эти данные только в этических целях!", Fore.LIGHTBLACK_EX)

# --- Запуск ---
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_line("\n[!] Прервано пользователем.", Fore.RED)
    except Exception as e:
        print_line(f"[ERROR] {str(e)}", Fore.RED)