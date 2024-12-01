import pytest
import json
from models import User, Task
from app import db 

def test_register_user(client):
    # Arrange
    data = {
        'username': 'testuser',
        'password': 'password',
        'cf_password': 'password',
        'first_name': 'Test',
        'last_name': 'User',
        'team': 'Admin Portal'
    }
    # Act
    response = client.post('/register', data=json.dumps(data), content_type='application/json')
    # Assert
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['username'] == 'testuser'
    assert response_data['id'] == 3


def test_login_user(client):
    # Arrange
    data = {
        'username': 'testuser2',
        'password': 'password',
    }
    # Act
    response = client.post('/login', data=json.dumps(data), content_type='application/json')
    # Assert
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['username'] == 'testuser2'
    assert response_data['id'] == 2


def test_change_password(client):
    # Arrange
    data1 = {
        'username': 'testuser1',
        'password': 'password',
    }
    data2 = {
        'old_password': 'password',
        'new_password': 'newpassword',
        'cf_password': 'newpassword',
    }
    # Act
    client.post('/login', data=json.dumps(data1), content_type='application/json')
    response = client.post('/change-password', data=json.dumps(data2), content_type='application/json')
    # Assert
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['message'] == 'Password changed'


def test_get_user(client):
    # Arrange
    data = {
        'username': 'testuser2',
        'password': 'password',
    }
    # Act
    client.post('/login', data=json.dumps(data), content_type='application/json')
    response = client.get('/@me')
    # Assert
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['username'] == 'testuser2'
    assert response_data['id'] == 2
    assert response_data['name'] == 'Test User 2'
    assert response_data['team'] == 'Admin Portal'


def test_one_level(client):
    # Arrange
    data = {
        'username': 'testuser2',
        'password': 'password',
    }
    # Act
    client.post('/login', data=json.dumps(data), content_type='application/json')
    response = client.get('/individual/2/level')
    # Assert
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['point'] == 4
    assert response_data['max_score'] == 42


def test_one_metrics(client):
    # Arrange
    data = {
        'username': 'testuser2',
        'password': 'password',
    }
    # Act
    client.post('/login', data=json.dumps(data), content_type='application/json')
    response = client.get('/individual/2/metrics')
    # Assert
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['point'] == 4
    assert response_data['rank'] == 1
    assert response_data['total'] == 2
    assert response_data['completion_rate'] == 0.5
    assert response_data['average_peer_rating'] == 0
    

def test_one_monthly_pts(client):
    # Arrange
    data = {
        'username': 'testuser2',
        'password': 'password',
    }
    # Act
    client.post('/login', data=json.dumps(data), content_type='application/json')
    response = client.get('/individual/2/monthly_pts')
    # Assert
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['01-2023'] == 0
    assert response_data['05-2023'] == 1
    assert response_data['06-2023'] == 3
    assert response_data['08-2023'] == 0
    assert response_data['12-2023'] == 0


def test_one_sprint_pts(client):
    # Arrange
    data = {
        'username': 'testuser2',
        'password': 'password',
    }
    # Act
    client.post('/login', data=json.dumps(data), content_type='application/json')
    response = client.get('/individual/2/sprint_pts')
    # Assert
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['1'] == {'completed': 1, 'incomplete': 2} 
    assert response_data['2'] == {'completed': 3, 'incomplete': 2}


def test_one_monthly_tasks(client):
    # Arrange
    data = {
        'username': 'testuser2',
        'password': 'password',
    }
    # Act
    client.post('/login', data=json.dumps(data), content_type='application/json')
    response = client.get('/individual/2/monthly_tasks')
    # Assert
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['01-2023'] == {'1pt_task': 0, '2pt_task': 0, '3pt_task': 0}
    assert response_data['05-2023'] == {'1pt_task': 1, '2pt_task': 0, '3pt_task': 0}
    assert response_data['06-2023'] == {'1pt_task': 0, '2pt_task': 0, '3pt_task': 1}
    assert response_data['08-2023'] == {'1pt_task': 0, '2pt_task': 0, '3pt_task': 0}
    assert response_data['12-2023'] == {'1pt_task': 0, '2pt_task': 0, '3pt_task': 0}


def test_one_month_time(client):
    # Arrange
    data = {
        'username': 'testuser2',
        'password': 'password',
    }
    # Act
    client.post('/login', data=json.dumps(data), content_type='application/json')
    response = client.get('/individual/2/monthly_time')
    # Assert
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['01-2023'] == {'1pt_time': 0, '2pt_time': 0, '3pt_time': 0}
    assert response_data['05-2023'] == {'1pt_time': 131.18, '2pt_time': 0, '3pt_time': 0}
    assert response_data['06-2023'] == {'1pt_time': 0, '2pt_time': 0, '3pt_time': 360}
    assert response_data['08-2023'] == {'1pt_time': 0, '2pt_time': 0, '3pt_time': 0}
    assert response_data['12-2023'] == {'1pt_time': 0, '2pt_time': 0, '3pt_time': 0}


def test_whole_monthly_rank(client):
    # Arrange
    data = {
        'username': 'testuser2',
        'password': 'password',
    }
    # Act
    client.post('/login', data=json.dumps(data), content_type='application/json')
    response = client.get('/team/monthly_rank/06-2023')
    # Assert
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data[0] == {'points': 3, 'name': 'Test User 2'}
    assert response_data[1] == {'points': 0, 'name': 'Test User 1'}


def test_team_monthly_rank(client):
    # Arrange
    data = {
        'username': 'testuser2',
        'password': 'password',
    }
    # Act
    client.post('/login', data=json.dumps(data), content_type='application/json')
    response = client.get('/team/2/monthly_rank/06-2023')
    # Assert
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data[0] == {'last_points': 1, 'last_rank': 1, 'points': 3, 'rank': 1, 
                                'name': 'Test User 2', 'status': 'same'}
    assert response_data[1] == {'last_points': 0, 'last_rank': 2, 'points': 0, 'rank': 2, 
                                'name': 'Test User 1', 'status': 'same'}


def test_team_completion_rate(client):
    # Arrange
    data = {
        'username': 'testuser2',
        'password': 'password',
    }
    # Act
    client.post('/login', data=json.dumps(data), content_type='application/json')
    response = client.get('/team/completion')
    # Assert
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['Admin Portal']['01-2023'] == 0.0
    assert response_data['Admin Portal']['05-2023'] == 1.0
    assert response_data['Admin Portal']['06-2023'] == 0.6
    assert response_data['Admin Portal']['08-2023'] == 0.0


def test_logout_user(client):
    # Arrange
    data = {
        'username': 'testuser2',
        'password': 'password',
    }
    # Act
    client.post('/login', data=json.dumps(data), content_type='application/json')
    response = client.post('/logout')
    # Assert
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['message'] == 'Logged out'

