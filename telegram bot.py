import urllib
import requests
import time
import schedule
from bs4 import BeautifulSoup
import re
import os.path
import urllib.request
from tqdm import tqdm
import re


from datetime import datetime
import requests
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import threading
import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


from boto3.s3.transfer import S3Transfer
import boto3
import telebot
from telebot import types
from telegram.ext.dispatcher import run_async
import logging
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) 

aws_key_id=' aws key id '
aws_access_key='access key'
bucket_name='bucket name'

API_TOKEN='telegram bot api'

bot = telebot.TeleBot(API_TOKEN)

#conneect to ibm databas
import ibm_db
import ibm_db_dbi  
def SQL():
    db = ibm_db.connect("username host password",'','') 
    
    conn = ibm_db_dbi.Connection(db)   
    cur = conn.cursor()
    
    return cur,conn


    

@run_async
def echo(update, context):
    context.bot.send_message(update.message.chat_id, text=update.message.text)

url_list=np.load('url_list.npy') # load url data after crawling the notice link
url_list=list(url_list)
timetable_list=np.load('timetable_list.npy')


#this class work on background and crawl site
#DEAMON

class Deamon(object):
    

    def __init__(self):
       
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
 
    def run(self):
        
        while True:
             
             new_url_list=[]
             url='https://www.nitandhra.ac.in/main/'
             response = requests.get(url, proxies=urllib.request.getproxies())
             soup = BeautifulSoup(response.text, "html.parser")
             for one_a_tag in soup.findAll('a'): 
                    
                    link = one_a_tag['href']
                    if re.search(r'\w+:?(?=/)',link) :
                        result = re.findall(r'\w+:?(?=/)',link)
                        
                        if 'Announcements' in result:       #if herf strat with annoncement 
                                if result[0]=='Announcements':
                                      download_url = url+ link 
                                      _,extension=os.path.splitext(download_url)
                                     
                                      if download_url not in url_list and extension=='.pdf':
                                          url_list.insert(0,download_url)     #update the previoud url list
                                          new_url_list.append(download_url)
                                else:
                                      download_url=link
                                      _,extension=os.path.split(download_url)
                                      if download_url not in url_list and extension=='.pdf':
                                          url_list.insert(0,download_url)
                                          new_url_list.append(download_url)
                               
                    time.sleep(1) 
                      
             result=[]
             if len(new_url_list)>0:
                       print('mkjk')
                       for url in new_url_list:
                           result = [re.split("\w+:?(?=/)", i) for i in url]
                           for i in range(len(result)):
                               if result[i][0]=='/':
                                   s=i
                           result=url[s+1:]  
                           response = requests.get(url, stream=True)
               
                           with open(str(result), "wb") as handle:#location of pdf where to store
                               for data in tqdm(response.iter_content()):
                                   handle.write(data)
                       
                       new_announcement(result) #call the function to send notice to every one
                        
             #break
            
             
             time.sleep(600) #after every 10 miniute it will crawl
  

     
Deamon()    #run the class     
   

#IBM assistance to to classify intent
def IBM_CHAT_BOT():
        
    authenticator = IAMAuthenticator('key')
    assistant = AssistantV2(
        version='2020-04-01',
        authenticator = authenticator
    )
    
    assistant.set_service_url('assistence url')
    
    response = assistant.create_session(
        assistant_id='assistence id'
    ).get_result()

    session_idd=response['session_id']
    return session_idd,assistant



@bot.message_handler(func=lambda message: message.text=='timetable' or message.text=='Timetable' or message.text=='Time table')
def time_table(message):
    put_context(message)
   
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    item1=types.InlineKeyboardButton('1st Year', callback_data='1st_Year')
    item2=types.InlineKeyboardButton('2nd Year', callback_data='2nd_Year')
    item3= types.InlineKeyboardButton('3rd Year', callback_data='3rd_Year')
    item4= types.InlineKeyboardButton('4rd Year', callback_data='4th_Year')
   
    keyboard.add(item1,item2,item3,item4)
    
    bot.send_message(message.chat.id, 'Select your Btech year :', reply_markup=keyboard)

 
@bot.callback_query_handler(func =lambda query: query.data in ['1st_Year','2nd_Year','3rd_Year','4th_Year'])
def year_callback(query):
    put_query(query)
    if query.data=='1st_Year':
             

              Year_1(query)  
    elif query.data=='2nd_Year':
           

              Year_2(query) 
    elif query.data=='3rd_Year':
          
           Year_3(query) 
    elif query.data=='4th_Year':
         

           Year_4(query)  
  
