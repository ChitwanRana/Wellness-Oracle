# predict.py
import pandas as pd
import pickle
from predictor.utils.data import preprocessed_symptoms as original_symptoms




# Load the trained model from the .pkl file
def load_model(model_path):
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

# Make predictions using the model
def make_predictions(model, data):
    try:
        predictions = model.predict(data)
        return predictions
    except Exception as e:
        print(f"Error making predictions: {e}")
        return None

# Convert matched symptoms to binary format
def convert_to_binary_vector(matched_symptoms, original_symptoms):
    # Create a binary vector with 0's initially
    binary_vector = [0] * len(original_symptoms)
    
    # Map the matched symptoms to their corresponding index in the original_symptoms list
    for symptom, _ in matched_symptoms:
        if symptom in original_symptoms:
            index = original_symptoms.index(symptom)
            binary_vector[index] = 1  # Set the matched symptom to 1
    
    return binary_vector

# Function to get predictions based on matched symptoms
def get_prediction(matched_symptoms):
    model_file = 'LR-83.pkl'
    
    # Load the model
    model = load_model(model_file)
    
    if model:
        # Convert matched symptoms to a binary vector
        binary_vector = convert_to_binary_vector(matched_symptoms, original_symptoms)
        
        # Convert binary_vector to a DataFrame (if needed by your model)
        new_data = pd.DataFrame([binary_vector], columns=original_symptoms)
        
        # Make predictions
        predictions = make_predictions(model, new_data)
        
        return predictions
    return None
