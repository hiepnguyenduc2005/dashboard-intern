from flask import json, session, jsonify
from functools import wraps
from models import User
from sqlalchemy import text
from datetime import datetime
from sql_queries import get_users, get_user_by_id, get_user_by_usernum, get_tasks

### decorators for validation
# login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# id confirmed decorator
def id_confirmed(db):
    def decorator(f):
        @wraps(f)
        def decorated_function(id, *args, **kwargs):
            user_id = session.get('user_id')
            user = get_user_by_id(db, user_id, query="usernum")
            if int(id) != user.usernum:
                return jsonify({'message': 'Unauthorized'}), 401
            return f(id, *args, **kwargs)
        return decorated_function
    return decorator

### helpers for initialization
# new user update
def new_user_update(db, id):
    min_sprint, max_sprint = process_sprint(db)
    timeline_data = process_timeline(db)
    user = User.query.filter_by(usernum=id).first()
    if user is None:
        return jsonify({'message': 'User does not exist'}), 404
    performance, sprint, time = initial_user(min_sprint, max_sprint, timeline_data)
    merge_task(user, performance, sprint, time)
    update_query = text("""UPDATE users SET performance = :performance, sprint_pts = :sprint, 
                        time = :time WHERE usernum = :user_id""")
    db.session.execute(update_query, {'performance': json.dumps(performance), 'sprint': json.dumps(sprint), 
                                        'time': json.dumps(time), 'user_id': id})
    db.session.commit()
    users = get_users(db)
    calc_metric(user, db, users)
    update_rank(db)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200


# merege two relational data
def preprocess(db):
    min_sprint, max_sprint = process_sprint(db)
    timeline_data = process_timeline(db)
    users = User.query.all()    
    for user in users:
        performance, sprint, time = initial_user(min_sprint, max_sprint, timeline_data)
        merge_task(user, performance, sprint, time)
        update_query = text("""UPDATE users SET performance = :performance, sprint_pts = :sprint, time = :time 
                            WHERE usernum = :user_id""")
        db.session.execute(update_query, {'performance': json.dumps(performance), 'sprint': json.dumps(sprint), 
                                        'time': json.dumps(time), 'user_id': user.usernum})
    db.session.commit()
    return jsonify({'message': 'All users updated successfully'})


# process the intergrated dataset on users
def process(db):
    users = get_users(db)
    for user in users:
       calc_metric(user, db, users)
    update_rank(db)
    db.session.commit()
    return jsonify({'message': 'All users calculated successfully'})


### helper functions for above
# extract time period from task
def process_timeline(db):
    tasks = get_tasks(db)
    timeline_data = []
    for task in tasks:
        try:
            assign = task.time_assigned
            month = assign.month
            year = assign.year
        except AttributeError:
            assign = datetime.fromisoformat(task.time_assigned)
            month = assign.month
            year = assign.year
        timeline = f'{month:02}-{year:4}'
        if timeline not in timeline_data:
            timeline_data.append(timeline)
    return timeline_data


# extract sprint period from task
def process_sprint(db):
    min_sprint_query = text("""SELECT MIN(sprint) FROM tasks""")
    min_sprint = db.session.execute(min_sprint_query).fetchone()[0]
    max_sprint_query = text("""SELECT MAX(sprint) FROM tasks""")
    max_sprint = db.session.execute(max_sprint_query).fetchone()[0] + 1
    return min_sprint, max_sprint


# initial the user data
def initial_user(min_sprint, max_sprint, timeline_data):
    # initialize monthly task points and time 
    performance = dict()
    time = dict()
    for timeline in timeline_data:
        performance[timeline] = {'total_points': 0, 'incomplete': 0, '1pt_task': 0, '2pt_task': 0, '3pt_task': 0}
        time[timeline] = {'1pt_time': 0, '2pt_time': 0, '3pt_time': 0}

    # intialize task based on sprint
    sprint = dict()
    for sprinting in range(min_sprint, max_sprint):
        sprint[sprinting] = {'completed': 0, 'incomplete': 0}
    return performance, sprint, time


# merge the task into user
def merge_task(user, performance, sprint, time):
    tasks_user = user.tasks
    # import from task data to user
    for task in tasks_user:  
        point = task.point
        sprints = task.sprint
        assign = task.time_assigned
        month = assign.month
        year = assign.year
        timeline = f'{month:02}-{year:4}'
        if task.status_completed:
            complete = task.time_completed
            timing = complete - assign
            # based on pt_task
            performance[timeline][f'{point}pt_task'] += 1
            performance[timeline]['total_points'] += point
            time[timeline][f'{point}pt_time'] = round(time[timeline][f'{point}pt_time']\
                                                               + timing.days * 24 + timing.seconds / 3600, 2)
            # based on sprint
            sprint[sprints]['completed'] += point
        else:
            performance[timeline]['incomplete'] += point
            sprint[sprints]['incomplete'] += point
    

# update the metric of users
def calc_metric(user, db, users):
    # total points completion monthly
    try:
        performance = json.loads(user.performance)
    except TypeError:
        performance = user.performance
    
    # total experience points 
    total_points = sum([performance[timeline]['total_points'] for timeline in performance.keys()])

    # average peer rating
    def strlist(str):
        list = json.loads(str)[1:-1].split(', ')
        actual_list = [int(i) for i in list]
        return actual_list

    user_id = user.usernum
    users_num = len(users)
    try:
        peer_rate = round((sum([strlist(peer.peer_ratings)[user_id - 1] for peer in users]) \
                                - strlist(user.peer_ratings)[user_id - 1]) / (users_num - 1), 2)
    except TypeError:
        peer_rate = 0
    except IndexError:
        peer_rate = 0
    
    # completion rate
    try:
        sprinting = json.loads(user.sprint_pts)
    except TypeError:
        sprinting = user.sprint_pts
    points_completed = sum([sprinting[sprint]['completed'] for sprint in sprinting.keys()])
    points_assigned = points_completed + sum([sprinting[sprint]['incomplete'] for sprint in sprinting.keys()])
    try: 
        completion_rate = round(points_completed / points_assigned, 4)
    except ZeroDivisionError:
        completion_rate = 0

    update_query = text("""UPDATE users SET total_points = :total_points, completion_rate = :completion_rate, 
                        peer_rate = :peer_rate WHERE usernum = :user_id""")
    db.session.execute(update_query, {'total_points': total_points, 'completion_rate': completion_rate, 'peer_rate': peer_rate, 'user_id': user.usernum})


# update the ranking of users
def update_rank(db):
    update_rank_query = text("""
        UPDATE users
        SET ranking = (
            SELECT ranking
            FROM (
                SELECT
                    usernum,
                    RANK() OVER (ORDER BY total_points DESC) AS ranking
                FROM users
            ) ranked_users
            WHERE ranked_users.usernum = users.usernum
        );
    """)
    db.session.execute(update_rank_query)


# process month to generate tuple of last month and current month
def process_last_month(month, timeline_data):
    last_month = processing_last_month(month)
    if last_month in timeline_data:
        return last_month
    else:
        return month
    
def processing_last_month(month):
    cmonth = int(month.split('-')[0])
    cyear = int(month.split('-')[1])
    if cmonth > 1:
        lmonth = cmonth - 1
        lyear = cyear
    else:  
        lmonth = 12
        lyear = cyear - 1
    last_month = f'{lmonth:02}-{lyear}'
    return last_month

def process_time(time):
    return datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
