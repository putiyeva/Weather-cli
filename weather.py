"""
Weather CLI - A simple tool to check the weather from your terminal.

Usage:
    python weather.py "Baku"
    python weather.py "Istanbul" --forecast
"""

import argparse
import sys
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

API_KEY = "YOUR_API_KEY_HERE"  # Get a free key at https://openweathermap.org/api
BASE_URL = "https://api.openweathermap.org/data/2.5"

console = Console()


def get_current_weather(city: str):
    """Fetch the current weather data for a given city."""
    url = f"{BASE_URL}/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "en"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        console.print(f"[bold red]Error:[/bold red] City '{city}' not found.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Network error:[/bold red] {e}")
        sys.exit(1)


def get_forecast(city: str):
    """Fetch the 5-day weather forecast for a given city."""
    url = f"{BASE_URL}/forecast"
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "en"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)


def show_current(data: dict):
    """Display the current weather data in a nicely formatted panel."""
    city = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"].capitalize()
    wind_speed = data["wind"]["speed"]

    text = (
        f"[bold cyan]{city}, {country}[/bold cyan]\n\n"
        f"🌡️  Temperature: [bold]{temp}°C[/bold] (feels like {feels_like}°C)\n"
        f"☁️  Condition: {description}\n"
        f"💧 Humidity: {humidity}%\n"
        f"💨 Wind speed: {wind_speed} m/s"
    )

    console.print(Panel(text, title="Weather Report", box=box.ROUNDED, expand=False))


def show_forecast(data: dict, city: str):
    """Display the 5-day forecast as a table."""
    table = Table(title=f"5-Day Forecast for {city}", box=box.SIMPLE_HEAD)
    table.add_column("Date / Time", style="cyan")
    table.add_column("Temperature", justify="right")
    table.add_column("Condition", justify="left")

    # The API returns data in 3-hour steps, so we take every 4th entry (~once a day)
    for entry in data["list"][::4]:
        dt_text = entry["dt_txt"]
        temp = entry["main"]["temp"]
        desc = entry["weather"][0]["description"].capitalize()
        table.add_row(dt_text, f"{temp}°C", desc)

    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="Check the weather from your terminal.")
    parser.add_argument("city", help="Name of the city (e.g. Baku, Istanbul, London)")
    parser.add_argument(
        "--forecast", action="store_true", help="Show the 5-day forecast"
    )
    args = parser.parse_args()

    if API_KEY == "YOUR_API_KEY_HERE":
        console.print(
            "[bold yellow]Warning:[/bold yellow] No API key set. "
            "Please set the API_KEY variable in weather.py."
        )
        sys.exit(1)

    if args.forecast:
        data = get_forecast(args.city)
        show_forecast(data, args.city)
    else:
        data = get_current_weather(args.city)
        show_current(data)


if __name__ == "__main__":
    main()
