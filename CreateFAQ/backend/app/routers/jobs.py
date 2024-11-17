"""
-----------------------------------------------------------------------
File: routers/jobs.py
Creation Time: Nov 17th 2024, 7:39 am
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
"""

from fastapi import APIRouter, Query
from typing import List, Dict
from fastapi import Query
from typing import Optional
from pydantic import BaseModel
from ..services.db import with_connection

router = APIRouter(prefix="/repairjobs", tags=["Repair Jobs"])


@with_connection
def get_unique_machine_types_from_repairjob(conn) -> List[str]:
    """
    Retrieve all unique machine types from the `repairjob` table.

    Args:
        conn: Database connection (handled by @with_connection decorator).

    Returns:
        A list of unique machine types.
    """
    query = """
    SELECT DISTINCT machine_type
    FROM repairjob
    """

    with conn.cursor() as cur:
        cur.execute(query)
        machine_types = [row[0] for row in cur.fetchall()]

    return machine_types


@router.get("/machine-types", response_model=List[str])
async def get_machine_types():
    """
    API to retrieve all unique machine types from the `repairjob` table.

    Returns:
        List of unique machine types.
    """
    try:
        machine_types = get_unique_machine_types_from_repairjob()
        return machine_types
    except Exception as e:
        return {"error": str(e)}
