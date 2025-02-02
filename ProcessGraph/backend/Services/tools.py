import json
import uuid
import os
from dotenv import load_dotenv
from openai import OpenAI
import re
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import shutil

# Load environment variables from .env file
load_dotenv()

def initialize_tree_with_openai(name, content):
    """
    Initialize a tree structure for a process tree using OpenAI API and store it in a JSON file.
    """
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    prompt = """
    Create a tree structure for a process tree in JSON format. The tree should include:
    - UUID: A unique identifier for each node.
    - TreeLevel: An integer indicating the depth of the node (0 for the root).
    - Step: A simple step in the process.
    - IDList: A list of video IDs associated with the step.
    - ChildNodeUUID: A list of UUIDs of child nodes.

    The tree should be represented as a dictionary where:
    - Each key is the UUID of a node.
    - Each value is a dictionary containing the node's attributes.
    - The root node has TreeLevel 0.
    - Each level represents a new step in the process.
    - The entire structure is saved in JSON format.
    -start-```json
    """
    try:
        # Generate the process tree structure using OpenAI
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ],
            stream=False,
        )

        raw_content = completion.choices[0].message.content
        print("Raw Content:\n", raw_content)

        if "```json" in raw_content:
            json_content = raw_content.split("```json", 1)[1].split("```", 1)[0].strip()
        else:
            raise ValueError("JSON block not found in the response content")

        print("Processed JSON Content:\n", json_content)

        # Parse the cleaned JSON content
        tree = json.loads(json_content)

        # Save the tree to a JSON file
        with open(f"{name}.json", 'w') as json_output_file:
            json.dump(tree, json_output_file, indent=4)

        print(f"Process tree initialized and saved as {name}.json")
    except Exception as e:
        print(f"Error initializing process tree: {e}")


def make_tasks(content):
    """
    Break the video content into simple tasks using OpenAI API.
    """
    try:
        client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        prompt = """
        The following is a video transcript. Break it down into simple, actionable tasks. Ensure that the tasks are relevant to the work being done in the video. Keep each task concise and clear.
        """
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ],
            stream=False,
        )
        raw_content = completion.choices[0].message.content.strip()
        tasks = [task.strip() for task in raw_content.split('\n') if task.strip()]
        return tasks
    except Exception as e:
        print(f"Error processing content: {e}")
        return []


def get_uuid(task, filepath, videoid):
    """
    Determines the UUID for the task in the JSON file or adds the task if not present.
    """
    try:
        with open(filepath, 'r') as json_file:
            tree = json.load(json_file)

        client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        prompt = f"""
        You will be given a JSON file representing a process tree.
        Each key in the JSON is a UUID, and each value is a node with attributes:
        - TreeLevel
        - Step
        - IDList
        - ChildNodeUUID

        You will also be given a task. Determine whether this task already exists in the process tree.

        - If a similar task exists, specify that the action should be UPDATE and provide the UUID of the existing task.
        - If the task does not exist, specify that the action should be ADD, provide the UUID of the parent node where it would be the next step, and include the task description. I want a flat structure, so the task should be added as a child of the parent node.

        Output format:
        - For ADD: Action: ADD, UUID: <Parent_UUID>, TASK: "<Task Description>"
        - For UPDATE: Action: UPDATE, UUID: <Existing_Task_UUID>

        Task: "{task}"
        JSON Tree:
        {json.dumps(tree, indent=4)}
        """
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}],
            stream=False,
            max_tokens=150,
        )
        result = completion.choices[0].message.content.strip()

        print(f"OpenAI Response for Task '{task}': {result}")

        # Parse the action and extract the UUID
        action_match = re.search(r"Action:\s*(ADD|UPDATE)", result, re.IGNORECASE)
        uuid_match = re.search(r"UUID:\s*([\w-]+)", result, re.IGNORECASE)

        if action_match and uuid_match:
            action = action_match.group(1).upper()
            uuid_value = uuid_match.group(1)  # Extract the clean UUID

            # Call the appropriate function
            if action == "ADD":
                add_node(uuid_value, task, filepath, videoid)
            elif action == "UPDATE":
                update_node(uuid_value, videoid, filepath)
            else:
                print("Unexpected action returned.")
        else:
            print("Unable to parse the response. Ensure the prompt generates clear output.")
            print(f"Response: {result}")
    except Exception as e:
        print(f"Error processing content with OpenAI: {e}")


