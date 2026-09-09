# Weather CLI

A simple Python command-line tool to check the weather for any city, right from your terminal.

## Features

- Current weather for any city (temperature, humidity, wind speed)
- 5-day forecast displayed as a table
- Clean, colorful terminal output powered by `rich`
- Lightweight — no configuration files needed

## Installation

```bash
git clone https://github.com/your-username/weather-cli.git
cd weather-cli
pip install -r requirements.txt
```

## API Key

This project uses the free [OpenWeatherMap](https://openweathermap.org/api) API.

1. Create a free account at [openweathermap.org](https://openweathermap.org/api)
2. Copy your API key
3. Open `weather.py` and replace this line:

```python
API_KEY = "YOUR_API_KEY_HERE"
```

with your own key.

## Usage

Get the current weather:

```bash
python weather.py "Baku"
```

Get the 5-day forecast:

```bash
python weather.py "Baku" --forecast
```

## 🛠️ Built With

- Python 3
- [requests](https://pypi.org/project/requests/) — for making API calls
- [rich](https://pypi.org/project/rich/) — for beautiful terminal output

## Roadmap

- [ ] Compare weather across multiple cities at once
- [ ] Export results to CSV/JSON
- [ ] Plot temperature trends with matplotlib

## License

MIT
