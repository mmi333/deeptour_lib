"""
The oldest functions are as old as the program itself.

If an old function still survives, it's likely an integral part of the program.

Let's summarize it!

"""


import json
from collections import namedtuple
from models.huggingface_summary_model import huggingface_summary_model
import torch
import gc
import utils
from collections import OrderedDict
from datetime import datetime
class create_summary_tour:
    def __init__(self, stats_dict, project_path, lang, mode, nsteps, import_info):
        self.stats_dict = stats_dict
        self.project_path = project_path
        self.lang = lang
        self.mode = mode
        self.nsteps = nsteps
        self.import_info = import_info


    def create_summary_tour(self):
        if self.import_info != []:
            most_imported_modules= self.import_info[0]
            most_imported_files = self.import_info[1]
            most_imported_functions = self.import_info[2]
        function_data = self.stats_dict

        summarized_count = 0
        filecount = {}

        steps_list = []
        if self.lang == 'py':
            steps_list.append({"description": "Welcome to the summary tour!\n\nThese are the most imported modules:\n\n" + "\n\n".join(most_imported_modules[:10])})
        model = huggingface_summary_model(self.lang)

        if self.mode == "newest":
           function_data = OrderedDict(sorted(function_data.items(), key=lambda item: datetime.strptime(item[1]['function_date'], "%a, %d %b %Y %H:%M"), reverse=True))
        if self.mode == "oldest":
           function_data = OrderedDict(sorted(function_data.items(), key=lambda item: datetime.strptime(item[1]['function_date'], "%a, %d %b %Y %H:%M")))

        for function_name, data in function_data.items():
            step = {}

            file_path, line_number, function_date = data['file_path'], data['line_number'], data['function_date']
            if file_path not in filecount.keys():
                filecount[file_path] = 0
            else:
                if filecount[file_path] == 1:
                    continue
                filecount[file_path] += 1

            description = model.predict(data['function_string'])

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

        utils.write_tour("summary", self.project_path, steps_list)