def Year_1(query):
    put_query(query)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    item1=types.InlineKeyboardButton('SEC A', callback_data='1year_secA')
    item2=types.InlineKeyboardButton('SEC B', callback_data='1year_secB')
    item3=types.InlineKeyboardButton('SEC C', callback_data='1year_secC')
    item4=types.InlineKeyboardButton('SEC D', callback_data='1year_secD')
    item5=types.InlineKeyboardButton('SEC E', callback_data='1year_secE')   
    item6=types.InlineKeyboardButton('SEC F', callback_data='1year_secF')
    item7=types.InlineKeyboardButton('SEC G', callback_data='1year_secG')
    item8=types.InlineKeyboardButton('SEC H', callback_data='1year_secH')
    keyboard.add(item1,item2,item3,item4,item5,item6,item7,item8)
    
    bot.send_message(query.message.chat.id, 'Select your Branch :', reply_markup=keyboard)

  
def Year_2(query):
    put_query(query)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    item1=types.InlineKeyboardButton('BIOTECH', callback_data='2year_biotech')
    item2=types.InlineKeyboardButton('CHEMICAL', callback_data='2year_chem')
    item3=types.InlineKeyboardButton('CIVIL', callback_data='2year_civil')
    item4=types.InlineKeyboardButton('COMPUTER SCIENCE', callback_data='2year_cse')
    item5=types.InlineKeyboardButton('EEE', callback_data='2year_eee')   
    item6=types.InlineKeyboardButton('ECE', callback_data='2year_ece')
    item7=types.InlineKeyboardButton('METALLURGY', callback_data='2year_metallurgy')
    item8=types.InlineKeyboardButton('MECHANICAL', callback_data='2year_mech')
    keyboard.add(item1,item2,item3,item4,item5,item6,item7,item8)
    
    bot.send_message(query.message.chat.id, 'Select your Branch :', reply_markup=keyboard)

  
def Year_3(query):
    put_query(query)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    item1=types.InlineKeyboardButton('BIOTECH', callback_data='3year_biotech')
    item2=types.InlineKeyboardButton('CHEMICAL', callback_data='3year_chem')
    item3=types.InlineKeyboardButton('CIVIL', callback_data='3year_civil')
    item4=types.InlineKeyboardButton('COMPUTER SCIENCE', callback_data='3year_cse')
    item5=types.InlineKeyboardButton('EEE', callback_data='3year_eee')   
    item6=types.InlineKeyboardButton('ECE', callback_data='3year_ece')
    item7=types.InlineKeyboardButton('METALLURGY', callback_data='3year_metallurgy')
    item8=types.InlineKeyboardButton('MECHANICAL', callback_data='3year_mech')
    keyboard.add(item1,item2,item3,item4,item5,item6,item7,item8)
    
    bot.send_message(query.message.chat.id, 'Select your Branch :', reply_markup=keyboard)



def Year_4(query):
    put_query(query)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    item1=types.InlineKeyboardButton('BIOTECH', callback_data='4year_biotech')
    item2=types.InlineKeyboardButton('CHEMICAL', callback_data='4year_chem')
    item3=types.InlineKeyboardButton('CIVIL', callback_data='4year_civil')
    item4=types.InlineKeyboardButton('COMPUTER SCIENCE', callback_data='4year_cse')
    item5=types.InlineKeyboardButton('EEE', callback_data='4year_eee')   
    item6=types.InlineKeyboardButton('ECE', callback_data='4year_ece')
    item7=types.InlineKeyboardButton('METALLURGY', callback_data='4year_metallurgy')
    item8=types.InlineKeyboardButton('MECHANICAL', callback_data='4year_mech')
    keyboard.add(item1,item2,item3,item4,item5,item6,item7,item8)
    
    bot.send_message(query.message.chat.id, 'Select your Branch :', reply_markup=keyboard)

@bot.callback_query_handler(func =lambda query: query.data in timetable_list)
def timetable(query):
    branch_time_table(query.data,query.message)
    
    
def new_announcement(path):
    
    conn=ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-02.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=hsw38568;PWD=kqx814-tqfxn1zhw",'','')
    pconn=ibm_db_dbi.Connection(conn)
    dataframe=pd.read_sql("SELECT * FROM USER_DATA ",pconn)

    unq_id=[]
    for i,unqe_id in enumerate(dataframe['USER_ID']):
        if unqe_id not in unq_id:
            unq_id.append(unqe_id)
    
    doc = open(path, 'rb')
    for i,chat_id in enumerate(unq_id):
                                  
           bot.send_document(chat_id, doc)
       
      

