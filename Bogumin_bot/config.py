from dotenv import load_dotenv
import os


load_dotenv()


class Config:
    API_TOKEN_BOT = os.getenv("API_TOKEN_BOT")
    API_PROPERTIES = os.getenv("API_PROPERTIES")

    # Константы для клавиатур
    MOSCOW = 'Москва'
    KRASNOGORSK = 'Красногорск'
    NAHABINO = 'Нахабино'
    ALL_ADRESS = 'Во всех'
    PROPERTY = 'Недвижимость'
    HOUSE = 'Дом'
    APARTAMENT = 'Квартира'
    TYPE_RENT_DAILY = 'Арендная плата в день'
    SQUARE_METERS = 'Кол-во м²'
    BUILDING_FLOORS = 'Кол-во этажей'
    HAS_RENOVATION = 'Ремонт'
    HAS_BALCONY = 'Балкон'
    HAS_PARKING = 'Парковка'
    PETS = 'Домашние питомцы'
    BACK = 'Назад'
    GET_DATA = 'Поиск..'
