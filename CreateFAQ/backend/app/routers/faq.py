import random
from fastapi import APIRouter, Query
from typing import List, Dict, Optional
from pydantic import BaseModel
from ..services.db import with_connection

router = APIRouter(prefix="/faqs", tags=["FAQs"])


@with_connection
def get_faqs(
    conn,
    machine_type: Optional[str] = None,
    searchQuery: Optional[str] = None,
    sortBy: Optional[str] = None,
    page: Optional[int] = 1,
    limit: Optional[int] = 10,
):
    """
    Query the FAQs table with optional filtering, sorting, and pagination.

    Args:
        conn: Database connection.
        machine_type: Filter by machine type.
        searchQuery: Search by faq_name or content fields (common repairs, culprits, solutions).
        sortBy: Sorting criteria (e.g., rating_desc, rating_asc, newest, oldest).
        page: Pagination page number.
        limit: Number of results per page.
    """
    query = """
    SELECT faq_id, faq_name, machine_type, cluster_id, common_3_repairs,
           common_3_culprits, solution_to_single_frequent_culprit, tags, rating, created_at
    FROM faqs
    WHERE 1=1
    """
    params = []

    # Filtering by machine type
    if machine_type:
        query += " AND machine_type = %s"
        params.append(machine_type)

    # Search by faq_name or text fields
    if searchQuery:
        query += """
        AND (faq_name ILIKE %s
             OR common_3_repairs ILIKE %s
             OR common_3_culprits ILIKE %s
             OR solution_to_single_frequent_culprit ILIKE %s)
        """
        params.extend([f"%{searchQuery}%"] * 4)

    # Sorting
    if sortBy == "rating_desc":
        query += " ORDER BY rating DESC"
    elif sortBy == "rating_asc":
        query += " ORDER BY rating ASC"
    elif sortBy == "newest":
        query += " ORDER BY created_at DESC"
    elif sortBy == "oldest":
        query += " ORDER BY created_at ASC"

    # Pagination
    offset = (page - 1) * limit
    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    # Execute the query
    with conn.cursor() as cur:
        cur.execute(query, params)
        results = cur.fetchall()

    return results


@router.get("/")
async def fetch_faqs(
    machine_type: Optional[str] = Query(None),
    searchQuery: Optional[str] = Query(None),
    sortBy: Optional[str] = Query(None),
    page: Optional[int] = Query(1),
    limit: Optional[int] = Query(10),
):
    """
    Fetch FAQs with optional filtering, sorting, and pagination.

    Args:
        machine_type: Filter by machine type.
        searchQuery: Search by faq_name or text fields (common repairs, culprits, solutions).
        sortBy: Sorting criteria (e.g., rating_desc, rating_asc, newest, oldest).
        page: Pagination page number.
        limit: Number of results per page.

    Returns:
        List of FAQs matching the criteria.
    """
    try:
        faqs = get_faqs(
            machine_type=machine_type,
            searchQuery=searchQuery,
            sortBy=sortBy,
            page=page,
            limit=limit,
        )
        return [
            {
                "faq_id": faq[0],
                "faq_name": faq[1],
                "machine_type": faq[2],
                "cluster_id": faq[3],
                "common_3_repairs": faq[4],
                "common_3_culprits": faq[5],
                "solution_to_single_frequent_culprit": faq[6],
                "tags": faq[7],
                "rating": random.randint(1, 5),
                "created_at": faq[9],
            }
            for faq in faqs
        ]
    except Exception as e:
        return {"error": str(e)}


class Feedback(BaseModel):
    faq_id: int
    rating: int
    feedback: Optional[str]


@with_connection
def add_feedback(conn, feedback: Feedback):
    query = """
    INSERT INTO faq_feedback (faq_id, rating, feedback)
    VALUES (%s, %s, %s)
    """
    with conn.cursor() as cur:
        cur.execute(query, (feedback.faq_id, feedback.rating, feedback.feedback))


@router.post("/feedback")
async def submit_faq_feedback(feedback: Feedback):
    add_feedback(feedback)
    return {"message": "Feedback submitted successfully"}
