"""
The oldest functions are as old as the program itself.

If an old function still survives, it's likely an integral part of the program.

Let's summarize it!

"""


import json
from collections import namedtuple
from models.huggingface_java_to_cs_model import huggingface_java_to_cs_model

import torch
import gc
import utils
from collections import OrderedDict
from datetime import datetime

class create_java_to_cs_tour:
    def __init__(self, stats_dict, project_path, lang, mode, nsteps):
        self.stats_dict = stats_dict
        self.project_path = project_path
        self.lang = lang
        self.mode = mode
        self.nsteps = nsteps




    def create_java_to_cs_tour(self):
        if self.lang != "java":
            return

        function_data = self.stats_dict

        predicted_count = 0
        filecount = {}
        
        steps_list = []

        java_to_cs_model = huggingface_java_to_cs_model()


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


            function_string = data['function_string']

            translated = java_to_cs_model.predict(function_string)
            translated = translated.replace(";", ";\n\n")
            translated = translated.replace("{", "{\n\n")

            step["file"] = file_path.replace(self.project_path + "/", "")
            step["description"] = translated + "\n\n First created on :" + function_date
            step["line"] = int(line_number)
            steps_list.append(step)

            predicted_count += 1
            if predicted_count > self.nsteps:
                break

        del java_to_cs_model

        gc.collect()
        torch.cuda.empty_cache()

        utils.write_tour("java_to_cs", self.project_path, steps_list)