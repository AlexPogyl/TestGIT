import subprocess
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import telebot

botTimeWeb = telebot.TeleBot('xxxxxxxx')

@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    first_mess = f" Привет!\nНу что, может быть начнем?"
    botTimeWeb.send_message(message.chat.id, first_mess)

TOKEN = 'xxxxxxx'
TARGET_CHAT_ID = 'xxxxxxx'
MESSAGE_THREAD_ID = 'xxxxxx'
bot = telebot.TeleBot(TOKEN)
img = "https://icon-library.com/images/2018/6647985_peppa-pig-cumpleaos-peppa-pig-png-logo-png.png"
text = "Проверяю работоспособность и начинаю"
bot.send_message(TARGET_CHAT_ID, f'<a href="{img}">{text}</a>', parse_mode='html',message_thread_id=MESSAGE_THREAD_ID)

my_file = open('search.txt', "w+", encoding='utf-8')
my_file.close()

def get_avito_data(previous_data):
    url = "https://www.avito.ru/all/igry_pristavki_i_programmy?cd=1&q=psp&s=104"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    chromedriver_path = '/usr/lib/chromium-browser/chromedriver'
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    new_data = set()
    items = soup.find_all("a", itemprop="url")
    
    with open('search.txt', 'r', encoding='utf-8') as input_file:
        existing_data = input_file.read().splitlines()
    
    with open('search.txt', 'a', encoding='utf-8') as output_file:
        for item in items:
            item_title = item.get("title")
            if "Объявление" not in item_title:  
                item_href = f"https://www.avito.ru{item.get('href')}"
                price = "Цена: Не указана"
                price_value = item.find_next("meta", itemprop="price")
                if price_value:
                    price = f"Цена: {price_value.get('content')} руб."
                if item_href not in previous_data and item_href not in existing_data:
                    new_data.add(item_href)
                    output_file.write(f"Название: {item_title}  Ссылка: {item_href}  {price}\n\n")
                    text = f'<a href="{item_href}">{item_title}</a>\n{price}'
                    time.sleep(3)
                    bot.send_message(TARGET_CHAT_ID, text, parse_mode='html', message_thread_id=MESSAGE_THREAD_ID)
                    time.sleep(1)
                    
    driver.quit()

    return new_data

def main():
    previous_data = set()
    while True:
        previous_data |= get_avito_data(previous_data)
        time.sleep(1)

if __name__ == "__main__":
    main()
