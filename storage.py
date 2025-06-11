import os
import pandas as pd

def save_entry(entry):
    path = "data/entries.csv"
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame([entry])
    if os.path.exists(path):
        df.to_csv(path, mode='a', header=False, index=False)
    else:
        df.to_csv(path, index=False)
    return path