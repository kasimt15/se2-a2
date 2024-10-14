from App.models import User  
from App.database import db

def initialize():
    db.drop_all()  
    db.create_all()  
    bob = User(name='bob', password='bobpass', email='bob@example.com', phone='1234567890', role= 'employer')
    rob = User(name="rob", password="robpass", email="rob@example.com", phone="1234567890", role="user")
    db.session.add(bob)  
    db.session.add(rob)
    db.session.commit()  
