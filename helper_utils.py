import json

def load_json_to_dict(path):
    with open(path, "r") as read_file:
        data = json.load(read_file)
        return data