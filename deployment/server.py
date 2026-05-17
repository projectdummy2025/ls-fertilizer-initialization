from flask import Flask, request, jsonify
from fertilizer_engine import fertilizer_engine
import os

# --- Step 1: Initialize the API ---
fertilizer_app = Flask(__name__)

# Setup model path relative to this script
current_folder = os.path.dirname(os.path.abspath(__file__))
model_folder = os.path.join(current_folder, 'model_artifacts')

# Load the logic engine
soil_logic = fertilizer_engine(model_path=model_folder)

# --- Step 2: Define the Recommendation Endpoint ---
@fertilizer_app.route('/predict', methods=['POST'])
def get_prediction():
    """
    Endpoint to receive soil data and return fertilizer suggestions.
    Expects JSON input.
    """
    try:
        # Get data from the request body
        input_data = request.get_json()
        
        # Extract variables with explicit names
        # Default values are provided for safety
        soil_ph = input_data.get('soil_ph', 6.5)
        nitrogen_input = input_data.get('nitrogen_level', 50)
        phosphorus_input = input_data.get('phosphorus_level', 40)
        potassium_input = input_data.get('potassium_level', 40)
        carbon_input = input_data.get('organic_carbon', 2.0)
        moisture_input = input_data.get('soil_moisture', 30.0)
        crop_input = input_data.get('crop_type', 'Rice')

        # Run the engine
        analysis_result = soil_logic.get_recommendation(
            soil_ph=soil_ph,
            nitrogen_level=nitrogen_input,
            phosphorus_level=phosphorus_input,
            potassium_level=potassium_input,
            organic_carbon=carbon_input,
            soil_moisture=moisture_input,
            crop_type=crop_input
        )

        # Return the result as JSON
        return jsonify(analysis_result), 200

    except Exception as error_found:
        # Return error message if something goes wrong
        return jsonify({'error': str(error_found)}), 400

# --- Step 3: Run the Server ---
if __name__ == '__main__':
    # Running on port 5000 by default
    print("Fertilizer API is starting...")
    fertilizer_app.run(host='0.0.0.0', port=5000)
