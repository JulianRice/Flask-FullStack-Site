import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Document):
    user_id         = db.IntField(unique=True)
    first_name      = db.StringField(max_length=50)
    last_name       = db.StringField(max_length=50)
    email           = db.StringField(max_length=30, unique=True)
    password        = db.StringField() #128 is needed for hashing

    def SetPassword(self, password):
        self.password = generate_password_hash(password)
    
    def GetPassword(self, password):
        return check_password_hash(self.password, password)

class Course(db.Document):
    courseID = db.StringField(max_length=10, unique=True)
    title = db.StringField(max_length=100)
    description = db.StringField(max_length=255)
    credits = db.IntField()
    term = db.StringField(max_length=25)

#Many to Many Relationship
#One course can have many students and...
#One student can have many courses
class Enrollment(db.Document):
    #ObjectIdField() -> Usable as well
    user_id = db.IntField()
    courseID = db.IntField(max_length=10)