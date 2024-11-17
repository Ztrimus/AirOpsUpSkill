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
        -   brew install pgvector
        -   brew services start postgresql
        -   psql -U postgres
        -   CREATE DATABASE air_ops_up_skill_db;
        -   CREATE USER saurabh_zinjad WITH PASSWORD 'Honeywell@123';
        -   GRANT ALL PRIVILEGES ON DATABASE air_ops_up_skill_db TO saurabh_zinjad;
        -   GRANT USAGE ON SCHEMA public TO saurabh_zinjad;
        -   GRANT CREATE ON SCHEMA public TO saurabh_zinjad;
        -   For PgVector
        -   psql -U saurabh_zinjad -d air_ops_up_skill_db
        -   CREATE EXTENSION IF NOT EXISTS vector;

# How it Works:

## 1. Purpose:

-   Automatically generate FAQs for specific repair jobs, processes, or scenarios.
-   Enable technicians or users to quickly access concise answers to common questions.

## 2. Core Workflow:

-   Input Data: Collect repair job data, transcripts, videos, or logs.
-   Data Extraction: Use AI to extract key questions and answers (e.g., "What went wrong?", "Steps to fix it", "Common issues").
-   Standardization: Organize extracted content into a user-friendly FAQ format.
-   Search and Fetch: Allow users to query FAQs by keywords or context.

---

# Database

```psql
CREATE TABLE embeddings (
embedding_id SERIAL PRIMARY KEY,
repair_job_id TEXT NOT NULL,
text_content TEXT NOT NULL,
machine_type VARCHAR(50),
text_type VARCHAR(50) NOT NULL,
embedding VECTOR(768),
chunk_level VARCHAR(10),
cluster_id INT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE embeddings
ADD CONSTRAINT fk_repair_job
FOREIGN KEY (repair_job_id) REFERENCES repairjob(ticket_id) ON DELETE CASCADE;
```

Columns Explanation:
repair_job_id: Links the embedding to a specific repair job in the repair_jobs table.
text_type: Indicates whether the embedding is derived from description, transcription, or summary_steps.
embedding: Stores the dense vector representation of the text.
cluster_id: Helps group embeddings into clusters based on unsupervised learning.
created_at: Tracks when the embedding was created.

```psql
CREATE TABLE faqs (
    faq_id SERIAL PRIMARY KEY,
    faq_name TEXT,
    machine_type VARCHAR(50),
    cluster_id INT,
    common_3_repairs TEXT, -- Stores the 3 most common repairs
    common_3_culprits TEXT, -- Stores the 3 most common culprits
    solution_to_single_frequent_culprit TEXT, -- Detailed solution for the single most frequent culprit
    tags TEXT[], -- Optional tags for categorization
    rating INT DEFAULT 0, -- Rating based on user feedback
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Auto-generated creation timestamp
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Auto-generated update timestamp
);

```

Explanation of Columns:
machine_type: Groups FAQs by machine type for easy filtering.
cluster_id: Associates the FAQ with a specific cluster of repair jobs for traceability.
question: Stores the FAQ question (e.g., "What causes sensor misalignment in AF500?").
answer: Stores the corresponding answer to the FAQ.
tags: Tags (e.g., "failure", "repair", "preventive") help in filtering and categorizing FAQs.
rating: Tracks user feedback to improve or refine FAQs over time.

```psql
CREATE TABLE faq_feedback (
feedback_id SERIAL PRIMARY KEY,
faq_id INT NOT NULL REFERENCES faqs(faq_id),
user_id INT,
feedback TEXT,
rating INT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

```psql
CREATE INDEX embeddings_vector_idx ON embeddings USING ivfflat (embedding) WITH (lists = 100);
CREATE INDEX faqs_machine_type_idx ON faqs(machine_type);
CREATE INDEX faqs_tags_idx ON faqs USING gin(tags);
```
