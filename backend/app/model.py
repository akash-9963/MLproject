import pickle
import numpy as np
import pandas as pd

# Load the trained model and scaler
def load_model():
    model_path = "static/crop_recommendation_model.pkl"
    scaler_path = "static/scaler.pkl"
    
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    
    with open(scaler_path, 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
        
    return model, scaler

# Function to predict crop based on user input
def predict_crop(input_data):
    model, scaler = load_model()

    # Ensure input_data is in a pandas DataFrame format with the same column names as during training
    column_names = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'humidity', 'ph', 'rainfall']
    input_data_df = pd.DataFrame([input_data], columns=column_names)

    # Scale the input data
    input_data_scaled = scaler.transform(input_data_df)

    # Predict the crop
    prediction = model.predict(input_data_scaled)
    
    return prediction[0]
