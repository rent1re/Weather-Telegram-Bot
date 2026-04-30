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
 
#  ФУНКЦИИ
def t(user_id: int, key: str) -> str:
    lang = user_lang.get(user_id, "ru")
    return TEXTS[lang].get(key, key)
 
 
def get_lang(user_id: int) -> str:
    return user_lang.get(user_id, "ru")
 
 
def get_wmo(code: int, lang: str):
    return WMO_CODES[lang].get(code, ("—", "🌡️"))
 
 
def wind_deg_to_dir(deg: float, lang: str) -> str:
    ru = ["С", "СВ", "В", "ЮВ", "Ю", "ЮЗ", "З", "СЗ"]
    en = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    dirs = ru if lang == "ru" else en
    return dirs[round(deg / 45) % 8]
 
 
def format_date(date_str: str, lang: str, full: bool = False) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    names = WEEKDAYS_FULL[lang] if full else WEEKDAYS_SHORT[lang]
    day_name = names.get(dt.strftime("%A"), dt.strftime("%A"))
    return f"{day_name}, {dt.strftime('%d.%m')}"
 
 
def uv_level(uv: float, lang: str) -> str:
    if uv <= 2:
        return TEXTS[lang]["uv_low"]
    elif uv <= 5:
        return TEXTS[lang]["uv_mid"]
    elif uv <= 7:
        return TEXTS[lang]["uv_high"]
    return TEXTS[lang]["uv_very_high"]

def get_coordinates(city: str, lang: str) -> dict | None:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": lang, "format": "json"}
    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("results"):
                res = data["results"][0]
                return {
                    "lat": res["latitude"],
                    "lon": res["longitude"],
                    "name": res["name"],
                    "country": res.get("country", ""),
                }
        return None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None
 
 
#  ЗАПРОСЫ К API
def get_current_weather(lat: float, lon: float) -> dict | None:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "current": [
            "temperature_2m", "apparent_temperature", "relative_humidity_2m",
            "wind_speed_10m", "wind_direction_10m", "weather_code",
            "surface_pressure", "cloud_cover", "precipitation", "uv_index"
        ],
        "timezone": "auto",
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        print(f"Weather error: {e}")
        return None
 
 
def get_forecast(lat: float, lon: float) -> dict | None:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "daily": [
            "temperature_2m_max", "temperature_2m_min", "weather_code",
            "precipitation_sum", "precipitation_probability_max",
            "wind_speed_10m_max", "uv_index_max", "sunrise", "sunset"
        ],
        "timezone": "auto",
        "forecast_days": 7,
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        print(f"Forecast error: {e}")
        return None
 
 
def get_history(lat: float, lon: float, date_str: str) -> dict | None:
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat, "longitude": lon,
        "start_date": date_str, "end_date": date_str,
        "daily": ["temperature_2m_max", "temperature_2m_min", "weather_code", "precipitation_sum", "wind_speed_10m_max"],
        "timezone": "auto",
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        print(f"History error: {e}")
        return None
    
#formatter

def format_current(data: dict, loc: dict, user_id: int) -> str:
    lang = get_lang(user_id)
    tx = TEXTS[lang]
    cur = data["current"]
    code = cur["weather_code"]
    condition, emoji = get_wmo(code, lang)
    wind_dir = wind_deg_to_dir(cur["wind_direction_10m"], lang)
    uv = cur.get("uv_index", 0) or 0
    now = datetime.now().strftime("%H:%M")
 
    text = (
        f"<b>{loc['name']}</b>  ·  {now}\n\n"
        f"{emoji} <b>{cur['temperature_2m']}°C</b>  —  {condition}\n"
        f"<i>{tx['feels_like']} {cur['apparent_temperature']}°C</i>\n\n"
        f"<code>"
        f"{tx['humidity']:<16}{cur['relative_humidity_2m']}%\n"
        f"{tx['wind']:<16}{cur['wind_speed_10m']} km/h {wind_dir}\n"
        f"{tx['cloud']:<16}{cur['cloud_cover']}%\n"
        f"{tx['pressure']:<16}{round(cur['surface_pressure'])} mbar\n"
        f"{tx['uv']:<16}{uv} — {uv_level(uv, lang)}"
        f"</code>"
    )
 
    if cur.get("precipitation", 0) > 0:
        text += f"\n<code>{tx['precip']:<16}{cur['precipitation']} mm</code>"
 
    return text
 
 
