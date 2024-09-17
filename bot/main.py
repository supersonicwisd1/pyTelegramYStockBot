import os
import telebot
import yfinance as yf

API_KEY = os.getenv('API_KEY')

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['greet'])
def greet(message):
    """
    This function is to reply to message command
    'Greet' and respond with 'Hey! How are you doing?'
    This will reply to the particular message
    """
    bot.reply_to(message, "Hey! How are you doing?")

@bot.message_handler(commands=['hello'])
def hello(message):
    """
    This function sends 'Hello!' for every
    'hello' command 
    """
    bot.send_message(message.chat.id, "Hello!")

@bot.message_handler(commands=['wsb'])
def get_stock(message):
    response = ""
    stocks = ['gme', 'amc', 'nok']
    stock_data = []
    for stock in stocks:
        data = yf.download(tickers=stock, period='2d', interval='1d')
        data = data.reset_index()

# this keeps checking for message, probably every sec
bot.polling()