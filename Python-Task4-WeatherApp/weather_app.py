import tkinter as tk
from tkinter import messagebox
import requests
import os
from io import BytesIO

from dotenv import load_dotenv
from PIL import Image, ImageTk


# Load API key from .env file
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Start with Celsius
unit = "metric"

# Keep images in memory
weather_icon = None


def get_weather():
    global weather_icon

    city = city_entry.get().strip()

    # Check empty input
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    if not API_KEY:
        messagebox.showerror(
            "Error",
            "API key not found. Please check your .env file."
        )
        return

    # Current weather API
    weather_url = "https://api.openweathermap.org/data/2.5/weather"

    weather_params = {
        "q": city,
        "appid": API_KEY,
        "units": unit
    }

    try:
        response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        # Handle common API errors
        if response.status_code == 404:
            messagebox.showerror(
                "Error",
                "City not found. Please check the city name."
            )
            return

        if response.status_code == 401:
            messagebox.showerror(
                "Error",
                "Invalid API key."
            )
            return

        response.raise_for_status()

        data = response.json()

        # Current weather information
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        icon_code = data["weather"][0]["icon"]

        temperature_unit = "°C" if unit == "metric" else "°F"
        wind_unit = "m/s" if unit == "metric" else "mph"

        # Display current weather
        result_label.config(
            text=(
                f"Temperature: {temperature:.1f} {temperature_unit}\n"
                f"Humidity: {humidity}%\n"
                f"Condition: {condition.title()}\n"
                f"Wind Speed: {wind_speed:.1f} {wind_unit}"
            )
        )

        # Load weather icon
        icon_url = (
            f"https://openweathermap.org/img/wn/"
            f"{icon_code}@2x.png"
        )

        icon_response = requests.get(
            icon_url,
            timeout=10
        )

        icon_image = Image.open(
            BytesIO(icon_response.content)
        )

        icon_image = icon_image.resize((90, 90))

        weather_icon = ImageTk.PhotoImage(icon_image)

        icon_label.config(image=weather_icon)

        # Get forecast
        get_forecast(city)

    except requests.exceptions.Timeout:
        messagebox.showerror(
            "Error",
            "The request timed out. Please try again."
        )

    except requests.exceptions.ConnectionError:
        messagebox.showerror(
            "Error",
            "Unable to connect to the weather service."
        )

    except requests.exceptions.RequestException:
        messagebox.showerror(
            "Error",
            "Something went wrong while getting weather data."
        )

    except (KeyError, ValueError):
        messagebox.showerror(
            "Error",
            "The weather data could not be read."
        )


def get_forecast(city):
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    forecast_params = {
        "q": city,
        "appid": API_KEY,
        "units": unit
    }

    try:
        response = requests.get(
            forecast_url,
            params=forecast_params,
            timeout=10
        )

        if response.status_code != 200:
            return

        data = response.json()

        # Clear old forecast
        for widget in forecast_frame.winfo_children():
            widget.destroy()

        temperature_unit = "°C" if unit == "metric" else "°F"

        # -----------------------------
        # Next 6 hours
        # -----------------------------

        hourly_title = tk.Label(
            forecast_frame,
            text="Next 6 Hours",
            font=("Arial", 14, "bold")
        )

        hourly_title.pack(pady=10)

        hourly_data = data["list"][:2]

        for item in hourly_data:
            time_text = item["dt_txt"][11:16]
            temp = item["main"]["temp"]
            description = item["weather"][0]["description"]

            hourly_label = tk.Label(
                forecast_frame,
                text=(
                    f"{time_text}  |  "
                    f"{temp:.1f}{temperature_unit}  |  "
                    f"{description.title()}"
                ),
                font=("Arial", 10)
            )

            hourly_label.pack()

        # -----------------------------
        # Next 5 days
        # -----------------------------

        daily_title = tk.Label(
            forecast_frame,
            text="5-Day Forecast",
            font=("Arial", 14, "bold")
        )

        daily_title.pack(pady=(15, 10))

        # Select one forecast entry per day
        days_seen = set()
        daily_items = []

        for item in data["list"]:
            date = item["dt_txt"].split(" ")[0]

            if date not in days_seen:
                days_seen.add(date)
                daily_items.append(item)

            if len(daily_items) == 5:
                break

        for item in daily_items:
            date = item["dt_txt"].split(" ")[0]
            temp = item["main"]["temp"]
            description = item["weather"][0]["description"]

            daily_label = tk.Label(
                forecast_frame,
                text=(
                    f"{date}  |  "
                    f"{temp:.1f}{temperature_unit}  |  "
                    f"{description.title()}"
                ),
                font=("Arial", 10)
            )

            daily_label.pack(pady=2)

    except requests.exceptions.RequestException:
        messagebox.showerror(
            "Error",
            "Unable to load forecast data."
        )


def change_unit():
    global unit

    if unit == "metric":
        unit = "imperial"
        unit_button.config(text="Switch to °C")
    else:
        unit = "metric"
        unit_button.config(text="Switch to °F")

    # Refresh weather if city is already entered
    if city_entry.get().strip():
        get_weather()


# ---------------------------------------
# Create main window
# ---------------------------------------

window = tk.Tk()

window.title("Weather App")
window.geometry("600x750")

window.resizable(False, False)


# ---------------------------------------
# Title
# ---------------------------------------

title_label = tk.Label(
    window,
    text="Weather App",
    font=("Arial", 26, "bold")
)

title_label.pack(pady=20)


# ---------------------------------------
# City input
# ---------------------------------------

city_label = tk.Label(
    window,
    text="Enter City Name:",
    font=("Arial", 12)
)

city_label.pack()


city_entry = tk.Entry(
    window,
    width=30,
    font=("Arial", 14)
)

city_entry.pack(pady=10)


# ---------------------------------------
# Get Weather button
# ---------------------------------------

weather_button = tk.Button(
    window,
    text="Get Weather",
    font=("Arial", 12),
    command=get_weather
)

weather_button.pack(pady=8)


# ---------------------------------------
# Celsius / Fahrenheit button
# ---------------------------------------

unit_button = tk.Button(
    window,
    text="Switch to °F",
    font=("Arial", 11),
    command=change_unit
)

unit_button.pack(pady=5)


# ---------------------------------------
# Weather icon
# ---------------------------------------

icon_label = tk.Label(window)

icon_label.pack(pady=5)


# ---------------------------------------
# Current weather result
# ---------------------------------------

result_label = tk.Label(
    window,
    text="Enter a city to see the weather.",
    font=("Arial", 13),
    justify="left"
)

result_label.pack(pady=10)


# ---------------------------------------
# Forecast area
# ---------------------------------------

forecast_frame = tk.Frame(window)

forecast_frame.pack(pady=10)


# Start application
window.mainloop()