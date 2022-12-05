import const as keys
import responses as R
import json
import asyncio
from telegram.ext import *

print("Bot started...")
messageReceivers = []


def start_command(update, context):
    update.message.reply_text("Type something random to get started!")

def getReceivers_command(update, context):
    for receiver in messageReceivers:
        update.message.reply_text(f"{receiver.first_name} {receiver.last_name} - {receiver.username} - {receiver.id}")


def help_command(update, context):
    update.message.reply_text(f"Die bas URL ist {context.bot.base_url}")

def addReceiver_command(update, context):
    msg = update.message
    messageReceivers.append(msg.from_user)

def handle_message(update, context):
    for receiver in messageReceivers:
        update.message.copy(receiver.id)

async def handle_documents(update, context):
    msg = update.message
    print(f"Download of {msg.document.file_name} started")
    await msg.document.get_file().download_to_drive()
    

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    application = Application.builder().token(keys.API_KEY).build()
    # updater = Updater(keys.API_KEY, use_context=True, base_url="http://192.168.43.53:8081/bot")
    # updater.bot.logOut();

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("addMe", addReceiver_command))
    application.add_handler(CommandHandler("getReceivers", getReceivers_command))
    # application.add_handler(MessageHandler(Filters.all, handle_message))
    application.add_handler(MessageHandler(filters.Document, handle_documents))
    application.add_error_handler(error)

    application.run_polling()
main()
