import pandas as pd

# Load the data
df = pd.read_csv("patient_details.csv", parse_dates=['VALID_FROM'])

# Sort data for proper versioning
df = df.sort_values(by=['PATIENT_ID', 'VALID_FROM'])

# Initialize the dimension table
dimension = pd.DataFrame(columns=[
    'PATIENT_ID', 'PATIENT_NAME', 'COVID_STATUS', 'VALID_FROM', 'VALID_TO', 'IS_CURRENT'
])

# Process SCD Type 2

# Improved SCD Type 2 logic
for pid in df['PATIENT_ID'].unique():
    patient_rows = df[df['PATIENT_ID'] == pid].sort_values(by='VALID_FROM').reset_index(drop=True)
    for i in range(len(patient_rows)):
        row = patient_rows.loc[i].copy()
        valid_from = row['VALID_FROM']
        if i == len(patient_rows) - 1:
            valid_to = pd.NaT  # Open-ended for current record
            is_current = True
        else:
            # Set VALID_TO to the day before the next VALID_FROM
            next_valid_from = patient_rows.loc[i + 1, 'VALID_FROM']
            valid_to = next_valid_from - pd.Timedelta(days=1)
            is_current = False

        dimension = pd.concat([dimension, pd.DataFrame([{
            'PATIENT_ID': row['PATIENT_ID'],
            'PATIENT_NAME': row['PATIENT_NAME'],
            'COVID_STATUS': row['COVID_STATUS'],
            'VALID_FROM': valid_from,
            'VALID_TO': valid_to,
            'IS_CURRENT': is_current
        }])], ignore_index=True)

# Save the output
dimension.to_csv("patient_dimension.csv", index=False)
print(dimension)
