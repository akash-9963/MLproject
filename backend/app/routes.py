from flask import request, jsonify
from app import app
from app.model import predict_crop

@app.route('/api/recommend_crop', methods=['POST'])
def recommend_crop():
    try:
        # Get data from the request
        data = request.get_json()

        # Ensure all necessary data is provided
        required_fields = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Extract the user input data
        input_data = [
            data['nitrogen'],
            data['phosphorus'],
            data['potassium'],
            data['temperature'],
            data['humidity'],
            data['ph'],
            data['rainfall']
        ]
        
        # Predict the crop
        predicted_crop = predict_crop(input_data)
        
        return jsonify({"crop": predicted_crop})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
