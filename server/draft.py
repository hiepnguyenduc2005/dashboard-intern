# from models import User, Task
# from app import app, db
# from sqlalchemy import text
# from helpers import process_timeline, process_last_month
# import json
from datetime import datetime

# with app.app_context():

#     # user = User.query.filter_by(usernum=1).first()
#     # print(user.tasks[0].tasknum)
#     # task = Task.query.filter_by(tasknum=1).first()
#     # print(task.user.username)
#     users_query = text("""SELECT * FROM users""")
#     users = db.session.execute(users_query).fetchall()
#     users_num = len(users)
#     user = users[0]
#     user_id = user.usernum
#     # total points completion monthly

#     # performance = json.loads(user.performance)
#     # print(type(performance))
#     # print(performance.keys())

#     # def strlist (str):
#     #     list = json.loads(str)[1:-1].split(', ')
#     #     actual_list = [int(i) for i in list]
#     #     return actual_list
    
#     # print(type((strlist(user.peer_ratings))))
#     # print(strlist(user.peer_ratings)[0])    
    
#     # peer_rate = round((sum([strlist(peer.peer_ratings)[user_id - 1] for peer in users]) \
#     #                                 - strlist(user.peer_ratings)[user_id - 1]) / (users_num - 1), 2)
    
#     # print(peer_rate)

#     team = "Data Fusion"
#     month = "06-2023"
#     team_users_query = text("""SELECT firstname, lastname, performance FROM users WHERE team = :team""")
#     team_users = db.session.execute(team_users_query, {'team': team}).fetchall()
#     team_rank = [{'name': f"{employee.firstname} {employee.lastname}", 
#                   'last_points': json.loads(employee.performance)[process_last_month(month)]['total_points'], 
#                   'points': json.loads(employee.performance)[month]['total_points']} for employee in team_users]
#     team_rank = sorted(team_rank, key=lambda x: x['last_points'], reverse=True)
#     for employee in team_rank:
#         employee['last_rank'] = team_rank.index(employee) + 1
#     team_rank = sorted(team_rank, key=lambda x: (x['points'], x['name']), reverse=True)
#     for employee in team_rank:
#         employee['rank'] = team_rank.index(employee) + 1
#         if employee['last_rank'] > employee['rank']:
#             employee['status'] = 'up'
#         elif employee['last_rank'] < employee['rank']:
#             employee['status'] = 'down'
#         else:
#             employee['status'] = 'same'
#     print(team_rank[:5])

date = datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
print(date)