# Slowly Changing Dimensions (SCD) Implementation - Healthcare Data

## Project Overview
This project demonstrates my learning journey with Slowly Changing Dimensions (SCD) in data warehousing, specifically applied to COVID-19 patient data tracking. It includes both a Python implementation and a web-based dashboard, showcasing different SCD types and their practical applications.

## 🔍 Key Features
- **SCD Type 2 Implementation**: Complete historical tracking of patient status changes
- **Web Dashboard**: Interactive UI for data visualization and management
- **Data Versioning**: Proper handling of temporal data with VALID_FROM/VALID_TO dates
- **SQLite Integration**: Persistent storage with proper database design

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

