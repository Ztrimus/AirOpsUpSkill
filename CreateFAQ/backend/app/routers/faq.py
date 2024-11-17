from fastapi import APIRouter, Query
from typing import List, Dict

router = APIRouter(prefix="/faqs", tags=["FAQs"])

# Dummy data for testing
dummy_faqs = [
    {
        "id": 1,
        "question": "What causes E02 error in machine AF500?",
        "answer": "Sensor misalignment or loose wiring.",
        "tags": ["failure", "E02", "AF500"],
        "related_videos": ["https://youtu.be/fake-video1"],
        "repair_time": "15 minutes",
        "common_failures": ["Sensor misalignment", "Loose wiring"],
    },
    {
        "id": 2,
        "question": "How to resolve E02 error?",
        "answer": "1. Check sensor alignment. 2. Tighten wiring. 3. Reset the system.",
        "tags": ["repair", "E02", "AF500"],
        "related_videos": ["https://youtu.be/fake-video2"],
        "repair_time": "10 minutes",
        "common_failures": ["Loose sensor connections"],
    },
    {
        "id": 3,
        "question": "What is the preventive maintenance for AF500?",
        "answer": "Regularly inspect sensors and secure wiring connections.",
        "tags": ["preventive", "maintenance", "AF500"],
        "related_videos": ["https://youtu.be/fake-video3"],
        "repair_time": "30 minutes (inspection)",
        "common_failures": [],
    },
]


@router.get("/")
def get_faqs(
    query: str = Query(None, description="Search query for FAQs")
) -> List[Dict]:
    """
    Fetch FAQs based on a search query.
    If no query is provided, return all FAQs.
    """
    if query:
        # Filter FAQs based on the query
        filtered_faqs = [
            faq
            for faq in dummy_faqs
            if query.lower() in faq["question"].lower() or query.lower() in faq["tags"]
        ]
        return filtered_faqs
    return dummy_faqs