def announcement_5(message):
   
    result=[]
    
    keyboard = types.InlineKeyboardMarkup(row_width=1.5)
    put_context(message)
    
    for i,url in enumerate(url_list):
            
            final = [re.split("\w+:?(?=/)", j) for j in url]
            for k in range(len(final)):
                if final[k][0]=='/':
                    s=k
            result.append(url[s+1:-4])
            if i==4:
                break
    item1=types.InlineKeyboardButton(result[0], callback_data='0_doc')
    item2=types.InlineKeyboardButton(result[1], callback_data='1_doc')
    item3= types.InlineKeyboardButton(result[2], callback_data='2_doc')
    item4= types.InlineKeyboardButton(result[3], callback_data='3_doc')
    item5= types.InlineKeyboardButton(result[4], callback_data='4_doc')        
    keyboard.row(item1)
    keyboard.row(item2)
    keyboard.row(item3)
    keyboard.row(item4)
    keyboard.row(item5)
    bot.send_message(message.chat.id, 'Recent five notice :', reply_markup=keyboard)    

    

    

@bot.callback_query_handler(func =lambda query: query.data in ['0_doc','1_doc','2_doc','3_doc','4_doc'])
def announcement_query(query):
    put_query(query)
    data = query.data
   
    
    if data.startswith('0'):
        path=pdf_download(url_list[0],query.message.chat.id)
        pdf_doc_send(path,query.message.chat.id)
       
    if data.startswith('1'):
        path=pdf_download(url_list[1],query.message.chat.id)
        pdf_doc_send(path,query.message.chat.id)
    if data.startswith('2'):
        path=pdf_download(url_list[2],query.message.chat.id)
        pdf_doc_send(path,query.message.chat.id)
    if data.startswith('3'):
       path=pdf_download(url_list[3],query.message.chat.id)
       pdf_doc_send(path,query.message.chat.id)
    if data.startswith('4'):
       path=pdf_download(url_list[4],query.message.chat.id)
       pdf_doc_send(path,query.message.chat.id)

#downloding file in local directory  
def pdf_download(url,chat_id):
    bot.send_chat_action(chat_id ,action = telegram.ChatAction.TYPING)
   
    response = requests.get(url, stream=True)
    final = [re.split("\w+:?(?=/)", j) for j in url]
    for k in range(len(final)):
        if final[k][0]=='/':
            s=k
    
    path=url[s+1:]                                  #file path
    with open(path, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)
    return path
#sending file
def pdf_doc_send(path,chat_id):
   
    doc = open(path, 'rb')
    bot.send_document(chat_id, doc)
   
#collecting data
def put_context(message):
    
    msz=str(message.text)
    first_name=str(message.chat.first_name)
    last_name=str(message.chat.last_name)
    msz_id=int(message.message_id)
    chat_id=int(message.chat.id)
    timestamp= str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    cur,conn=SQL()
    sql= """INSERT INTO USER_DATA (user_id ,first_name,last_name,text ,date_time ,message_id )
            VALUES(?, ?, ?, ?, ?, ?)"""
            
        
    cur.execute(sql, (chat_id,first_name,last_name,msz, timestamp,msz_id)) 
    

def feeback(message,feedback):
    
    msz=str(message.text)
    first_name=str(message.chat.first_name)
    last_name=str(message.chat.last_name)
    msz_id=int(message.message_id)
    chat_id=int(message.chat.id)
    timestamp= str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    username=str(message.chat.username)
    cur,conn=SQL()
    sql= """INSERT INTO feedback (user_id ,first_name,last_name,user_name,text ,date_time ,message_id ,feedback)
            VALUES(?, ?, ?, ?, ?, ?,?,?)"""
            
        
    cur.execute(sql, (chat_id,first_name,last_name,username,msz, timestamp,msz_id,feedback)) 

def put_query(query):
    msz=str(query.data)
    first_name=str(query.message.chat.first_name)
    last_name=str(query.message.chat.last_name)
    msz_id=int(query.message.message_id)
    chat_id=int(query.message.chat.id)
    timestamp= str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
   
    cur,conn=SQL()
        
    sql= """INSERT INTO USER_DATA (user_id ,first_name,last_name,text ,date_time ,message_id )
            VALUES(?, ?, ?, ?, ?, ?)"""
            
 
    cur.execute(sql, (chat_id,first_name,last_name,msz, timestamp,msz_id)) 
    #ibm_db.close(conn)
    #ibm_db.close(cur)


