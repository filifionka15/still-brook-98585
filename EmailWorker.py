import smtplib
from email.message import EmailMessage
import typing
import os


class EmailWorker:

    #variables
    __sender = 'ultimaratiotechgroup@gmail.com'
    __password = 'UR_Group5'
    __receiver = 'nikashovi4@list.ru'
    __s = None
    __host = 'smtp.gmail.com'

    def __init__(self):
        self.__s = smtplib.SMTP(self.__host)
        self.__s.ehlo_or_helo_if_needed()
        self.__s.starttls()
        self.__s.ehlo_or_helo_if_needed()
        self.__s.login(self.__sender, self.__password)
        

    def sendMessage(self, data : str, title : str,  receiver : typing.Optional[str] = None, sender : typing.Optional[str] = None, files : typing.List = None):
        message = EmailMessage()
        message.set_content(data)
        message['Subject'] = title
        message['From'] = self.__sender if sender == None else sender
        message['To'] = self.__receiver if receiver == None else receiver

        for file in files:
            with open(file, 'rb') as f:
                file_data = f.read()
                path_to, file_name = os.path.split(file)
            message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        self.__s.send_message(message)

