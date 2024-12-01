import pymysql
from flask import jsonify, json
from dotenv import load_dotenv
import os
import requests
from models import User, Task
from helpers import preprocess, process
from sql_queries import get_num_users

# initial database
def initial_db():
    load_dotenv()
    PASSWORD = os.getenv('PASSWORD')
    hostname = 'db'
    user = 'root'
    db = 'dashboard'
    database = pymysql.connections.Connection(
        host=hostname,
        user=user,
        password=PASSWORD,
        db = db,
    )
    cursor = database.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS dashboard")
    cursor.execute("SHOW DATABASES")

    # Closing the cursor and connection to the database
    cursor.close()
    database.close()


# initial tables
def initial_tables(db, bcrypt):
    usersnum = get_num_users(db)
    if usersnum == 0:
        # initial data if first time
        initial_data(db, bcrypt)
        # merge the tasks into users
        preprocess(db)
        # calculation on users' performance
        process(db)


def daily_update_tables(db):
    # merge the tasks into users
    preprocess(db)
    # calculation on users' performance
    process(db)


# initial data from API
def initial_data(db, bcrypt):
    WEBSITE = os.getenv('WEBSITE')
    API_KEY = os.getenv('API_KEY')
    # load the tasks API
    task_response = requests.get(f'{WEBSITE}/tasks.json?key={API_KEY}')
    task_data = task_response.json()
    # load the users API
    user_response = requests.get(f'{WEBSITE}/users.json?key={API_KEY}')
    user_data = user_response.json()
    for user in user_data:
        hashed_password = bcrypt.generate_password_hash(user['password'])
        new_user = User(
            username=user['user_name'], 
            password=hashed_password, 
            usernum=user['user_id'], 
            firstname=user['first_name'], 
            lastname=user['last_name'], 
            team=user['team'], 
            peer_ratings=json.dumps(user['peer_rating']),
            )
        db.session.add(new_user)
    for task in task_data:
        if task['status'] == 'Completed':
            task_status = True
        else:
            task_status = False
        new_task = Task(
            tasknum=task['task_id'],
            sprint=task['sprint'],
            time_assigned=task['date_assigned'],
            status_completed=task_status, 
            time_completed=task['date_completed'],
            point=task['points'],
            usernum=task['user_id']
            )
        db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'All tasks added and users registered successfully'}), 200