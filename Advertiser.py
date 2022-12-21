from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, CallbackContext, ChatMemberHandler,RegexHandler
from telegram import Bot,Update, Chat, ChatMember, ParseMode, ChatMemberUpdated
from cryptography.hazmat.primitives import serialization
import configparser
import rsa
import mysql.connector 
from mysql.connector import Error
import os
from threading import Timer  
from datetime import datetime,timedelta
import pytz

def DbConnect():
    global connection
    try:
        connection = mysql.connector.connect(host='localhost',
                                             db='advertiser',
                                             user='Advertiser'
                                            )
        if not connection.is_connected():
            print("Could not connected to MySQL")
            if timer is not None:
                timer.cancel()
            os._exit(1)
    except Error as e:
        print("Error while connecting to MySQL", e)
        if timer is not None:
            timer.cancel()
        os._exit(1)

def isBotAdmin(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Advertiser_Users WHERE User_Id=%s AND Admin=1 AND Active=1;",[user_id])
    adm = cursor.fetchone()
    cursor.close()
    if adm is not None:
        return True
    return False

def botStart(update : Update, context : CallbackContext):
    if update is not None:
        if update.message is not None:
            if update.message.chat is not None:
                if update.message.chat.type == 'private':
                    if isBotAdmin(update.message.from_user.id):
                        startMessage = """
                        Commands:
                        /start : منوي اصلي
                        /adv_list : لیست تبلغات فعال
                        /adv_last : وضعیت آخرین تبلیغ فعال
                        /adv_list_not_active : لیست تبلغات غیر فعال
                        /adv_show_status:[adv_id] : وضعیت تبلیغ
                        /adv_show:[adv_id] : نمایش تبلیغ
                        /adv_acrivate:[adv_id] : فعال کردن تبلیغ
                        /adv_deacrivate:[adv_id] : غیر فعال کردن تبلیغ
                        /adv_start : راه اندازی تبلیغ دهنده
                        /adv_stop : توقف تبلیغ دهنده
                        /bot_group_list : لیست گروه های ربات
                        /about : درباره ...
                        """
                    else:
                        startMessage = """
                        Commands:
                        /start : منوي اصلي
                        /adv_list : لیست تبلغات فعال من
                        /adv_last : وضعیت آخرین تبلیغ فعال من
                        /adv_list_not_active : لیست تبلغات غیر فعال من
                        /adv_show_status:[adv_id] : وضعیت تبلیغ من
                        /adv_show:[adv_id] : نمایش تبلیغ من
                        /adv_acrivate:[adv_id] : فعال کردن تبلیغ من
                        /adv_deacrivate:[adv_id] : غیر فعال کردن تبلیغ من
                        /about : درباره ...
                        """
                    chat_id = update.message.chat_id
                    context.bot.send_message(chat_id=chat_id, text=startMessage)

def botAdvStr(r):
    adv = "Id:"+str(r[0])+";Start:"+str(r[1])+";Count:"+str(r[2])+";Remain:"+str(r[3])+";Next:"+str(r[4])+"(UTC);Period:"+str(r[5])+";Groups:"+str(r[6])+";UserName:"+r[7]+";Active:"+str(r[8])
    return adv

def botAdvListStr(recs):
    advs = ""
    for r in recs:
        advs = advs+"\n"+botAdvStr(r)
    return advs

def getAdvList(user_id,active,last,adv_id):
    global connection
    add_act_where_cluase = ""
    add_adv_where_cluase = ""
    add_user_where_cluase = ""
    last_exp = ""
    if active is not None:
        if active:
            add_act_where_cluase = "AND Active=1"
        else:
            add_act_where_cluase = "AND Active=0"
    if adv_id is not None:
        add_adv_where_cluase = "AND A.Advertise_Id="+adv_id
    if not isBotAdmin(user_id):
        add_user_where_cluase = "AND A.Uset_Id"+user_id
    if last:
        last_exp = "DESC LIMIT 1"
    cursor = connection.cursor()
    cursor.execute("""
                    SELECT A.Advertise_Id,A.Start_Time,A.Advertise_Count,
                        IFNULL(min(R.Advertise_Remain),A.Advertise_Count) As Adv_Remain,
                        IFNULL(max(R.Advertise_NextRun),A.Start_Time) As Adv_NextRun,
                        A.Advertise_Period,
                        IFNULL(GROUP_CONCAT(G.Group_Name SEPARATOR ','),"ALL GROUPS") Groups, 
                        A.User_Name,A.Active
                    FROM Advertise A 
                        LEFT JOIN Advertise_Group G ON G.Advertise_Id=A.Advertise_Id 
                        LEFT JOIN Advertise_Runs R ON R.Advertise_Id=A.Advertise_Id 
                    WHERE (A.Advertise_Count=0 OR R.Advertise_Remain IS NULL OR R.Advertise_Remain>0)
                    """+" "+add_act_where_cluase+" "+add_user_where_cluase+" "+add_adv_where_cluase+" GROUP By A.Advertise_Id "+last_exp)
    recs = cursor.fetchall()
    cursor.close()
    return recs

def botAdvList(update : Update, context : CallbackContext):
    if update is not None:
        if update.message is not None:
            if update.message.chat is not None:
                if update.message.chat.type == 'private':
                    recs = getAdvList(update.message.from_user.id,True,False,None)
                    advList = "Lists ("+str(len(recs))+")" + botAdvListStr(recs)
                    chat_id = update.message.chat_id
                    context.bot.send_message(chat_id=chat_id, text=advList)

def botAdvLast(update : Update, context : CallbackContext):
    if update is not None:
        if update.message is not None:
            if update.message.chat is not None:
                if update.message.chat.type == 'private':
                    recs = getAdvList(update.message.from_user.id,True,True,None)
                    if len(recs)>0:
                        adv = botAdvStr(recs[0])
                        chat_id = update.message.chat_id
                        context.bot.send_message(chat_id=chat_id, text=adv)

def botAdvNotActiveList(update : Update, context : CallbackContext):
    if update is not None:
        if update.message is not None:
            if update.message.chat is not None:
                if update.message.chat.type == 'private':
                    recs = getAdvList(update.message.from_user.id,False,False,None)
                    advList = "Lists ("+str(len(recs))+")" + botAdvListStr(recs)
                    chat_id = update.message.chat_id
                    context.bot.send_message(chat_id=chat_id, text=advList)

def botAdvShowStatus(update : Update, context : CallbackContext):
    if update is not None:
        if update.message is not None:
            if update.message.chat is not None:
                if update.message.chat.type == 'private':
                    params = update.message.text.split(":")
                    adv_id = params[1]
                    recs = getAdvList(update.message.from_user.id,None,False,adv_id)
                    if len(recs)>0:
                        adv = botAdvStr(recs[0])
                    else:
                        adv = "پیام تبلیغاتی پیدا نشد"
                    chat_id = update.message.chat_id
                    context.bot.send_message(chat_id=chat_id, text=adv)

def botAdvShow(update : Update, context : CallbackContext):
    global connection
    if update is not None:
        if update.message is not None:
            if update.message.chat is not None:
                if update.message.chat.type == 'private':
                    params = update.message.text.split(":")
                    adv_id = params[1]
                    recs = getAdvList(update.message.from_user.id,None,False,adv_id)
                    adv = "پیام تبلیغاتی پیدا نشد"
                    chat_id = update.message.chat_id
                    if len(recs)>0:
                        cursor = connection.cursor()
                        cursor.execute("SELECT Group_Id FROM Bot_Groups WHERE Advertise_Group=1 AND Active=1;")
                        adv_group = cursor.fetchone()
                        cursor.close()
                        if adv_group is not None:
                            adv = recs[0][0]
                            context.bot.forward_message(chat_id,adv_group[0],adv)
                        else:
                            context.bot.send_message(chat_id=chat_id, text=adv)
                    else:
                        context.bot.send_message(chat_id=chat_id, text=adv)

def botAdvActivate(update : Update, context : CallbackContext):
    global connection
    if update is not None:
        if update.message is not None:
            if update.message.chat is not None:
                if update.message.chat.type == 'private':
                    params = update.message.text.split(":")
                    adv_id = params[1]
                    recs = getAdvList(update.message.from_user.id,None,False,adv_id)
                    if len(recs)>0:
                        if recs[0][8]==0:
                            cursor = connection.cursor()
                            cursor.execute("UPDATE Advertise SET Active = 1 WHERE Advertise_Id = %s",[recs[0][0]])
                            connection.commit()
                            cursor.close()
                            msg = "تبلیع فعال شد"
                        else:
                            msg = "تبلیغ فعال است!"
                    else:
                        msg = "پیام تبلیغاتی پیدا نشد"
                    chat_id = update.message.chat_id
                    context.bot.send_message(chat_id=chat_id, text=msg)

def botAdvDeactivate(update : Update, context : CallbackContext):
    global connection
    if update is not None:
        if update.message is not None:
            if update.message.chat is not None:
                if update.message.chat.type == 'private':
                    params = update.message.text.split(":")
                    adv_id = params[1]
                    recs = getAdvList(update.message.from_user.id,None,False,adv_id)
                    if len(recs)>0:
                        if recs[0][8]==1:
                            cursor = connection.cursor()
                            cursor.execute("UPDATE Advertise SET Active = 0 WHERE Advertise_Id = %s",[recs[0][0]])
                            connection.commit()
                            cursor.close()
                            msg = "تبلیع غیر فعال شد"
                        else:
                            msg = "تبلیغ غیر فعال است!"
                    else:
                        msg = "پیام تبلیغاتی پیدا نشد"
                    chat_id = update.message.chat_id
                    context.bot.send_message(chat_id=chat_id, text=msg)

def botGroupList(update : Update, context : CallbackContext):
    global connection
    if update is not None:
        if update.message is not None:
            if update.message.chat is not None:
                if update.message.chat.type == 'private':
                    if isBotAdmin(update.message.from_user.id):
                        cursor = connection.cursor()
                        cursor.execute("SELECT Group_Id,Group_Name FROM Bot_Groups WHERE Active=1 AND Advertise_Group=0;")
                        recs = cursor.fetchall()
                        cursor.close()
                        advList = "Lists ("+str(len(recs))+")"
                        for rec in recs:
                            advList = advList+"\nId:"+str(rec[0])+";Name:"+rec[1]
                        chat_id = update.message.chat_id
                        context.bot.send_message(chat_id=chat_id, text=advList)

def botAbout(update : Update, context : CallbackContext):
    if update is not None:
        if update.message is not None:
            if update.message.chat is not None:
                if update.message.chat.type == 'private':
                    aboutMessage = """
                    مالک ربات : بهزاد مهرابي
                    """
                    chat_id = update.message.chat_id
                    context.bot.send_message(chat_id=chat_id, text=aboutMessage)

def botAdvHandler(update : Update, context : CallbackContext):
    global connection
    if update is not None:
        if update.message is not None:
            if update.message.chat is not None:
                if update.message.chat.type == 'private':
                    tx = "Unknown Command!"
                    chat_id = update.message.chat_id
                    context.bot.send_message(chat_id=chat_id, text=tx)
                elif len(update.message.new_chat_photo)==0:
                    if update.message.chat.type=='group' or update.message.chat.type=='supergroup':
                        if update.message.from_user is not None:
                            cursor = connection.cursor()
                            cursor.execute("SELECT Group_Id FROM Bot_Groups WHERE Advertise_Group=1 AND Active=1;")
                            adv_group = cursor.fetchone()
                            cursor.close()
                            if adv_group is not None:
                                if update.message.chat.id == adv_group[0]: 
                                    if isBotAdmin(update.message.from_user.id):
                                        user_id         = update.message.from_user.id
                                        user_name = ""
                                        if update.message.from_user.username is not None:
                                            user_name = update.message.from_user.username
                                        user_first_name = ""
                                        if update.message.from_user.first_name is not None:
                                            user_first_name = update.message.from_user.first_name
                                        user_last_name = ""
                                        if update.message.from_user.last_name is not None:
                                            user_last_name = update.message.from_user.last_name
                                        user_full_name  = user_first_name+" "+user_last_name
                                        if update.message.forward_sender_name is not None:
                                            user_id         = -1
                                            user_name       = ""
                                            user_first_name = ""
                                            user_last_name  = ""
                                            user_full_name  = update.message.forward_sender_name
                                        if update.message.forward_from is not None:
                                            user_id   = update.message.forward_from.id
                                            user_name = ""
                                            if update.message.forward_from.username is not None:
                                                user_name = update.message.forward_from.username
                                            user_first_name = ""
                                            if update.message.forward_from.first_name is not None:
                                                user_first_name = update.message.forward_from.first_name
                                            user_last_name = ""
                                            if update.message.forward_from.last_name is not None:
                                                user_last_name = update.message.forward_from.last_name
                                            user_full_name  = user_first_name+" "+user_last_name
                                        dt = datetime.now().astimezone(pytz.UTC)
                                        cursor = connection.cursor()
                                        cursor.execute("""
                                                        INSERT INTO Advertise (Advertise_Id,Start_Time,Advertise_Count,Advertise_Period,User_Id,User_Name,User_First_Name,User_Last_Name,User_Full_Name,Active)
                                                            VALUES (%s,%s,1,24,%s,%s,%s,%s,%s,0);
                                                        """,[update.message.message_id,dt,user_id,user_name,user_first_name,user_last_name,user_full_name])
                                        connection.commit()

def memberOnJoin(update : Update, context : CallbackContext):
    global connection
    #chat_id = update.message.chat_id
    #context.bot.send_message(chat_id=chat_id, text='WelCome')
    #context.bot.delete_message(chat_id=update.message.chat_id,message_id=update.message.message_id)
    if update is not None:
        if update.message is not None:
            if update.message.chat is not None:
                if update.message.chat.type=='group' or update.message.chat.type=='supergroup':
                    if update.message.new_chat_members is not None:
                        if update.message.new_chat_members[0] is not None:
                            if update.message.new_chat_members[0].username=='BM_Advertiser_Bot':
                                cursor = connection.cursor()
                                cursor.execute("INSERT INTO Bot_Groups (Group_Id,Group_Name,Advertise_Group,Active) VALUES (%s,%s,0,1);",[update.message.chat.id,update.message.chat.title])
                                connection.commit()
                                cursor.close()

def memberOnLeft(update : Update, context : CallbackContext):
    global connection
    #chat_id = update.message.chat_id
    #context.bot.send_message(chat_id=chat_id, text='WelCome')
    #context.bot.delete_message(chat_id=update.message.chat_id,message_id=update.message.message_id)
    if update is not None:
        if update.message is not None:
            if update.message.chat is not None:
                if update.message.chat.type=='group' or update.message.chat.type=='supergroup':
                    if update.message.left_chat_member is not None:
                        if update.message.left_chat_member.username=='BM_Advertiser_Bot':
                            cursor = connection.cursor()
                            #cursor.execute("DELETE FROM Bot_Groups WHERE Group_Id = %s;",[update.message.chat.id])
                            cursor.execute("UPDATE Bot_Groups SET Active=0 WHERE Group_Id = %s;",[update.message.chat.id])
                            connection.commit()
                            cursor.close()

def botAdvRun(context : CallbackContext,cur_time,advertise_id,advertise_count,advertise_remain,advertise_period,group_id,group_name,advertise_group_id):
    global connection
    adv_remain = advertise_remain
    send_msg = False
    print("1")
    try:
        context.bot.forward_message(group_id,advertise_group_id,advertise_id)
        print("2")
        send_msg = True
    except Error as e:
        print(group_id)
        print(e)
        send_msg = False
    print("3")
    if send_msg:
        print("4")
        adv_remain = adv_remain - 1
        adv_next_run = cur_time + timedelta(hours=advertise_period) #timedelta(hours=advertise_period)  #timedelta(seconds=1.5*advertise_period)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Advertise_Runs (Advertise_Id,Advertise_Remain,Advertise_NextRun,Group_Id,Group_Name) VALUES (%s,%s,%s,%s,%s);",[advertise_id,adv_remain,adv_next_run,group_id,group_name])
        connection.commit()
        cursor.close()
        if adv_remain<=0 and advertise_count!=0:
            context.bot.delete_message(chat_id=advertise_group_id,message_id=advertise_id)
            cursor = connection.cursor()
            cursor.execute("UPDATE Advertise SET Active=0 WHERE Advertise_Id=%s;",[advertise_id])
            connection.commit()
            cursor.close()
    return adv_remain

def botAdvRuns(context : CallbackContext):
    global connection
    cursor = connection.cursor()
    cursor.execute("SELECT Group_Id FROM Bot_Groups WHERE Advertise_Group=1 AND Active=1;")
    adv_group = cursor.fetchone()
    cursor.close()
    if adv_group is not None:
        cursor = connection.cursor()
        cursor.execute("""
                        SELECT A.Advertise_Id,B.Group_Id,B.Group_Name,A.Advertise_Count,A.Advertise_Period,
                            IFNULL(min(R.Advertise_Remain),A.Advertise_Count) As Adv_Remain,
                            IFNULL(max(R.Advertise_NextRun),A.Start_Time) As Adv_NextRun
                        FROM Advertise A 
                            LEFT JOIN Advertise_Group G ON G.Advertise_Id=A.Advertise_Id
                            LEFT JOIN Advertise_Runs R ON R.Advertise_Id=A.Advertise_Id 
                            LEFT JOIN bot_groups B ON B.Group_Id=G.Group_Id
                        WHERE A.Active=1 AND (A.Advertise_Count=0 OR R.Advertise_Remain IS NULL OR R.Advertise_Remain>0)
                            AND (B.Group_Id is Null or B.Active=1)
                        GROUP By A.Advertise_Id
                       """)
        advs = cursor.fetchall()
        cursor.close()
        for adv in advs:
            adv_remain = adv[5]
            if adv_remain>0 or adv[3]==0:
                dt = datetime.now().astimezone(pytz.UTC)
                adv_dt = adv[6].replace(tzinfo=pytz.UTC)
                if dt>=adv_dt:
                    if adv[1] is None:
                        cursor = connection.cursor()
                        cursor.execute("SELECT Group_Id,Group_Name FROM Bot_Groups WHERE Advertise_Group=0 AND Active=1;")
                        adv_groups = cursor.fetchall()
                        cursor.close()
                        for grp in adv_groups:
                            adv_remain = botAdvRun(context,dt,adv[0],adv[3],adv_remain,adv[4],grp[0],grp[1],adv_group[0])
                    else:
                        adv_remain = botAdvRun(context,dt,adv[0],adv[3],adv_remain,adv[4],adv[1],adv[2],adv_group[0])

class botAdvTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):  
            self.function(*self.args,**self.kwargs)
           
