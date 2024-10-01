from App.database import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    company = db.Column(db.String(100), nullable=False)

    def __init__(self, title, description, company):
        self.title = title
        self.description = description
        self.company = company

    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'company': self.company
        }
