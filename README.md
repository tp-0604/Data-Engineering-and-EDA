# Python-Based EDA Pipeline with PostgreSQL Integration

A simple end-to-end data exploration and visualization pipeline built using Python and Streamlit, with PostgreSQL for data storage.

## 📌 Overview — What the Project Does

This project performs:
- Data ingestion & exploratory data analysis (EDA) via a custom Python pipeline
- Database connectivity using PostgreSQL
- Interactive UI built with Streamlit
- Secure configuration using environment variables

It is designed as a lightweight, modular pipeline that reads data, processes it, loads it into a database, and provides a Streamlit interface for visual exploration.

## 🧰 Tech Stack
- Python  
- Streamlit  
- [Azure] PostgreSQL  
- Pandas / NumPy    

## 📁 Folder Structure
```
project-root/
├── pycache/ # Python cache files
├── app.py # Streamlit application
├── eda_pipeline.py # EDA / data processing pipeline
├── db_config.py # PostgreSQL connection config
├── requirements.txt # Python dependencies
└── README.md # Project documentation (this file)
```


## ⚙️ Environment Variables

Create a `.env` file in the project root with your Postgres database credentials:
```
DB_HOST=your_host
DB_PORT=5432
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
```

## 🚀 How to Run the Project

### 1. Clone the repo
```
git clone https://github.com/tp-0604/Data-Engineering-and-EDA.git
cd your-repo
```

### 2. Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Set up your `.env` file  
(See environment variables section above.)

### 5. Run the EDA pipeline
```  
python eda_pipeline.py
```

### 6. Run the Streamlit app
```
streamlit run app.py
```

The app will be available at:
```
http://localhost:8501
```








