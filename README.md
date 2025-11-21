# Project Title

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
- PostgreSQL  
- Pandas / NumPy  
- python-dotenv  

## 📁 Folder Structure
project-root/
│
├── __pycache__/          # Python cache files
│
├── app.py                # Streamlit application
├── eda_pipeline.py       # EDA / data processing pipeline
├── db_config.py          # PostgreSQL connection config
├── .env                  # Environment variables (NOT committed)
├── requirements.txt      # Python dependencies
│
└── README.md             # Project documentation (this file)
