import joblib
import os
import numpy as np
import pandas as pd

class fertilizer_engine:
    """
    Class to handle fertilizer recommendations using ML and soil rules.
    Designed with Humane Compression for easy reading.
    """

    def __init__(self, model_path='model_artifacts'):
        # Step 1: Set the directory for model files
        self.model_path = model_path
        
        # Step 2: Load the trained model and encoders
        # These files must exist in the model_path directory
        self.trained_model = joblib.load(os.path.join(model_path, 'fertilizer_model.joblib'))
        self.crop_encoder = joblib.load(os.path.join(model_path, 'le_crop.joblib'))
        self.target_encoder = joblib.load(os.path.join(model_path, 'le_target.joblib'))
        
        # Step 3: Load the list of features used during training
        with open(os.path.join(model_path, 'features.txt'), 'r') as file_reader:
            self.model_features = file_reader.read().splitlines()

    def get_recommendation(self, soil_ph, nitrogen_level, phosphorus_level, potassium_level, organic_carbon, soil_moisture, crop_type):
        """
        Main logic to calculate recommendations based on soil data.
        Returns a dictionary with status and suggestions.
        """
        
        # Initialize the result dictionary with default values
        output_data = {
            'health_status': 'Healthy',
            'warning_list': [],
            'soil_amendment': None,
            'organic_addition': None,
            'main_fertilizer': None,
            'logic_rationale': []
        }

        # --- Part 1: Soil pH Logic (Safety Gatekeeper) ---
        
        # If soil is too acidic (pH < 5.5)
        if soil_ph < 5.5:
            output_data['health_status'] = 'Critical'
            output_data['warning_list'].append('Soil is too acidic.')
            output_data['soil_amendment'] = 'Dolomite/Lime'
            output_data['logic_rationale'].append('Apply Dolomite/Lime to increase pH. Acidic soil locks nutrients.')
            
        # If soil is too alkaline (pH > 7.5)
        elif soil_ph > 7.5:
            output_data['health_status'] = 'Warning'
            output_data['warning_list'].append('Soil is too alkaline.')
            output_data['soil_amendment'] = 'ZA (Ammonium Sulfate)'
            output_data['logic_rationale'].append('Apply ZA to decrease pH. High pH limits micronutrients.')

        # --- Part 2: Organic Carbon Logic ---
        
        # If carbon is low, we need organic matter
        if organic_carbon < 1.5:
            # Change status to Warning if it was Healthy
            if output_data['health_status'] == 'Healthy':
                output_data['health_status'] = 'Warning'
                
            output_data['organic_addition'] = 'Organic Compost/Manure'
            output_data['logic_rationale'].append('Low organic carbon detected. Apply compost to improve soil structure.')

        # --- Part 3: ML Prediction Logic ---
        
        try:
            # Step A: Encode the crop name into a number
            encoded_crop = self.crop_encoder.transform([crop_type])[0]
            
            # Step B: Create a simple table for the model input
            feature_values = [soil_ph, nitrogen_level, phosphorus_level, potassium_level, organic_carbon, soil_moisture, encoded_crop]
            input_table = pd.DataFrame([feature_values], columns=self.model_features)
            
            # Step C: Get prediction index and convert back to fertilizer name
            predicted_index = self.trained_model.predict(input_table)[0]
            fertilizer_name = self.target_encoder.inverse_transform([predicted_index])[0]
            
            # Step D: Save the final result
            output_data['main_fertilizer'] = fertilizer_name
            output_data['logic_rationale'].append(f"ML suggests {fertilizer_name} based on NPK balance.")
            
        except Exception as error_message:
            # Catch errors if prediction fails
            output_data['warning_list'].append(f"AI Error: {str(error_message)}")

        return output_data
