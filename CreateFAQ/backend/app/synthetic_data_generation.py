"""
-----------------------------------------------------------------------
File: app/synthetic_data_generation.py
Creation Time: Nov 16th 2024, 10:02 pm
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
"""

import os
import random
import logging
from datetime import datetime, timedelta
from db import create_table, create_repair_job, RepairJob
from openai import OpenAI
import json

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize Gemini Client
if "GEMINI_API_KEY" not in os.environ:
    raise EnvironmentError("GEMINI_API_KEY not found in environment variables.")

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# List of sample data
manufacturing_plants = ["PHX01", "TOR01", "BLR01", "PRG01"]
engineers = [
    "ENG-JD-1234",
    "ENG-MA-5678",
    "ENG-KS-9012",
    "ENG-RT-3456",
    "ENG-LW-2345",
    "ENG-TM-7890",
    "ENG-PG-4567",
    "ENG-SK-3451",
    "ENG-AB-5673",
    "ENG-ML-2234",
    "ENG-CW-6789",
    "ENG-NV-4321",
    "ENG-BP-1290",
    "ENG-RS-3459",
    "ENG-DC-8765",
    "ENG-TP-5467",
    "ENG-AG-2348",
    "ENG-FK-0987",
    "ENG-MN-4563",
    "ENG-VR-7643",
]
machine_types = [
    "Auxiliary Power Units (APUs)",
    "Turbofan Engines",
    "Environmental Control Systems",
    "Avionics Systems",
    "Landing Systems",
]

# Machine Models
machine_models = {
    "Auxiliary Power Units (APUs)": [
        "131-9A (Airbus A320 family)",
        "331-350C (Boeing 777)",
        "36-150 (Helicopters)",
    ],
    "Turbofan Engines": [
        "HTF7000 (Business jets)",
        "TFE731 (Business jets)",
        "ALF502/LF507 (Regional airliners)",
    ],
    "Environmental Control Systems": [
        "Cabin Pressure Control Systems",
        "Air Conditioning Packs",
        "Bleed Air Systems",
    ],
    "Avionics Systems": [
        "Primus Epic integrated avionics system",
        "IntuVue RDR-4000 weather radar",
        "LASEREF VI Inertial Reference System",
    ],
    "Landing Systems": [
        "Electric Braking Systems",
        "Wheels and Brakes",
        "Tire Pressure Monitoring Systems",
    ],
}
repair_jobs = [
    "Fuel pump failure causing startup issues",
    "Oil filter clog leading to overheating",
    "Sensor module malfunction causing erroneous readings",
    "Compressor blade wear causing vibration",
    "Avionics system software update failure",
    "APU not starting due to electrical issue",
    "Engine overheating under load",
    "Landing gear retraction failure",
    "Weather radar displaying incorrect data",
    "Cabin pressure control system failure",
]

