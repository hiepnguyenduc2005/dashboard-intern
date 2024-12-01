from flask_bcrypt import Bcrypt
from flask import Blueprint, jsonify, session
from helpers import login_required, id_confirmed
import controllers
import views
from models import db, RegisterModel, LoginModel, ChangePasswordModel
from flask_pydantic import validate

bcrypt = Bcrypt()
bp = Blueprint('blueprint', __name__)

@bp.route('/register', methods=['POST'])
@validate(body=RegisterModel)
def register_user(body: RegisterModel):
    try:
        session.clear()
        user = controllers.UserController(db).register_user(body)
        session['user_id'] = user.id
        return views.user(user, message='Registered')
    except ValueError as e:
        return jsonify({'message': str(e)}), 409
    

@bp.route('/login', methods=['POST'])
@validate(body=LoginModel)
def login_user(body: LoginModel):
    try:
        session.clear()
        user = controllers.UserController(db).login_user(body)
        session['user_id'] = user.id
        return views.user(user, message='Logged in')
    except PermissionError as e:
        return jsonify({'message': str(e)}), 401


@bp.route('/logout', methods=['POST'])
@login_required
def logout_user():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out'})


@bp.route('/change-password', methods=['POST'])
@login_required
@validate(body=ChangePasswordModel)
def change_password(body: ChangePasswordModel):
    try:
        user_id = session.get('user_id')
        user = controllers.UserController(db).change_password(body, user_id)
        return views.user(user, message='Password changed')
    except PermissionError as e:
        return jsonify({'message': str(e)}), 401


@bp.route('/@me')
@login_required
def get_user():
    user_id = session.get('user_id')
    user = controllers.UserController(db).get_user(user_id)
    return views.full_user(user)


@bp.route('/individual/<id>/level')
@login_required
@id_confirmed(db)
def one_level(id):
    user_id = session.get('user_id')
    user = controllers.UserController(db).get_user(user_id)
    return views.one_level(user, 42)
    

@bp.route('/individual/<id>/metrics')
@login_required
@id_confirmed(db)
def one_metrics(id):
    user_id = session.get('user_id')
    user = controllers.UserController(db).get_user(user_id)
    total = controllers.UserController(db).get_num_users()
    return views.one_metrics(user, total)


@bp.route('/individual/<id>/monthly_pts')
@login_required
@id_confirmed(db)
def one_monthly_pts(id):
    user_id = session.get('user_id')
    monthly_points = controllers.UserController(db).one_monthly_pts(user_id)
    return jsonify(monthly_points)


@bp.route('/individual/<id>/sprint_pts')
@login_required
@id_confirmed(db)
def one_sprint_pts(id):
    user_id = session.get('user_id')
    sprint_points = controllers.UserController(db).one_sprint_pts(user_id)
    return jsonify(sprint_points)


@bp.route('/individual/<id>/monthly_tasks')
@login_required
@id_confirmed(db)
def one_monthly_tasks(id):
    user_id = session.get('user_id')
    monthly_tasks = controllers.UserController(db).one_monthly_tasks(user_id)
    return jsonify(monthly_tasks)


@bp.route('/individual/<id>/monthly_time')
@login_required
@id_confirmed(db)
def one_month_time(id):
    user_id = session.get('user_id')
    monthly_time = controllers.UserController(db).one_month_time(user_id)
    return jsonify(monthly_time)


@bp.route('/team/monthly_rank/<month>')
@login_required
def whole_monthly_rank(month):
    top_rank = controllers.UserController(db).whole_monthly_rank(month)
    return jsonify(top_rank)


@bp.route('/team/<id>/monthly_rank/<month>')
@login_required
@id_confirmed(db)
def team_monthly_rank(id, month):
    user_id = session.get('user_id')
    top_rank = controllers.UserController(db).team_monthly_rank(user_id, month)
    return jsonify(top_rank)


@bp.route('/team/completion')
@login_required
def team_completion():
    teams_rate = controllers.UserController(db).team_completion()
    return jsonify(teams_rate)