def botAdvStart(update : Update, context : CallbackContext):
    global timer
    if update is not None:
        if update.message is not None:
            if update.message.chat is not None:
                if update.message.chat.type == 'private':
                    if isBotAdmin(update.message.from_user.id):
                        chat_id = update.message.chat_id
                        if timer is None:
                            timer = botAdvTimer(0.5,botAdvRuns,[context])
                            timer.start()
                            tx = "Adviser is ON now"
                            print(tx)
                            context.bot.send_message(chat_id=chat_id, text=tx)
                            botAdvRuns(context)
                        else:
                            tx = "Adviser is ON not OFF"
                            print(tx)
                            context.bot.send_message(chat_id=chat_id, text=tx)

def botAdvStop(update : Update, context : CallbackContext):
    global timer
    if update is not None:
        if update.message is not None:
            if update.message.chat is not None:
                if update.message.chat.type == 'private':
                    if isBotAdmin(update.message.from_user.id):
                        if timer is not None:
                            timer.cancel()
                            timer = None
                            tx = "Adviser is OFF now"
                        else:
                            tx = "Adviser is not ON"
                        print(tx)
                        chat_id = update.message.chat_id
                        context.bot.send_message(chat_id=chat_id, text=tx)

def main():
    global timer
    DbConnect()
    timer = None
    cpass = configparser.RawConfigParser()
    cpass.read('config.data')
    if not cpass.has_section('Bot'):
        print("No BOT Information Found")
        if timer is not None:
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
    dp.add_handler(CommandHandler('start',botStart))
    dp.add_handler(CommandHandler('adv_list',botAdvList))
    dp.add_handler(CommandHandler('adv_last',botAdvLast))
    dp.add_handler(CommandHandler('adv_list_not_active',botAdvNotActiveList))
    dp.add_handler(CommandHandler('adv_start',botAdvStart))
    dp.add_handler(CommandHandler('adv_stop',botAdvStop))
    dp.add_handler(CommandHandler('bot_group_list',botGroupList))
    dp.add_handler(CommandHandler('about',botAbout))
    dp.add_handler(MessageHandler(Filters.regex('^/adv_show_status:[+-]?[0-9]+$'),botAdvShowStatus))
    dp.add_handler(MessageHandler(Filters.regex('^/adv_show:[+-]?[0-9]+$'),botAdvShow))
    dp.add_handler(MessageHandler(Filters.regex('^/adv_activate:[+-]?[0-9]+$'),botAdvActivate))
    dp.add_handler(MessageHandler(Filters.regex('^/adv_deactivate:[+-]?[0-9]+$'),botAdvDeactivate))
    #dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,memberOnJoin))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member,memberOnLeft))
    #dp.add_handler(MessageHandler(Filters.update,botAdvHandler))
    dp.add_handler(MessageHandler(Filters.all,botAdvHandler))
    print("Bot is now ready")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
  main()
