import pandas as pd
import numpy as np
from scripts.inference_engine import FertilizerInferenceEngine
import itertools
from tqdm import tqdm

def run_stress_test():
    engine = FertilizerInferenceEngine()
    
    # Define ranges for inputs
    ph_range = [4.0, 5.5, 6.5, 7.5, 8.5]
    n_range = [20, 80, 150]
    p_range = [20, 45, 100]
    k_range = [20, 60, 150]
    carbon_range = [0.5, 1.5, 2.5]
    moisture_range = [15, 35, 55]
    crops = engine.le_crop.classes_

    combinations = list(itertools.product(
        ph_range, n_range, p_range, k_range, carbon_range, moisture_range, crops
    ))

    print(f"Running validation on {len(combinations)} input combinations...")
    
    errors = []
    results_summary = {
        'Healthy': 0,
        'Warning': 0,
        'Critical': 0
    }

    for combo in tqdm(combinations):
        try:
            res = engine.get_recommendation(*combo)
            results_summary[res['soil_health_badge']] += 1
            
            # Basic sanity checks
            if combo[0] < 5.5 and res['soil_health_badge'] != 'Critical':
                errors.append(f"Logic Error: pH {combo[0]} should be Critical, got {res['soil_health_badge']}")
            
            if combo[4] < 1.5 and res['organic_amendment'] is None:
                errors.append(f"Logic Error: Carbon {combo[4]} should trigger organic amendment")

        except Exception as e:
            errors.append(f"Execution Error for {combo}: {str(e)}")

    print("\n--- Validation Summary ---")
    print(f"Total Combinations: {len(combinations)}")
    print(f"Status Distribution: {results_summary}")
    
    if errors:
        print(f"Total Errors Found: {len(errors)}")
        for err in errors[:10]: # Show first 10
            print(f"- {err}")
    else:
        print("✅ All sanity checks passed!")

if __name__ == "__main__":
    run_stress_test()
