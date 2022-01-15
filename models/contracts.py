

from enum import Enum
from mongoengine import StringField, FloatField, PointField, ListField, \
    ReferenceField, EmbeddedDocument, EmbeddedDocumentListField, DateTimeField, EnumField
from mongoengine.document import Document

class QType(Enum):
    CHOICE = "choice"
    INPUTTEXT = "inputText"
    BOOLEAN = "boolean"


class Question(EmbeddedDocument):
    name = StringField(required = True)
    text = StringField(required = True)
    qtype = EnumField(QType, default=QType.CHOICE)
    answers = ListField()


class Contract(Document):
    name = StringField(required=True)
    questions = EmbeddedDocumentListField(Question, default=list)
    template = StringField
