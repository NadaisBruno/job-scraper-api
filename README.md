# FastAPI Job Scraper API

A REST API built with Python that scrapes job offers from Net-Empregos, stores them in a database, prevents duplicates 
and provides filtering and pagination for querying the results.

## Features

    - Scrapes job offers
    - Stores job offers in a local SQLite database using SQLAlchemy ORM 
    - Prevents duplicates of job offers
    - Provides filtering by title, location and company
    - Supports pagination 
    - Includes a streamlit interface to view and filter job offers

## Endpoint

    - GET /job_offers - Lists job offers by title, location and company including pagination support

## How to run

1 - Install the dependencies:

    pip install -r requirements.txt

2 - Run the scraper to collect job offers:
    
    python main.py

3 - Start the API server:

    uvicorn api:app --reload

4 - Open the Swagger documentation in your browser:

    http://127.0.0.1:8000/docs

5 - Run streamlit to view the data in a web app
    
    streamlit run streamlit_app.py

## Technologies Used

    - Python >= 3.10 
    - FastAPI
    - BeautifulSoup
    - Requests
    - SQLite
    - SQLAlchemy
    - Streamlit
    - Uvicorn


    