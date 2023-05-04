import const as keys
import responses as R
import json
import asyncio
from telegram import Update
from telegram.ext import *
import os
import subprocess
import re

print("Bot started...")
# messageReceivers = ["713224638","1794172761","5571326730"]
messageReceivers = []

async def getReceivers_command(update, context):
    for receiver in messageReceivers:
        await update.message.reply_text(f"{receiver.first_name} {receiver.last_name} - {receiver.username} - {receiver.id}")

async def help_command(update, context):
    await update.message.reply_text(f"Die bas URL ist {context.bot.base_url}")

async def addReceiver_command(update, context):
    msg = update.message
    messageReceivers.append(msg.from_user)
    #print(msg)

async def handle_message(update, context):
    for receiver in messageReceivers:
        await update.message.copy(receiver)

"""
async def handle_documents(update: Update, context: CallbackContext):
    msg = update.message
    # print(msg)
    # print(f"Download of {msg.document.file_name} started")
    file = await msg.document.get_file(read_timeout=3600)
    print(file)
    old_name = file.file_path
    new_name = os.path.dirname(os.path.abspath(old_name)) + "/" + msg.document.file_name.replace(" ", "_") 
    x = re.search(r"part([0-9])*.rar|zip.([0-9])*$", txt)

    if (not x) or (x and x.group(1) == "1"):
        #os.rename(old_name, new_name)
        bashCommand = f"atool -x {new_name}"
        print(bashCommand)

        x = re.search(r"(.*)\.(?:part|zip.)(([0-9])*)(?:.rar$|$)", new_name)

        if x.group(1) in volumes:
            volumes[x.group(1)][x.group(3)] = new_name       
        else:
            volumes[x.group(1)] = {x.group(3):new_name}
              
        if "1" in volumes[x.group(1)]:
            print("extract")
        else:
            print("wait")

        #process = subprocess.Popen(['unrar','x',new_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #output, error = process.communicate()
        #print(output)
        #print(error)
""" 
def error(update, context):
    print(f"Update {update} caused error {context.error}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def main():
    print("main")
    application = Application.builder().token(keys.API_KEY).build()
    application = Application.builder().base_url("http://192.168.43.53:8081/bot").token(keys.API_KEY).build()
    # updater = Updater(keys.API_KEY, use_context=True, base_url="http://192.168.43.53:8081/bot")
    # updater.bot.logOut();

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("addMe", addReceiver_command))
    application.add_handler(CommandHandler("getReceivers", getReceivers_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_message))
    #application.add_handler(MessageHandler(filters.Document.ALL, handle_documents))
    application.add_error_handler(error)

    application.run_polling()
    # await application.bot.logOut()
    # print("logged out")
main()
# loop = asyncio.get_event_loop()
# tasks = [
#     loop.create_task(main()),
# ]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()
