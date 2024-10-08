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
def get_stocks(message):
    response = ""
    stocks = ['gme', 'amc', 'nok']
    stock_data = []
    for stock in stocks:
        data = yf.download(tickers=stock, period='5d', interval='1d')
        data = data.reset_index()
        response += f"-----{stock}-----\n"
        stock_data.append([stock])
        columns = ['stock']
        for index, row in data.iterrows():
            stock_position = len(stock_data) - 1
            price = round(row['Close'], 2)
            format_date = row['Date'].strftime('%m/%d')
            response += f"{format_date}: {price}\n"
            stock_data[stock_position].append(price)
            columns.append(format_date)
        print()

    response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
    for row in stock_data:
        response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
    response += "\nStock Data"
    print(response)
    bot.send_message(message.chat.id, response)

def stock_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() not in "price":
        return False
    else:
        return True

@bot.message_handler(func=stock_request)
def send_price(message):
    request = message.text.split()[1]
    data = yf.download(tickers=request, period='1d', interval='1h')
    if data.size > 0:
        data = data.reset_index()
        data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
        data.set_index('format_date', inplace=True)
        print(data.to_string())
        bot.send_message(message.chat.id, f"{request.capitalize()} STOCK DATA \n{data['Close'].to_string(header=False)}")
    else:
        bot.send_message(message.chat.id, "No data!?")

# this keeps checking for message, probably every sec
bot.polling()