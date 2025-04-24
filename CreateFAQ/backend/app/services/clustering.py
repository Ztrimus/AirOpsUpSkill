"""
-----------------------------------------------------------------------
File: services/clustering.py
Creation Time: Nov 17th 2024, 4:52 am
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
"""

import ast
import time
from typing import List
import hdbscan
from db import with_connection
import numpy as np
import psycopg2
import os
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from langchain_core.output_parsers import JsonOutputParser

# Initialize Gemini Client
if "GEMINI_API_KEY" not in os.environ:
    raise EnvironmentError("GEMINI_API_KEY not found in environment variables.")

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


@with_connection
def fetch_embeddings(conn, machine_type=None):
    """Fetch embeddings for a specific machine_type or all embeddings."""
    try:
        query = (
            """
        SELECT embedding_id, embedding, repair_job_id
        FROM embeddings
        WHERE machine_type = %s
        """
            if machine_type
            else """
        SELECT embedding_id, embedding, repair_job_id
        FROM embeddings
        """
        )
        with conn.cursor() as cur:
            cur.execute(query, (machine_type,) if machine_type else None)
            results = cur.fetchall()

        # Convert embeddings from list to numpy array
        embeddings = np.vstack([np.array(ast.literal_eval(row[1])) for row in results])
        embedding_ids = [row[0] for row in results]
        repair_job_ids = [row[2] for row in results]
        return embeddings, embedding_ids, repair_job_ids
    except psycopg2.Error as e:
        print(e)
        return None, None, None


def cluster_with_hdbscan(embeddings, min_cluster_size=10, min_samples=3):
    """
    Perform clustering using HDBSCAN.
    :param embeddings: Numpy array of embeddings.
    :param min_cluster_size: Minimum size of clusters.
    :param min_samples: Minimum samples for a point to be considered core.
    :return: Cluster labels and probabilities.
    """
    try:
        # Normalize your embedding vectors
        from sklearn.preprocessing import normalize

        # modified_embeddings = normalize(embeddings)
        from sklearn.metrics.pairwise import cosine_distances

        modified_embeddings = cosine_distances(normalize(embeddings))

        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=min_cluster_size,
            min_samples=min_samples,
            metric="precomputed",
            cluster_selection_epsilon=0.05,
        )
        cluster_labels = clusterer.fit_predict(modified_embeddings)
        probabilities = clusterer.probabilities_
        return cluster_labels, probabilities, clusterer
    except Exception as e:
        print(e)
        return None, None, None


@with_connection
def update_hdbscan_clusters(conn, cluster_labels, embedding_ids):
    """
    Update cluster IDs in the database using HDBSCAN results.
    :param conn: The database connection object (provided by @with_connection).
    :param cluster_labels: Array of cluster labels from HDBSCAN.
    :param embedding_ids: Array of embedding IDs.
    """
    update_query = """
    UPDATE embeddings
    SET cluster_id = %s
    WHERE embedding_id = %s
    """
    with conn.cursor() as cur:
        for cluster_id, embedding_id in zip(cluster_labels, embedding_ids):
            cur.execute(
                update_query,
                (
                    (
                        int(cluster_id) if cluster_id != -1 else None
                    ),  # Assign NULL for noise
                    embedding_id,
                ),
            )


def reassign_noise(embeddings, cluster_labels, clusterer):
    """
    Reassign noise points to the closest cluster.
    :param embeddings: Numpy array of all embeddings.
    :param cluster_labels: HDBSCAN cluster labels.
    :param clusterer: HDBSCAN clusterer object.
    :return: Updated cluster labels.
    """
    cluster_centers = clusterer.weighted_cluster_centroids_
    for i, label in enumerate(cluster_labels):
        if label == -1:  # Noise point
            similarities = cosine_similarity([embeddings[i]], cluster_centers)
            cluster_labels[i] = similarities.argmax()  # Closest cluster
    return cluster_labels


def parse_json_markdown(json_string: str) -> dict:
    try:
        # Try to find JSON string within first and last triple backticks
        if json_string[3:13].lower() == "typescript":
            json_string = json_string.replace(json_string[3:13], "", 1)

        if "JSON_OUTPUT_ACCORDING_TO_RESUME_DATA_SCHEMA" in json_string:
            json_string = json_string.replace(
                "JSON_OUTPUT_ACCORDING_TO_RESUME_DATA_SCHEMA", "", 1
            )

        if json_string[3:7].lower() == "json":
            json_string = json_string.replace(json_string[3:7], "", 1)

        parser = JsonOutputParser()
        parsed = parser.parse(json_string)

        return parsed
    except Exception as e:
        print(e)
        return None


