import requests  # pip install requests
from bs4 import BeautifulSoup  # pip install BeautifulSoup
import json  # json
import telebot  # pip install pyTelegramBotAPI
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot("token")

cities = {
    'Москва': 'https://msk.kassir.ru/',
    'Санкт-Петербург': 'https://spb.kassir.ru/',
    'Абакан': 'https://aba.kassir.ru/',
    'Анапа': 'https://anapa.kassir.ru/',
    'Архангельск': 'https://arh.kassir.ru/',
    'Астрахань': 'https://astr.kassir.ru/',
    'Барнаул': 'https://brn.kassir.ru/',
    'Белгород': 'https://belgorod.kassir.ru/',
    'Благовещенск': 'https://blag.kassir.ru/',
    'Брянск': 'https://bryansk.kassir.ru/',
    'Великий Новгород': 'https://nov.kassir.ru/',
    'Владивосток': 'https://vl.kassir.ru/',
    'Владимир': 'https://vlm.kassir.ru/',
    'Волгоград': 'https://vlg.kassir.ru/',
    'Вологда': 'https://vologda.kassir.ru/',
    'Воронеж': 'https://vrn.kassir.ru/',
    'Геленджик': 'https://gel.kassir.ru/',
    'Екатеринбург': 'https://ekb.kassir.ru/',
    'Иваново': 'https://ivanovo.kassir.ru/',
    'Ижевск': 'https://izhevsk.kassir.ru/',
    'Иркутск': 'https://irk.kassir.ru/',
    'Йошкар-Ола': 'https://yola.kassir.ru/',
    'Казань': 'https://kzn.kassir.ru/',
    'Калининград': 'https://kgd.kassir.ru/',
    'Калуга': 'https://klg.kassir.ru/',
    'Кемерово': 'https://kemerovo.kassir.ru/',
    'Киров': 'https://kirov.kassir.ru/',
    'Комсомольск-на-Амур': 'https://komsomolsk.kassir.ru/',
    'Краснодар': 'https://krd.kassir.ru/',
    'Красноярск': 'https://krs.kassir.ru/',
    'Курск': 'https://kursk.kassir.ru/',
    'Лазаревское': 'https://lzr.kassir.ru/',
    'Липецк': 'https://lipetsk.kassir.ru/',
    'Магнитогорск': 'https://mgn.kassir.ru/',
    'Мурманск': 'https://murm.kassir.ru/',
    'Набережные Челны': 'https://nabchelny.kassir.ru/',
    'Нижний Новгород': 'https://nn.kassir.ru/',
    'Новокузнецк': 'https://novokuznetsk.kassir.ru/',
    'Новороссийск': 'https://nvrsk.kassir.ru/',
    'Новосибирск': 'https://nsk.kassir.ru/',
    'Омск': 'https://omsk.kassir.ru/',
    'Орёл': 'https://orel.kassir.ru/',
    'Оренбург': 'https://orenburg.kassir.ru/',
    'Орск': 'https://orsk.kassir.ru/',
    'Пенза': 'https://pnz.kassir.ru/',
    'Пермь': 'https://perm.kassir.ru/',
    'Петрозаводск': 'https://ptz.kassir.ru/',
    'Петропавловск-Камчаский': 'https://kam.kassir.ru/',
    'Псков': 'https://pskov.kassir.ru/',
    'Ростов-на-Дону': 'https://rnd.kassir.ru/',
    'Рязань': 'https://rzn.kassir.ru/',
    'Самара': 'https://smr.kassir.ru/',
    'Саранск': 'https://saransk.kassir.ru/',
    'Саратов': 'https://saratov.kassir.ru/',
    'Смоленск': 'https://smolensk.kassir.ru/',
    'Сочи': 'https://sochi.kassir.ru/',
    'Ставрополь': 'https://sk.kassir.ru/',
    'Старый Оскол': 'https://oskol.kassir.ru/',
    'Сургут': 'https://sur.kassir.ru/',
    'Тамбов': 'https://tambov.kassir.ru/',
    'Тверь': 'https://tver.kassir.ru/',
    'Тольятти': 'https://tlt.kassir.ru/',
    'Томск': 'https://tomsk.kassir.ru/',
    'Тула': 'https://tula.kassir.ru/',
    'Тюмень': 'https://tmn.kassir.ru/',
    'Улан-Удэ': 'https://ulan.kassir.ru/',
    'Ульяновск': 'https://ulyanovsk.kassir.ru/',
    'Уфа': 'https://ufa.kassir.ru/',
    'Хабаровск': 'https://hbr.kassir.ru/',
    'Чайковский': 'https://chaik.kassir.ru/',
    'Чебоксары': 'https://cheboksary.kassir.ru/',
    'Челябинск': 'https://chel.kassir.ru/',
    'Череповец': 'https://cher.kassir.ru/',
    'Чита': 'https://chita.kassir.ru/',
    'Южно-Сахалинск': 'https://sakh.kassir.ru/',
    'Ярославль': 'https://yar.kassir.ru/'
}

