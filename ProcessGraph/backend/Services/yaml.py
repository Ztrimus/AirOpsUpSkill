import yaml
import uuid
import os
from dotenv import load_dotenv
from openai import OpenAI
import re
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import shutil

load_dotenv()

def initialize_tree_with_openai(name, content):
    """
    Initialize a tree structure for a process tree using OpenAI API and store it in a YAML file.
    """
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    prompt = """
    Create a tree structure for a process tree in YAML format. The tree should include:
    - UUID: A unique identifier for each node.
    - TreeLevel: An integer indicating the depth of the node (0 for the root).
    - Step: A simple step in the process.
    - IDList: A list of video IDs associated with the step.
    - ChildNodeUUID: A list of UUIDs of child nodes.

    The tree should be represented as a dictionary of dictionaries, where:
    - The root node is at TreeLevel 0.
    - Each level represents a new step in the process.
    - Each node's attributes are stored in a dictionary.
    - The entire structure is saved in YAML format.
    """
    try:
        # Generate the process tree structure using OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": content}],
            stream=False,
        )

        raw_content = completion.choices[0].message.content
        print("Raw Content:\n", raw_content)

        if "```yaml" in raw_content:
            yaml_content = raw_content.split("```yaml", 1)[1].split("```", 1)[0].strip()
        else:
            raise ValueError("YAML block not found in the response content")

        print("Processed YAML Content:\n", yaml_content)

        # Parse the cleaned YAML content
        tree = yaml.safe_load(yaml_content)

        # Save the tree to a YAML file
        with open(f"{name}.yaml", 'w') as yaml_output_file:
            yaml.dump(tree, yaml_output_file)

        print(f"Process tree initialized and saved as {name}.yaml")
    except Exception as e:
        print(f"Error initializing process tree: {e}")