standard_repair_steps = {
    "Fuel pump failure causing startup issues": [
        "Inspect fuel pump for visible damage.",
        "Clean and recalibrate fuel pump connections.",
        "Replace faulty fuel pump with a new unit.",
        "Inspect and clean fuel lines for debris.",
        "Conduct system test to verify fuel pump performance.",
    ],
    "Oil filter clog leading to overheating": [
        "Drain and inspect engine oil for contaminants.",
        "Replace clogged oil filter with a new filter.",
        "Flush the oil system to remove residue.",
        "Inspect and clean oil lines for blockages.",
        "Refill engine with recommended oil.",
        "Test engine operation under load to ensure proper cooling.",
    ],
    "Sensor module malfunction causing erroneous readings": [
        "Disconnect and inspect the faulty sensor module.",
        "Check wiring connections for wear or loose fittings.",
        "Clean sensor module contact points.",
        "Replace faulty sensor module with a new one.",
        "Calibrate the new sensor module.",
        "Verify accuracy of the sensor readings through diagnostic tests.",
        "Document calibration results for records.",
    ],
    "Compressor blade wear causing vibration": [
        "Inspect compressor blades for visible wear or damage.",
        "Remove worn or damaged compressor blades.",
        "Install replacement blades according to manufacturer specifications.",
        "Balance the compressor assembly to minimize vibration.",
        "Perform alignment tests on the engine components.",
        "Test engine operation at various speeds to verify performance.",
        "Record vibration test results for future reference.",
    ],
    "Avionics system software update failure": [
        "Perform diagnostic tests to identify the software issue.",
        "Back up the current avionics system configuration.",
        "Reset the avionics system to factory settings.",
        "Reinstall the latest software version.",
        "Verify software installation through system checks.",
        "Conduct functional tests for critical avionics features.",
        "Document software update results and any anomalies.",
    ],
    "APU not starting due to electrical issue": [
        "Inspect APU electrical connections for wear or damage.",
        "Test the APU starter motor for proper functionality.",
        "Check the APU battery voltage and replace if necessary.",
        "Repair or replace faulty electrical wiring.",
        "Inspect and clean APU control relays.",
        "Test APU operation under no-load conditions.",
        "Verify proper startup sequence and load-bearing capability.",
    ],
    "Engine overheating under load": [
        "Inspect the cooling system for blockages.",
        "Check engine oil levels and quality.",
        "Replace worn-out coolant pump or hoses.",
        "Test the radiator for leaks or blockages.",
        "Inspect and clean air intake filters.",
        "Perform an engine heat test under load conditions.",
        "Replace or repair any failed components.",
    ],
    "Landing gear retraction failure": [
        "Inspect landing gear hydraulic lines for leaks.",
        "Test landing gear actuators for proper operation.",
        "Replace hydraulic fluid and bleed the system.",
        "Check and repair landing gear sensors.",
        "Inspect landing gear mechanical linkages for wear.",
        "Test landing gear retraction and extension cycles.",
        "Verify system performance through multiple cycles.",
    ],
    "Weather radar displaying incorrect data": [
        "Inspect radar antenna for physical damage.",
        "Test radar signal connections and wiring.",
        "Update radar software to the latest version.",
        "Replace faulty radar modules as needed.",
        "Calibrate radar signal strength and accuracy.",
        "Perform flight tests to validate radar data.",
        "Document radar performance results and system status.",
    ],
    "Cabin pressure control system failure": [
        "Inspect cabin pressure control valves for wear.",
        "Check and replace faulty sensors in the pressure control system.",
        "Test pneumatic lines for leaks or blockages.",
        "Replace or repair damaged pressure regulators.",
        "Calibrate the pressure control system.",
        "Conduct a pressure test under simulated flight conditions.",
        "Document system performance and calibration data.",
    ],
}


