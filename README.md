# Weather App

A simple weather application that fetches and displays current weather information for any city using a public weather API.

## Features

- Search for current weather by city name
- Displays temperature, humidity, wind speed, and weather conditions
- Responsive and user-friendly interface

## How It Works

1. **Enter a City:**  
    Gets the city Locations and Sent to OpenWeatherMap.

2. **Fetch Weather Data:**  
    The app sends a request to a weather API (such as OpenWeatherMap) to retrieve current weather data for the specified city.

3. **Display Results:**  
    The app displays the temperature, humidity, wind speed, and a brief description of the weather.

## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/E-Rick-M/weather.git
    cd weather
    ```

2. Install dependencies:  
    If you have a `pyproject.toml` file, run:
    ```bash
    uv pip install -r requirements.txt
    ```
    Or, to add new dependencies:
    ```bash
    uv add <package-name>
    ```

3. Add your API key:  
    Create a `.env` file and add your weather API key:
    ```
    OPENWEATHER_API_KEY=your_api_key_here
    TWILIO_SID=your_api_key_here
    TWILIO_AUTH_TOKEN=your_api_key_here
    FROM_WHATSAPP_NUMBER=your_api_key_here
    TO_WHATSAPP_NUMBER=your_api_key_here
    ```

4. Start the app:
    ```bash
    uv run main.py
    ```

## Technologies Used

- Python
- [OpenWeatherMap API](https://openweathermap.org/api)

## License

This project is licensed under the MIT License.