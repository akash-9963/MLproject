from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from the frontend

# Load the trained model and scaler
def load_model_and_scaler():
    try:
        # Load the model and scaler
        model_path = "static/crop_recommendation_model.pkl"
        scaler_path = "static/scaler.pkl"

        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)

        with open(scaler_path, 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)

        print("Model and scaler loaded successfully.")
        return model, scaler
    except Exception as e:
        print(f"Error loading model/scaler: {e}")
        raise

# API endpoint to get crop recommendation
@app.route('/api/recommend_crop', methods=['POST'])
def recommend_crop():
    try:
        # Get data from the request
        data = request.get_json()

        # Log the received data for debugging
        print("Received data:", data)

        # Ensure all necessary fields are provided
        required_fields = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall']
        for field in required_fields:
            if field not in data:
                print(f"Missing field: {field}")
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Prepare the data for prediction
        input_data = [data[field] for field in required_fields]

        # Load the model and scaler
        model, scaler = load_model_and_scaler()

        # Convert input data to a DataFrame
        input_data_df = pd.DataFrame([input_data], columns=required_fields)

        # Rename columns to match the model's feature names
        input_data_df = input_data_df.rename(columns={
            'nitrogen': 'N',
            'phosphorus': 'P',
            'potassium': 'K'
        })

        # Scale the input data
        input_data_scaled = scaler.transform(input_data_df)

        # Make the prediction
        prediction = model.predict(input_data_scaled)

        # Ensure prediction is 1D
        prediction = prediction.flatten()

        # Load the label encoder to map the predicted number to the crop name
        label_encoder_path = 'static/label_encoder.pkl'
        with open(label_encoder_path, 'rb') as le_file:
            label_encoder = pickle.load(le_file)

        # Convert the prediction from model (a NumPy array) back to the crop name using the LabelEncoder
        predicted_crop = label_encoder.inverse_transform(prediction)[0]

        # Return the recommended crop name
        return jsonify({"recommended_crop": predicted_crop})

    except Exception as e:
        # Log the error for debugging
        print("Error in /api/recommend_crop:", str(e))
        return jsonify({"error": "An error occurred while processing the request."}), 500

if __name__ == '__main__':
    app.run(debug=True)
