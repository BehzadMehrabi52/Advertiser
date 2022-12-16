from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, CallbackContext, ChatMemberHandler
from telegram import Bot,Update, Chat, ChatMember, ParseMode, ChatMemberUpdated
from cryptography.hazmat.primitives import serialization
import configparser
import rsa
import mysql.connector 
from mysql.connector import Error
import os
from threading import Timer  
from datetime import datetime,timedelta

timer = None

def DbConnect():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             db='advertiser',
                                             user='Advertiser',
                                             password='nXsCBUf5)zlD)bnG'
                                            )
        if not connection.is_connected():
            print("Could not connected to MySQL")
            if timer!=None:
                timer.cancel()
            os._exit(1)
    except Error as e:
        print("Error while connecting to MySQL", e)
        if timer!=None:
            timer.cancel()
        os._exit(1)
    return connection

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
        /adv_start : راه اندازی تبلیغ دهنده
        /adv_stop : توقف تبلیغ دهنده
        /about : درباره ...
        """
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=startMessage)

def botAdvStr(r):
    adv = "Id:"+str(r[0])+";Start:"+str(r[1])+";Count:"+str(r[2])+";Remain:"+str(r[3])+";Next:"+str(r[4])+";Period:"+str(r[5])+";Groups:"+str(r[6])+";UserName:"+r[7]+";Active:"+str(r[8])
    return adv

def botAdvListStr(recs):
    advs = ""
    for r in recs:
        advs = advs+"\n"+botAdvStr(r)
    return advs

def botAdvList(update : Update, context : CallbackContext):
    if update.message.chat.type == 'private':
        connection = DbConnect()
        cursor = connection.cursor()
        cursor.execute("""
                        SELECT A.Advertise_Id,A.Start_Time,A.Advertise_Count,
                            IFNULL(min(R.Advertise_Remain),A.Advertise_Count) As Advertise_Remain,
                            IFNULL(max(R.Advertise_NextRun),A.Start_Time) As Advertise_NextRun,
                            A.Advertise_Period,
                            IFNULL(GROUP_CONCAT(G.Group_Name SEPARATOR ','),"ALL GROUPS") Groups, 
                            A.User_Name,A.Active
                        FROM Advertise A 
                            LEFT JOIN Advertise_Group G ON G.Advertise_Id=A.Id 
                            LEFT JOIN Advertise_Runs R ON R.Advertise_Id=A.Id 
                        WHERE A.Active=1
                        GROUP By Advertise_Id;
                       """)
        recs = cursor.fetchall()
        cursor.close()
        connection.close()
        advList = "Lists ("+str(len(recs))+")" + botAdvListStr(recs)
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=advList)

def botAdvLast(update : Update, context : CallbackContext):
    if update.message.chat.type == 'private':
        connection = DbConnect()
        cursor = connection.cursor()
        cursor.execute("""
                        SELECT A.Advertise_Id,A.Start_Time,A.Advertise_Count,
                            IFNULL(min(R.Advertise_Remain),A.Advertise_Count) As Advertise_Remain,
                            IFNULL(max(R.Advertise_NextRun),A.Start_Time) As Advertise_NextRun,
                            A.Advertise_Period,
                            IFNULL(GROUP_CONCAT(G.Group_Name SEPARATOR ','),"ALL GROUPS") Groups, 
                            A.User_Name,A.Active
                        FROM Advertise A 
                            LEFT JOIN Advertise_Group G ON G.Advertise_Id=A.Id 
                            LEFT JOIN Advertise_Runs R ON R.Advertise_Id=A.Id 
                        WHERE A.Active=1
                        GROUP By Advertise_Id;
                       """)
        recs = cursor.fetchall()
        cursor.close()
        connection.close()
        if len(recs)>0:
            adv = botAdvStr(recs[len(recs)-1])
            chat_id = update.message.chat_id
            context.bot.send_message(chat_id=chat_id, text=adv)

"""
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
"""

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
                            cursor.execute("INSERT INTO Advertise (Advertise_Id,Start_Time,Advertise_Count,Active_Period,Active,User_Id,User_Name) VALUES (%s,CURRENT_TIMESTAMP,0,24,0,0,'');",[update.message.message_id])
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

def botAdvRun(connection,cursor,cur_time,Advertise_Id,Advertise_Remain,Advertise_Period,Group_Id,Group_Name):
    adv_remain = Advertise_Remain - 1
    if adv_remain<0:
        adv_remain = 0
    adv_next_run = cur_time + timedelta(seconds=1.5*Advertise_Period) #timedelta(hours=Advertise_Period) 
    cursor.execute("INSERT INTO Advertise_Runs (Advertise_Id,Advertise_Remain,Advertise_NextRun,Group_Id,Group_Name) VALUES (%s,%s,%s,%s,%s);",[Advertise_Id,adv_remain,adv_next_run,Group_Id,Group_Name])
    connection.commit()

def botAdvFunction(context : CallbackContext):
    connection = DbConnect()
    cursor = connection.cursor()
    cursor.execute("SELECT Group_Id FROM Bot_Groups WHERE Advertise_Group=1;")
    adv_group = cursor.fetchone()
    if adv_group!=None:
        cursor.execute("""
                        SELECT A.Id,A.Advertise_Id,B.Group_Id,B.Group_Name,A.Advertise_Period,
                            IFNULL(min(R.Advertise_Remain),A.Advertise_Count) As Advertise_Remain,
                            IFNULL(max(R.Advertise_NextRun),A.Start_Time) As Advertise_NextRun
                        FROM Advertise A 
                            LEFT JOIN Advertise_Group G ON G.Advertise_Id=A.Id
                            LEFT JOIN Advertise_Runs R ON R.Advertise_Id=A.Id 
                            LEFT JOIN bot_groups B ON B.Id=G.Group_Id
                        WHERE A.Active=1
                        GROUP By Advertise_Id
                       """)
        advs = cursor.fetchall()
        for adv in advs:
            if adv[5]>0:
                dt = datetime.now()
                if dt>adv[6]:
                    if adv[2]==None:
                        cursor.execute("SELECT Group_Id,Group_Name FROM Bot_Groups WHERE Advertise_Group=0;")
                        adv_groups = cursor.fetchall()
                        for grp in adv_groups:
                            context.bot.forward_message(grp[0],adv_group[0],adv[1])
                            botAdvRun(connection,cursor,dt,adv[0],adv[5],adv[4],grp[0],grp[1])
                    else:
                        context.bot.forward_message(adv[2],adv_group[0],adv[1])
                        botAdvRun(connection,cursor,dt,adv[0],adv[5],adv[4],adv[2],adv[3])
        cursor.close()
        connection.close()

class botAdvTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):  
            self.function(*self.args,**self.kwargs)
           
def botAdvStart(update : Update, context : CallbackContext):
    global timer
    timer = botAdvTimer(0.5,botAdvFunction,[context])
    timer.start()

def botAdvStop(update : Update, context : CallbackContext):
    if timer!=None:
        timer.cancel()

def main():
    cpass = configparser.RawConfigParser()
    cpass.read('config.data')
    if not cpass.has_section('Bot'):
        print("No BOT Information Found")
        if timer!=None:
            timer.cancel()
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
    #dp.add_handler(CommandHandler('start',botStart))
    dp.add_handler(CommandHandler('adv_list',botAdvList))
    dp.add_handler(CommandHandler('adv_last',botAdvLast))
    #dp.add_handler(CommandHandler('adv_ins',botAdvInsert))
    #dp.add_handler(CommandHandler('adv_ins_group',botAdvInsertGroup))
    #dp.add_handler(CommandHandler('adv_del',botAdvDelete))
    dp.add_handler(CommandHandler('adv_start',botAdvStart))
    dp.add_handler(CommandHandler('adv_stop',botAdvStop))
    #dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,memberOnJoin))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member,memberOnLeft))
    dp.add_handler(MessageHandler(Filters.all, botAdvHandler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
  main()

