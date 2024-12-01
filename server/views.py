from flask import jsonify, json

def user(user, message):
    return jsonify({'id': user.usernum, 'username': user.username, 'message': message})

def full_user(user):
    try:
        name = user.firstname + ' ' + user.lastname
        team = user.team
    except TypeError:
        name = 'New User'
        team = 'Not Applicable'
    return jsonify({'id': user.usernum, 'username': user.username, 'name': name, 'team': team})   

def one_level(user, max_score):
    point = user.total_points
    return jsonify({"point": point, 'max_score': max_score})

def one_metrics(user, total):
    point = user.total_points
    rank = user.ranking
    completion_rate = user.completion_rate
    average_peer_rating = user.peer_rate
    return jsonify({'point': point, 'rank': rank, 'total': total, 'completion_rate': completion_rate, 
                    'average_peer_rating': average_peer_rating})