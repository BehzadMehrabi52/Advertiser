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
                            IFNULL(min(R.Advertise_Remain),A.Advertise_Count) As Adv_Remain,
                            IFNULL(max(R.Advertise_NextRun),A.Start_Time) As Adv_NextRun,
                            A.Advertise_Period,
                            IFNULL(GROUP_CONCAT(G.Group_Name SEPARATOR ','),"ALL GROUPS") Groups, 
                            A.User_Name,A.Active
                        FROM Advertise A 
                            LEFT JOIN Advertise_Group G ON G.Advertise_Id=A.Id 
                            LEFT JOIN Advertise_Runs R ON R.Advertise_Id=A.Id 
                        WHERE A.Active=1 AND (A.Advertise_Count=0 OR R.Advertise_Remain IS NULL OR R.Advertise_Remain>0)
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
                            IFNULL(min(R.Advertise_Remain),A.Advertise_Count) As Adv_Remain,
                            IFNULL(max(R.Advertise_NextRun),A.Start_Time) As Adv_NextRun,
                            A.Advertise_Period,
                            IFNULL(GROUP_CONCAT(G.Group_Name SEPARATOR ','),"ALL GROUPS") Groups, 
                            A.User_Name,A.Active
                        FROM Advertise A 
                            LEFT JOIN Advertise_Group G ON G.Advertise_Id=A.Id 
                            LEFT JOIN Advertise_Runs R ON R.Advertise_Id=A.Id 
                        WHERE A.Active=1 AND (A.Advertise_Count=0 OR R.Advertise_Remain IS NULL OR R.Advertise_Remain>0)
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
        tx = "Unknown Command!"
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=tx)
    elif update.message.chat!=None and len(update.message.new_chat_photo)==0:
        if update.message.chat.type=='group' or update.message.chat.type=='supergroup':
            if update.message.from_user!=None:
                if update.message.from_user.id==2057086971:  #'Modern_Istanbul' user id
                    user_id   = update.message.from_user.id
                    user_name = update.message.from_user.username+"("+update.message.from_user.first_name+" "+update.message.from_user.last_name+")"
                    if update.message.forward_sender_name is not None:
                        user_id = 0
                        user_name = "("+update.message.forward_sender_name+")"+"<No User Id>"
                    if update.message.forward_from is not None:
                        user_id   = update.message.forward_from.id
                        user_name = ""
                        if update.message.forward_from.username is not None:
                            user_name = user_name + update.message.forward_from.username
                        user_name = user_name+"("
                        if update.message.forward_from.first_name is not None:
                            user_name = user_name + update.message.forward_from.first_name
                        if update.message.forward_from.last_name is not None:
                            user_name = user_name + update.message.forward_from.last_name
                        user_name = user_name+")"
                    connection = DbConnect()
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM Bot_Groups WHERE Advertise_Group=1 AND Active=1;")
                    adv_group = cursor.fetchone()
                    if adv_group!=None:
                        if update.message.chat.id == adv_group[1]: 
                            cursor.execute("INSERT INTO Advertise (Advertise_Id,Start_Time,Advertise_Count,Advertise_Period,Active,User_Id,User_Name) VALUES (%s,CURRENT_TIMESTAMP,1,24,0,%s,%s);",[update.message.message_id,user_id,user_name])
                            connection.commit()
                    cursor.close()
                    connection.close()
                    """
                    if adv_group!=None:
                        connection = DbConnect()
                        cursor = connection.cursor()
                        cursor.execute("SELECT * FROM Bot_Groups WHERE Advertise_Group=0 AND Active=1;")
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
        if update.message.chat.type=='group' or update.message.chat.type=='supergroup':
            if update.message.new_chat_members!=None:
                if update.message.new_chat_members[0]!=None:
                    if update.message.new_chat_members[0].username=='BM_Advertiser_Bot':
                        connection = DbConnect()
                        cursor = connection.cursor()
                        cursor.execute("INSERT INTO Bot_Groups (Group_Id,Group_Name,Advertise_Group,Active) VALUES (%s,%s,0,1);",[update.message.chat.id,update.message.chat.title])
                        connection.commit()
                        cursor.close()
                        connection.close()

def memberOnLeft(update : Update, context : CallbackContext):
    #chat_id = update.message.chat_id
    #context.bot.send_message(chat_id=chat_id, text='WelCome')
    #context.bot.delete_message(chat_id=update.message.chat_id,message_id=update.message.message_id)
    if update.message.chat!=None:
        if update.message.chat.type=='group' or update.message.chat.type=='supergroup':
            if update.message.left_chat_member!=None:
                if update.message.left_chat_member.username=='BM_Advertiser_Bot':
                    connection = DbConnect()
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM Bot_Groups WHERE Group_Id = %s;",[update.message.chat.id])
                    connection.commit()
                    cursor.close()
                    connection.close()

def botAdvRun(context : CallbackContext,connection,cursor,cur_time,adv_id,advertise_id,advertise_count,advertise_remain,advertise_period,group_id,group_name,advertise_group_id):
    context.bot.forward_message(group_id,advertise_group_id,advertise_id)
    adv_remain = advertise_remain - 1
    adv_next_run = cur_time + timedelta(seconds=2*advertise_period) #timedelta(hours=advertise_period)  #timedelta(seconds=1.5*advertise_period)
    cursor.execute("INSERT INTO Advertise_Runs (Advertise_Id,Advertise_Remain,Advertise_NextRun,Group_Id,Group_Name) VALUES (%s,%s,%s,%s,%s);",[adv_id,adv_remain,adv_next_run,group_id,group_name])
    if adv_remain<=0 and advertise_count!=0:
        context.bot.delete_message(chat_id=advertise_group_id,message_id=advertise_id)
        cursor.execute("UPDATE Advertise SET Active=0 WHERE Id=%s;",[adv_id])
    connection.commit()
    return adv_remain

def botAdvRuns(context : CallbackContext):
    connection = DbConnect()
    cursor = connection.cursor()
    cursor.execute("SELECT Group_Id FROM Bot_Groups WHERE Advertise_Group=1 AND Active=1;")
    adv_group = cursor.fetchone()
    if adv_group!=None:
        cursor.execute("""
                        SELECT A.Id,A.Advertise_Id,B.Group_Id,B.Group_Name,A.Advertise_Count,A.Advertise_Period,
                            IFNULL(min(R.Advertise_Remain),A.Advertise_Count) As Adv_Remain,
                            IFNULL(max(R.Advertise_NextRun),A.Start_Time) As Adv_NextRun
                        FROM Advertise A 
                            LEFT JOIN Advertise_Group G ON G.Advertise_Id=A.Id
                            LEFT JOIN Advertise_Runs R ON R.Advertise_Id=A.Id 
                            LEFT JOIN bot_groups B ON B.Id=G.Group_Id
                        WHERE A.Active=1 AND (A.Advertise_Count=0 OR R.Advertise_Remain IS NULL OR R.Advertise_Remain>0)
                            AND B.Active=1
                        GROUP By Advertise_Id
                       """)
        advs = cursor.fetchall()
        for adv in advs:
            adv_remain = adv[6]
            if adv_remain>0 or adv[4]==0:
                dt = datetime.now()
                if dt>adv[7]:
                    if adv[2]==None:
                        cursor.execute("SELECT Group_Id,Group_Name FROM Bot_Groups WHERE Advertise_Group=0 AND Active=1;")
                        adv_groups = cursor.fetchall()
                        for grp in adv_groups:
                            adv_remain = botAdvRun(context,connection,cursor,dt,adv[0],adv[1],adv[4],adv_remain,adv[5],grp[0],grp[1],adv_group[0])
                    else:
                        adv_remain = botAdvRun(context,connection,cursor,dt,adv[0],adv[1],adv[4],adv_remain,adv[5],adv[2],adv[3],adv_group[0])
        cursor.close()
        connection.close()

class botAdvTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):  
            self.function(*self.args,**self.kwargs)
           
def botAdvStart(update : Update, context : CallbackContext):
    global timer
    if timer is None:
        timer = botAdvTimer(0.5,botAdvRuns,[context])
        timer.start()
        tx = "Adviser is ON now"
    else:
        tx = "Adviser is ON not OFF"
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=tx)

def botAdvStop(update : Update, context : CallbackContext):
    global timer
    if timer is not None:
        timer.cancel()
        timer = None
        tx = "Adviser is OFF now"
    else:
        tx = "Adviser is not ON"
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=tx)

def main():
    global timer
    timer = None
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
