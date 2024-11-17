-   frontend
    -   npm install
    -   npm start
-   backend
    -   FastAPI
        -   pip install poetry
        -   poetry shell
        -   poetry install
        -   python -m app.main
    -   database
        -   brew install postgresql
        -   brew services start postgresql
        -   psql -U postgres
        -   CREATE DATABASE air_ops_up_skill_db;
        -   CREATE USER saurabh_zinjad WITH PASSWORD 'Honeywell@123';
        -   GRANT ALL PRIVILEGES ON DATABASE air_ops_up_skill_db TO saurabh_zinjad;
        -   GRANT USAGE ON SCHEMA public TO saurabh_zinjad;
        -   GRANT CREATE ON SCHEMA public TO saurabh_zinjad;

# How it Works:

## 1. Purpose:

-   Automatically generate FAQs for specific repair jobs, processes, or scenarios.
-   Enable technicians or users to quickly access concise answers to common questions.

## 2. Core Workflow:

-   Input Data: Collect repair job data, transcripts, videos, or logs.
-   Data Extraction: Use AI to extract key questions and answers (e.g., "What went wrong?", "Steps to fix it", "Common issues").
-   Standardization: Organize extracted content into a user-friendly FAQ format.
-   Search and Fetch: Allow users to query FAQs by keywords or context.

DataType

-   Ticket Id
-   Ticket Info
-   Manufacturing Plant
-   Labor Cost
-   Item Cost
-   Total Cost
-   Repair Time
-   Replacement Items List
-   Description
-   Audio transcription
-   Video link
-   Audio link
-   Downtime
-   Summary Line
-   Summary Setps
-   Failed Again Ticket
