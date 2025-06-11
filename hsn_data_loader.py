import pandas as pd

def load_hsn_codes(path=r"C:\Users\vamsi\Downloads\HSN_SAC.xlsx"):
    try:
        df = pd.read_excel(path)
        return df[['HSN_CD', 'HSN_Description']].dropna()
    except Exception as e:
        print(f"Error loading HSN codes: {e}")
        return pd.DataFrame(columns=['HSN_CD', 'HSN_Description'])