import os
import requests
import datetime
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# Load credentials from .env
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP_NUMBER = os.getenv("FROM_WHATSAPP_NUMBER")
TO_WHATSAPP_NUMBER = os.getenv("TO_WHATSAPP_NUMBER")

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Define locations with lat/lon
LOCATIONS = {
    "Nairobi": (1.2921, 36.8219),
    "Ongata Rongai": (-1.3961, 36.7517),
    "Zimmerman": (1.2195, 36.8954),
}

# Get 3-hour forecast data for each location
def get_forecast_weather(latitude, longitude):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Analyze today's forecast blocks
def analyze_today_weather(forecast_data):
    today = datetime.datetime.utcnow().date()
    weather_counts = {}
    temps = []
    rain_expected = False

    for item in forecast_data.get("list", []):
        forecast_time = datetime.datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
        if forecast_time.date() != today:
            continue

        weather_main = item["weather"][0]["main"].lower()
        temps.append(item["main"]["feels_like"])
        weather_counts[weather_main] = weather_counts.get(weather_main, 0) + 1

        if any(term in weather_main for term in ["rain", "drizzle", "thunderstorm"]):
            rain_expected = True

    avg_temp = round(sum(temps) / len(temps), 1) if temps else "-"
    min_temp = round(min(temps), 1) if temps else "-"
    max_temp = round(max(temps), 1) if temps else "-"
    most_common_weather = max(weather_counts, key=weather_counts.get) if weather_counts else "unknown"

    return rain_expected, most_common_weather, avg_temp, min_temp, max_temp

# Build the final grouped weather message
def generate_weather_message():
    name = "Erick 😎"
    weather_groups = {}

    for location, (lat, lon) in LOCATIONS.items():
        data = get_forecast_weather(lat, lon)
        if not data:
            entry = f"{location} - Unable to fetch forecast data."
            advice = "No advice available."
            weather_groups.setdefault(advice, []).append(entry)
            continue

        rain, condition, avg_temp, min_temp, max_temp = analyze_today_weather(data)

        entry = f"{location} - Expect {condition} with temperatures between {min_temp}°C and {max_temp}°C (avg: {avg_temp}°C)."


        if rain:
            advice = "Don't forget your umbrella!☔⛈"
        elif "cloud" in condition or avg_temp < 20:
            advice = "It might be a bit gloomy today. Consider wearing a heavy jacket.🧥"
        elif avg_temp > 30:
            advice = "It's quite warm☀, stay hydrated!🥤"
        elif "clear" in condition:
            advice = "It's a clear day☁, wear a light jacket!"
        else:
            advice = "Weather looks normal today."

        weather_groups.setdefault(advice, []).append(entry)

    
    messages = [f"Good morning {name}\nHere's the weather summary update for today:"]
    for advice, entries in weather_groups.items():
        messages.extend(entries)
        messages.append(advice)

    return "\n\n".join(messages)


def send_whatsapp_message(message):
    try:
        msg = client.messages.create(
            body=message,
            from_=FROM_WHATSAPP_NUMBER,
            to=TO_WHATSAPP_NUMBER
        )
        print(f"✅ Message sent: {msg.sid}")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")


def main():
    if datetime.datetime.today().weekday() == 6:  # Sunday = 6
        print("Skipping weather update on Sunday.")
        return
    message = generate_weather_message()
    send_whatsapp_message(message)

if __name__ == "__main__":
    main()