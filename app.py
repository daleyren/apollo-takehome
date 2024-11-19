from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'vehicle.db'

# build initial vehicles table/database
def init_db():
    connection = sqlite3.connect(app.config['DATABASE'])
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
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


@app.route('/vehicle', methods=['GET'])
def get_vehicles():
    connection = sqlite3.connect(app.config['DATABASE'])
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vehicles")
    vehicles = cursor.fetchall()
    connection.close()

    vehicle_list = [
        {
            "manufacturer_name": v[0],
            "description": v[1],
            "horsepower": v[2],
            "model_name": v[3],
            "model_year": v[4],
            "purchase_price": v[5],
            "fuel_type": v[6],
            "vin": v[7]
        }
        for v in vehicles
    ]
    return jsonify(vehicle_list), 200


@app.route('/vehicle', methods=['POST'])
def add_vehicle():
    data = request.get_json()

    # validate required fields
    required_fields = [
        "manufacturer_name", "description", "horsepower",
        "model_name", "model_year", "purchase_price", "fuel_type", "vin"
    ]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 422

    try:
        connection = sqlite3.connect(app.config['DATABASE'])
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO vehicles (
            manufacturer_name,
            description,
            horsepower,
            model_name,
            model_year,
            purchase_price,
            fuel_type,
            vin
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['manufacturer_name'],
            data['description'],
            data['horsepower'],
            data['model_name'],
            data['model_year'],
            data['purchase_price'],
            data['fuel_type'],
            data['vin']
        ))
        connection.commit()
        connection.close()
        return jsonify(data), 201
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: vehicles.vin" in str(e):
            return jsonify({"error": "VIN must be unique"}), 422
        else:
            return jsonify({"error": "Database error"}), 500


@app.route('/vehicle/<vin>', methods=['GET'])
def get_vehicle_by_vin(vin):
    connection = sqlite3.connect(app.config['DATABASE'])
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM vehicles WHERE vin = ?", (vin,))
    vehicle = cursor.fetchone()
    connection.close()

    if vehicle:
        return jsonify({
            "manufacturer_name": vehicle[0],
            "description": vehicle[1],
            "horsepower": vehicle[2],
            "model_name": vehicle[3],
            "model_year": vehicle[4],
            "purchase_price": vehicle[5],
            "fuel_type": vehicle[6],
            "vin": vehicle[7]
        }), 200
    else:
        return jsonify({"error": "Vehicle not found"}), 404

@app.route('/vehicle/<vin>', methods=['PUT'])
def update_vehicle(vin):
    data = request.get_json()

    try:
        connection = sqlite3.connect(app.config['DATABASE'])
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE vehicles
        SET manufacturer_name = ?,
            description = ?,
            horsepower = ?,
            model_name = ?,
            model_year = ?,
            purchase_price = ?,
            fuel_type = ?
        WHERE vin = ?
        """, (
            data.get('manufacturer_name'),
            data.get('description'),
            data.get('horsepower'),
            data.get('model_name'),
            data.get('model_year'),
            data.get('purchase_price'),
            data.get('fuel_type'),
            vin
        ))
        connection.commit()
        connection.close()

        if cursor.rowcount == 0:
            return jsonify({"error": "Vehicle not found"}), 404
        return jsonify({"message": "Vehicle updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/vehicle/<vin>', methods=['DELETE'])
def delete_vehicle(vin):
    connection = sqlite3.connect(app.config['DATABASE'])
    cursor = connection.cursor()
    cursor.execute("DELETE FROM vehicles WHERE vin = ?", (vin,))
    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Vehicle not found"}), 404
    return '', 204


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
