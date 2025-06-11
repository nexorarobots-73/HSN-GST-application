import pandas as pd

def load_hsn_codes():
    try:
        df = pd.read_excel("HSN_SAC.xlsx")
        codes = df['HSN_CD'].astype(str).tolist()
        return codes, df.set_index('HSN_CD')['HSN_Description'].to_dict()
    except Exception as e:
        print(f"Error loading HSN data: {e}")
        # Return sample data as fallback
        sample_codes = ['0101', '0102', '0201', '0202', '0301']
        sample_map = {
            '0101': 'Live horses',
            '0102': 'Live bovine animals',
            '0201': 'Meat of bovine animals, fresh',
            '0202': 'Meat of bovine animals, frozen',
            '0301': 'Live fish'
        }
        return sample_codes, sample_map