citie = ''


def get_events(url):
    events = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_="new--w-12 new--w-sm-4 new--w-md-3 new--w-lg-1/5 new--px-2 new--pb-4")

    for n, i in enumerate(items, start=1):
        itemName = i.find('div', class_="title").text.strip()
        time_element = i.find('time', class_='date date--md')
        itemTime = time_element.get_text(strip=True)
        itemvenue = i.find('div', class_="venue").text.strip()
        itemlink = i.select_one('a').get('href')
        itemimg = i.select_one('img').get('data-src')
        events.append((itemName, itemTime, itemvenue, itemlink, itemimg))
    return events


@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(row_width=2)
    buttons = [KeyboardButton(city) for city in cities.keys()]
    markup.add(*buttons)
    bot.send_message(message.chat.id, 'Выберите город:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in cities.keys())
def handle_city_selection(message):
    global citie
    city = message.text
    citie = city
    url = cities.get(city)
    print('start')
    event = get_events(url)
    count = len(event)
    page = 1
    itemName, itemTime, itemvenue, itemlink, itemimg = event[page - 1]
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Ссылка", url=itemlink))
    markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
    markup.add(InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
               InlineKeyboardButton(text=f'Вперёд --->',
                                    callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                        page + 1) + ",\"CountPage\":" + str(count) + "}"))
    bot.send_message(message.from_user.id, f'Название[:]({itemimg}) {itemName}\n'
                                           f'Время проведения: {itemTime}\n'
                                           f'Место: {itemvenue}\n'
                                           f'Страница {page} из {count}', parse_mode='markdown', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    url = cities.get(citie)
    event = get_events(url)
    req = call.data.split('_')

    if req[0] == 'unseen':
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif 'pagination' in req[0]:
        json_string = json.loads(req[0])
        count = json_string['CountPage']
        page = json_string['NumberPage']
        markdown = """
                *bold text*
                _italic text_
                [text](URL)
                """
        itemName, itemTime, itemvenue, itemlink, itemimg = event[page - 1]
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Ссылка", url=itemlink))
        markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))

        if page == 1:
            markup.add(InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                       InlineKeyboardButton(text=f'Вперёд --->',
                                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                page + 1) + ",\"CountPage\":" + str(count) + "}"))

        elif page == count:
            markup.add(InlineKeyboardButton(text=f'<--- Назад',
                                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                page - 1) + ",\"CountPage\":" + str(count) + "}"),
                       InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '))

        else:
            markup.add(InlineKeyboardButton(text=f'<--- Назад',
                                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                page - 1) + ",\"CountPage\":" + str(count) + "}"),
                       InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                       InlineKeyboardButton(text=f'Вперёд --->',
                                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                page + 1) + ",\"CountPage\":" + str(count) + "}"))
        bot.edit_message_text(f'Название[:]({itemimg}) {itemName}\n'
                              f'Время проведения: {itemTime}\n'
                              f'Место: {itemvenue}\n'
                              f'Страница {page} из {count}', parse_mode='markdown', reply_markup=markup,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)


bot.polling()
