from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, CallbackContext, ChatMemberHandler
from telegram import Bot,Update, Chat, ChatMember, ParseMode, ChatMemberUpdated
from cryptography.hazmat.primitives import serialization
import configparser
import rsa
import mysql.connector 
from mysql.connector import Error
import os
from threading import Event,Thread 

adv_bot = None

def DbConnect():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             db='advertiser',
                                             user='Advertiser',
                                             password='nXsCBUf5)zlD)bnG'
                                            )
        if not connection.is_connected():
            print("Could not connected to MySQL")
            stopFlag.set()
            os._exit(1)
    except Error as e:
        print("Error while connecting to MySQL", e)
        stopFlag.set()
        os._exit(1)
    return connection

def botStart(update : Update, context : CallbackContext):
    global adv_bot
    adv_bot = context.bot
    print('at start')
    print(adv_bot)
    #if update.message.chat.type == 'private':
    #    startMessage = """
    #    Commands:
    #    /start : منوي اصلي
    #    /adv_list :  لیست تبلغات
    #    /adv_last : آخرین پیام
    #    /adv_show[:adv_id] : نمایش پیام
    #    /adv_ins[:adv_id:start_time:adv_count] : ایجاد تبلیغ در تمامی گروه ها
    #    /adv_ins_group[:adv_id:group_id:start_time:adv_count] : ایجاد تبلیغ در گروه خاص
    #    /adv_del[:adv_id] : حذف تبلیغ
    #    /adv_stop : توقف تبلیغ دهنده
    #    /about : درباره ...
    #    """
    #    chat_id = update.message.chat_id
    #    context.bot.send_message(chat_id=chat_id, text=startMessage)

def botAdvListStr(recs):
    advs = ""
    for r in recs:
        advs = advs+"\nAdvId:"+str(r[1])+";StartTime:"+str(r[2])+";Count:"+str(r[3])+";Remain:"+str(r[4])+";Active:"+str(r[5])+";UserName:"+r[7]+";GroupName="+str(r[11])
    return advs


def botAdvList(update : Update, context : CallbackContext):
    if update.message.chat.type == 'private':
        connection = DbConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Advertise A LEFT JOIN Advertise_Group G ON G.Advertise_Id=A.Id;")
        recs = cursor.fetchall()
        cursor.close()
        connection.close()
        groupList = "Lists ("+str(len(recs))+")" + botAdvListStr(recs)
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
"""
def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def bop(update : Update, context : CallbackContext):
    url = get_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)
"""
def botAdvHandler(update : Update, context : CallbackContext):
    if update.message.chat.type == 'private':
        groupList = "Unknown Command!"
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=groupList)
    elif update.message.entities!=None and update.message.chat!=None:
        if update.message.chat.type=='group':
            if update.message.from_user!=None:
                if update.message.from_user.username=='Modern_Istanbul':
                    connection = DbConnect()
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM Bot_Groups WHERE Advertise_Group=1;")
                    adv_group = cursor.fetchone()
                    if adv_group!=None:
                        if update.message.chat.id == adv_group[1]: 
                            cursor.execute("INSERT INTO Advertise (Advertise_Id,Start_Time,Advertise_Count,Advertise_Remain,Active) VALUES (%s,CURRENT_TIMESTAMP,0,0,0);",[update.message.message_id])
                            connection.commit()
                    cursor.close()
                    connection.close()
                    """
                    if adv_group!=None:
                        connection = DbConnect()
                        cursor = connection.cursor()
                        cursor.execute("SELECT * FROM Bot_Groups WHERE Advertise_Group=0;")
                        adv_groups = cursor.fetchall()
                        for g in adv_groups:
                            context.bot.forward_message(g[1],adv_group[1],update.message.message_id)
                        cursor.close()
                        connection.close()
                    """

def memberOnJoin(update : Update, context : CallbackContext):
    #chat_id = update.message.chat_id
    #context.bot.send_message(chat_id=chat_id, text='WelCome')
    #context.bot.delete_message(chat_id=update.message.chat_id,message_id=update.message.message_id)
    if update.message.chat!=None:
        if update.message.chat.type=='group':
            if update.message.new_chat_members!=None:
                if update.message.new_chat_members[0]!=None:
                    if update.message.new_chat_members[0].username=='BM_Advertiser_Bot':
                        connection = DbConnect()
                        cursor = connection.cursor()
                        cursor.execute("INSERT INTO Bot_Groups (Group_Id,Group_Name,Advertise_Group) VALUES (%s,%s,0);",[update.message.chat.id,update.message.chat.title])
                        connection.commit()
                        cursor.close()
                        connection.close()

def memberOnLeft(update : Update, context : CallbackContext):
    #chat_id = update.message.chat_id
    #context.bot.send_message(chat_id=chat_id, text='WelCome')
    #context.bot.delete_message(chat_id=update.message.chat_id,message_id=update.message.message_id)
    if update.message.chat!=None:
        if update.message.chat.type=='group':
            if update.message.left_chat_member!=None:
                if update.message.left_chat_member.username=='BM_Advertiser_Bot':
                    connection = DbConnect()
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM Bot_Groups WHERE Group_Id = %s;",[update.message.chat.id])
                    connection.commit()
                    cursor.close()
                    connection.close()

def botAdvStop():
    stopFlag.set()

def botAdvTimer():
    print('at timer')
    print(adv_bot)
    if adv_bot!=None:
        print("job executing...")
        connection = DbConnect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Bot_Groups WHERE Advertise_Group=1;")
        adv_group = cursor.fetchone()
        if adv_group!=None:
            cursor.execute("SELECT * FROM Advertise A LEFT JOIN Advertise_Group G ON G.Advertise_Id=A.Id;")
            advs = cursor.fetchall()
            for adv in advs:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Bot_Groups WHERE Advertise_Group=0;")
                adv_groups = cursor.fetchall()
                for grp in adv_groups:
                    if adv[10]==None or adv[10]==grp[1]:
                        adv_bot.forward_message(grp[1],adv_group[1],adv[1])
            cursor.close()
            connection.close()
        print("job executed.")

def main():
    cpass = configparser.RawConfigParser()
    cpass.read('config.data')
    if not cpass.has_section('Bot'):
        print("No BOT Information Found")
        stopFlag.set()
        os._exit(1)

    """
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
    """
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
    dp.add_handler(CommandHandler('adv_stop',botAdvStop))
    #dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,memberOnJoin))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member,memberOnLeft))
    dp.add_handler(MessageHandler(Filters.all, botAdvHandler))
    updater.start_polling()
    updater.idle()

class BotAdvThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(2):
            botAdvTimer()

stopFlag = Event()
thread = BotAdvThread(stopFlag)
thread.start()

if __name__ == '__main__':
  main()

