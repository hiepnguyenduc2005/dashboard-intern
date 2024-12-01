import pytest

from models import User, Task

def test_user():
    user = User(username='testuser', password='password', firstname='Test', lastname='User', team='Admin Portal')
    assert user.username == 'testuser'
    assert user.password == 'password'
    assert user.firstname == 'Test'
    assert user.lastname == 'User'
    assert user.team == 'Admin Portal'

def test_task():
    task1 = Task(tasknum=1, sprint=1, time_assigned='2023-01-01 00:00:00', status_completed=False, point=1, usernum=1)
    assert task1.tasknum == 1
    assert task1.sprint == 1
    assert task1.time_assigned == '2023-01-01 00:00:00'
    assert task1.status_completed == False
    assert task1.point == 1
    assert task1.usernum == 1

    task2 = Task(tasknum=2, sprint=1, time_assigned='2023-12-01 00:00:00', status_completed=True, time_completed='2023-12-31 00:00:00', point=2, usernum=1)
    assert task2.tasknum == 2
    assert task2.sprint == 1
    assert task2.time_assigned == '2023-12-01 00:00:00'
    assert task2.status_completed == True
    assert task2.time_completed == '2023-12-31 00:00:00'
    assert task2.point == 2
    assert task2.usernum == 1