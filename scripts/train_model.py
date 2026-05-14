import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def train_fertilizer_model(data_path, save_dir):
    """
    Train a fertilizer recommendation model specifically for the 'Sowing' stage.
    """
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)

    # 1. Filter for 'Sowing' stage as per docs/pre_planting_scenario.md
    print("Filtering data for 'Sowing' stage...")
    df_sowing = df[df['Crop_Growth_Stage'] == 'Sowing'].copy()

    if df_sowing.empty:
        print("Error: No data found for 'Sowing' stage.")
        return

    # 2. Feature Selection (as per docs/data_schema.md)
    # Core Features + Crop_Type
    features = [
        'Soil_pH', 
        'Nitrogen_Level', 
        'Phosphorus_Level', 
        'Potassium_Level', 
        'Organic_Carbon', 
        'Soil_Moisture',
        'Crop_Type'
    ]
    target = 'Recommended_Fertilizer'

    X = df_sowing[features]
    y = df_sowing[target]

    # 3. Encoding Categorical Features
    print("Encoding categorical features...")
    le_crop = LabelEncoder()
    X['Crop_Type'] = le_crop.fit_transform(X['Crop_Type'])

    le_target = LabelEncoder()
    y = le_target.fit_transform(y)

    # 4. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. Model Training
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 6. Evaluation
    accuracy = model.score(X_test, y_test)
    print(f"Model Accuracy on Test Set: {accuracy:.4f}")

    # 7. Save Artifacts
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    model_path = os.path.join(save_dir, 'fertilizer_model.joblib')
    le_crop_path = os.path.join(save_dir, 'le_crop.joblib')
    le_target_path = os.path.join(save_dir, 'le_target.joblib')

    joblib.dump(model, model_path)
    joblib.dump(le_crop, le_crop_path)
    joblib.dump(le_target, le_target_path)

    print(f"Model and encoders saved to {save_dir}")
    
    # Save the list of features for reference
    with open(os.path.join(save_dir, 'features.txt'), 'w') as f:
        f.write('\n'.join(features))

if __name__ == "__main__":
    DATA_PATH = 'save/fertilizer_localized.csv'
    SAVE_DIR = 'save/model_artifacts'
    
    train_fertilizer_model(DATA_PATH, SAVE_DIR)
