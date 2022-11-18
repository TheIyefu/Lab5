import requests
import json
import datetime
from tabulate import tabulate
from tkinter import *
from PIL import Image

#question 1
r = requests.get("https://github.com/ITMOPython-2022/Lab-5")
print(f"1. {r}\n")

#question 2
def get_weather(city_name):
    api_key = '590260f28e26ef37fbb58452bd15161c'
    r = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={api_key}")
    data = r.json()
    lat = data[0]['lat']
    lon = data[0]['lon']
    r_city = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}")
    data_city = r_city.json()
    weather = f"{data_city['list'][0]['weather'][0]['main']}, {data_city['list'][0]['weather'][0]['description']}"
    humidity = data_city['list'][0]['main']['humidity']
    pressure = data_city['list'][0]['main']['pressure']
    return weather, humidity, pressure

city_name = 'Москва'
info_tuple = get_weather(city_name)
print(f"2. Информация о погоде в {city_name}\nОписание погоды: {info_tuple[0]}\nВлажность: {info_tuple[1]}\n"
      f"Давление: {info_tuple[2]}\n")

#question 3
def json_parse(url):
    r = requests.get(url)
    data = json.loads(r.text)

    datetime_str = data['Date']
    datetime_obj = datetime.datetime.fromisoformat(datetime_str)
    date = datetime_obj.date()

    len_currencies = len(data['Valute'])

    info_headers = ['валюта', 'название валюты', 'текущий курс обмена валюты', 'прошлый курс обмена валюты']
    info = []
    for currency in data['Valute']:
        info.append([currency, data['Valute'][currency]['Name'],data['Valute'][currency]['Value'], data['Valute'][currency]['Previous']])

    return info, info_headers, date, len_currencies

total_info = json_parse("https://www.cbr-xml-daily.ru/daily_json.js")
print(f"3. Информация, полученная из API обменного курса cbr.ru\nдата: {total_info[2]}\nколичество считаемой валюты: {total_info[3]}"
      f"\n{tabulate(total_info[0], headers=total_info[1])}")

#Допзадание
def cat_display():
    window = Tk()
    window.title("Random Key Generator")
    window.geometry('800x600')

    r = requests.get('https://aws.random.cat/meow')
    img_data = r.json()['file']
    img  = Image.open(requests.get(img_data, stream=True).raw)
    img = img.save("cats.png")

    cat_image = PhotoImage(file='cats.png')
    cats = Label(window, image=cat_image)
    cats.place(x=0, y=0)

    def change():
        global cat_image
        r = requests.get('https://aws.random.cat/meow')
        img_data = r.json()['file']
        img = Image.open(requests.get(img_data, stream=True).raw)
        img = img.save("cats.png")

        cat_image = PhotoImage(file='cats.png')
        cats.configure(image=cat_image)

    b = Button(window, text="Смените имидж", font=("Arial", 15), command=change)
    b.grid(row=5, column=3)

    window.mainloop()

cat_display()