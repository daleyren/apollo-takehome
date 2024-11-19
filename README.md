# Vehicle Director

## Overview

The **Vehicle Directory** is a simple RESTful API built with Flask that allows users to manage a collection of vehicles. It supports creating, reading, updating, and deleting vehicle records stored in an SQLite database.

## Features

- **Add Vehicles:** Create new vehicle entries with details like manufacturer, model, year, and VIN.
- **View Vehicles:** Retrieve a list of all vehicles or a specific vehicle by its VIN.
- **Update Vehicles:** Modify details of an existing vehicle.
- **Delete Vehicles:** Remove a vehicle from the database.

## Tech Stack

- **Backend Framework:** Flask
- **Database:** SQLite
- **Testing Framework:** pytest
- **Language:** Python 3.8+

## Setup Instructions

### Installation

1. **Clone the Repository**

```bash
  git clone https://github.com/daleyren/apollo-takehome.git
  cd apollo-takehome
```

2. **Create a Virtual Environment**

```bash
  python3 -m venv venv
  source venv/bin/activate
```

3. **Install Dependencies**

```bash
  pip install -r requirements.txt
```

## API Endpoints

### 1. Get All Vehicles

- **URL:** `/vehicle`
- **Method:** `GET`
- **Description:** Retrieve a list of all vehicles.
- **Response:** JSON array of vehicle objects.

### 2. Add a New Vehicle

- **URL:** `/vehicle`
- **Method:** `POST`
- **Description:** Add a new vehicle to the database.
- **Request Body:** JSON object with fields:
  - `manufacturer_name` (string)
  - `description` (string)
  - `horsepower` (integer)
  - `model_name` (string)
  - `model_year` (integer)
  - `purchase_price` (float)
  - `fuel_type` (string)
  - `vin` (string, unique)
- **Response:** JSON object of the created vehicle.

### 3. Get Vehicle by VIN

- **URL:** `/vehicle/<vin>`
- **Method:** `GET`
- **Description:** Retrieve a specific vehicle by its VIN.
- **Response:** JSON object of the vehicle or an error message if not found.

### 4. Update Vehicle by VIN

- **URL:** `/vehicle/<vin>`
- **Method:** `PUT`
- **Description:** Update details of a specific vehicle.
- **Request Body:** JSON object with fields to update.
- **Response:** Success message or error if the vehicle is not found.

### 5. Delete Vehicle by VIN

- **URL:** `/vehicle/<vin>`
- **Method:** `DELETE`
- **Description:** Delete a specific vehicle by its VIN.
- **Response:** No content on success or an error message if not found.

## Running Application

The server will start on http://127.0.0.1:5000/.

```bash
  python app.py
```

## Running Pytests

```bash
  python pytest test.py
```
