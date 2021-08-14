from coinbase.wallet.client import Client
from telegram import ParseMode
from telegram.ext import Defaults, Updater, PrefixHandler
from tracker import get_prices

COINBASE_KEY = 'Your Key'
COINBASE_SECRET = 'Your Key'
TELEGRAM_TOKEN = 'Your token'

coinbase_client = Client(COINBASE_KEY, COINBASE_SECRET)

BASE_CURRENCY = '-INR'


def startCommand(update, context):
    print('start')
    chat_id = update.effective_chat.id
    message = ""

    crypto_data = get_prices()
    for i in crypto_data:
        coin = crypto_data[i]["coin"]
        price = crypto_data[i]["price"]
        change_day = crypto_data[i]["change_day"]
        change_hour = crypto_data[i]["change_hour"]
        # message += f"Follow me on Github: vampirepapi :) \n"
        message += f"Coin: {coin}\nPrice: ₹{price:,.2f}\nHour Change: {change_hour:.3f}%\nDay Change: {change_day:.3f}%\n\n"

    context.bot.send_message(chat_id=chat_id, text=message)


def priceAlertCallback(context):
    crypto = context.job.context[0]
    sign = context.job.context[1]
    price = context.job.context[2]
    chat_id = context.job.context[3]

    send = False

    spot_price = coinbase_client.get_spot_price(
        currency_pair=crypto + BASE_CURRENCY)['amount']

    if sign == '<':
        if float(price) >= float(spot_price):
            send = True
    else:
        if float(price) <= float(spot_price):
            send = True

    if send:
        response = f'Hey!👋 {crypto} has surpassed ₹{price} and has just reached <b>₹{spot_price}</b> !'

        context.job.schedule_removal()

        context.bot.send_message(chat_id=chat_id, text=response)


def priceAlert(update, context):
    print('priceAlert', context)
    if len(context.args) > 2:
        crypto = context.args[0].upper()
        sign = context.args[1]
        price = context.args[2]

        context.job_queue.run_repeating(priceAlertCallback, interval=15, first=15, context=[
                                        crypto, sign, price, update.message.chat_id])

        response = f"⏳Notification Confirmed, will send you a message when the price of {crypto} reaches ₹{price} \n"
        response += f"Current price of {crypto} is ₹{coinbase_client.get_spot_price(currency_pair=crypto + BASE_CURRENCY)['amount']}"
        # response += f"Follow my creator on Github : Vampirepapi"

    else:
        response = '⚠️ Please provide a crypto code and a price value: \n<i>/price_alert {crypto code} {> / &lt;} {price}</i>'

    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


if __name__ == '__main__':
    defaults = Defaults(parse_mode=ParseMode.HTML,)
    updater = Updater(token=TELEGRAM_TOKEN,
                      use_context=True, defaults=defaults)
    dp = updater.dispatcher

    dp.add_handler(PrefixHandler('/', 'start', startCommand))
    dp.add_handler(PrefixHandler('/', 'alert', priceAlert))

    updater.start_polling()  # Start the bot
    updater.idle()