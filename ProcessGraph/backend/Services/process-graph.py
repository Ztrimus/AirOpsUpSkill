import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt
import json

def read_data(file_path):
    if not hasattr(read_data, "reader"):
        read_data.reader = pd.read_csv(file_path, chunksize=5)
    try:
        df = next(read_data.reader)
        json_data = df.set_index('Video_ID')['Transcript'].to_dict()
        return json_data
    except StopIteration:
        read_data.reader = pd.read_csv(file_path, chunksize=5)
        return {}

def csv_dump(json_data, file_path):
    data = json.loads(json_data)
    df = pd.DataFrame(data, columns=['Tree_Level', 'Task', 'Parent_Task', 'Video_ID'])
    if os.path.isfile(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, mode='w', header=True, index=False)


def preprocess_data(df):
    """
    Preprocesses the DataFrame to clean and standardize the Tree_Level and Video_ID columns.
    """
    def clean_video_id(value):
        if pd.isna(value):  # Handle NaN values
            return []
        try:
            # Safely parse Video_ID values
            return ast.literal_eval(value) if isinstance(value, str) else value
        except (ValueError, SyntaxError):
            # Handle malformed Video_ID values
            print(f"Invalid Video_ID value: {value}. Replacing with empty list.")
            return []

    def clean_tree_level(value):
        if pd.isna(value):  # Handle NaN values
            print(f"Missing Tree_Level value. Skipping this row.")
            return None  # Mark as invalid
        try:
            return int(value)  # Convert to integer
        except (ValueError, TypeError):
            print(f"Invalid Tree_Level value: {value}. Skipping this row.")
            return None

    # Clean the Video_ID column
    df['Video_ID'] = df['Video_ID'].apply(clean_video_id)
    
    # Clean the Tree_Level column
    df['Tree_Level'] = df['Tree_Level'].apply(clean_tree_level)

    # Drop rows with invalid Tree_Level
    initial_row_count = df.shape[0]
    df = df.dropna(subset=['Tree_Level'])
    final_row_count = df.shape[0]
    dropped_rows = initial_row_count - final_row_count
    if dropped_rows > 0:
        print(f"Dropped {dropped_rows} rows due to invalid Tree_Level.")

    # Ensure Tree_Level is integer
    df['Tree_Level'] = df['Tree_Level'].astype(int)

    return df

def generate_tree(csv_path):
    """
    Generates a hierarchical tree structure from a CSV file.

    Parameters:
        csv_path (str): Path to the CSV file.

    Returns:
        dict: Nested dictionary representing the tree.
    """
    # Load CSV data
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
        return {}
    except pd.errors.EmptyDataError:
        print(f"No data: {csv_path} is empty.")
        return {}
    except Exception as e:
        print(f"Error reading {csv_path}: {e}")
        return {}

    # Preprocess the data
    df = preprocess_data(df)

    # Initialize an empty tree
    tree = {}

    # Iterate through each row in the DataFrame
    for _, row in df.iterrows():
        level = row['Tree_Level']
        task = row['Task']
        parent_task = row['Parent_Task']
        video_ids = row['Video_ID']  # Already cleaned
        weight = len(video_ids)  # Calculate weight

        node = {'Task': task, 'Video_ID': video_ids, 'Weight': weight, 'Children': {}}

        if level == 1:
            # Top-level node (no parent)
            tree[task] = node
        else:
            # Non-top-level node: find its parent and add to its children
            try:
                current = tree
                # Traverse the tree to the appropriate level
                for _ in range(1, level):
                    if parent_task not in current:
                        raise KeyError(f"Parent task '{parent_task}' not found for '{task}'.")
                    current = current[parent_task]['Children']
                current[task] = node
            except KeyError as e:
                print(f"Error: {e}. Skipping task '{task}'.")
                continue

    return tree

def visualize_tree(tree):
    """
    Visualizes a tree structure using networkx and matplotlib.

    Parameters:
        tree (dict): The tree data structure to visualize.

    Returns:
        None: Displays the graph.
    """
    if not tree:
        print("The tree is empty. Nothing to visualize.")
        return

    # Initialize a directed graph
    graph = nx.DiGraph()

tree = generate_tree('CleanedData/Cleaned_Data.csv')