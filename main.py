import time

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium_stealth import stealth

import telebot
from telebot.types import InputMediaPhoto
from telebot import types

bot = telebot.TeleBot(token='7541428785:AAEUZfKlSVSLGeXaxPNNUTq7eih7HkvM54Y')

opts = webdriver.ChromeOptions()
opts.add_argument('--start-maximized')
#opts.add_argument('--headless')

browser = webdriver.Chrome(options=opts)

stealth(browser , 
        languages=['en-US' , 'en'] ,
        vendor="Google Inc." ,
        platform="Win32" ,
        webgl_vendor="Intel Inc." ,
        renderer="Intel Iris OpenGL Engine" ,
        fix_hairline=True
        )


def search(search):
    try:
        search = search.replace(' ', '+')
        browser.get(f'https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=gg&search={search}')
        time.sleep(5)
        browser.find_element(By.XPATH , "/html/body/div[1]/main/div[2]/div[2]/div[2]/div/div/div[4]/div[1]/div[1]/div/article[1]/div/a").click()
        browser.find_element(By.XPATH , '/html/body/div[4]/div/div/button').click()
        time.sleep(5)

        link_WB = browser.current_url
        search1 = browser.find_element(By.XPATH , '/html/body/div[1]/main/div[2]/div[2]/div[3]/div/div[3]/div[9]/div[1]/h1').text
        browser.save_screenshot('wb.png')

        search1 = search1.replace(' ' , '+')

        browser.get(f'https://www.ozon.ru/search/?text={search1}&from_global=true')
        time.sleep(5)
        browser.find_element(By.XPATH , '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[4]/div[1]/div/div/div[1]/div/a/div/div[2]/div').click()
        browser.switch_to.window(browser.window_handles[1])
        link_ozon = browser.current_url
        time.sleep(5)
        browser.save_screenshot('ozon.png')
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        browser.get('data:,')
        #browser.quit()
        
        return [True , link_WB , link_ozon]
    except:
        return[False]


@bot.message_handler(commands=['start'])
def start (msg):
    bot.send_message(msg.chat.id, f'привет, {msg.from_user.username}!'
                                  f'\n я помогу тебе сравнить цены на wildberris и ozon, напиши что ты хочешь найти и я помогу тебя'
                                  f'\n поиски заинимают около 15-20 секунд')

@bot.message_handler(content_types=['text'])
def lalala (msg):
    ans = search(msg.text)
    if ans[0] == True:
        bot.send_message(msg.chat.id , f'wb:{ans[1]} \n ozon: {ans[2]}')
        #bot.send_media_group(msg.chat.id, [open('wb.jpg', 'rb'), open('ozon.jpg', 'rb')])
    else:
        bot.send_message(msg.chat.id , 'произошла какая-то ошибка, попробуйдете ещё раз')

while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)
        time.sleep(15)
print('end')