# Slowly Changing Dimensions (SCD) Implementation - Healthcare Data

## Project Overview
This project demonstrates my learning journey with Slowly Changing Dimensions (SCD) in data warehousing, specifically applied to COVID-19 patient data tracking. It includes both a Python implementation and a web-based dashboard, showcasing different SCD types and their practical applications.

## 🔍 Key Features
- **SCD Type 2 Implementation**: Complete historical tracking of patient status changes
- **Web Dashboard**: Interactive UI for data visualization and management
- **Data Versioning**: Proper handling of temporal data with VALID_FROM/VALID_TO dates
- **SQLite Integration**: Persistent storage with proper database design

## 🛠️ Technical Implementation

### Python SCD Implementation
```python
# Key SCD Type 2 logic
for pid in df['PATIENT_ID'].unique():
    patient_rows = df[df['PATIENT_ID'] == pid].sort_values(by='VALID_FROM')
    for i in range(len(patient_rows)):
        if i == len(patient_rows) - 1:
            valid_to = pd.NaT  # Open-ended for current record
            is_current = True
        else:
            next_valid_from = patient_rows.loc[i + 1, 'VALID_FROM']
            valid_to = next_valid_from - pd.Timedelta(days=1)
            is_current = False
```

### Key Concepts Implemented
1. **Version Tracking**: Maintaining complete history of changes
2. **Time-based Validity**: Using VALID_FROM and VALID_TO dates
3. **Current Record Flagging**: IS_CURRENT flag for latest version
4. **Data Integrity**: Ensuring no gaps in temporal coverage

## 📊 Data Model
- **Patient Dimension Table**
  - PATIENT_ID (Primary Key)
  - PATIENT_NAME
  - COVID_STATUS
  - VALID_FROM
  - VALID_TO
  - IS_CURRENT

## 🔧 Technologies Used
- Python 3.x
- Pandas for data manipulation
- SQLite for data storage
- HTML/JavaScript for dashboard
- Bootstrap 5 for UI

## 📚 Learning Outcomes
- Understanding SCD concepts and their importance in data warehousing
- Implementing different SCD types (Type 1, 2, and 3)
- Building a full-stack application with data versioning
- Database design for temporal data
- Web UI development for data management

## 🚀 Getting Started
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install pandas
   ```
3. Run the Python script:
   ```bash
   python a.py
   ```
4. Launch the web dashboard:
   ```bash
   python -m http.server 8000
   ```

## 📝 Notes
This project was developed as part of my data science learning journey, focusing on:
- Data warehouse concepts
- Dimensional modeling
- Historical data tracking
- Full-stack development

## 📌 Future Enhancements
- [ ] Add support for more complex SCD scenarios
- [ ] Implement data quality checks
- [ ] Add data visualization features
- [ ] Optimize performance for large datasets

## 👨‍💻 Author
- Your Name
- LinkedIn: [Your LinkedIn Profile]
- Portfolio: [Your Portfolio Website]

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details
