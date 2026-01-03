from fastapi.testclient import TestClient

from src.main import app

import pytest
from httpx import AsyncClient
from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'nonexistent@example.com'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user_data = {'name': 'Alice Brown', 'email': 'alice@example.com'}
    response = client.post("/api/v1/user", json=new_user_data)
    assert response.status_code == 201
    # Возвращается ID созданного пользователя
    assert isinstance(response.json(), int)

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    existing_email = users[0]['email']
    response = client.post("/api/v1/user", json={'name': 'Duplicate User', 'email': existing_email})
    assert response.status_code == 409
    assert response.json() == {'detail': 'User with this email already exists'}


def test_delete_user():
    '''Удаление пользователя'''
    # Сначала создадим пользователя для удаления
    user_to_delete = {'name': 'User To Delete', 'email': 'delete@example.com'}
    create_response = client.post("/api/v1/user", json=user_to_delete)
    user_id = create_response.json()
    
    # Удаляем пользователя
    delete_response = client.delete("/api/v1/user", params={'email': 'delete@example.com'})
    assert delete_response.status_code == 204
    
    # Проверяем, что пользователь действительно удалён
    check_response = client.get("/api/v1/user", params={'email': 'delete@example.com'})
    assert check_response.status_code == 404
