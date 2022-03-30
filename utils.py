import json
import os

def write_tour(mode, project_path, steps_list):
    if not os.path.exists(project_path + "/.tours"):
        os.mkdir(project_path + "/.tours")
    
    tour = {
        "$schema": "https://aka.ms/codetour-schema",
        "title": mode + " tour",
        "steps": steps_list,
        "description": mode + " tour"
    }

    open(project_path + f"/.tours/{mode}.tour", "w").write(json.dumps(tour))
    print(mode + " tour generated")