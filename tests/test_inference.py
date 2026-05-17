import pytest
import os
from scripts.inference_engine import FertilizerInferenceEngine

@pytest.fixture
def engine():
    # Ensure artifacts directory exists, otherwise this will fail
    # In a real CI environment, we might mock joblib.load
    return FertilizerInferenceEngine(artifacts_dir='save/model_artifacts')

def test_engine_initialization(engine):
    """Test if engine loads correctly and has required attributes."""
    assert engine.model is not None
    assert engine.le_crop is not None
    assert engine.le_target is not None
    assert len(engine.features) > 0

def test_acidic_soil_heuristic(engine):
    """Test if pH < 5.5 triggers dolomite/lime recommendation."""
    result = engine.get_recommendation(
        soil_pH=5.0, 
        nitrogen=50, 
        phosphorus=40, 
        potassium=40, 
        organic_carbon=2.0, 
        soil_moisture=30.0, 
        crop_type='Rice'
    )
    assert result['soil_health_badge'] == 'Critical'
    assert 'Dolomite/Lime' in result['soil_amendment']
    assert any('acidic' in w.lower() for w in result['warnings'])

def test_alkaline_soil_heuristic(engine):
    """Test if pH > 7.5 triggers ZA recommendation."""
    result = engine.get_recommendation(
        soil_pH=8.0, 
        nitrogen=50, 
        phosphorus=40, 
        potassium=40, 
        organic_carbon=2.0, 
        soil_moisture=30.0, 
        crop_type='Rice'
    )
    assert result['soil_health_badge'] == 'Warning'
    assert 'ZA' in result['soil_amendment']
    assert any('alkaline' in w.lower() for w in result['warnings'])

def test_low_organic_carbon_heuristic(engine):
    """Test if low organic carbon triggers compost recommendation."""
    result = engine.get_recommendation(
        soil_pH=6.5, 
        nitrogen=50, 
        phosphorus=40, 
        potassium=40, 
        organic_carbon=1.0, 
        soil_moisture=30.0, 
        crop_type='Rice'
    )
    assert 'Organic Compost/Manure' in result['organic_amendment']
    assert 'Organic Carbon is low' in ' '.join(result['rationale'])

def test_ml_prediction_output(engine):
    """Test if the ML model provides a basal fertilizer recommendation."""
    result = engine.get_recommendation(
        soil_pH=6.5, 
        nitrogen=80, 
        phosphorus=45, 
        potassium=60, 
        organic_carbon=2.0, 
        soil_moisture=35.0, 
        crop_type='Rice'
    )
    assert result['basal_fertilizer'] is not None
    assert isinstance(result['basal_fertilizer'], str)

def test_output_structure(engine):
    """Test if the output dictionary has all required keys."""
    required_keys = [
        'soil_health_badge', 'warnings', 'soil_amendment', 
        'organic_amendment', 'basal_fertilizer', 'rationale'
    ]
    result = engine.get_recommendation(6.5, 50, 40, 40, 2.0, 30.0, 'Rice')
    for key in required_keys:
        assert key in result
