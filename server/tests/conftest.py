
import pytest
from config import TestConfig
from app import create_app, db, bcrypt
from models import User, Task
from helpers import process_time
from initial import daily_update_tables

@pytest.fixture(scope='function')
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        
        hashed_password = bcrypt.generate_password_hash('password')
        user1 = User(username='testuser1', password=hashed_password, firstname='Test', lastname='User 1', team='Admin Portal', 
                    usernum=1)
        user2 = User(username='testuser2', password=hashed_password, firstname='Test', lastname='User 2', team='Admin Portal',
                    usernum=2)
        task1 = Task(tasknum=1, sprint=1, time_assigned=process_time('2023-01-01 00:00:00'), status_completed=False, 
                     point=1, usernum=1)
        task2 = Task(tasknum=2, sprint=2, time_assigned=process_time('2023-12-01 00:00:00'), status_completed=True, 
                     time_completed=process_time('2023-12-31 00:00:00'), point=2, usernum=1)
        task3 = Task(tasknum=6, sprint=1, time_assigned=process_time('2023-07-05 03:12:00'), status_completed=True,
                     time_completed=process_time('2023-07-10 01:21:00'), point=1, usernum=1)
        task4 = Task(tasknum=3, sprint=2, time_assigned=process_time('2023-06-01 00:00:00'), status_completed=True, 
                 time_completed=process_time('2023-06-16 00:00:00'), point=3, usernum=2)
        task5 = Task(tasknum=4, sprint=1, time_assigned=process_time('2023-08-01 00:00:00'), status_completed=False, 
                    point=2, usernum=2)
        task6 = Task(tasknum=5, sprint=1, time_assigned=process_time('2023-05-05 00:00:00'), status_completed=True,
                    time_completed=process_time('2023-05-10 11:11:00'), point=1, usernum=2)
        task7 = Task(tasknum=7, sprint=2, time_assigned=process_time('2023-06-05 03:12:00'), status_completed=False, 
                    point=2, usernum=2)
        user1.tasks.append(task1)
        user1.tasks.append(task2)
        user1.tasks.append(task3)
        user2.tasks.append(task4)
        user2.tasks.append(task5)
        user2.tasks.append(task6)
        user2.tasks.append(task7)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        daily_update_tables(db)
        db.session.commit()

        yield app
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()