import os
import requests
import datetime
from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()

print("Loading environment variables...")
print(f"OPENWEATHER_API_KEY: {os.getenv('OPENWEATHER_API_KEY')}")
print(f"TWILIO_SID: {os.getenv('TWILIO_SID')}")
print(f"TWILIO_AUTH_TOKEN: {os.getenv('TWILIO_AUTH_TOKEN')}")
print(f"FROM_WHATSAPP_NUMBER: {os.getenv('FROM_WHATSAPP_NUMBER')}")
print(f"TO_WHATSAPP_NUMBER: {os.getenv('TO_WHATSAPP_NUMBER')}")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP_NUMBER = os.getenv("FROM_WHATSAPP_NUMBER")
TO_WHATSAPP_NUMBER = os.getenv("TO_WHATSAPP_NUMBER")


client= Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

LOCATIONS={
    "Nairobi":(1.2921, 36.8219),
    "kajiado":(-1.8520, 36.7763),
    "Ongata Rongai":(-1.3961, 36.7517),
    "Zimmerman":(1.2195, 36.8954),
}

def get_weather(latitude, longitude):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        # print(f"Weather data fetched successfully for coordinates: ({latitude}, {longitude})")
        # print(f"Response: {response.json()}")
        return response.json()
    else:
        return None
    
def generate_weather_message():
    weather_groups = {}
    name = f"Erick 😎"

    for location, (lat, lon) in LOCATIONS.items():
        weather_data = get_weather(lat, lon)
        temp = weather_data['main']["feels_like"]
        weather = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        rain = "rain" in weather_data['weather'][0]['main'].lower()
        cloudy = "clouds" in weather_data['weather'][0]['main'].lower()

        # Determine advice only
        if rain:
            advice = "Don't forget your umbrella!☔⛈️"
        elif cloudy or temp < 20:
            advice = "It might be a bit _gloomy_ today. Consider wearing a heavy jacket.🧥"
        elif temp > 30:
            advice = "It's quite _warm_☀️, stay hydrated!🥤"
        elif "clear" in weather.lower():
            advice = "It's a _clear_ day☁️, wear a light jacket!"
        else:
            advice = "Weather looks normal today."

        # Prepare entry
        entry = f"*{location}* - {weather} with a temperature of {temp}°C and humidity of {humidity}%."
        weather_groups.setdefault(advice, []).append(entry)

    # Build the final message
    messages = [f"Good morning {name}!\nHere's the weather update for today:"]
    for advice, entries in weather_groups.items():
        messages.extend(entries)
        messages.append(advice)

    return "\n\n".join(messages)

def send_whatsapp_message(message):
    try:
        message = client.messages.create(
            body=message,
            from_=FROM_WHATSAPP_NUMBER,
            to=TO_WHATSAPP_NUMBER
        )
        print(f"Message sent successfully: {message.sid}")
    except Exception as e:
        print(f"Failed to send message: {e}")
        


# schedule.every().day.at("06:10").do(lambda: send_whatsapp_message(generate_weather_message()))

def main():
    if datetime.datetime.today().weekday() == 6:
        return
    weather_message = generate_weather_message()
    send_whatsapp_message(weather_message)


if __name__ == "__main__":
    main()
    
    


