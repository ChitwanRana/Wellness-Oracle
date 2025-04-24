import json
import os

json_path = os.path.join(os.path.dirname(__file__), "disease_info.json")

with open(json_path, "r") as f:
    disease_data = json.load(f)