@with_connection
def summarize_hdbscan_clusters(conn, cluster_labels, embedding_ids, machine_type):
    """
    Summarize clusters generated by HDBSCAN and generate FAQs.
    :param conn: Database connection passed by the @with_connection decorator.
    :param cluster_labels: Array of cluster labels from HDBSCAN.
    :param embedding_ids: Array of embedding IDs.
    """
    try:
        clusters = set(cluster_labels.tolist())
        faq_clusters = []
        all_custer_ids, all_machine_types = get_unique_cluster_ids_and_machine_types()

        for cluster_id in clusters:
            if cluster_id == -1:  # Skip noise
                continue

            if cluster_id in all_custer_ids and machine_type in all_machine_types:
                continue

            query = """
            SELECT text_content
            FROM embeddings
            WHERE cluster_id = %s
            """
            with conn.cursor() as cur:
                cur.execute(query, (cluster_id,))
                texts = [row[0] for row in cur.fetchall()]

            # Use GPT or another LLM for summarization
            prompt = f"""
    Based on the following repair descriptions, generate a JSON object containing the most frequent repairs, culprits, and solutions:
    {texts}

    The output should be in the JSON format:
    {{
        "faq_name": "<Name of the FAQ topic>",
        "common_3_repairs": "<The 3 most common repairs performed in this cluster and in comma spearated string format>",
        "common_3_culprits": "<The 3 most frequent culprits/issues in this cluster and in comma spearated string format>",
        "solution_to_single_frequent_culprit": "<Detailed solution for the most frequent single culprit with its name>"
    }}

    Ensure the following:
    1. Analyze patterns in repair descriptions to extract frequent repairs and culprits.
    2. Identify and summarize one solution for the most frequent culprit.
    3. Ensure the response is concise and relevant.
    """
            time.sleep(1)
            response = client.chat.completions.create(
                model="gemini-1.5-flash",
                n=1,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )

            # Extract the content from the response
            content = response.choices[0].message.content.strip()
            content = parse_json_markdown(content)
            if "faq_name" in content or "faq_name" in content[0]:
                if "faq_name" in content:
                    content = [content]
                for faq in content:
                    faq_name = faq["faq_name"]
                    # Extract fields from the content
                    common_3_repairs = faq.get("common_3_repairs", "")
                    common_3_culprits = faq.get("common_3_culprits", "")
                    solution_to_single_frequent_culprit = faq.get(
                        "solution_to_single_frequent_culprit", ""
                    )

                    # Insert into the faqs table
                    insert_faq(
                        faq_name,
                        machine_type,
                        cluster_id,
                        common_3_repairs,
                        common_3_culprits,
                        solution_to_single_frequent_culprit,
                    )

            faq_clusters.append((cluster_id, content))

        return faq_clusters
    except Exception as e:
        print(e)


@with_connection
def insert_faq(
    conn,
    faq_name,
    machine_type,
    cluster_id=None,
    common_3_repairs=None,
    common_3_culprits=None,
    solution_to_single_frequent_culprit=None,
    tags=None,
    rating=0,
):
    """
    Insert a new FAQ into the faqs table.

    Args:
        conn: Database connection (handled by @with_connection).
        faq_name (str): The name or title of the FAQ.
        machine_type (str): The machine type associated with the FAQ.
        cluster_id (int, optional): The cluster ID associated with the FAQ.
        common_3_repairs (str, optional): The 3 most common repairs in this cluster.
        common_3_culprits (str, optional): The 3 most common culprits/issues.
        solution_to_single_frequent_culprit (str, optional): Solution for the most frequent culprit.
        tags (list, optional): Tags for the FAQ (e.g., ["failure", "repair"]).
        rating (int, optional): Initial rating for the FAQ (default: 0).
    """
    insert_query = """
    INSERT INTO faqs (
        faq_name, machine_type, cluster_id, common_3_repairs, 
        common_3_culprits, solution_to_single_frequent_culprit, 
        tags, rating
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING faq_id;
    """
    with conn.cursor() as cur:
        cur.execute(
            insert_query,
            (
                faq_name,
                machine_type,
                cluster_id,
                common_3_repairs,
                common_3_culprits,
                solution_to_single_frequent_culprit,
                tags if tags else [],  # Use an empty list if no tags are provided
                rating,
            ),
        )
        faq_id = cur.fetchone()[0]  # Get the generated FAQ ID
    return faq_id


@with_connection
def get_unique_cluster_ids_and_machine_types(conn) -> dict:
    """
    Retrieve all unique cluster IDs and machine types from the `faqs` table.

    Args:
        conn: Database connection (handled by @with_connection decorator).

    Returns:
        A dictionary with two keys:
        - 'cluster_ids': List of unique cluster IDs (excluding NULL values).
        - 'machine_types': List of unique machine types.
    """
    query_cluster_ids = """
    SELECT DISTINCT cluster_id
    FROM faqs
    WHERE cluster_id IS NOT NULL
    """

    query_machine_types = """
    SELECT DISTINCT machine_type
    FROM faqs
    """

    with conn.cursor() as cur:
        # Fetch unique cluster IDs
        cur.execute(query_cluster_ids)
        cluster_ids = [row[0] for row in cur.fetchall()]

        # Fetch unique machine types
        cur.execute(query_machine_types)
        machine_types = [row[0] for row in cur.fetchall()]

    return cluster_ids, machine_types


def process_and_cluster_with_hdbscan(
    machine_type=None, min_cluster_size=2, min_samples=1
):
    """
    Process embeddings, perform HDBSCAN clustering, and generate summaries.
    """
    # Step 1: Fetch embeddings
    embeddings, embedding_ids, repair_job_ids = fetch_embeddings(machine_type)

    # Step 2: Perform HDBSCAN clustering
    cluster_labels, probabilities, clusterer = cluster_with_hdbscan(
        embeddings, min_cluster_size=min_cluster_size, min_samples=min_samples
    )

    # Step 3: Update cluster IDs in the database
    update_hdbscan_clusters(cluster_labels, embedding_ids)

    # Step 4: Summarize clusters and generate FAQs
    faq_clusters = summarize_hdbscan_clusters(
        cluster_labels, embedding_ids, machine_type
    )


@with_connection
def get_all_machine_types(conn):
    """
    Fetch all distinct machine types from the repairjob table.

    Args:
        conn: Database connection (provided by @with_connection decorator).

    Returns:
        List of distinct machine types (List[str]).
    """
    query = """
    SELECT DISTINCT machine_type
    FROM repairjob
    """
    with conn.cursor() as cur:
        cur.execute(query)
        result = cur.fetchall()
        # Extract machine_type values from the query result
        return [row[0] for row in result] if result else []


if __name__ == "__main__":
    machine_types_list = get_all_machine_types()
    for machine_type in machine_types_list:
        process_and_cluster_with_hdbscan(machine_type, 2, 1)
