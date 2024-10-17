from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
import requests
from kivymd.uix.screenmanager import *
from settings import*
from kivymd.uix.card import MDCard

class WScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city = "Володимир-Волинський"

    def get_weather(self,city):
        params = {
            "q": city,
            "appid": API_KEY,
        }
        data = requests.get(CURRENT_WEATHER_URL,params)
        response = data.json()
        print(response)
        return response
    def search(self):
        
        self.city = self.ids.city.text
        weather = self.get_weather(self.city)

        temp =  weather["main"]["temp"]
        self.ids.temp.text = f"Температура:{round(temp)}°C"


        humidity =  weather["main"]["humidity"]
        self.ids.humidity.text = f"Вологість:{round(humidity)}%"



        descr =  weather["weather"][0]["description"]
        self.ids.descr.text = f"{descr}"

        feels_like =  weather["main"]["feels_like"]
        self.ids.feel.text = f"Відчувається як:{round(feels_like)}°C"

        wind =  weather["wind"]["speed"]
        self.ids.wind.text = f"Вітер:{wind} м/с"     

        icon =  weather["weather"][0]["icon"]
        self.ids.icon.source = f'https://openweathermap.org/img/wn/{icon}@2x.png'

    def show_forecast(self):
        forecast_data = self.forecast.get_forecast(self.city)
        self.forecast.show_forecast(forecast_data)
        self.manager.transition.direction = 'left'
        self.manager.current = 'forecast'
        

class WeatherCard(MDCard):
    def __init__(self,weather, *args, **kwargs):
        super().__init__(*args, **kwargs)
        temp =  weather["main"]["temp"]
        self.ids.temp.text = f"Температура:{round(temp)}°C"
        icon =  weather["weather"][0]["icon"]
        self.ids.icon.source = f'https://openweathermap.org/img/wn/{icon}@2x.png'
        descr =  weather["weather"][0]["description"]
        self.ids.descr.text = f"{descr}"

        


    




class FScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_forecast(self,city):
        params = {
            "q": city,
            "appid": API_KEY,
        }
        data = requests.get(FORECAST_WEATHER_URL,params)
        response = data.json()
        print(response)
        return response["list"]
    
    def show_forecast(self,forecast):
        for data in forecast:
            card =  WeatherCard(data)
            self.ids.weather_list.add_widget(card)

    
    def back(self):
        self.manager.transition.direction = "right"
        self.manager.current = 'home'


class WReportApp(MDApp):
    def build(self):
        Builder.load_file("style.kv")
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        sm = MDScreenManager()
        self.weather_screen = WScreen(name = "home")
        self.forecast_screen = FScreen(name = "forecast")
        self.weather_screen.forecast = self.forecast_screen
        sm.add_widget(self.weather_screen)
        sm.add_widget(self.forecast_screen)
        return sm
        

WReportApp().run()
