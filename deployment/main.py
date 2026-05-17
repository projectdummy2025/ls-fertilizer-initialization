import streamlit as st
import pandas as pd
import os
from fertilizer_engine import fertilizer_engine

# --- Step 1: Page Setup ---
st.set_page_config(page_title="LumbungStack Fertilizer Dashboard")

@st.cache_resource
def start_engine():
    # Load the logic engine from the local model folder
    # We use os.path.join for safety across different systems
    current_folder = os.path.dirname(os.path.abspath(__file__))
    model_folder = os.path.join(current_folder, 'model_artifacts')
    return fertilizer_engine(model_path=model_folder)

# Load the engine once and cache it
try:
    logic_engine = start_engine()
except Exception as error_found:
    st.error(f"Could not load AI files: {error_found}")
    st.stop()

# --- Step 2: User Interface Design ---
st.title("Fertilizer Recommendation Dashboard")
st.markdown("### Decision Support for Precision Farming")

with st.form("input_form"):
    st.write("#### Soil Analysis Data")
    
    # Split input into two columns for better look
    left_side, right_side = st.columns(2)
    
    with left_side:
        soil_ph = st.number_input("Soil pH (1-14)", min_value=1.0, max_value=14.0, value=6.5)
        nitrogen_input = st.number_input("Nitrogen Level (mg/kg)", min_value=0, value=50)
        phosphorus_input = st.number_input("Phosphorus Level (mg/kg)", min_value=0, value=40)
        
    with right_side:
        potassium_input = st.number_input("Potassium Level (mg/kg)", min_value=0, value=40)
        carbon_input = st.number_input("Organic Carbon (%)", min_value=0.0, max_value=10.0, value=2.0)
        moisture_input = st.number_input("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=30.0)

    # Let user pick the crop type from the encoder's list
    crop_input = st.selectbox("Select Crop Type", options=logic_engine.crop_encoder.classes_)
    
    # Process button
    submit_button = st.form_submit_button("Generate Recommendation")

# --- Step 3: Processing & Results ---
if submit_button:
    # Run the logic engine with user data
    analysis_result = logic_engine.get_recommendation(
        soil_ph=soil_ph,
        nitrogen_level=nitrogen_input,
        phosphorus_level=phosphorus_input,
        potassium_level=potassium_input,
        organic_carbon=carbon_input,
        soil_moisture=moisture_input,
        crop_type=crop_input
    )
    
    st.divider()
    
    # A. Display Health Status with Colors
    status_label = analysis_result['health_status']
    color_map = {"Healthy": "green", "Warning": "orange", "Critical": "red"}
    st.markdown(f"### Soil Health: :{color_map[status_label]}[{status_label}]")
    
    # B. Show Warnings if any
    for message in analysis_result['warning_list']:
        st.warning(message)
            
    # C. Display Suggested Actions
    st.write("#### Recommended Actions:")
    
    if analysis_result['soil_amendment']:
        st.info(f"**Chemical Adjustment:** {analysis_result['soil_amendment']}")
        
    if analysis_result['organic_addition']:
        st.info(f"**Organic Matter:** {analysis_result['organic_addition']}")
        
    if analysis_result['main_fertilizer']:
        st.success(f"**Main Fertilizer:** {analysis_result['main_fertilizer']}")
        
    # D. Explanation Logic
    st.write("#### Rationale:")
    for note in analysis_result['logic_rationale']:
        st.write(f"- {note}")
