from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Initialize the Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for all routes

# Load the trained models, scaler, label encoder, and dataset for clustering
rf_model = joblib.load('crop_recommendation_model.pkl')  # Load RandomForest model
scaler = joblib.load('scaler.pkl')  # Load StandardScaler
label_encoder = joblib.load('label_encoder.pkl')  # Load LabelEncoder
crop_data = pd.read_csv('Crop_recommendation.csv')  # Read crop dataset for clustering

# Create a function to predict the crop
@app.route('/predict', methods=['POST'])
def predict_crop():
    data = request.get_json()

    required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400
    
    try:
        # Extract input data
        input_data = [
            data['N'],
            data['P'],
            data['K'],
            data['temperature'],
            data['humidity'],
            data['ph'],
            data['rainfall']
        ]
        
        # Convert input data into DataFrame
        input_df = pd.DataFrame([input_data], columns=required_fields)

        # Scale input data
        input_scaled = scaler.transform(input_df)

        # Make prediction using the RandomForest model
        prediction = rf_model.predict(input_scaled)

        # Convert prediction from encoded value back to crop label
        predicted_crop = label_encoder.inverse_transform([prediction[0]])[0]

        return jsonify({"crop": predicted_crop})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
