#!/usr/bin/env python
# pylint: disable=C0116,W0613

import logging
from typing import List

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from comandos.justificante import genera_justificante

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!. Soy el profesor bot, ¿Cómo puedo ayudarte\?',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def justificante(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text("Procesando el justificante")
    args=update.message.text.split(';')
    
    nombre = args[0].replace('/justificante ','')
    profe = args[1]
    dni = args[2]
    hInit = args[3]
    hFin = args[4]
    dia = args[5]
    
    file=genera_justificante(nombre,dni,hInit,hFin,dia,profe)

    context.bot.sendDocument(chat_id=update.message.chat_id, document=open('./'+file, 'rb'))


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5093419260:AAGqIgccppz2vt-ygOdoz0CtmFPvWnWgpNk")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start, Filters.user(username="@jagalindo")))
    dispatcher.add_handler(CommandHandler("help", help_command,Filters.user(username="@jagalindo")))

    dispatcher.add_handler(CommandHandler("justificante", justificante, Filters.user(username="@jagalindo")))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()