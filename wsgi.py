from App.main import create_app
from App.database import db
from App.models import User
from App import create_job, get_all_jobs_json, apply_to_job, get_all_applications_json, get_all_users_json, create_user
from App.controllers.initialize import initialize
import click
from flask.cli import AppGroup

app = create_app()

with app.app_context():
    db.create_all()

@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()  
    print('database initialized')

# CLI commands for user
user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create", help="Create a new user")
@click.argument("name")
@click.argument("password")
@click.argument("email")
@click.argument("phone")
def create_user_command(name, password, email, phone):
    with app.app_context():
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f'User with email {email} already exists.')
            return

        new_user = create_user(name, password, email, phone)
        print(f'User {name} created with ID {new_user.id}.')

@user_cli.command("list", help="Return JSON of all users")
def get_all_users_json_command():
    users = get_all_users_json()
    print(users)

app.cli.add_command(user_cli)

# CLI commands for job
job_cli = AppGroup('job', help='Job object commands')

@job_cli.command("create", help="Create a new job")
@click.argument("title")
@click.argument("description")
@click.argument("company")
@click.argument("employer")
def create_job_command(title, description, company, employer):
    create_job(title, description, company, employer)
    print(f'Job {title} created.')

@job_cli.command("list", help="List all jobs")
def list_jobs_command():
    jobs = get_all_jobs_json()
    print(jobs)

app.cli.add_command(job_cli)

# CLI commands for applications
application_cli = AppGroup('application', help='Application object commands')

@application_cli.command("apply", help="Apply to a job")
@click.argument("user_id")
@click.argument("job_id")
def apply_to_job_command(user_id, job_id):
    apply_to_job(user_id, job_id)
    print(f'Application created for user {user_id} on job {job_id}.')

@application_cli.command("list", help="List all applicants for a job")
@click.argument("job_id")
def list_applications_command(job_id):
    applications = get_all_applications_json(job_id)
    print(applications)

app.cli.add_command(application_cli)

if __name__ == "__main__":
    app.run(debug=True)
