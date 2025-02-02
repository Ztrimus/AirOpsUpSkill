"""
-----------------------------------------------------------------------
File: services/embeddings.py
Creation Time: Nov 17th 2024, 3:18 am
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
"""

import re
import os
import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel
import torch
from dotenv import load_dotenv
from db import with_connection

load_dotenv()

# Load Embedding Models
mpnet_model = SentenceTransformer(
    "sentence-transformers/all-mpnet-base-v2", cache_folder=os.environ["CACHE_DIR"]
)
e5_tokenizer = AutoTokenizer.from_pretrained(
    "intfloat/e5-base-v2",
    cache_dir=os.environ["CACHE_DIR"],
)
e5_model = AutoModel.from_pretrained(
    "intfloat/e5-base-v2", cache_dir=os.environ["CACHE_DIR"]
)


def get_mpnet_embedding(text):
    """Generate sentence-level embeddings using all-mpnet-base-v2."""
    emb = mpnet_model.encode([text])[0]
    return emb


def get_e5_embedding(text, prefix="passage: "):
    """Generate paragraph-level embeddings using E5-base-v2."""
    inputs = e5_tokenizer(
        [prefix + text], padding=True, truncation=True, return_tensors="pt"
    )
    with torch.no_grad():
        outputs = e5_model(**inputs)
    return outputs.last_hidden_state[:, 0].numpy()[0]


@with_connection
def store_embedding(
    conn, repair_job_id, machine_type, embedding, chunk_level, text_content, text_type
):
    """Store embeddings in PostgreSQL, converting numpy types to standard Python types."""
    try:
        sql = """
        INSERT INTO embeddings (repair_job_id, machine_type, embedding, chunk_level, text_content, text_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        # Convert numpy array to Python list
        embedding_list = (
            embedding.tolist() if isinstance(embedding, np.ndarray) else embedding
        )

        # Ensure elements in the list are Python float
        embedding_list = [float(value) for value in embedding_list]

        with conn.cursor() as cur:
            cur.execute(
                sql,
                (
                    repair_job_id,
                    machine_type,
                    embedding_list,
                    chunk_level,
                    text_content,
                    text_type,
                ),
            )
    except psycopg2.Error as e:
        conn.rollback()
        raise e


def parse_summary_steps_with_numbers(summary_steps):
    """
    Parses the summary_steps string into a list of tuples (step_number, step_description),
    ensuring proper splitting and preserving the step numbers.
    """
    # Use a regex pattern to capture step numbers and their descriptions
    matches = re.findall(r"(\d+)\.\s(.*?)(?=\d+\.|$)", summary_steps.strip(), re.DOTALL)

    # Clean up results into a list of tuples (step_number, step_description)
    steps_with_numbers = [
        (int(match[0]), match[1].strip())
        for match in matches
        if len(match[1].strip()) > 0
    ]

    return steps_with_numbers


@with_connection
def fetch_all_text_content(conn):
    """
    Fetch all text_content from the embeddings table.
    """
    sql = "SELECT text_content FROM embeddings"
    with conn.cursor() as cur:
        cur.execute(sql)
        result = cur.fetchall()  # Fetch all rows
        return {row[0] for row in result}  # Return a set of text_content


def check_sentences_against_embeddings(sentences, paragraph):
    """
    Check a list of sentences against existing text_content in the database.
    """
    existing_text_content = fetch_all_text_content()

    return [
        sentence for sentence in sentences if sentence not in existing_text_content
    ], paragraph in existing_text_content


# Example Usage
def process_repair_job(
    repair_job_id, machine_type, description, transcription, summary_steps
):
    # Generate Sentence-Level Embeddings
    sentence_embeddings = []
    sentences = []
    sentences.extend(
        [
            ("description", text.strip())
            for text in description.split(".")
            if len(text.strip()) > 0
        ]
    )
    sentences.extend(
        [
            ("transcription", text.strip())
            for text in transcription.split(".")
            if len(text.strip()) > 0
        ]
    )
    parsed_steps = parse_summary_steps_with_numbers(summary_steps)
    enhanced_parsed_steps = [
        (
            "summary_steps",
            f"{machine_type} -> Step {step_number}: {step_description.strip()}",
        )
        for step_number, step_description in parsed_steps
        if len(step_description.strip()) > 0
    ]
    sentences.extend(enhanced_parsed_steps)

    sentences = list(set(sentences))

    paragraph_text = (
        f"{description}\n\n---\n\n{summary_steps}\n\n---\n\n{transcription} "
    )

    sentences, is_paragraph_present = check_sentences_against_embeddings(
        sentences, paragraph_text
    )

    for text in sentences:
        sentence_embeddings.append(get_mpnet_embedding(text[1]))

    # Store Sentence-Level Embeddings
    for text_content, embedding in zip(sentences, sentence_embeddings):
        store_embedding(
            repair_job_id=repair_job_id,
            machine_type=machine_type,
            embedding=embedding,
            chunk_level="sentence",
            text_content=text_content[1],
            text_type=text_content[0],
        )

    if not is_paragraph_present:
        paragraph_embedding = get_e5_embedding(paragraph_text)
        # Store Paragraph-Level Embedding
        store_embedding(
            repair_job_id=repair_job_id,
            machine_type=machine_type,
            embedding=paragraph_embedding,
            chunk_level="paragraph",
            text_content=paragraph_text,
            text_type="description, transcription, summary_steps",
        )


@with_connection
def fetch_new_repair_jobs(conn):
    """Fetch unprocessed repair jobs from the database."""
    select_query = """
    SELECT ticket_id, machine_type, description, transcription, summary_steps
    FROM repairjob
    WHERE ticket_id NOT IN (SELECT repair_job_id FROM embeddings)
    """
    with conn.cursor() as cur:
        cur.execute(select_query)
        return cur.fetchall()


def process_new_jobs():
    """Process new repair jobs dynamically."""
    jobs = fetch_new_repair_jobs()
    for index, job in enumerate(jobs):
        print(f"Processing Job {index + 1}/{len(jobs)}")
        repair_job_id, machine_type, description, transcription, summary_steps = job
        process_repair_job(
            repair_job_id, machine_type, description, transcription, summary_steps
        )
    print("All Jobs Processed!")


if __name__ == "__main__":
    # Schedule this function periodically
    process_new_jobs()
