import pandas as pd
import os
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
    df = pd.DataFrame(data, columns=['Tree_Level', 'Task', 'Video_ID'])
    if os.path.isfile(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, mode='w', header=True, index=False)

def generate_graph(csv_path):
    df = pd.read_csv(csv_path)
    grouped = df.groupby(['Tree_Level', 'Task']).agg(
        Video_ID=('Video_ID', list),
        Weight=('Video_ID', 'count')
    ).to_dict(orient='index')
    return grouped