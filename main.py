import telebot
import requests
from datetime import datetime

bot = telebot.TeleBot("1073733205:AAEpRjMOZivEvvQSstDyV-q5whd41nLslDA")


def upload_image(image_url):
    return requests.get(image_url).content


@bot.message_handler(commands=['apod'])
def send_apod(message):
    try:
        date = message.text.replace("/apod", "").replace(" ", "")
        if date == "":
            date = datetime.today().strftime('%Y-%m-%d')
        data = requests.get("https://api.nasa.gov/planetary/apod?api_key=xG24VpzI1N9vyG2hcMvDVrlMpncePGSj6UPOMPtM&date="+date)
        image = upload_image(data.json()['url'])
        title = data.json()['title']
        bot.send_message(message.chat.id, title)
        bot.send_photo(message.chat.id, image)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "We have some problems. We are sorry!")


@bot.message_handler(commands=['mars_photos'])
def send_mars_rover_photos(message):
    try:
        page = message.text.replace("/mars_photos", "").replace(" ", "")
        if page == "":
            page = "1"
        data = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&page="+page+"&api_key=xG24VpzI1N9vyG2hcMvDVrlMpncePGSj6UPOMPtM")
        for photo in data.json()['photos']:
            image = upload_image(photo['img_src'])
            bot.send_photo(message.chat.id, image)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "We have some problems. We are sorry!")


@bot.message_handler(commands=['search_files'])
def send_files(message):
    try:
        search_text = message.text.replace("/search_files", "").replace(" ", "")
        data = requests.get("https://images-api.nasa.gov/search?q=" + search_text)
        for item in data.json()['collection']['items'][:5]:
            image = upload_image(item['links'][0]['href'])
            bot.send_photo(message.chat.id, image)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "We have some problems. We are sorry!")


bot.polling()