def user_send_doc(message,url):
    
    msz=str(message.text)
    first_name=str(message.chat.first_name)
    last_name=str(message.chat.last_name)
    msz_id=int(message.message_id)
    chat_id=int(message.chat.id)
    timestamp= str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
   
    cur,conn=SQL()
    sql= """INSERT INTO user_send_doc (user_id ,first_name,last_name,text ,date_time ,message_id,url )
            VALUES(?, ?, ?, ?, ?, ?,?)"""
            
        
    cur.execute(sql, (chat_id,first_name,last_name,msz, timestamp,msz_id,url)) 
    
   
    bot.send_message(1102848119,'something uploaded')
    bot.send_message(1102848119,url)
    
def chatbot_performence(message,reply,confidence):
    msz=str(message.text)
    first_name=str(message.chat.first_name)
    last_name=str(message.chat.last_name)
    msz_id=int(message.message_id)
    chat_id=int(message.chat.id)
    timestamp= str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    input_msz=str(message.text)
    reply=str(reply)
    
    username=str(message.chat.username)
       
    cur,conn=SQL()
    sql= """INSERT INTO chatbot_performence (user_id ,first_name,last_name,user_name,text ,date_time ,message_id,input,reply,confidence )
    VALUES(?, ?, ?, ?, ?, ?,?,?,?,?)"""


    cur.execute(sql, (chat_id,first_name,last_name,username,msz, timestamp,msz_id,msz,reply,confidence)) 
   

 
@bot.message_handler(regexp="#(\w+)")
def handle_message(message):
    msz=re.findall(r"#(\w+)",message.text)
    
    for i in range(len(msz)):
        msz[i]=msz[i].lower()
    if 'feedback' in msz:
        feeback(message,message.text)
        bot.reply_to(message,'Thank you for Feedback')
        bot.send_message(1102848119,'Someone given a feedback'+u'\U0001F601')

import telegram

@bot.message_handler(func=lambda message: True)
def all_msz(message):
    
    bot.send_chat_action(chat_id=message.chat.id ,action = telegram.ChatAction.TYPING)
    
    msz=message.text
    msz=msz.lower()
    ratio=fuzz.ratio(msz,'timetable')
    if ratio>80:
        time_table(message)
        return
    notice_ratio=fuzz.ratio(msz,'notice')    
    if notice_ratio>70:
        announcement_5(message)
        return
  
    response=connect(message)
    
    reply=response['output']['generic'][0]['text']
    
    if reply=='Irrelevant' :
               
        bot.send_message(message.chat.id,"Sorry we couldn't find anything") 
        return
    
    result=response['output']['intents'][0]['intent']

    
    confidence=response['output']['intents'][0]['confidence']
    
    
    if result=='notice' and confidence>0.65:
        confi(message,confidence)
        notice(message)
        chatbot_performence(message,result,confidence)
    
    elif result in timetable_list:
        confi(message,confidence)
        branch_time_table(result,message)
        chatbot_performence(message,result,confidence)
        
    
    elif confidence>0.65:
        confi(message,confidence)
        print_inline(message,reply)
       
        chatbot_performence(message,reply,confidence)
    else:
        
        bot.send_message(message.chat.id,"Sorry we couldn't find anything")

def connect(message):
    
     try:
        
        response = assistant.message(
            assistant_id='assistance id',
            session_id=session_idd,
            input={
                'message_type': 'text',
                'text': message.text
            }
        ).get_result()
       
       
        
     except :
            print('Connecting to IBM.....')
            session_idd,assistant=IBM_CHAT_BOT()
            
            response = assistant.message(
                assistant_id='assistence id',
                session_id=session_idd,
                input={
                    'message_type': 'text',
                    'text': message.text
                }
            ).get_result()
    
     return response
    
    
global mz
    
