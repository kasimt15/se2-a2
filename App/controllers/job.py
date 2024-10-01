from App.models import Job
from App.database import db

def create_job(title, description, company):
    new_job = Job(title=title, description=description, company=company)
    db.session.add(new_job)
    db.session.commit()
    return new_job

def get_job(id):
    return Job.query.get(id)

def get_all_jobs():
    return Job.query.all()

def get_all_jobs_json():
    jobs = Job.query.all()
    if not jobs:
        return []
    return [job.get_json() for job in jobs]