def make_tasks(content):
    """
    Break the video content into simple tasks using OpenAI API.
    """
    try:
        client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        prompt = """
        The following is a video content. Break it down into simple tasks. Make sure the tasks are related to the work being done in the video. Keep it short and simple.
        """
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": content}],
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
    Determines the UUID for the task in the YAML file or adds the task if not present.
    """
    try:
        with open(filepath, 'r') as yaml_file:
            tree = yaml.safe_load(yaml_file)
        
        client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        prompt = f"""
        You will be given a YAML file in the form of a text file. The YAML file consists of a tree structure for a process tree.
        You will be given a task, and you have to find the UUID of the task in the YAML file. 
        Be very specific with the output
        -If a similar task is present it should use the update action otherwise it should use the add action.
        - If the task is present in the YAML file, return the UUID of the task that should be updated.
        - If the task is not present in the YAML file, return the UUID of the parent where the task can be added.
        - Output format:  Action: ADD, UUID: NodeUUID6, TASK: "Task to be done" or Action: UPDATE, UUID: NodeUUID6

        Task: {task}
        YAML Tree:
        {yaml.dump(tree, default_flow_style=False)}
        """
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}],
            stream=False,
            max_completion_tokens=60,
        )
        result = completion.choices[0].message.content.strip()

        # Parse the action and extract the UUID, removing "UUID" prefix
        action_match = re.search(r"Action:\s*(ADD|UPDATE)", result, re.IGNORECASE)
        uuid_match = re.search(r"UUID:\s*([\w-]+)", result, re.IGNORECASE)

        if action_match and uuid_match:
            action = action_match.group(1).upper()
            uuid = uuid_match.group(1)  # Extract the clean UUID (e.g., NodeUUID6)

            # Call the appropriate function
            if action == "ADD":
                add_node(uuid, task, filepath, videoid)
            elif action == "UPDATE":
                update_node(uuid, videoid, filepath)
            else:
                print("Unexpected action returned.")
        else:
            print("Unable to parse the response. Ensure the prompt generates clear output.")
            print(f"Response: {result}")
    except Exception as e:
        print(f"Error processing content with OpenAI: {e}")

def add_node(parent_uuid, task, file, video_id):
    """
    Adds a new task node to the YAML file under the specified parent UUID.

    Parameters:
    - parent_uuid (str): The UUID of the parent node under which the new node will be added.
    - task (str): The task description for the new node.
    - file (str): Path to the YAML file.
    - video_id (str): The video ID associated with the new task.
    """
    try:
        with open(file, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)

        # Access the ProcessTree
        tree = data.get('ProcessTree', {})

        # Generate a new UUID for the new node
        new_uuid = str(uuid.uuid4())[:8]  # Shorten for readability, adjust as needed

        # Create the new node
        new_node = {
            'UUID': new_uuid,
            'Step': task,
            'TreeLevel': None,  # Will set this later
            'IDList': [video_id],
            'ChildNodeUUID': []
        }

        # Find the parent node by searching through the tree
        parent_node = None
        for node_key, node_value in tree.items():
            if node_value.get('UUID') == parent_uuid:
                parent_node = node_value
                break

        if parent_node:
            # Update the parent's ChildNodeUUID list
            if 'ChildNodeUUID' in parent_node and parent_node['ChildNodeUUID'] is not None:
                parent_node['ChildNodeUUID'].append(new_uuid)
            else:
                parent_node['ChildNodeUUID'] = [new_uuid]

            # Set the TreeLevel of the new node
            parent_level = parent_node.get('TreeLevel', 0)
            new_node['TreeLevel'] = parent_level + 1

            # Add the new node to the tree under a key that is its UUID
            tree[new_uuid] = new_node
        else:
            print(f"Parent UUID {parent_uuid} not found in the YAML file.")
            return

        # Write the updated data back to the file
        with open(file, 'w') as yaml_output_file:
            yaml.dump(data, yaml_output_file, default_flow_style=False)

        print(f"Task '{task}' added successfully under parent UUID {parent_uuid}.")

    except FileNotFoundError:
        print(f"The file '{file}' does not exist.")
    except yaml.YAMLError as yaml_err:
        print(f"Error parsing YAML file: {yaml_err}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def update_node(node_uuid, video_id, file):
    """
    Updates the node with the given UUID in the YAML file by adding the video_id to the IDList field,
    appending it even if it's already present.
    """
    try:
        with open(file, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)

        # Access the ProcessTree
        tree = data.get('ProcessTree', {})

        # Find the node to update by searching through the tree
        node_to_update = None
        for node_key, node_value in tree.items():
            if node_value.get('UUID') == node_uuid:
                node_to_update = node_value
                break

        if node_to_update:
            # Append the video_id to the IDList without checking for duplicates
            if 'IDList' in node_to_update and node_to_update['IDList'] is not None:
                node_to_update['IDList'].append(video_id)
            else:
                node_to_update['IDList'] = [video_id]

            # Write the updated data back to the file
            with open(file, 'w') as yaml_output_file:
                yaml.dump(data, yaml_output_file, default_flow_style=False)

            print(f"Video ID '{video_id}' appended successfully for UUID {node_uuid}.")
        else:
            print(f"UUID {node_uuid} not found in the YAML file.")

    except FileNotFoundError:
        print(f"The file '{file}' does not exist.")
    except yaml.YAMLError as yaml_err:
        print(f"Error parsing YAML file: {yaml_err}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def plot_yaml_tree(yaml_file, output_image="yaml_tree.png"):
    """
    Reads the YAML tree and plots it as a graph.

    Parameters:
    - yaml_file (str): Path to the YAML file.
    - output_image (str): Filename for the saved plot image.
    """
    try:
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)

        G = nx.DiGraph()

        def add_edges(node, parent=None):
            node_id = node.get("uuid")
            node_task = node.get("task", "No Task")
            label = f"{node_task}\n({node_id})"
            G.add_node(node_id, label=label)

            if parent:
                G.add_edge(parent, node_id)

            children = node.get("children", [])
            for child in children:
                add_edges(child, node_id)

        # Assuming the YAML has a top-level key 'nodes' which is a list
        nodes = data.get("nodes", [])
        for node in nodes:
            add_edges(node)

        # Extract labels
        labels = nx.get_node_attributes(G, 'label')

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=0.5, iterations=50)
        nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color="lightblue", font_size=8, font_weight="bold", arrows=True)
        plt.title("YAML Task Tree")
        plt.tight_layout()
        plt.savefig(output_image)
        plt.close()
        print(f"YAML tree plotted and saved as '{output_image}'.")
    except FileNotFoundError:
        print(f"Error: The file '{yaml_file}' does not exist.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"Unexpected error during plotting: {e}")

def backup_yaml(file):
    """
    Creates a backup of the YAML file.

    Parameters:
    - file (str): Path to the YAML file.
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
    Main function to process the CSV file and update the YAML tree.
    After processing each row, it plots the YAML tree.
    """
    import os
    import pandas as pd

    csv_file = "ProcessGraph/backend/MockData/Unique_First-Person_Video_Transcripts_for_Mini_Cooper_2015_Oil_Change.csv"  
    yaml_file = "process_tree.yaml"

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

    # Check if YAML file exists; if not, initialize it
    if not os.path.exists(yaml_file):
        print("YAML file does not exist. Initializing...")
        if df.empty:
            print("Error: CSV file is empty. Cannot initialize YAML tree.")
            return
        first_row = df.iloc[0]  # Extract the first row
        # Combine Video_ID and Transcript into a single string
        first_row_string = f"Video_ID: {first_row['Video_ID']}, Transcript: {first_row['Transcript']}"
        initialize_tree_with_openai("process_tree", first_row_string)
        plot_yaml_tree(yaml_file, output_image="yaml_tree_initial.png")

    # Process each row in the CSV
    for index, row in df.iterrows():
        video_id = row['Video_ID']
        transcript = row['Transcript']

        tasks = make_tasks(transcript)
        print(f"\n[Row {index + 1}] Generated Tasks for Video ID {video_id}: {tasks}")

        # Update the YAML tree with tasks
        for task in tasks:
            get_uuid(task, yaml_file, video_id)

        # Plot the YAML tree after processing each row
        output_image = f"yaml_tree_after_row_{index + 1}.png"
        plot_yaml_tree(yaml_file, output_image=output_image)

if __name__ == "__main__":
    main()
