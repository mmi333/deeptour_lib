"""
The oldest functions are as old as the program itself.

If an old function still survives, it's likely an integral part of the program.

Let's summarize it!

"""


import json
from collections import namedtuple
from models.huggingface_refine_model import huggingface_refine_model
from models.huggingface_defect_model import huggingface_defect_model

import torch
import gc
import utils
from collections import OrderedDict
from datetime import datetime

class create_refine_if_defect_tour:
    def __init__(self, stats_dict, project_path, lang, mode, nsteps):
        self.stats_dict = stats_dict
        self.project_path = project_path
        self.lang = lang
        self.mode = mode
        self.nsteps = nsteps




    def create_refine_if_defect_tour(self):
        if self.lang != "java":
            return


        function_data = self.stats_dict

        predicted_count = 0
        filecount = {}
        
        steps_list = []

        defect_model = huggingface_defect_model()

        refine_model = huggingface_refine_model(self.lang)

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

            defective = defect_model.predict(function_string)
            if not defective:
                continue
            refined = refine_model.predict(function_string)
            refined = refined.replace(";", ";\n\n")
            refined = refined.replace("{", "{\n\n")

            step["file"] = file_path.replace(self.project_path + "/", "")
            step["description"] = refined + "\n\n First created on :" + function_date
            step["line"] = int(line_number)
            steps_list.append(step)

            predicted_count += 1
            if predicted_count > self.nsteps:
                break

        del defect_model
        del refine_model

        gc.collect()
        torch.cuda.empty_cache()

        utils.write_tour("refine", self.project_path, steps_list)