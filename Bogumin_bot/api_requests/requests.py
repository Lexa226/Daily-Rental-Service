from src.bot_config import bot
from telebot.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
from PIL import Image
import io
import urllib.parse
import requests
from telebot.types import CallbackQuery


def get_data(user_data, user_id):
    try:
        # Убедитесь, что user_data[user_id] - это словарь с параметрами для GET запроса
        response = requests.get(
            'http://127.0.0.1:8000/api/properties/', params=user_data[user_id])
        response.raise_for_status()  # Это вызовет исключение, если статус ответа не 200
        data = response.json()  # Получаем данные в формате JSON

        # Сохраняем полученные данные в файл, это шаг опционален
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

        return data
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - for user {user_id}")
    except Exception as err:
        print(f"An error occurred: {err} - for user {user_id}")
    return None


def create_map_url(address):
    base_url = "https://yandex.ru/maps/?text="
    query = urllib.parse.quote(address)
    return base_url + query


def compress_image(image_path, quality=75, min_size=(320, 320), max_size=(1280, 1280)):
    with open(image_path, 'rb') as file:
        image_data = file.read()
        img = Image.open(io.BytesIO(image_data))

        # Check and adjust image dimensions
        current_width, current_height = img.size
        if current_width < min_size[0] or current_height < min_size[1]:
            scale = max(min_size[0] / current_width,
                        min_size[1] / current_height)
            new_size = (int(current_width * scale),
                        int(current_height * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        elif current_width > max_size[0] or current_height > max_size[1]:
            scale = min(max_size[0] / current_width,
                        max_size[1] / current_height)
            new_size = (int(current_width * scale),
                        int(current_height * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=quality)
        img_byte_arr.seek(0)
        return img_byte_arr


def send_properties(bot, chat_id, data):
    for item in data:
        media_group = []
        images = item.get('images', [])
        if images:
            images = images[0].split(", ")
            for image_path in images:
                if os.path.exists(image_path):
                    compressed_image = compress_image(image_path, quality=50)
                    media_group.append(
                        InputMediaPhoto(compressed_image.read()))

        description = prepare_property_description(item)
        map_url = create_map_url(item.get('streetaddress', 'Не указано'))

        # Создаем кнопки
        markup = InlineKeyboardMarkup()
        map_button = InlineKeyboardButton("Показать на карте", url=map_url)
        markup.add(map_button)

        if media_group:
            bot.send_media_group(chat_id, media_group)
        bot.send_message(chat_id, description,
                         parse_mode='HTML', reply_markup=markup)


def prepare_property_description(item):
    # Используйте значения напрямую без дополнительного кодирования/декодирования
    address = item.get('streetaddress', 'Не указано')
    description_text = item.get('description', 'Не указано')

    description = (
        f"<b>Тип жилья:</b> {item.get('typename', 'Не указано')}\n"
        f"<b>Адрес:</b> {address}\n"
        f"<b>Почтовый индекс:</b> {item.get('postalcode', 'Не указано')}\n"
        f"<b>Площадь (кв. метры):</b> {item.get('squaremeters',
                                                'Не указано')} кв.м.\n"
        f"<b>Месячная аренда (руб.):</b> {item.get(
            'monthlyrent', 'Не указано')} руб.\n"
        f"<b>Дневная аренда (руб.):</b> {item.get('dailyrent',
                                                  'Не указано')} руб.\n"
        f"<b>Ремонт:</b> {'да' if item.get('hasrenovation',
                                           False) else 'нет'}\n"
        f"<b>Расстояние до метро (км):</b> {item.get(
            'metroproximity', 'Не указано')} км.\n"
        f"<b>Этажей в доме:</b> {item.get('buildingfloors', 'Не указано')}\n"
        f"<b>Балкон:</b> {'да' if item.get('hasbalcony', False) else 'нет'}\n"
        f"<b>Парковка:</b> {'да' if item.get('hasparking',
                                             False) else 'нет'}\n"
        f"<b>Описание:</b> {description_text}\n"
        f"<b>Домашние животные:</b> {
            'да' if item.get('pets', False) else 'нет'}\n"
        f"<b>Контактная информация:</b> {
            item.get('contactinfo', 'Не указано')}\n"
    )
    return description
