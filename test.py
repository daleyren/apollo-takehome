import pytest
import sqlite3
import os
from app import app

TEST_DB = 'test_vehicle.db'

@pytest.fixture(scope='function')
def test_client():
    app.config['TESTING'] = True
    app.config['DATABASE'] = TEST_DB

    with app.test_client() as client:
        connection = sqlite3.connect(TEST_DB)
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS vehicles")
        cursor.execute("""
        CREATE TABLE vehicles (
            manufacturer_name TEXT,
            description TEXT,
            horsepower INTEGER,
            model_name TEXT,
            model_year INTEGER,
            purchase_price REAL,
            fuel_type TEXT,
            vin TEXT UNIQUE
        )
        """)
        connection.commit()
        connection.close()

        yield client

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_get_empty_vehicles(test_client):
    """test vehicle retrieval with empty table"""
    response = test_client.get('/vehicle')
    assert response.status_code == 200
    assert response.get_json() == []


def test_add_vehicle(test_client):
    """test add new vehicle"""
    vehicle_data = {
        "manufacturer_name": "Toyota",
        "description": "flat tire, missing windows, missing engine",
        "horsepower": 200,
        "model_name": "Camry",
        "model_year": 2020,
        "purchase_price": 24000.50,
        "fuel_type": "Gasoline",
        "vin": "1HGCM82633A123456"
    }
    response = test_client.post('/vehicle', json=vehicle_data)
    assert response.status_code == 201
    assert response.get_json() == vehicle_data


def test_get_vehicle_by_vin(test_client):
    """test vin vehicle retrieval"""
    # add vehicle
    vehicle_data = {
        "manufacturer_name": "Honda",
        "description": "completely totaled",
        "horsepower": 180,
        "model_name": "Civic",
        "model_year": 2019,
        "purchase_price": 22000.00,
        "fuel_type": "Gasoline",
        "vin": "1HGCM82633A123456"
    }
    post_response = test_client.post('/vehicle', json=vehicle_data)
    assert post_response.status_code == 201

    # retrieve vehicle by VIN
    vin = "1HGCM82633A123456"
    response = test_client.get(f'/vehicle/{vin}')
    assert response.status_code == 200
    assert response.get_json()['vin'] == vin


def test_update_vehicle(test_client):
    """test update on vehicle using vin"""
    # add vehicle
    original_data = {
        "manufacturer_name": "Honda",
        "description": "completely totaled",
        "horsepower": 180,
        "model_name": "Civic",
        "model_year": 2019,
        "purchase_price": 22000.00,
        "fuel_type": "Gasoline",
        "vin": "1HGCM82633A123456"
    }
    post_response = test_client.post('/vehicle', json=original_data)
    assert post_response.status_code == 201

    # update vehicle by vin
    updated_data = {
        "manufacturer_name": "Honda",
        "description": "Updated description",
        "horsepower": 220,
        "model_name": "Civic",
        "model_year": 2021,
        "purchase_price": 25000.00,
        "fuel_type": "Gasoline"
    }
    vin = "1HGCM82633A123456"
    response = test_client.put(f'/vehicle/{vin}', json=updated_data)
    assert response.status_code == 200
    assert response.get_json()['message'] == "Vehicle updated successfully"
    
    # verify
    get_response = test_client.get(f'/vehicle/{vin}')
    assert get_response.status_code == 200
    assert get_response.get_json()['description'] == "Updated description"
    assert get_response.get_json()['horsepower'] == 220
    assert get_response.get_json()['model_year'] == 2021
    assert get_response.get_json()['purchase_price'] == 25000.00


def test_delete_vehicle(test_client):
    """test vehicle deletion"""
    # add vehicle
    vehicle_data = {
        "manufacturer_name": "Honda",
        "description": "Reliable car",
        "horsepower": 180,
        "model_name": "Civic",
        "model_year": 2019,
        "purchase_price": 22000.00,
        "fuel_type": "Gasoline",
        "vin": "1HGCM82633A123456"
    }
    post_response = test_client.post('/vehicle', json=vehicle_data)
    assert post_response.status_code == 201

    # delete vehicle
    vin = "1HGCM82633A123456"
    response = test_client.delete(f'/vehicle/{vin}')
    assert response.status_code == 204

    # verify
    get_response = test_client.get(f'/vehicle/{vin}')
    assert get_response.status_code == 404


def test_add_vehicle_duplicate_vin(test_client):
    """test duplicate VIN"""
    vehicle_data = {
        "manufacturer_name": "Honda",
        "description": "Another reliable car",
        "horsepower": 180,
        "model_name": "Civic",
        "model_year": 2019,
        "purchase_price": 22000.00,
        "fuel_type": "Gasoline",
        "vin": "1HGCM82633A123456"
    }
    # add vehicle
    response = test_client.post('/vehicle', json=vehicle_data)
    assert response.status_code == 201

    # add vehicle again
    duplicate_response = test_client.post('/vehicle', json=vehicle_data)
    assert duplicate_response.status_code == 422
    assert "VIN must be unique" in duplicate_response.get_json()['error']


def test_add_vehicle_missing_field(test_client):
    """test vehicle with missing fields"""
    # missing model_year and other fields
    incomplete_vehicle_data = {
        "manufacturer_name": "Ford",
        "description": "A truck",
        "horsepower": 300,
        "model_name": "F-150",
    }
    response = test_client.post('/vehicle', json=incomplete_vehicle_data)
    assert response.status_code == 422
    assert "Missing field" in response.get_json()['error']
