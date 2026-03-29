import pytest
import os
import sqlite3
from app import app, init_db, DB_FILE

# Fixture to set up a clean test environment
@pytest.fixture
def client():
    # Use a separate database for testing to avoid messing up production data
    app.config['TESTING'] = True
    
    # Ensure fresh database before testing
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    init_db()

    with app.test_client() as client:
        yield client
        
    # Cleanup after tests
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"ACEest Fitness API is running" in response.data

def test_add_client(client):
    data = {
        "name": "John Doe",
        "age": 28,
        "weight": 80.5,
        "program": "Hypertrophy (HT)"
    }
    response = client.post('/client', json=data)
    assert response.status_code == 201
    
    # 80.5 * 30 = 2415
    json_data = response.get_json()
    assert json_data['message'] == "Client added successfully"
    assert json_data['calories'] == 2415

def test_add_duplicate_client(client):
    data = {"name": "Jane", "age": 25, "weight": 60, "program": "Fat Loss (FL)"}
    client.post('/client', json=data)
    
    # Try adding again
    response = client.post('/client', json=data)
    assert response.status_code == 409
    assert b"Client already exists" in response.data

def test_get_client(client):
    # Setup test data
    data = {"name": "Mike", "age": 35, "weight": 90, "program": "General Fitness (GF)"}
    client.post('/client', json=data)
    
    # Fetch data
    response = client.get('/client/Mike')
    assert response.status_code == 200
    
    json_data = response.get_json()
    assert json_data['name'] == "Mike"
    assert json_data['program'] == "General Fitness (GF)"
    assert json_data['calories'] == 2340  # 90 * 26

def test_get_nonexistent_client(client):
    response = client.get('/client/Nobody')
    assert response.status_code == 404