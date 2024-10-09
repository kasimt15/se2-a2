from App.models import User  
from App.database import db

class Application(db.Model):
    __tablename__= "Application"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('Job.id'), nullable=False)
 
    
    user = db.relationship('User', backref=db.backref('applications', lazy=True))
    job= db.relationship('Job', backref=db.backref('applications', lazy= True))

    def __init__(self, user_id, job_id):
        self.user_id = user_id
        self.job_id = job_id
   

    def get_json(self):
        user = User.query.get(self.user_id)
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': user.name,  
            'user_email': user.email,  
            'user_phone': user.phone,  
            'job_id': self.job_id,
            'job_Name': self.job.title,
        }
