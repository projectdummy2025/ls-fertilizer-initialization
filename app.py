import streamlit as st
from scripts.inference_engine import FertilizerInferenceEngine
import pandas as pd

# Page configuration
st.set_page_config(page_title="LumbungStack Fertilizer Recommendation", page_icon="🌱")

@st.cache_resource
def load_engine():
    return FertilizerInferenceEngine()

try:
    engine = load_engine()
except Exception as e:
    st.error(f"Error loading model artifacts: {e}. Please run `scripts/train_model.py` first.")
    st.stop()

st.title("🌱 Fertilizer Recommendation System")
st.subheader("Pre-Planting Intelligence Module")

with st.form("soil_input_form"):
    st.write("### Soil Test Results")
    col1, col2 = st.columns(2)
    
    with col1:
        soil_pH = st.number_input("Soil pH", min_value=1.0, max_value=14.0, value=6.5, step=0.1)
        nitrogen = st.number_input("Nitrogen Level (mg/kg)", min_value=0, value=50)
        phosphorus = st.number_input("Phosphorus Level (mg/kg)", min_value=0, value=40)
        
    with col2:
        potassium = st.number_input("Potassium Level (mg/kg)", min_value=0, value=40)
        organic_carbon = st.number_input("Organic Carbon (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
        soil_moisture = st.number_input("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=30.0)

    crop_type = st.selectbox("Crop Type", options=engine.le_crop.classes_)
    
    submit_button = st.form_submit_button("Get Recommendation")

if submit_button:
    result = engine.get_recommendation(
        soil_pH=soil_pH,
        nitrogen=nitrogen,
        phosphorus=phosphorus,
        potassium=potassium,
        organic_carbon=organic_carbon,
        soil_moisture=soil_moisture,
        crop_type=crop_type
    )
    
    st.divider()
    
    # Display Results
    badge_colors = {"Healthy": "green", "Warning": "orange", "Critical": "red"}
    st.markdown(f"### Soil Health Status: :{badge_colors[result['soil_health_badge']]}[{result['soil_health_badge']}]")
    
    if result['warnings']:
        for warning in result['warnings']:
            st.warning(warning)
            
    st.write("#### Recommended Actions:")
    
    if result['soil_amendment']:
        st.info(f"**Soil Amendment:** {result['soil_amendment']}")
        
    if result['organic_amendment']:
        st.info(f"**Organic Amendment:** {result['organic_amendment']}")
        
    if result['basal_fertilizer']:
        st.success(f"**Basal Fertilizer:** {result['basal_fertilizer']}")
        
    st.write("#### Rationale:")
    for note in result['rationale']:
        st.write(f"- {note}")
