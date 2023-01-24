from flask import Flask
from flask import request
from flask import Response
from pytube import YouTube
import os
import requests

TOKEN = "" # Telegram Bot API Token (BotFather)

app = Flask(__name__)
 
def tel_parse_message(message):
    print("message-->",message)
    try:
        chat_id = message['message']['chat']['id']
        message_id = message['message']['message_id']
        txt = message['message']['text']
        print("chat_id-->", chat_id)
        print("message_id-->", message_id)
        print("txt-->", txt)

        return chat_id,txt
    except:
        print("NO text found-->>")
 
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
 
    return r

def tel_send_audio(chat_id, audio):
    url = f'https://api.telegram.org/bot{TOKEN}/sendAudio'
 
    payload = {
        'chat_id': chat_id,
        "audio": "https://swift-cows-speak-116-89-84-26.loca.lt/" + audio # port 5500 from open file directory to grab mp3 link

    }
 
    r = requests.post(url, json=payload)
 
    return r

 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        try:
            chat_id, txt = tel_parse_message(msg)
            print(len(txt.split(" ")))
            txt1 = txt.split(" ")[0]
            print(txt1)
            if txt1 == "/download" and len(txt.split(" ")) == 2:
                tel_send_message(chat_id, "Downloading...")
                yt = YouTube(txt.split(" ")[1])
                video = yt.streams.filter(only_audio=True).first()
                destination = '.'
                out_file = video.download(output_path=destination)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                print(out_file, new_file)
                yttitle = new_file[89 : len(new_file)]
                print(yttitle + " has been successfully downloaded.")
                tel_send_audio(chat_id, yttitle)
                tel_send_message(chat_id, yttitle + " has been downloaded successfully!")
                os.remove(new_file)
                print(yttitle + " has been successfully deleted")
            elif txt == "/help":
                tel_send_message(chat_id, "Welcome to the Youtube to MP3 Telegram Bot Documentation! Use /status to test the activity status of the bot, the bot should repond with 'Bot is Active!' if active. If the bot does not respond, it should most likely be offline. Use the /download <Youtube Link> to download your favourite songs to MP3 format. If download is spelt wrongly or if the youtube link has an additional space in it, the bot will not respond. If a non-existent youtube link is added, the bot would respond with an invalid link message. Hence, be sure to check for spelling!")
            elif txt == "/status":
                tel_send_message(chat_id, "Bot is Active!")
            elif txt1 == "/download":
                tel_send_message(chat_id, "Please input a youtube link after the command")
        except:
            print("index-->")
            tel_send_message(5097619817, "Invalid Link! Please try again")
        
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
    app.run(threaded=True, port='5500')