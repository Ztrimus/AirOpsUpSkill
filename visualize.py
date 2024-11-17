class TreeNode:
    def __init__(self, uuid, step, tree_level, id_list):
        self.uuid = uuid
        self.step = step
        self.tree_level = tree_level
        self.id_list = id_list
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

# Your provided data
data = {
    "UUID_001": {
        "TreeLevel": 0,
        "Step": "Introduction to changing oil in a Mini Cooper S",
        "IDList": ["vid_1"],
        "ChildNodeUUID": [
            "UUID_002",
            "UUID_005",
            "UUID_007",
            "UUID_008",
            "UUID_010",
            "572b6efe-afc8-4486-9da4-1f0f6cb9faca"
        ]
    },
    "UUID_002": {
        "TreeLevel": 1,
        "Step": "Gather tools: socket wrench, oil filter wrench, new oil filter, and synthetic oil",
        "IDList": ["vid_1"],
        "ChildNodeUUID": ["UUID_003"]
    },
    "UUID_003": {
        "TreeLevel": 2,
        "Step": "Jack up the car safely",
        "IDList": ["vid_1"],
        "ChildNodeUUID": ["UUID_004"]
    },
    "UUID_004": {
        "TreeLevel": 3,
        "Step": "Locate the oil drain plug",
        "IDList": ["vid_1"],
        "ChildNodeUUID": ["9cf54e02-4b36-4932-b539-8257cb7bea90"]
    },
    "UUID_005": {
        "TreeLevel": 1,
        "Step": "Unscrew the oil drain plug",
        "IDList": ["vid_1"],
        "ChildNodeUUID": [
            "UUID_006",
            "56b055a9-ef86-4c37-a1d0-93ccfafec83d"
        ]
    },
    "UUID_006": {
        "TreeLevel": 2,
        "Step": "Let old oil drain completely",
        "IDList": ["vid_1"],
        "ChildNodeUUID": []
    },
    "UUID_007": {
        "TreeLevel": 1,
        "Step": "Replace the oil filter",
        "IDList": ["vid_1"],
        "ChildNodeUUID": [
            "UUID_008",
            "dabe5f60-2b49-453d-96f7-bd19642de01c",
            "54bafedc-3683-43a3-b445-7636a8fc8f83",
            "ef260601-b686-449c-a083-15042145a024",
            "b3f8f4d9-4872-47cf-bab7-2e62349a6335",
            "bc8a6544-e1f8-4d4f-894b-c32d9a483dac"
        ]
    },
    "UUID_008": {
        "TreeLevel": 1,
        "Step": "Add fresh oil to the engine",
        "IDList": ["vid_1"],
        "ChildNodeUUID": [
            "UUID_009",
            "618115b9-d092-40e4-8d25-2800eac8b452",
            "17b7a766-9971-48c5-8062-92a489420528"
        ]
    },
    "UUID_009": {
        "TreeLevel": 2,
        "Step": "Checking the oil level",
        "IDList": ["vid_1"],
        "ChildNodeUUID": ["1a66b053-11ee-4e98-b4db-e719ed72c904"]
    },
    "UUID_010": {
        "TreeLevel": 1,
        "Step": "Check for leaks and ensure Mini is running smoothly",
        "IDList": ["vid_1"],
        "ChildNodeUUID": [
            "5f35e412-b3c3-40c5-9aad-d42027f2114b",
            "8e8ed680-354c-4e18-8474-2d7d14efb8d4",
            "ca918e67-fa00-47ba-96e8-1c98a9d55a6c"
        ]
    },
    "5f35e412-b3c3-40c5-9aad-d42027f2114b": {
        "UUID": "5f35e412-b3c3-40c5-9aad-d42027f2114b",
        "Step": "8. Check the car for any oil leaks.",
        "TreeLevel": 2,
        "IDList": ["vid_1"],
        "ChildNodeUUID": []
    },
    "8e8ed680-354c-4e18-8474-2d7d14efb8d4": {
        "UUID": "8e8ed680-354c-4e18-8474-2d7d14efb8d4",
        "Step": "9. Ensure the Mini Cooper S is running smoothly after the oil change.",
        "TreeLevel": 2,
        "IDList": ["vid_1"],
        "ChildNodeUUID": []
    },
    "56b055a9-ef86-4c37-a1d0-93ccfafec83d": {
        "UUID": "56b055a9-ef86-4c37-a1d0-93ccfafec83d",
        "Step": "2. Drain the old oil from the engine.",
        "TreeLevel": 2,
        "IDList": ["vid_2", "vid_3"],
        "ChildNodeUUID": []
    },
    "dabe5f60-2b49-453d-96f7-bd19642de01c": {
        "UUID": "dabe5f60-2b49-453d-96f7-bd19642de01c",
        "Step": "3. Replace the old oil filter with a high-performance one.",
        "TreeLevel": 2,
        "IDList": ["vid_2"],
        "ChildNodeUUID": []
    },
    "54bafedc-3683-43a3-b445-7636a8fc8f83": {
        "UUID": "54bafedc-3683-43a3-b445-7636a8fc8f83",
        "Step": "4. Clean the filter housing thoroughly.",
        "TreeLevel": 2,
        "IDList": ["vid_2"],
        "ChildNodeUUID": []
    },
    "ef260601-b686-449c-a083-15042145a024": {
        "UUID": "ef260601-b686-449c-a083-15042145a024",
        "Step": "5. Fill the engine with synthetic oil.",
        "TreeLevel": 2,
        "IDList": ["vid_2", "vid_3"],
        "ChildNodeUUID": []
    },
    "618115b9-d092-40e4-8d25-2800eac8b452": {
        "UUID": "618115b9-d092-40e4-8d25-2800eac8b452",
        "Step": "6. Understand why using the right type of oil is important for the overall health and efficiency of your car.",
        "TreeLevel": 2,
        "IDList": ["vid_2"],
        "ChildNodeUUID": []
    },
    "17b7a766-9971-48c5-8062-92a489420528": {
        "UUID": "17b7a766-9971-48c5-8062-92a489420528",
        "Step": "7. Reset the service indicator on the dashboard once the oil change is complete.",
        "TreeLevel": 2,
        "IDList": ["vid_2"],
        "ChildNodeUUID": []
    },
    "9cf54e02-4b36-4932-b539-8257cb7bea90": {
        "UUID": "9cf54e02-4b36-4932-b539-8257cb7bea90",
        "Step": "4. Inspect the condition of the drain plug before carrying onwards.",
        "TreeLevel": 4,
        "IDList": ["vid_3"],
        "ChildNodeUUID": []
    },
    "b3f8f4d9-4872-47cf-bab7-2e62349a6335": {
        "UUID": "b3f8f4d9-4872-47cf-bab7-2e62349a6335",
        "Step": "6. Prepare the new oil filter by applying a thin layer of oil for a perfect fit.",
        "TreeLevel": 2,
        "IDList": ["vid_3"],
        "ChildNodeUUID": []
    },
    "bc8a6544-e1f8-4d4f-894b-c32d9a483dac": {
        "UUID": "bc8a6544-e1f8-4d4f-894b-c32d9a483dac",
        "Step": "7. Install the new oil filter into the engine.",
        "TreeLevel": 2,
        "IDList": ["vid_3"],
        "ChildNodeUUID": []
    },
    "1a66b053-11ee-4e98-b4db-e719ed72c904": {
        "UUID": "1a66b053-11ee-4e98-b4db-e719ed72c904",
        "Step": "9. Check the oil levels using the dipstick to ensure accuracy.",
        "TreeLevel": 3,
        "IDList": ["vid_3"],
        "ChildNodeUUID": []
    },
    "572b6efe-afc8-4486-9da4-1f0f6cb9faca": {
        "UUID": "572b6efe-afc8-4486-9da4-1f0f6cb9faca",
        "Step": "10. Make sure to dispose of the old oil in an environmentally friendly manner.",
        "TreeLevel": 1,
        "IDList": ["vid_3"],
        "ChildNodeUUID": []
    },
    "ca918e67-fa00-47ba-96e8-1c98a9d55a6c": {
        "UUID": "ca918e67-fa00-47ba-96e8-1c98a9d55a6c",
        "Step": "11. Observe if vehicle is running smoothly after the oil change.",
        "TreeLevel": 2,
        "IDList": ["vid_3"],
        "ChildNodeUUID": []
    }
}

