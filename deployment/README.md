# Fertilizer Recommendation System (Deployment Package)

This package contains the production-ready version of the Fertilizer Recommendation System. It is designed to be independent, efficient, and easy to integrate via a Web Dashboard or a REST API.

---

## Project Overview
This system provides precision farming recommendations by combining Machine Learning (Random Forest) with established soil science heuristics. It analyzes soil parameters to suggest the best fertilizer, chemical amendments (like lime), and organic additions.

### Core Components
- **Dashboard (`main.py`)**: A user-friendly web interface built with Streamlit.
- **API Service (`server.py`)**: A lightweight REST API built with Flask for system-to-system integration.
- **Logic Engine (`fertilizer_engine.py`)**: The brain that processes soil data and generates recommendations.
- **Model Artifacts (`model_artifacts/`)**: Trained AI models and feature encoders.

---

## Quick Setup

### 1. Initialize Environment
Ensure you are using the local virtual environment provided in this folder:
```bash
# Navigate to deployment folder
cd deployment

# Create and activate venv (if not already done)
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install flask pandas scikit-learn joblib streamlit
```

### 2. Run the Dashboard
To start the web interface:
```bash
streamlit run main.py
```

### 3. Run the API Server
To start the API service for integration:
```bash
python3 server.py
```
The server will run on `http://localhost:5000`.

---

## API Documentation

### Endpoint: `POST /predict`
Submit soil analysis data to receive a comprehensive recommendation.

#### Request Header
`Content-Type: application/json`

#### Request Body (JSON)
| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `soil_ph` | float | Soil acidity level (1.0 - 14.0) | 6.5 |
| `nitrogen_level` | int | Nitrogen content in mg/kg | 50 |
| `phosphorus_level` | int | Phosphorus content in mg/kg | 40 |
| `potassium_level` | int | Potassium content in mg/kg | 40 |
| `organic_carbon` | float | Organic carbon percentage | 2.0 |
| `soil_moisture` | float | Soil moisture percentage | 30.0 |
| `crop_type` | string | Target crop (e.g., Rice, Maize, Cotton) | "Rice" |

#### Example Curl Command
```bash
curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '{
  "soil_ph": 5.5,
  "nitrogen_level": 80,
  "phosphorus_level": 40,
  "potassium_level": 40,
  "organic_carbon": 2.0,
  "soil_moisture": 30.0,
  "crop_type": "Maize"
}'
```

#### Success Response (200 OK)
```json
{
  "health_status": "Healthy",
  "warning_list": [],
  "soil_amendment": null,
  "organic_addition": null,
  "main_fertilizer": "NPK",
  "logic_rationale": [
    "ML suggests NPK based on NPK balance."
  ]
}
```

---

## Reference Guide

### Supported Crop Types
Use these exact strings for the `crop_type` field:
- `Cotton`, `Maize`, `Potato`, `Rice`, `Sugarcane`, `Tomato`, `Wheat`

### Soil Parameter Ranges (Ideal for Training Data)
To get the most accurate AI predictions, input values should ideally stay within these observed ranges:
- **Soil pH**: 4.5 – 8.5
- **Nitrogen Level**: 20 – 160 mg/kg
- **Phosphorus Level**: 10 – 90 mg/kg
- **Potassium Level**: 10 – 120 mg/kg
- **Organic Carbon**: 0.2% – 1.5%
- **Soil Moisture**: 10% – 60%

---

## Design Principles
- **Humane Compression**: Code is written to be concise yet highly readable for developers of all levels.
- **Linear Logic**: Step-by-step processing without complex abstractions.
- **Independent**: Self-contained folder with its own environment and artifacts.

**Built by Lumbung Stack Team**