def format_day(data: dict, loc: dict, index: int, label: str, user_id: int) -> str:
    lang = get_lang(user_id)
    tx = TEXTS[lang]
    daily = data["daily"]
    date_str = daily["time"][index]
    code = daily["weather_code"][index]
    condition, emoji = get_wmo(code, lang)
    date_pretty = format_date(date_str, lang, full=True)
 
    sunrise = daily["sunrise"][index].split("T")[1] if daily.get("sunrise") else "—"
    sunset = daily["sunset"][index].split("T")[1] if daily.get("sunset") else "—"
 
    text = (
        f"<b>{label}</b>  ·  {date_pretty}\n\n"
        f"{emoji} <b>{daily['temperature_2m_max'][index]}°C</b> / {daily['temperature_2m_min'][index]}°C  —  {condition}\n\n"
        f"<code>"
        f"{tx['precip']:<16}{daily['precipitation_sum'][index]} mm\n"
        f"{tx['precip_prob']:<16}{daily['precipitation_probability_max'][index]}%\n"
        f"{tx['wind_max']:<16}{daily['wind_speed_10m_max'][index]} km/h\n"
        f"{tx['uv_max']:<16}{daily['uv_index_max'][index]}\n"
        f"{tx['sunrise']:<16}{sunrise}\n"
        f"{tx['sunset']:<16}{sunset}"
        f"</code>"
    )
    return text
 
 
def format_week(data: dict, loc: dict, user_id: int) -> str:
    lang = get_lang(user_id)
    tx = TEXTS[lang]
    daily = data["daily"]
    text = f"<b>{loc['name']}  ·  {tx['week_title']}</b>\n\n"
 
    for i, date_str in enumerate(daily["time"]):
        code = daily["weather_code"][i]
        condition, emoji = get_wmo(code, lang)
        date_pretty = format_date(date_str, lang)
        label = f"  <i>{tx['today']}</i>" if i == 0 else f"  <i>{tx['tomorrow_label']}</i>" if i == 1 else ""
        rain = daily["precipitation_probability_max"][i]
        rain_str = f"  ☔ {rain}%" if rain > 20 else ""
 
        text += (
            f"{emoji} <b>{date_pretty}</b>{label}\n"
            f"<code>{daily['temperature_2m_min'][i]}°C → {daily['temperature_2m_max'][i]}°C{rain_str}</code>\n"
            f"<i>{condition}</i>\n\n"
        )
    return text
 
 
def format_history(data: dict, loc: dict, date_str: str, user_id: int) -> str:
    lang = get_lang(user_id)
    tx = TEXTS[lang]
    daily = data["daily"]
    code = daily["weather_code"][0]
    condition, emoji = get_wmo(code, lang)
    date_pretty = format_date(date_str, lang, full=True)
 
    text = (
        f"<b>{tx['yesterday_label']}</b>  ·  {date_pretty}\n\n"
        f"{emoji} <b>{daily['temperature_2m_max'][0]}°C</b> / {daily['temperature_2m_min'][0]}°C  —  {condition}\n\n"
        f"<code>"
        f"{tx['precip']:<16}{daily['precipitation_sum'][0]} mm\n"
        f"{tx['wind_max']:<16}{daily['wind_speed_10m_max'][0]} km/h"
        f"</code>\n\n"
        f"<b>{loc['name']}</b>"
    )
    return text
 
 
#  Keyvoard, Buttons
def lang_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🇷🇺 Русский", callback_data="setlang|ru"),
        InlineKeyboardButton("🇬🇧 English", callback_data="setlang|en"),
    )
    return kb
 
 
