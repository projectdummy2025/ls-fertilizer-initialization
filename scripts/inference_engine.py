import joblib
import os
import numpy as np

class FertilizerInferenceEngine:
    def __init__(self, artifacts_dir='save/model_artifacts'):
        self.artifacts_dir = artifacts_dir
        self.model = joblib.load(os.path.join(artifacts_dir, 'fertilizer_model.joblib'))
        self.le_crop = joblib.load(os.path.join(artifacts_dir, 'le_crop.joblib'))
        self.le_target = joblib.load(os.path.join(artifacts_dir, 'le_target.joblib'))
        
        with open(os.path.join(artifacts_dir, 'features.txt'), 'r') as f:
            self.features = f.read().splitlines()

    def get_recommendation(self, soil_pH, nitrogen, phosphorus, potassium, organic_carbon, soil_moisture, crop_type):
        """
        Implements the Pre-Planting Intelligence logic.
        """
        results = {
            'soil_health_badge': 'Healthy',
            'warnings': [],
            'soil_amendment': None,
            'organic_amendment': None,
            'basal_fertilizer': None,
            'rationale': []
        }

        # 1. pH Correction (The "Gatekeeper")
        if soil_pH < 5.5:
            results['soil_health_badge'] = 'Critical'
            results['warnings'].append('Soil is too acidic.')
            results['soil_amendment'] = 'Dolomite/Lime'
            results['rationale'].append('Apply Dolomite/Lime to increase pH. Nutrients like P and K are locked in acidic soil.')
        elif soil_pH > 7.5:
            results['soil_health_badge'] = 'Warning'
            results['warnings'].append('Soil is too alkaline.')
            results['soil_amendment'] = 'ZA (Ammonium Sulfate)'
            results['rationale'].append('Apply ZA to decrease pH. High pH can lead to micronutrient deficiencies.')

        # 2. Organic Carbon Status
        if organic_carbon < 1.5:
            if results['soil_health_badge'] == 'Healthy':
                results['soil_health_badge'] = 'Warning'
            results['organic_amendment'] = 'Organic Compost/Manure'
            results['rationale'].append('Organic Carbon is low. Apply Compost/Manure to improve soil structure and CEC.')

        # 3. ML Prediction for Basal Fertilizer
        # Prepare input for model
        try:
            import pandas as pd
            crop_encoded = self.le_crop.transform([crop_type])[0]
            input_df = pd.DataFrame([[
                soil_pH, nitrogen, phosphorus, potassium, organic_carbon, soil_moisture, crop_encoded
            ]], columns=self.features)
            
            pred_idx = self.model.predict(input_df)[0]
            recommendation = self.le_target.inverse_transform([pred_idx])[0]
            
            results['basal_fertilizer'] = recommendation
            results['rationale'].append(f"Based on NPK levels, the suggested basal fertilizer is {recommendation}.")
        except Exception as e:
            results['warnings'].append(f"Model prediction error: {str(e)}")

        return results

if __name__ == "__main__":
    # Example usage
    engine = FertilizerInferenceEngine()
    
    # Example 1: Acidic soil
    print("Example 1: Acidic Soil")
    rec1 = engine.get_recommendation(
        soil_pH=5.0, 
        nitrogen=40, 
        phosphorus=20, 
        potassium=30, 
        organic_carbon=1.2, 
        soil_moisture=25.0, 
        crop_type='Rice'
    )
    print(rec1)
    print("-" * 30)
    
    # Example 2: Healthy soil
    print("Example 2: Healthy Soil")
    rec2 = engine.get_recommendation(
        soil_pH=6.5, 
        nitrogen=80, 
        phosphorus=45, 
        potassium=60, 
        organic_carbon=2.0, 
        soil_moisture=35.0, 
        crop_type='Maize'
    )
    print(rec2)
