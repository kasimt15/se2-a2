from App.models import Application
from App.database import db

def apply_to_job(user_id, job_id):
    new_application = Application(user_id=user_id, job_id=job_id)
    db.session.add(new_application)
    db.session.commit()
    return new_application

def get_applications_by_job(job_id):
    return Application.query.filter_by(job_id=job_id).all()

def get_all_applications_json(job_id):
    applications = get_applications_by_job(job_id)
    if not applications:
        return []
    return [application.get_json() for application in applications]
