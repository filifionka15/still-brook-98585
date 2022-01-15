from BotTypes import *
import telebot
from telebot import types
import os
import threading
import docx2pdf
from DocumentWorker import *
from sys import platform
from subprocess import  Popen
import DictionaryForDocuments



def from_dummy_thread(func_to_call_from_main_thread):
    callback_queue.put(func_to_call_from_main_thread)

def from_main_thread_blocking():
    callback = callback_queue.get() #blocks until an item is available
    callback()

def from_main_thread_nonblocking():
    while True:
        try:
            callback = callback_queue.get(False) #doesn't block
        except queue.Empty: #raised when queue is empty
            break
        callback()


@bot.message_handler(commands=['start'])
def send_info(message : telebot.types.Message):
    text = (
        f"""
        <b>{message.chat.first_name}</b>, добро пожаловать в бета-версию телеграм бота <i>Legal Assistent!</i>
        Для получения дополнительной информации используйте /help
        """
    )
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Бесплатные документы', callback_data="Бесплатные документы")
    btn2 = types.InlineKeyboardButton('Договор купли продажи', callback_data="Договор купли продажи")
    btn3 = types.InlineKeyboardButton('Договор займа', callback_data="Договор займа")
    markup.add(btn1, btn2, btn3)
    bot.send_photo(message.chat.id, r'http://x-lines.ru/letters/i/cyrillicgothic/1214/280080/60/0/kis8e4mpcroframwpfzo.png', text, parse_mode='HTML', reply_markup=markup)

def convertDocx2PdfWindows(path : str, done : threading.Event):
    head, tail = os.path.split(path)
    filename, file_extension = os.path.splitext(tail)
    newFileName = filename + '.pdf'
    generated_path =  os.path.join(head, newFileName)

    done.clear()
    docx2pdf.convert(path, generated_path)
    done.set()
    return generated_path

def convertDocx2PdfLinux(path : str, done : threading.Event):
    done.clear()
    p = Popen(['soffice', '--headless', '--convert-to', 'pdf', '--outdir',
               './documents/', path])
    p.communicate()
    done.set()


def generateQuestions(message : types.Message):
    #get values
    
    reply_markup = None
    users_docs.get(message.chat.id)[1][users_docs.get(message.chat.id)[2]][1] = message.text #save the answer
    if users_docs.get(message.chat.id)[2] != (len(users_docs.get(message.chat.id)[1]) - 1): #here we check what last_number_of_question is not end
        users_docs.get(message.chat.id)[2] += 1
        question = users_docs.get(message.chat.id)[1][users_docs.get(message.chat.id)[2]][0]
        type = users_docs.get(message.chat.id)[1][users_docs.get(message.chat.id)[2]][2]
        answer_choices : list[str] = users_docs.get(message.chat.id)[1][users_docs.get(message.chat.id)[2]][3]
        #here we generate a replymarkup for fast choose
        if type == "test":
            reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for item in answer_choices:
                reply_markup.add(item)
        
        bot.send_message(message.chat.id, text=users_docs.get(message.chat.id)[1][users_docs.get(message.chat.id)[2]][0], reply_markup=reply_markup) #here we send new question to user
        
        bot.register_next_step_handler_by_chat_id(message.chat.id, generateQuestions)
    else:
        """
        here we can dump achieved data from user to database and generate a new document and then send
        """
        pass
    pass



@bot.callback_query_handler(func=lambda call: True)
def  callback_parser(call : types.CallbackQuery): # <- passes a CallbackQuery type object to your function
    if call.data == "Бесплатные документы":
        doc = DocumentWorker()

        path = './documents/Proba.docx'
        replacementdOn = DictionaryForDocuments.generateTestDictionary(call.from_user.username)

        docxPath = doc.replaceSpecWord(path, replacementdOn, call.from_user)


        head, tail = os.path.split(docxPath)
        filename, file_extension = os.path.splitext(tail)
        newFileName = filename + '.pdf'
        pdfPath =  os.path.join(head, newFileName)

        done = threading.Event()
        if platform == "linux" or platform == "linux2":
            from_dummy_thread(lambda: convertDocx2PdfLinux(docxPath, done))
            # linux
        elif platform == "darwin":
            # OS X
            pass
        elif platform == "win32":
            # Windows...
            from_dummy_thread(lambda: convertDocx2PdfWindows(docxPath, done))
        done.wait()

        file = open(pdfPath, "rb")

        bot.send_document(call.message.chat.id, file) #visible_file_name doesn't work

        file.close()

        os.remove(docxPath)
        os.remove(pdfPath)      

    elif call.data == "Договор купли продажи":
        #now we should be get information from database
        #1 - check previous state for that user, and get him answers if they are yet
        #2 - get document
        #3 - get questions from Database
        list_of_questions = [
            ["How are u?", None, "text", None],
            ["How old are u?", None, "text", None],
            ["That's test!", None, "test", ["Test 1", "Test 2", "Test 3"]]
        ]

        users_docs[call.message.chat.id] = [call.data, list_of_questions, 0, None] #created user instance

        #4 - register next callback function for that user
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, generateQuestions)

        bot.send_message(call.message.chat.id, text=users_docs.get(call.message.chat.id)[1][users_docs.get(call.message.chat.id)[2]][0])

        pass
    elif call.data == "Договор займа":
        pass
    else:
        bot.answer_callback_query(call.id, 'Данный раздел находится в разработке. Попробуйте позже.')


@bot.message_handler(commands=['help'])
def send_help(message):
    markup = types.InlineKeyboardMarkup(row_width=1)

    itembtn1 = types.InlineKeyboardButton('Техническая поддержка', callback_data="Техническая поддержка", url = 'https://t.me/nikasIlya')
    itembtn2 = types.InlineKeyboardButton('Главный канал', callback_data="Главный канал", url = 'https://t.me/itumor')
    itembtn3 = types.InlineKeyboardButton('Консультация юриста', callback_data="Консультация юриста")

    markup.add(itembtn1, itembtn2, itembtn3)
    bot.reply_to(message, "Выберите снизу необходимое поле:", reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text is not None)
def reply_to_message(message):
    if 'привет'in message.text.lower():
        bot.reply_to(message, 'Привет, как дела?')
    else:
        bot.reply_to(message, "Неизвестная команда. Для получения помощи используйте /help")
