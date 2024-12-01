from sqlalchemy.sql import text

# reusable SQL queries
def get_users(db, query="*"):
    users_query = text(f"""SELECT {query} FROM users""")
    users = db.session.execute(users_query).fetchall()
    return users


def get_user_by_username(db, username, query="*"):
    user_query = text(f"""SELECT {query} FROM users WHERE username = :username""")
    user = db.session.execute(user_query, {'username': username}).fetchone()
    return user


def get_user_by_id(db, user_id, query="*"):
    user_query = text(f"""SELECT {query} FROM users WHERE id = :user_id""")
    user = db.session.execute(user_query, {'user_id': user_id}).fetchone()
    return user


def get_user_by_usernum(db, usernum, query="*"):
    user_query = text(f"""SELECT {query} FROM users WHERE usernum = :usernum""")
    user = db.session.execute(user_query, {'usernum': usernum}).fetchone()
    return user


def get_num_users(db):
    total_query = text("""SELECT COUNT(*) FROM users""")
    total = db.session.execute(total_query).fetchone()[0]
    return total   


def get_tasks(db, query="*"):
    tasks_query = text(f"""SELECT {query} FROM tasks""")
    tasks = db.session.execute(tasks_query).fetchall()
    return tasks

def get_team_users(db, team, query="*"):
    team_users_query = text(f"""SELECT {query} FROM users WHERE team = :team""")
    team_users = db.session.execute(team_users_query, {'team': team}).fetchall()
    return team_users