def main_keyboard(city: str, user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(t(user_id, "btn_now"), callback_data=f"current|{city}"),
        InlineKeyboardButton(t(user_id, "btn_week"), callback_data=f"week|{city}"),
    )
    kb.add(
        InlineKeyboardButton(t(user_id, "btn_tomorrow"), callback_data=f"tomorrow|{city}"),
        InlineKeyboardButton(t(user_id, "btn_yesterday"), callback_data=f"yesterday|{city}"),
    )
    kb.add(
        InlineKeyboardButton(t(user_id, "btn_change_city"), callback_data="change_city"),
    )
    return kb
 
 
# ============================
#  HANDLERS
# ============================
@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(
        message.chat.id,
        TEXTS["ru"]["choose_lang"],
        reply_markup=lang_keyboard()
    )
 
 
@bot.message_handler(commands=["help"])
def cmd_help(message):
    bot.send_message(message.chat.id, t(message.from_user.id, "help"), parse_mode="HTML")
 
 
@bot.message_handler(commands=["lang"])
def cmd_lang(message):
    bot.send_message(
        message.chat.id,
        TEXTS["ru"]["choose_lang"],
        reply_markup=lang_keyboard()
    )
 
 
@bot.message_handler(func=lambda m: True)
def handle_city(message):
    user_id = message.from_user.id
    city = message.text.strip()
    lang = get_lang(user_id)
 
    loc = get_coordinates(city, lang)
    if not loc:
        bot.send_message(
            message.chat.id,
            t(user_id, "not_found").format(city),
            parse_mode="HTML"
        )
        return
 
    data = get_current_weather(loc["lat"], loc["lon"])
    if not data:
        bot.send_message(message.chat.id, t(user_id, "no_data"), parse_mode="HTML")
        return
 
    text = format_current(data, loc, user_id)
    bot.send_message(
        message.chat.id,
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard(city, user_id)
    )
 
 
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        user_id = call.from_user.id
        bot.answer_callback_query(call.id)
 
        if call.data.startswith("setlang|"):
            lang = call.data.split("|")[1]
            user_lang[user_id] = lang
            bot.edit_message_text(
                TEXTS[lang]["welcome"],
                call.message.chat.id,
                call.message.message_id,
                parse_mode="HTML"
            )
            return
 
        if call.data == "change_city":
            bot.send_message(call.message.chat.id, t(user_id, "change_city"))
            return
 
        action, city = call.data.split("|", 1)
        lang = get_lang(user_id)
 
        loc = get_coordinates(city, lang)
        if not loc:
            bot.send_message(call.message.chat.id, t(user_id, "city_not_found"))
            return
 
        loading_msg = bot.send_message(call.message.chat.id, t(user_id, "loading"))
 
        if action == "current":
            data = get_current_weather(loc["lat"], loc["lon"])
            text = format_current(data, loc, user_id) if data else t(user_id, "no_data")
 
        elif action == "week":
            data = get_forecast(loc["lat"], loc["lon"])
            text = format_week(data, loc, user_id) if data else t(user_id, "no_forecast")
 
        elif action == "tomorrow":
            data = get_forecast(loc["lat"], loc["lon"])
            if data and len(data["daily"]["time"]) >= 2:
                text = format_day(data, loc, index=1, label=t(user_id, "tomorrow_full"), user_id=user_id)
            else:
                text = t(user_id, "no_tomorrow")
 
        elif action == "yesterday":
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            data = get_history(loc["lat"], loc["lon"], yesterday)
            text = format_history(data, loc, yesterday, user_id) if data else t(user_id, "no_yesterday")
 
        else:
            text = t(user_id, "unknown_cmd")
 
        bot.delete_message(call.message.chat.id, loading_msg.message_id)
        bot.send_message(
            call.message.chat.id,
            text,
            parse_mode="HTML",
            reply_markup=main_keyboard(city, user_id)
        )
 
    except Exception as e:
        print(f"ОШИБКА: {e}")
        bot.send_message(call.message.chat.id, f"❌ Error: {e}")
 
 
#  ЗАПУСК
if __name__ == "__main__":
    print("🤖 Бот запущен!")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)