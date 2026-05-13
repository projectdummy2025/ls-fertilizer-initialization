import pandas as pd
import os

def preprocess_fertilizer_data(input_path, output_path):
    """
    Preprocess fertilizer dataset by removing localized concepts (Region)
    and mapping Indian seasons to Indonesian agricultural seasons.
    """
    print(f"Loading data from {input_path}...")
    
    # 1. Load Dataset
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    df = pd.read_csv(input_path)

    # 2. Remove 'Region' column
    # The user specified that Region is just a plot identifier, not geographical.
    if 'Region' in df.columns:
        print("Removing 'Region' column...")
        df = df.drop(columns=['Region'])

    # 3. Localize Seasons (India -> Indonesia)
    # Kharif: Rainy Season
    # Rabi: Dry Season
    # Zaid: Transition Season
    season_mapping = {
        'Kharif': 'Rainy',
        'Rabi': 'Dry',
        'Zaid': 'Transition'
    }
    
    print("Mapping seasons to Indonesian context...")
    df['Season'] = df['Season'].map(season_mapping)

    # 4. Save processed data
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df.to_csv(output_path, index=False)
    print(f"Preprocessing complete. Saved to: {output_path}")

if __name__ == "__main__":
    INPUT_FILE = 'data/fertilizer_dataset.csv'
    OUTPUT_FILE = 'save/fertilizer_localized.csv'
    
    preprocess_fertilizer_data(INPUT_FILE, OUTPUT_FILE)