# Create a dictionary to hold TreeNode instances by UUID
nodes = {}

# First, create all TreeNode instances without establishing relationships
for uuid, attributes in data.items():
    node = TreeNode(
        uuid=uuid,
        step=attributes.get('Step', 'No Step Defined'),
        tree_level=attributes.get('TreeLevel', None),
        id_list=attributes.get('IDList', [])
    )
    nodes[uuid] = node

# Now, establish parent-child relationships
for uuid, attributes in data.items():
    parent_node = nodes[uuid]
    for child_uuid in attributes.get('ChildNodeUUID', []):
        child_node = nodes.get(child_uuid)
        if child_node:
            parent_node.add_child(child_node)
        else:
            # Handle undefined child UUIDs by creating a placeholder node
            placeholder_node = TreeNode(
                uuid=child_uuid,
                step="Undefined Step",
                tree_level=None,
                id_list=[]
            )
            nodes[child_uuid] = placeholder_node
            parent_node.add_child(placeholder_node)

# Identify the root node (TreeLevel 0)
root = None
for node in nodes.values():
    if node.tree_level == 0:
        root = node
        break

if not root:
    raise Exception("Root node not found. Ensure there is a node with TreeLevel 0.")

def print_tree(node, indent=""):
    print(f"{indent}- {node.step} (UUID: {node.uuid})")
    for child in node.children:
        print_tree(child, indent + "  ")

# Print the tree starting from the root
print("Oil Change Process Flow for Mini Cooper S:")
print_tree(root)
