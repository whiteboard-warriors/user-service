'''
Test User operations
'''
from unittest.mock import ANY
import http.client

from faker import Faker
fake = Faker()


def test_register(client):
    new_user = {
        'fname': fake.first_name(),
        'lname': fake.last_name(),
        'username': fake.user_name(),
        'email': fake.email(),
        'password': fake.password(),
    }

    response = client.post('/api/register', data=new_user)
    result = response.json

    assert http.client.CREATED == response.status_code

    expected = {
        'id': ANY,
        'fname': new_user['fname'],
        'lname': new_user['lname'],
        'username': new_user['username'],
        'email': new_user['email']
    }

    assert result == expected


def test_login(client):
    new_user = {
        'fname': fake.first_name(),
        'lname': fake.last_name(),
        'username': fake.user_name(),
        'email': fake.email(),
        'password': fake.password(),
    }

    login_data = {
        'email': new_user['email'],
        'password': new_user['password']
    }
    response = client.post('/api/register', data=new_user)
    assert http.client.CREATED == response.status_code

    response = client.post('/api/login', data=login_data)
    result = response.json
    assert http.client.OK == response.status_code

    expected = {
        'Authorized': ANY,
    }

    assert result == expected
