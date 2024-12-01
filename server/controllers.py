from flask import json
from models import User, RegisterModel, LoginModel, ChangePasswordModel
from sqlalchemy import text
from sql_queries import get_user_by_username, get_user_by_id, get_user_by_usernum, get_num_users, get_users, get_team_users
import helpers
from flask_bcrypt import Bcrypt


class UserController:
    def __init__(self, db):
        self.db = db
        self.bcrypt = Bcrypt()


    def register_user(self, data: RegisterModel):
        user_exists = get_user_by_username(self.db, data.username) is not None
        if user_exists or data.password != data.cf_password:
            raise ValueError('User already registered or passwords do not match')
        hashed_password = self.bcrypt.generate_password_hash(data.password)
        new_user_num = get_num_users(self.db) + 1
        new_user = User(
            username=data.username,
            password=hashed_password,
            usernum=new_user_num,
            firstname=data.first_name,
            lastname=data.last_name,
            team=data.team
        )
        self.db.session.add(new_user)
        self.db.session.commit()
        self._initial_user_data(new_user_num)
        user = get_user_by_usernum(self.db, new_user_num)
        return user


    def _initial_user_data(self, new_user_num):
        helpers.new_user_update(self.db, new_user_num)
        self.db.session.commit()


    def login_user(self, data: LoginModel):
        user = get_user_by_username(self.db, data.username)
        if user is None or not self.bcrypt.check_password_hash(user.password, data.password):
             raise PermissionError({'message': 'Unauthorized'})
        return user
        

    def change_password(self, data: ChangePasswordModel, user_id: int) -> User:
        user = get_user_by_id(self.db, user_id)
        if not self.bcrypt.check_password_hash(user.password, data.old_password) or data.new_password != data.cf_password \
            or data.old_password == data.new_password:
            raise PermissionError({'message': 'Unauthorized'})
        change_password_query = text("""UPDATE users SET password = :new_password WHERE id = :user_id""")
        self.db.session.execute(change_password_query, {'new_password': self.bcrypt.generate_password_hash(data.new_password),
                                                        'user_id': user_id})
        self.db.session.commit()
        return user


    def get_user(self, user_id: int) -> User:
        user = get_user_by_id(self.db, user_id)
        return user


    def get_num_users(self) -> int:
        total = get_num_users(self.db)
        return total


    def one_monthly_pts(self, user_id: int) -> dict:
        user = get_user_by_id(self.db, user_id, query="performance")
        performance = json.loads(user.performance)
        monthly_points = dict()
        for timeline in performance.keys():
            monthly_points[timeline] = performance[timeline]['total_points']
        return monthly_points


    def one_sprint_pts(self, user_id: int) -> dict:
        user = get_user_by_id(self.db, user_id, query="sprint_pts")
        sprint_points = json.loads(user.sprint_pts)
        return sprint_points


    def one_monthly_tasks(self, user_id: int) -> dict:
        user = get_user_by_id(self.db, user_id, query="performance")
        performance = json.loads(user.performance)
        monthly_tasks = dict()
        for timeline in performance.keys():
            monthly_tasks[timeline] = dict()
            monthly_tasks[timeline]['1pt_task'] = performance[timeline]['1pt_task']
            monthly_tasks[timeline]['2pt_task'] = performance[timeline]['2pt_task']
            monthly_tasks[timeline]['3pt_task'] = performance[timeline]['3pt_task']
        return monthly_tasks

    def one_month_time(self, user_id: int) -> dict:
        user = get_user_by_id(self.db, user_id, query="time")
        timing = json.loads(user.time)
        monthly_time = dict()
        for timeline in timing.keys():
            monthly_time[timeline] = dict()
            monthly_time[timeline]['1pt_time'] = timing[timeline]['1pt_time']
            monthly_time[timeline]['2pt_time'] = timing[timeline]['2pt_time']
            monthly_time[timeline]['3pt_time'] = timing[timeline]['3pt_time']
        return monthly_time


    def whole_monthly_rank(self, month: str) -> list:
        users = get_users(self.db, query="firstname, lastname, performance")
        whole_rank = ({'name': f"{user.firstname} {user.lastname}", 'points': json.loads(user.performance)[month]['total_points']} for user in users)
        whole_rank = sorted(whole_rank, key=lambda x: (x['points'], x['name']), reverse=True)
        return whole_rank[:8]


    def team_monthly_rank(self, user_id: int, month: str) -> list:
        user = get_user_by_id(self.db, user_id, query="team")
        team = user.team
        team_users = get_team_users(self.db, team, query="firstname, lastname, performance")
        users = get_users(self.db)
        timeline_data = json.loads(users[0].performance).keys()
        team_rank = [{'name': f"{employee.firstname} {employee.lastname}", 
                    'last_points': json.loads(employee.performance)[helpers.process_last_month(month, timeline_data)]['total_points'], 
                    'points': json.loads(employee.performance)[month]['total_points']} for employee in team_users]
        team_rank = sorted(team_rank, key=lambda x: x['last_points'], reverse=True)
        for employee in team_rank:
            employee['last_rank'] = team_rank.index(employee) + 1
        team_rank = sorted(team_rank, key=lambda x: (x['points'], x['name']), reverse=True)
        for employee in team_rank:
            employee['rank'] = team_rank.index(employee) + 1
            if employee['last_rank'] > employee['rank']:
                employee['status'] = 'up'
            elif employee['last_rank'] < employee['rank']:
                employee['status'] = 'down'
            else:
                employee['status'] = 'same'
        return team_rank[:5]


    def team_completion(self) -> list:
        users = get_users(self.db)
        timeline_data = json.loads(users[0].performance).keys()
        team_set = set([user.team for user in users])
        if 'Not Applicable' in team_set:
            team_set.remove('Not Applicable')
        teams_individuals = dict()
        teams_rate = dict()
        for team in team_set:
            teams_individuals[team] = [user for user in users if user.team == team]
            teams_rate[team] = dict()
            for timeline in timeline_data:
                # initialize the monthly completion rate
                teams_rate[team][timeline] = 0    
                # calculate the monthly completion rate  
                points_team_completed = sum([json.loads(user.performance)[timeline]['total_points'] for user in teams_individuals[team]])
                points_team_assigned = points_team_completed + sum([json.loads(user.performance)[timeline]['incomplete'] for user in teams_individuals[team]])
                teams_rate[team][timeline] = round(points_team_completed / points_team_assigned, 4)
        return teams_rate