import os, tempfile, pytest, logging, unittest
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash



from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    apply_to_job, 
    create_job,
    get_all_applications_json,
    get_all_jobs_json
)

LOGGER = logging.getLogger(__name__)

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    # Set up the Flask application for testing
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    
    # Activate application context for the fixture
    with app.app_context():
        db.create_all()  # Create all database tables before running tests
        yield app.test_client()  # Provide a test client to use in the tests
        db.drop_all()  # Cleanup by dropping all tables after tests complete


@pytest.fixture()
def clear_db():
    app = create_app({'TESTING': True})
    with app.app_context():
        db.session.query(User).delete()  # Deletes all users
        db.session.commit()

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass", "bob@email.com", "321-1234", "user") 
        assert user.name == "bob"  

    def test_get_json(self):
        user = User("bob", "bobpass", "bob@email.com", "321-1234", "user")  
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id": None, "name": "bob", "role": "user"})  

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", "bobpass", "bob@email.com", "321-1234", "user")  
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password, "bob@email.com", "321-1234", "user")  
        assert user.check_password(password)


'''
    Integration Tests
    #notpassing
'''




def test_authenticate():
    user = create_user("bob", "bobpass", "bob@email.com", "321-1234", "user")
    print(f"User created: {user}") 
    logged_in_user = login("bob", "bobpass")
    print(f"Login result: {logged_in_user}")  
    assert logged_in_user != None


class UsersIntegrationTests(unittest.TestCase):
    
    def test_create_user(self):
        user = create_user("rob", "robpass", "robbie@email.com", "321-1222", "user")
        assert user.name == "rob"

    @pytest.mark.usefixtures("empty_db")
    def test_get_all_users_json(self):
      users_json = get_all_users_json()
      self.assertListEqual(
        [{"id": 1, "name": "bob", "role": "user"}, 
         {"id": 2, "name": "rob", "role": "user"}], users_json)
    
class JobsIntegrationTests(unittest.TestCase):

    def test_create_job(self):
        employer_id=1
        job = create_job("Software Engineer", "Develop and maintain software", "TechCorp", employer_id)
        assert job.title == "Software Engineer"

    def test_get_all_jobs_json(self):
     jobs_json = get_all_jobs_json()
     self.assertListEqual([
        {'id': 1, 'title': 'Software Engineer', 'description': 'Develop and maintain software', 'company': 'TechCorp', 'employer': 1},  # employer as ID
        {'id': 2, 'title': 'Software Engineer', 'description': 'Develop and maintain software', 'company': 'TechCorp', 'employer': 1}   # employer as ID
    ], jobs_json)



    def test_apply_to_job(self):
        job = create_job("Software Engineer", "Develop and maintain software", "TechCorp", 1)
        apply_to_job(1, 1)
        applications = get_all_applications_json(1)
        expected_applications = [{
            "id": 1,
            "user_id": 1,
            "user_name": "bob",
            "user_email": "bob@email.com",
            "user_phone": "321-1234",
            "job_id": 1,
            "job_Name": "Software Engineer"
        }]
        self.assertListEqual(expected_applications, applications)

    def test_get_all_applications_json(self):
        applications_json = get_all_applications_json(1)
        expected_applications = [{
            "id": 1,
            "user_id": 1,
            "user_name": "bob",
            "user_email": "bob@email.com",
            "user_phone": "321-1234",
            "job_id": 1,
            "job_Name": "Software Engineer"
        }]
        self.assertListEqual(expected_applications, applications_json)

if __name__ == '__main__':
    unittest.main()