def add_node(parent_uuid, task, file, video_id):
    """
    Adds a new task node to the JSON file under the specified parent UUID.

    Parameters:
    - parent_uuid (str): The UUID of the parent node under which the new node will be added.
    - task (str): The task description for the new node.
    - file (str): Path to the JSON file.
    - video_id (str): The video ID associated with the new task.
    """
    try:
        with open(file, 'r') as json_file:
            tree = json.load(json_file)

        # Generate a new UUID for the new node
        new_uuid = str(uuid.uuid4())

        # Create the new node
        new_node = {
            'UUID': new_uuid,
            'Step': task,
            'TreeLevel': None,  # Will set this later
            'IDList': [video_id],
            'ChildNodeUUID': []
        }

        # Find the parent node
        parent_node = tree.get(parent_uuid)

        if parent_node:
            # Update the parent's ChildNodeUUID list
            parent_node.setdefault('ChildNodeUUID', []).append(new_uuid)

            # Set the TreeLevel of the new node
            parent_level = parent_node.get('TreeLevel', 0)
            new_node['TreeLevel'] = parent_level + 1

            # Add the new node to the tree
            tree[new_uuid] = new_node
            print(f"Added new node with UUID {new_uuid} under parent UUID {parent_uuid}.")
        else:
            print(f"Parent UUID {parent_uuid} not found in the JSON file.")
            return

        # Write the updated tree back to the file
        with open(file, 'w') as json_output_file:
            json.dump(tree, json_output_file, indent=4)

        print(f"Task '{task}' added successfully under parent UUID {parent_uuid}.")

    except FileNotFoundError:
        print(f"The file '{file}' does not exist.")
    except json.JSONDecodeError as json_err:
        print(f"Error parsing JSON file: {json_err}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def update_node(node_uuid, video_id, file):
    """
    Updates the node with the given UUID in the JSON file by adding the video_id to the IDList field,
    only if it's not already present.

    Parameters:
    - node_uuid (str): The UUID of the node to update.
    - video_id (str): The video ID to append.
    - file (str): Path to the JSON file.
    """
    try:
        with open(file, 'r') as json_file:
            tree = json.load(json_file)

        # Find the node to update
        node_to_update = tree.get(node_uuid)

        if node_to_update:
            # Initialize IDList if it doesn't exist
            id_list = node_to_update.setdefault('IDList', [])

            if video_id in id_list:
                print(f"Video ID '{video_id}' already exists in node UUID {node_uuid}. No action taken.")
            else:
                # Append the video_id to the IDList
                id_list.append(video_id)
                print(f"Appended Video ID '{video_id}' to node UUID {node_uuid}.")

                # Write the updated tree back to the file
                with open(file, 'w') as json_output_file:
                    json.dump(tree, json_output_file, indent=4)

                print(f"Video ID '{video_id}' appended successfully for UUID {node_uuid}.")
        else:
            print(f"UUID {node_uuid} not found in the JSON file.")

    except FileNotFoundError:
        print(f"The file '{file}' does not exist.")
    except json.JSONDecodeError as json_err:
        print(f"Error parsing JSON file: {json_err}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def plot_json_tree(json_file, output_image="json_tree.png"):
    """
    Reads the JSON tree and plots it as a three.

    Parameters:
    - json_file (str): Path to the JSON file.
    - output_image (str): Filename for the saved plot image.
    """
    try:
        with open(json_file, 'r') as file:
            tree = json.load(file)

        G = nx.DiGraph()

        # Build the graph from the tree
        for node_uuid, node_value in tree.items():
            node_id = node_value.get("UUID")
            node_step = node_value.get("Step", "No Step")
            label = f"{node_step}\n({node_id})"
            G.add_node(node_id, label=label)

            # Add edges to child nodes
            child_uuids = node_value.get("ChildNodeUUID", [])
            for child_uuid in child_uuids:
                child_node = tree.get(child_uuid)
                if child_node:
                    child_id = child_node.get("UUID")
                    G.add_edge(node_id, child_id)
                else:
                    print(f"Child UUID {child_uuid} not found in the JSON file.")

        # Extract labels
        labels = nx.get_node_attributes(G, 'label')

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=0.5, iterations=100)
        nx.draw_networkx_nodes(G, pos, node_size=3000, node_color="lightblue")
        nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20)
        nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight="bold")

        plt.title("JSON Task Tree")
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_image)
        plt.close()
        print(f"JSON tree plotted and saved as '{output_image}'.")

    except FileNotFoundError:
        print(f"Error: The file '{json_file}' does not exist.")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
    except Exception as e:
        print(f"Unexpected error during plotting: {e}")


def backup_json(file):
    """
    Creates a backup of the JSON file.

    Parameters:
    - file (str): Path to the JSON file.
    """
    backup_file = f"{file}.backup"
    try:
        shutil.copyfile(file, backup_file)
        print(f"Backup created at '{backup_file}'.")
    except FileNotFoundError:
        print(f"Cannot create backup. The file '{file}' does not exist.")
    except Exception as e:
        print(f"Error creating backup: {e}")


def main():
    """
    Main function to process the CSV file and update the JSON tree.
    After processing each row, it plots the JSON tree.
    """
    csv_file = "ProcessGraph/backend/MockData/Unique_First-Person_Video_Transcripts_for_Mini_Cooper_2015_Oil_Change.csv"
    json_file = "process_tree.json"

    # Load the CSV file
    try:
        df = pd.read_csv(csv_file)
        print(f"Loaded CSV file '{csv_file}' successfully.")
    except FileNotFoundError:
        print(f"Error: The CSV file '{csv_file}' does not exist.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: The CSV file '{csv_file}' is empty.")
        return
    except Exception as e:
        print(f"Unexpected error loading CSV: {e}")
        return

    # Check if JSON file exists; if not, initialize it
    if not os.path.exists(json_file):
        print("JSON file does not exist. Initializing...")
        if df.empty:
            print("Error: CSV file is empty. Cannot initialize JSON tree.")
            return
        first_row = df.iloc[0]  # Extract the first row
        # Combine Video_ID and Transcript into a single string
        first_row_string = f"Video_ID: {first_row['Video_ID']}, Transcript: {first_row['Transcript']}"
        initialize_tree_with_openai("process_tree", first_row_string)
        plot_json_tree(json_file, output_image="json_tree_initial.png")

    # Process each row in the CSV
    for index, row in df.iterrows():
        video_id = row['Video_ID']
        transcript = row['Transcript']

        tasks = make_tasks(transcript)
        print(f"\n[Row {index + 1}] Generated Tasks for Video ID {video_id}: {tasks}")

        # Update the JSON tree with tasks
        for task in tasks:
            get_uuid(task, json_file, video_id)

        # Plot the JSON tree after processing each row
        output_image = f"json_tree_after_row_{index + 1}.png"
        plot_json_tree(json_file, output_image=output_image)


if __name__ == "__main__":
    main()
