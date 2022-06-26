import os
import telegram
from flask import Flask, request
from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

# Initial Flask app
app = Flask(__name__)


@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'


def hello(update: Update, context):
    update.message.reply_text('hello, {}'.format(update.message.from_user.first_name))


def start(update: Update, context):
    message = update.message
    chat = message['chat']
    update.message.reply_text(text='HI  ' + str(chat['id']) + ', I am ready to work.')   


def reply_handler(update: Update, context):
    """ default handler for messages """
    text = update.message.text
    update.message.reply_text(text)


# Configure token and id from environment variables
token = os.getenv('token', default=None)
bot = telegram.Bot(token=token)
user_id = os.getenv('user_id', default=None)
bot.send_message(chat_id=user_id, text='I am ready to work.')

# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message.
# For command handler
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('hello', hello))
# For this handler, it particular handle text message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))


if __name__ == "__main__":
    # Running server
    port = int(os.environ.get('PORT', 27017))
    app.run(host='0.0.0.0', port=port)
