from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# ===
# Data Models
# ===
from dataclasses import dataclass


@dataclass
class RepairJob:
    ticket_id: str
    manufacturing_plant_id: str
    video_path: str  # s3 path
    audio_path: str  # s3 path
    engineer_id: str
    machine_id: str
    machine_type: str  # should actually be in machine table
    downtime: int  # minutes
    repairtime: int  # minutes
    total_cost: int
    labor_cost: int
    item_cost: int
    item_bill_id: str
    replacement_items_list: str  # comma separated list
    # video and audio anaylsis
    description: str  # combines video modality with transcribed text
    transcription: str
    summary_steps: str  # opearating procedure followed in this video
    # repair job failed so previous and next ticket_id
    prev_failed_ticket_id: Optional[str] = None
    next_raised_ticket_id: Optional[str] = None


# ===
# DB Utils
# ===
import os
import uuid
from typing import Optional, List
import psycopg2
from psycopg2 import sql

# Connect to the database
PG_USER = os.environ["PG_USER"]
PG_PASSWORD = os.environ["PG_PASSWORD"]
PG_HOST = os.environ["PG_HOST"]
PG_PORT = os.environ["PG_PORT"]
PG_DB = os.environ["PG_DB"]


def with_connection(func):
    """
    Function decorator for passing connections
    """

    def connection(*args, **kwargs):
        # Here, you may even use a connection pool
        conn = psycopg2.connect(
            dbname=PG_DB, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT
        )
        try:
            rv = func(conn, *args, **kwargs)
        except Exception as e:
            conn.rollback()
            raise e
        else:
            # Can decide to see if you need to commit the transaction or not
            conn.commit()
        finally:
            conn.close()
        return rv

    return connection


# create table:
@with_connection
def create_table(conn):
    SQL = """
    CREATE TABLE IF NOT EXISTS RepairJob (
      ticket_id TEXT PRIMARY KEY,
      manufacturing_plant_id TEXT NOT NULL,
      video_path TEXT NOT NULL,
      audio_path TEXT NOT NULL,
      engineer_id TEXT NOT NULL,
      machine_id TEXT NOT NULL,
      machine_type TEXT NOT NULL,
      downtime INT NOT NULL,
      repairtime INT NOT NULL,
      total_cost INT NOT NULL,
      labor_cost INT NOT NULL,
      item_cost INT NOT NULL,
      item_bill_id TEXT NOT NULL,
      replacement_items_list TEXT NOT NULL,
      description TEXT NOT NULL,
      transcription TEXT NOT NULL,
      summary_steps TEXT NOT NULL,
      prev_failed_ticket_id TEXT,
      next_raised_ticket_id TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  """
    with conn.cursor() as cur:
        cur.execute(SQL)


# ===
# RepairJob
# ===
@with_connection
def create_repair_job(conn, repair_job: RepairJob):
    insert_query = """
    INSERT INTO RepairJob (
        ticket_id, manufacturing_plant_id, video_path, audio_path, engineer_id,
        machine_id, machine_type, downtime, repairtime, total_cost, labor_cost,
        item_cost, item_bill_id, replacement_items_list, description,
        transcription, summary_steps, prev_failed_ticket_id, next_raised_ticket_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    with conn.cursor() as cur:
        cur.execute(
            insert_query,
            (
                repair_job.ticket_id,
                repair_job.manufacturing_plant_id,
                repair_job.video_path,
                repair_job.audio_path,
                repair_job.engineer_id,
                repair_job.machine_id,
                repair_job.machine_type,
                repair_job.downtime,
                repair_job.repairtime,
                repair_job.total_cost,
                repair_job.labor_cost,
                repair_job.item_cost,
                repair_job.item_bill_id,
                repair_job.replacement_items_list,
                repair_job.description,
                repair_job.transcription,
                repair_job.summary_steps,
                repair_job.prev_failed_ticket_id,
                repair_job.next_raised_ticket_id,
            ),
        )


@with_connection
def read_repair_job(conn, ticket_id: str) -> Optional[RepairJob]:
    select_query = """
    SELECT ticket_id, manufacturing_plant_id, video_path, audio_path, engineer_id,
           machine_id, machine_type, downtime, repairtime, total_cost, labor_cost,
           item_cost, item_bill_id, replacement_items_list, description,
           transcription, summary_steps, prev_failed_ticket_id, next_raised_ticket_id
    FROM RepairJob
    WHERE ticket_id = %s
    """
    with conn.cursor() as cur:
        cur.execute(select_query, (ticket_id,))
        result = cur.fetchone()
        return RepairJob(*result) if result else None


@with_connection
def update_repair_job(conn, ticket_id: str, repair_job: RepairJob):
    update_query = """
    UPDATE RepairJob SET
        manufacturing_plant_id = %s, video_path = %s, audio_path = %s, engineer_id = %s,
        machine_id = %s, machine_type = %s, downtime = %s, repairtime = %s,
        total_cost = %s, labor_cost = %s, item_cost = %s, item_bill_id = %s,
        replacement_items_list = %s, description = %s, transcription = %s,
        summary_steps = %s, prev_failed_ticket_id = %s, next_raised_ticket_id = %s
    WHERE ticket_id = %s
    """
    with conn.cursor() as cur:
        cur.execute(
            update_query,
            (
                repair_job.manufacturing_plant_id,
                repair_job.video_path,
                repair_job.audio_path,
                repair_job.engineer_id,
                repair_job.machine_id,
                repair_job.machine_type,
                repair_job.downtime,
                repair_job.repairtime,
                repair_job.total_cost,
                repair_job.labor_cost,
                repair_job.item_cost,
                repair_job.item_bill_id,
                repair_job.replacement_items_list,
                repair_job.description,
                repair_job.transcription,
                repair_job.summary_steps,
                repair_job.prev_failed_ticket_id,
                repair_job.next_raised_ticket_id,
                ticket_id,
            ),
        )


@with_connection
def delete_repair_job(conn, ticket_id: str):
    delete_query = """
    DELETE FROM RepairJob WHERE ticket_id = %s
    """
    with conn.cursor() as cur:
        cur.execute(delete_query, (ticket_id,))
