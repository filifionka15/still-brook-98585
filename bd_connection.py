from models.contracts import QType
from mongoengine import connect
from models import Contract, Question

def get_database():
    connect(host="mongodb+srv://filifionka15:SrbD2JAPDSaOSVQj@cluster0.oibjw.mongodb.net/legal_assistant?retryWrites=true&w=majority")

    
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    get_database()
    q1 = Question(name = "заемщик", text = "Укажите заемщика", qtype = QType.INPUTTEXT)
    q2 = Question(name = "займодавец", text = "Займодавец:", qtype = QType.CHOICE)
    q2.answers = ["Физическое лицо","Юридическое лицо", "ИП"] 
    q3 = Question(name= "процентный заем", text="Процентный ли заем", qtype = QType.BOOLEAN)
    testdoc = Contract(name = "Договор займа")
    testdoc.questions = [q1,q2,q3]
    testdoc.save()

    