def notice(message):
    result=process.extract(message.text,url_list, limit=4)
    mz=str(np.linspace(0,len(url_list)-1,len(url_list)))
    display=[]
    keyboard = types.InlineKeyboardMarkup(row_width=1.5)
    buttons=0
    for i in range(4):
        if result[i][1]>50:
            buttons=buttons+1
       
    for i,url in enumerate(result):
            url=list(url)
            final = [re.split("\w+:?(?=/)", j) for j in url[0]]
            
            for k in range(len(final)):
                if final[k][0]=='/':
                    s=k
            display.append(url[0][s+1:-4])
            
    
        
    call=[]   
    for i in range(len(result)):
        call.append(result[i][0])
    index=[]
    for url in call:
        for i,url_1 in enumerate(url_list):
            if url==url_1:
                index.append(i)
    #index=index.astype('str')
    
    
    if buttons==0:
        bot.send_message(message.chat.id,"Sorry, we didn't find any document please select from these")
        announcement_5(message)
    if buttons==1:
        q1=index[0]
        q1=str(q1)
        item1=types.InlineKeyboardButton(display[0], callback_data=q1)
        keyboard.row(item1)
        bot.send_message(message.chat.id, 'Here is your doc', reply_markup=keyboard)    
    if buttons==2:
        q1=index[0]
        q1=str(q1)
        q2=index[1]
        q2=str(q2)
        item1=types.InlineKeyboardButton(display[0], callback_data=q1)
        item2=types.InlineKeyboardButton(display[1], callback_data=q2)
        keyboard.row(item1)
        keyboard.row(item2)
        bot.send_message(message.chat.id, 'Here is your doc', reply_markup=keyboard)     
    
    if buttons==3:
        q1=index[0]
        q1=str(q1)
        q2=index[1]
        q2=str(q2)
        q3=index[2]
        q3=str(q3)
        item1=types.InlineKeyboardButton(display[0], callback_data=q1)
        item2=types.InlineKeyboardButton(display[1], callback_data=q2)
        item3=types.InlineKeyboardButton(display[2], callback_data=q3)
        keyboard.row(item1)
        keyboard.row(item2)
        keyboard.row(item3)
        bot.send_message(message.chat.id, 'Here is your doc', reply_markup=keyboard)     
    
    
    if buttons==4:
        q1=index[0]
        q1=str(q1)
        q2=index[1]
        q2=str(q2)
        q3=index[2]
        q3=str(q3)
        q4=index[3]
        q4=str(q4)
        item1=types.InlineKeyboardButton(display[0], callback_data=q1)
        item2=types.InlineKeyboardButton(display[1], callback_data=q2)
        item3=types.InlineKeyboardButton(display[2], callback_data=q3)
        item4=types.InlineKeyboardButton(display[3], callback_data=q4)
        keyboard.row(item1)
        keyboard.row(item2)
        keyboard.row(item3)
        keyboard.row(item4)
        bot.send_message(message.chat.id, 'Here is your doc', reply_markup=keyboard)  
    #bot.send_message(message.chat.id, "Or may be it's not on the site")



 
@bot.callback_query_handler(func =lambda query: query.data in mz)   
def notice_query(query):
    put_query(query)    
    index=query.data
    print(index)
    index=int(index) 
    path=pdf_download(url_list[index],query.message.chat.id)
    pdf_doc_send(path,query.message.chat.id)



def branch_time_table(filename,message):
    bot.send_chat_action(chat_id=message.chat.id ,action = telegram.ChatAction.TYPING)
    y=np.random.randint(1,999999,1)
    path=str(filename)+str(y)+'.jpg'                                  #path of directory
   
    s3 = boto3.client('s3', aws_access_key_id=aws_key_id, aws_secret_access_key= aws_access_key)
    s3.download_file('s3accessbot', 'time_table/'+str(filename)+'.jpg',path) 
   
    photo = open(path, 'rb')
    bot.send_photo(message.chat.id,photo)
    
def confi(message,confidence):
    if message.chat.id==1102848119:
              bot.send_message(message.chat.id,"Confidence: "+str(confidence))


@bot.message_handler(content_types=['document', 'audio','video','photo','voice'])
def handle_docs_audio(message):
    content_types=message.content_type
    if content_types=='document':
       file_id=message.document.file_id
	
    if content_types=='photo':
           file_id = message.photo[2].file_id
           file_info = bot.get_file(file_id)
           downloaded_file = bot.download_file(file_info.file_path)
           
           bot.send_photo(1102848119,downloaded_file)
           #return
           
    if content_types=='video':
       file_id=message.video.file_id
    
    if content_types=='voice':
                 file_id=message.voice.file_id   
    if content_types=='audio':
                 file_id=message.audio.file_id   
    
    file_info=bot.get_file(file_id)    
    
   
    filepath='https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path)
    user_send_doc(message,filepath)
    

def msz_to_me():
    bot.send_message(1102848119,'something uploaded')

def print_inline(message,text):
        
    index=[]
    for i in range(len(text)-1):
        if text[i:i+1]== "\n"  :
           
            index.append(i)

    strng=[]
    for i in range(len(text)):
        if i in index:
           bot.send_message(message.chat.id,''.join(strng))

           strng=[]
           i+i+1
           continue
        elif i==len(text)-1:
            strng.append(text[i])
            bot.send_message(message.chat.id,''.join(strng))
        
        else:
          strng.append(text[i])


bot.polling(none_stop=True,timeout=None)    
    








