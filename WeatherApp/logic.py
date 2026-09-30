from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import requests
import sys
from gui import *

class Logic(QMainWindow, Ui_MainWindow):

    API_KEY = "7c3daca392f38c0aa7c5fcc385aeb4d1"

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.button_search.clicked.connect(lambda: self.search())

    def search(self):
        city_name = self.input_city.text().strip()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&APPID={Logic.API_KEY}"
        website_response = requests.get(url)

        try:
            website_response.raise_for_status()
            weather_data = website_response.json()

            # Check response code
            match weather_data["cod"]:
                case 200:
                    self.display_weather(weather_data)
                case 404:
                    self.display_error(weather_data)
        except requests.exceptions.HTTPError as http_error:           # statuscode between 400 and 500
            match website_response.status_code:
                case 400:
                    self.display_error("400: Bad Request", "Check city name")
                case 401:
                    self.display_error("401: Unauthorized", "Invalid API key")
                case 403:
                    self.display_error("403: Forbidden", "Access denied")
                case 404:
                    self.display_error("404: Not Found", "City not found    ")
                case 500:
                    self.display_error("500: Internal Server Error", "Try again later")
                case 502:
                    self.display_error("502: Bad Gateway", "Service Unavailable")
                case 503:
                    self.display_error("503: Service Unavailable" , "Try again later")
                case 504:
                    self.display_error("504: Gateway Timeout", "No server response")
                case _:
                    self.display_error(f"HTTP Error", f"{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error", "Check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error", "Request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("TooManyRedirects Error", "Check URL")
        except requests.exceptions.RequestException as req_error:    # network or invalid url
            self.display_error("Request Error", f"{req_error}")

    def display_weather(self, city):
        self.label_temperature.setText(f"{city["main"]["temp"]:.0f} °F")
        self.label_image.setText(Logic.get_weather_emoji(city["weather"][0]["id"]))
        self.label_condition.setText(f"{city["weather"][0]["description"].title()}")

    def display_error(self, error, reason):
        self.label_temperature.setText(error)
        self.label_image.setText("🚫")
        self.label_condition.setText(reason)

    @staticmethod
    def get_weather_emoji(icon_code):
        icon_code = int(icon_code)
        if 200 <= icon_code <= 232:
            return "⛈️"
        elif 300 <= icon_code <= 321:
            return "️🌧️"
        elif 500 <= icon_code <= 531:
            return "🌦️"
        elif 600 <= icon_code <= 622:
            return "❄️"
        elif 701 <= icon_code <= 781:
            return "🌪️"
        elif icon_code == 800:
            return "☀️"
        elif 801 <= icon_code <= 804:
            return "🌤️"
        else:
            return "🚫"