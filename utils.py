import json


def write_tour(mode, project_path, steps_list):

        tour = {
            "$schema": "https://aka.ms/codetour-schema",
            "title": mode + " tour",
            "steps": steps_list,
            "description": mode + " tour"
        }

        open(project_path + f"/{mode}.tour", "w").write(json.dumps(tour))
        print(mode + " tour generated")