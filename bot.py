import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from datetime import datetime, timedelta


BOT_TOKEN = "8774276245:AAF5xLq0I1TQBqPijDydlo58WuO2KrVU4I4"
 
bot = telebot.TeleBot(BOT_TOKEN)
user_lang = {}  # {user_id: "ru" | "en"}
 
 
#  localisition

TEXTS = {
    "ru": {
        "choose_lang": "Выбери язык / Choose language:",
        "welcome": "👋 <b>Привет! Я бот погоды</b>\n\nНапиши название города и я покажу погоду.\nНапример: <b>Бишкек</b> или <b>London</b>",
        "help": (
            "📖 <b>Как пользоваться:</b>\n\n"
            "Напиши название города, затем выбери режим кнопками:\n\n"
            "<code>Сейчас</code>  — текущая погода\n"
            "<code>Неделя</code>  — прогноз на 7 дней\n"
            "<code>Завтра</code>  — погода на завтра\n"
            "<code>Вчера</code>   — погода вчера"
        ),
        "not_found": "❌ <b>Город «{}» не найден.</b>\n\nПопробуй написать по-другому или на английском.",
        "no_data": "❌ Не удалось получить данные о погоде.",
        "loading": "Загружаю...",
        "change_city": "Напиши название города:",
        "city_not_found": "❌ Город не найден.",
        "no_forecast": "❌ Не удалось получить прогноз.",
        "no_tomorrow": "❌ Не удалось получить прогноз на завтра.",
        "no_yesterday": "❌ Не удалось получить данные за вчера.",
        "unknown_cmd": "❌ Неизвестная команда.",
        "btn_now": "🌤 Сейчас",
        "btn_week": "📅 Неделя",
        "btn_tomorrow": "🌅 Завтра",
        "btn_yesterday": "⏪ Вчера",
        "btn_change_city": "🔄 Другой город",
        "feels_like": "Ощущается как",
        "humidity": "Влажность",
        "wind": "Ветер",
        "cloud": "Облачность",
        "pressure": "Давление",
        "uv": "UV",
        "precip": "Осадки",
        "precip_prob": "Вероятность",
        "wind_max": "Ветер макс",
        "uv_max": "UV макс",
        "sunrise": "Восход",
        "sunset": "Закат",
        "uv_low": "Низкий", "uv_mid": "Умеренный", "uv_high": "Высокий", "uv_very_high": "Очень высокий",
        "today": "сегодня", "tomorrow_label": "завтра",
        "week_title": "7 дней",
        "yesterday_label": "Вчера",
        "tomorrow_full": "Завтра",
        "geocoding_lang": "ru",
    },
    "en": {
        "choose_lang": "Выбери язык / Choose language:",
        "welcome": "👋 <b>Hello! I'm a weather bot</b>\n\nType a city name and I'll show you the weather.\nExample: <b>Bishkek</b> or <b>London</b>",
        "help": (
            "📖 <b>How to use:</b>\n\n"
            "Type a city name, then choose a mode:\n\n"
            "<code>Now</code>      — current weather\n"
            "<code>Week</code>     — 7-day forecast\n"
            "<code>Tomorrow</code> — tomorrow's weather\n"
            "<code>Yesterday</code>— yesterday's weather"
        ),
        "not_found": "❌ <b>City «{}» not found.</b>\n\nTry a different spelling.",
        "no_data": "❌ Failed to get weather data.",
        "loading": "Loading...",
        "change_city": "Type a city name:",
        "city_not_found": "❌ City not found.",
        "no_forecast": "❌ Failed to get forecast.",
        "no_tomorrow": "❌ Failed to get tomorrow's forecast.",
        "no_yesterday": "❌ Failed to get yesterday's data.",
        "unknown_cmd": "❌ Unknown command.",
        "btn_now": "🌤 Now",
        "btn_week": "📅 Week",
        "btn_tomorrow": "🌅 Tomorrow",
        "btn_yesterday": "⏪ Yesterday",
        "btn_change_city": "🔄 Change city",
        "feels_like": "Feels like",
        "humidity": "Humidity",
        "wind": "Wind",
        "cloud": "Cloud cover",
        "pressure": "Pressure",
        "uv": "UV",
        "precip": "Precipitation",
        "precip_prob": "Probability",
        "wind_max": "Max wind",
        "uv_max": "Max UV",
        "sunrise": "Sunrise",
        "sunset": "Sunset",
        "uv_low": "Low", "uv_mid": "Moderate", "uv_high": "High", "uv_very_high": "Very high",
        "today": "today", "tomorrow_label": "tomorrow",
        "week_title": "7 days",
        "yesterday_label": "Yesterday",
        "tomorrow_full": "Tomorrow",
        "geocoding_lang": "en",
    }
}
 