# Helper function to generate random timestamps
def random_timestamp(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(
        days=random_days, hours=random.randint(0, 23), minutes=random.randint(0, 59)
    )


# Generate synthetic repair job instance
def generate_repair_job_instance(ticket_id, job_type):
    machine_type = random.choice(machine_types)
    plant = random.choice(manufacturing_plants)
    video_path = f"/media/repairs/2024/11/{ticket_id}_video.mp4"
    audio_path = f"/media/repairs/2024/11/{ticket_id}_audio.wav"
    engineer = random.choice(engineers)
    machine_id = (
        f"{random.choice(machine_models[machine_type])}-{random.randint(1, 1000):04}"
    )
    downtime = random.randint(24, 72)
    repairtime = random.randint(4, 12)
    total_cost = round(random.uniform(5000, 50000), 2)
    labor_cost = round(total_cost * 0.4, 2)
    item_cost = round(total_cost * 0.6, 2)
    created_at = random_timestamp(datetime(2024, 11, 1), datetime(2024, 11, 16))
    updated_at = created_at + timedelta(hours=random.randint(1, 48))
    status = random.choice(["success", "failed", "in-progress"])

    # Standard repair steps for the job type
    repair_steps = random.choice(standard_repair_steps[job_type])

    return {
        "ticket_id": ticket_id,
        "manufacturing_plant_id": plant,
        "video_path": video_path,
        "audio_path": audio_path,
        "engineer_id": engineer,
        "machine_id": machine_id,
        "machine_type": machine_type,
        "job_type": job_type,
        "downtime": downtime,
        "repairtime": repairtime,
        "total_cost": total_cost,
        "labor_cost": labor_cost,
        "item_cost": item_cost,
        "repair_steps": repair_steps,
        "status": status,
        "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": updated_at.strftime("%Y-%m-%d %H:%M:%S"),
    }


# Generate description, transcription, and summary using Gemini
def generate_text_fields_with_gemini(job):
    prompt = f"""
You are tasked with generating realistic repair documentation for a repair job, which may have one of the following outcomes and choose only one outcome from the following:
1. Correct/Successful repair.
2. Failed repair attempt.
3. Successful repair but through an alternate method.
4. Failed repair attempt with steps differing from the planned repair process.

Given the following repair job details, generate:
1. A detailed description of the issue, specifying what went wrong with the equipment.
2. A verbal transcription of the technician’s commentary during the repair process, reflecting their observations, actions, and decisions.
3. A step-by-step summary of the repair process, including deviations (if any) from the planned steps.

**Repair Job Details:**
- Ticket ID: {job["ticket_id"]}
- Manufacturing Plant: {job["manufacturing_plant_id"]}
- Machine Type: {job["machine_type"]}
- Machine ID: {job["machine_id"]}
- Job Type: {job["job_type"]}
- Planned Repair Steps: {job["repair_steps"]}

**Output Format:**
Please provide the output in JSON format with the following fields:
{{
  "Description": "Detailed description of the issue",
  "Transcription": "Verbal transcription of the technician’s commentary",
  "Summary Steps": "Step-by-step summary of the repair process"
}}

**Examples of Repair Outcomes:**
1. Correct Repair: The planned steps were followed successfully, and the issue was resolved.
2. Failed Repair: The planned steps were executed, but the issue could not be resolved due to unforeseen complications.
3. Alternate Success: The repair succeeded, but alternate methods or steps were required.
4. Failure with Deviations: The repair failed, and the actual steps differed significantly from the planned ones.

Make sure the output is valid JSON and adheres to the specified format.
"""

    try:
        logging.info(f"Sending prompt for job: {job['ticket_id']}")
        # Send the prompt to the Gemini API
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            n=1,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )

        # Extract the content from the response
        content = response.choices[0].message.content.strip()

        # Parse JSON response
        parsed_content = json.loads(content)

        # Assign values to the job
        job["description"] = parsed_content.get(
            "Description", "Description not available"
        ).strip()
        job["transcription"] = parsed_content.get(
            "Transcription", "Transcription not available"
        ).strip()
        job["summary_steps"] = parsed_content.get(
            "Summary Steps", "Summary Steps not available"
        )

        return job

    except Exception as e:
        logging.error(f"Error generating text fields for job {job['ticket_id']}: {e}")
        raise


# Generate full repair job dataset
def generate_full_repair_job_data():
    for i in range(26, 100):
        job_type = random.choice(repair_jobs)
        ticket_id = f"HON-2024-11-{i:03}"
        job_instance = generate_repair_job_instance(ticket_id, job_type)
        job = generate_text_fields_with_gemini(job_instance)
        save_repair_jobs_to_db(job)


def save_repair_jobs_to_db(job):
    """
    Save generated repair jobs to the PostgreSQL database.
    """
    try:
        # Create a RepairJob instance
        repair_job = RepairJob(
            ticket_id=job["ticket_id"],
            manufacturing_plant_id=job["manufacturing_plant_id"],
            video_path=job["video_path"],
            audio_path=job["audio_path"],
            engineer_id=job["engineer_id"],
            machine_id=job["machine_id"],
            machine_type=job["machine_type"],
            downtime=job["downtime"],
            repairtime=job["repairtime"],
            total_cost=job["total_cost"],
            labor_cost=job["labor_cost"],
            item_cost=job["item_cost"],
            item_bill_id="BILL-"
            + job["ticket_id"],  # Example for generating a unique bill ID
            replacement_items_list=job.get("replacement_items_list", ""),
            description=job["description"],
            transcription=job["transcription"],
            summary_steps=job["summary_steps"],
            prev_failed_ticket_id=None,  # Placeholder
            next_raised_ticket_id=None,  # Placeholder
        )

        # Save to database
        create_repair_job(repair_job)
        logging.info(
            f"Successfully saved repair job {job['ticket_id']} to the database."
        )
    except Exception as e:
        logging.error(
            f"Failed to save repair job {job['ticket_id']} to the database: {e}"
        )


# Main script
if __name__ == "__main__":
    try:
        # Step 1: Create the table if it doesn't exist
        logging.info("Creating RepairJob table if it doesn't exist.")
        create_table()

        # Step 2: Generate synthetic repair job data
        logging.info("Generating synthetic repair jobs.")
        repair_jobs_data = generate_full_repair_job_data()

        logging.info("All repair jobs have been processed.")

        logging.info("Repair jobs data saved successfully.")
    except Exception as e:
        logging.error(f"Critical failure: {e}")
