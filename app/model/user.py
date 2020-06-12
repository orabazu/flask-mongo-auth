from mongoengine import *
import json
from datetime import datetime

class User(Document):
    email = EmailField(required=True)
    password = BinaryField(required=True)
    registration_ip = StringField(required=True)
    last_login_ip = StringField(required=True)
    date_created = DateTimeField(default=datetime.utcnow)

    def jwt_payload(self):
        return {
            'email': self.email,
            'registration_ip': self.registration_ip,
            'last_login_ip': self.last_login_ip,
        }

    def json(self):
        user_dict = {
            'email': self.email,
            'registration_ip': self.registration_ip,
            'last_login_ip': self.last_login_ip,
        }
        return json.dumps(user_dict)
    
    meta = { 
        'alias': 'partnerly',
        'collection': 'users',
        'ordering': ['=date-created']
    }