WMO_CODES = {
    "ru": {
        0: ("Ясно", "☀️"), 1: ("Преимущественно ясно", "🌤"), 2: ("Переменная облачность", "⛅"),
        3: ("Пасмурно", "☁️"), 45: ("Туман", "🌫️"), 48: ("Изморозь", "🌫️"),
        51: ("Лёгкая морось", "🌦️"), 53: ("Морось", "🌦️"), 55: ("Сильная морось", "🌧️"),
        61: ("Небольшой дождь", "🌧️"), 63: ("Дождь", "🌧️"), 65: ("Сильный дождь", "🌧️"),
        71: ("Небольшой снег", "❄️"), 73: ("Снег", "❄️"), 75: ("Сильный снег", "❄️"),
        77: ("Снежные зёрна", "🌨️"), 80: ("Ливень", "🌧️"), 81: ("Сильный ливень", "🌧️"),
        82: ("Очень сильный ливень", "⛈️"), 85: ("Снегопад", "❄️"), 86: ("Сильный снегопад", "❄️"),
        95: ("Гроза", "⛈️"), 96: ("Гроза с градом", "⛈️"), 99: ("Сильная гроза с градом", "⛈️"),
    },
    "en": {
        0: ("Clear sky", "☀️"), 1: ("Mainly clear", "🌤"), 2: ("Partly cloudy", "⛅"),
        3: ("Overcast", "☁️"), 45: ("Fog", "🌫️"), 48: ("Icy fog", "🌫️"),
        51: ("Light drizzle", "🌦️"), 53: ("Drizzle", "🌦️"), 55: ("Heavy drizzle", "🌧️"),
        61: ("Light rain", "🌧️"), 63: ("Rain", "🌧️"), 65: ("Heavy rain", "🌧️"),
        71: ("Light snow", "❄️"), 73: ("Snow", "❄️"), 75: ("Heavy snow", "❄️"),
        77: ("Snow grains", "🌨️"), 80: ("Rain shower", "🌧️"), 81: ("Heavy shower", "🌧️"),
        82: ("Violent shower", "⛈️"), 85: ("Snow shower", "❄️"), 86: ("Heavy snow shower", "❄️"),
        95: ("Thunderstorm", "⛈️"), 96: ("Thunderstorm w/ hail", "⛈️"), 99: ("Heavy thunderstorm", "⛈️"),
    }
}
 
WEEKDAYS_SHORT = {
    "ru": {"Monday": "Пн", "Tuesday": "Вт", "Wednesday": "Ср", "Thursday": "Чт", "Friday": "Пт", "Saturday": "Сб", "Sunday": "Вс"},
    "en": {"Monday": "Mon", "Tuesday": "Tue", "Wednesday": "Wed", "Thursday": "Thu", "Friday": "Fri", "Saturday": "Sat", "Sunday": "Sun"},
}
 
WEEKDAYS_FULL = {
    "ru": {"Monday": "Понедельник", "Tuesday": "Вторник", "Wednesday": "Среда", "Thursday": "Четверг", "Friday": "Пятница", "Saturday": "Суббота", "Sunday": "Воскресенье"},
    "en": {"Monday": "Monday", "Tuesday": "Tuesday", "Wednesday": "Wednesday", "Thursday": "Thursday", "Friday": "Friday", "Saturday": "Saturday", "Sunday": "Sunday"},
}
 