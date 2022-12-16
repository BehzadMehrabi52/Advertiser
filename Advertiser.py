from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, CallbackContext, ChatMemberHandler
from telegram import Update, Chat, ChatMember, ParseMode, ChatMemberUpdated
from cryptography.hazmat.primitives import serialization
import configparser
import rsa
import mysql.connector 
from mysql.connector import Error
import os

def botStart(update : Update, context : CallbackContext):
    if update.message.chat.type == 'private':
        startMessage = """
        Commands:
        /start : منوي اصلي
        /adv_list :  لیست تبلغات
        /adv_last : آخرین پیام
        /adv_show[:adv_id] : نمایش پیام
        /adv_ins[:adv_id:start_time:adv_count] : ایجاد تبلیغ در تمامی گروه ها
        /adv_ins_group[:adv_id:group_id:start_time:adv_count] : ایجاد تبلیغ در گروه خاص
        /adv_del[:adv_id] : حذف تبلیغ
        /about : درباره ...
        """
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=startMessage)

def botAdvList(update : Update, context : CallbackContext):
    if update.message.chat.type == 'private':
        groupList = "Groups:\n" #+botGroupList(context)
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=groupList)

def botAdvLast(update : Update, context : CallbackContext):
    if update.message.chat.type == 'private':
        groupList = "Groups:\n" #+botGroupList(context)
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=groupList)

def botAdvShow(update : Update, context : CallbackContext):
    if update.message.chat.type == 'private':
        groupList = "Groups:\n" #+botGroupList(context)
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=groupList)

def botAdvInsert(update : Update, context : CallbackContext):
    if update.message.chat.type == 'private':
        groupList = "Groups:\n" #+botGroupList(context)
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=groupList)

def botAdvInsertGroup(update : Update, context : CallbackContext):
    if update.message.chat.type == 'private':
        groupList = "Groups:\n" #+botGroupList(context)
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=groupList)

def botAdvDelete(update : Update, context : CallbackContext):
    if update.message.chat.type == 'private':
        groupList = "Groups:\n" #+botGroupList(context)
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=groupList)

def botAbout(update : Update, context : CallbackContext):
    if update.message.chat.type == 'private':
        aboutMessage = """
        مالک ربات : بهزاد مهرابي
        """
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=aboutMessage)

#def get_url():
#    contents = requests.get('https://random.dog/woof.json').json()
#    url = contents['url']
#    return url

#def bop(update : Update, context : CallbackContext):
#    url = get_url()
#    chat_id = update.message.chat_id
#    context.bot.send_photo(chat_id=chat_id, photo=url)

def messageHandler(update : Update, context : CallbackContext):
    if update.message.chat.type == 'private':
        groupList = "Unknown Command!"
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=groupList)
    else:
        print(update.message.text)

def memberOnJoin(update : Update, context : CallbackContext):
    #chat_id = update.message.chat_id
    #context.bot.send_message(chat_id=chat_id, text='WelCome')
    context.bot.delete_message(chat_id=update.message.chat_id,message_id=update.message.message_id)
    print("removed")

def memberOnLeft(update : Update, context : CallbackContext):
    #chat_id = update.message.chat_id
    #context.bot.send_message(chat_id=chat_id, text='WelCome')
    context.bot.delete_message(chat_id=update.message.chat_id,message_id=update.message.message_id)
    print("removed")
    
def main():
    cpass = configparser.RawConfigParser()
    cpass.read('config.data')
    if not cpass.has_section('Bot'):
        print("No BOT Information Found")
        os._exit(1)

    try:
        connection = mysql.connector.connect(host='localhost',
                                             db='advertiser',
                                             user='Advertiser'
                                             )
        
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.close()
            #key = cpass['Bot']['Key']
            #print(key)
            #privkey = rsa.PrivateKey.load_pkcs1(key)
            #print(private_key)
            #token = rsa.decrypt(cpass['Bot']['Token'], key).decode()
            token = cpass['Bot']['Token']
            #print(token)
            updater = Updater(token,use_context=True)
            dp = updater.dispatcher
            dp.add_handler(CommandHandler('start',botStart))
            dp.add_handler(CommandHandler('adv_list',botAdvList))
            dp.add_handler(CommandHandler('adv_last',botAdvLast))
            dp.add_handler(CommandHandler('adv_ins',botAdvInsert))
            dp.add_handler(CommandHandler('adv_ins_group',botAdvInsertGroup))
            dp.add_handler(CommandHandler('adv_del',botAdvDelete))
#           dp.add_handler(CommandHandler('bop',bop))
            dp.add_handler(MessageHandler(Filters.text, messageHandler))
            dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,memberOnJoin))
            dp.add_handler(MessageHandler(Filters.status_update.left_chat_member,memberOnLeft))
            updater.start_polling()
            updater.idle()

    except Error as e:
        print(e)
        print("Error while connecting to MySQL", e)
        os._exit(1)
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
            os._exit(1)


if __name__ == '__main__':
  main()

