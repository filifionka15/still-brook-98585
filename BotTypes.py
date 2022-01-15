import telebot
import queue


TOKEN = '1874310722:AAH3VZACp1Fw0sNLdCjuu2w8zK8sUJ0YWr0'
DATABASE_URL = 'postgres://lebxtcvagnekgg:c70338595c0ac19ac85865e4adebd46e11a6ea596c94348b7583380c4f3e3437@ec2-3-230-38-145.compute-1.amazonaws.com:5432/daqrnausjgobb7'
GROUPCHAT = '@ultimaratiogroup'
bot = telebot.TeleBot(token=TOKEN)
callback_queue = queue.Queue()

#{ chat_id : [ name_of_document, [ [question, answer, type, answer_choices] ], index_of_last_question] }
users_docs = {}