from App.models import User  
from App.database import db

def initialize():
    db.drop_all()  
    db.create_all()  
    bob = User(name='bob', password='bobpass', email='bob@example.com', phone='1234567890')
    db.session.add(bob)  
    db.session.commit()  
