import json
from collections import namedtuple
from models.huggingface_insecure_code_model import huggingface_insecure_code_model
import torch
import gc
import utils

class create_insecure_code_tour:
    def __init__(self, stats_dict, project_path, mode, nsteps):
        self.stats_dict = stats_dict
        self.project_path = project_path
        self.mode = mode
        self.nsteps = nsteps




    def create_insecure_code_tour(self):
        most_imported_modules= self.stats_dict['modules']
        most_imported_files = self.stats_dict['files'] 
        most_imported_functions = self.stats_dict['most_imported_functions']
        function_and_date = self.stats_dict['function_and_date']

        function_data = self.stats_dict['function_data']

        summarized_count = 0
        filecount = {}

        steps_list = []
        steps_list.append({"description": "These are the most imported modules:\n" + "\n".join(most_imported_modules)})
        model = huggingface_insecure_code_model()

        if self.mode == "most_imported":
            list_to_loop_in = most_imported_functions
        if self.mode == "newest":
            list_to_loop_in = function_and_date
        if self.mode == "oldest":
            list_to_loop_in = function_and_date[::-1]


        for function_name in list_to_loop_in:
            step = {}

            if function_name not in function_data.keys():
                continue
            file_path, line_number, function_date = function_data[function_name].split('\n')[:3]
            if file_path not in filecount.keys():
                filecount[file_path] = 0
            else:
                if filecount[file_path] == 1:
                    continue
                filecount[file_path] += 1

            description = model.predict('\n'.join(function_data[function_name].split('\n')[3:]))

            step["file"] = file_path.replace(self.project_path + "/", "")
            step["description"] = description + "\n\n First created on :" + function_date
            step["line"] = int(line_number)
            steps_list.append(step)

            summarized_count += 1
            if summarized_count > self.nsteps:
                break

        del model
        gc.collect()
        torch.cuda.empty_cache()

        utils.write_tour("insecure_code", self.project_path, steps_list)