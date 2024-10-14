from App.database import db

class Job(db.Model):
    __tablename__= "Job"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    employer_id= db.Column(db.Integer, db.ForeignKey('User.id'), nullable= False)

    employer = db.relationship('User', backref='jobs')
    
    def __init__(self, title, description, company, employer_id):
        self.title = title
        self.description = description
        self.company = company
        self.employer_id= employer_id

    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'company': self.company,
            'employer': self.employer
        }
