from flask import Flask
from threading import Thread
from main import bot
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")

app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
    app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
bot.run(DISCORD_API_SECRET,root_logger=True)