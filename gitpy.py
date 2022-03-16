from git import Repo
import time
import ast
import os
from parsers import python_parser
from parsers.javascript_parser import get_js_function_data

import pickle


class gitpy:

    def __init__(self, path):
        self.path = path
        self.repo = Repo(path)
        assert not self.repo.bare


    def get_dates_by_line(self, filepath):

        lines_and_dates = []
        for commit, lines in self.repo.blame('HEAD', filepath):
            for line in lines:
                time.asctime(time.gmtime(commit.committed_date))
                date = time.strftime("%a, %d %b %Y %H:%M", time.gmtime(commit.committed_date))
                lines_and_dates.append(date)

        return lines_and_dates

    def get_function_data(self, lang):

        if os.path.exists(self.path.split('/')[-1] + ".pkl"):
            function_data = pickle.loads(self.path.split('/')[-1] + ".pkl")
            return function_data


        if lang == "py":
            function_data = python_parser.get_py_function_data(self.path)
        if lang == "js":
            raise NotImplementedError("Not yet...")
        if lang == "java":
            raise NotImplementedError("Not yet...")
        if lang == "cs":
            raise NotImplementedError("Not yet...")

        file_function = {}
        for function, data in function_data.items():
            if data['file_path'] not in file_function.keys():
                file_function[data['file_path']] = [function]
                continue
            file_function[data['file_path']].append(function)

        for file, function_list in file_function.items():
            lines_and_dates = self.get_dates_by_line(file)
            for function in function_list:
                data = function_data[function]
                data["function_date"] = lines_and_dates[int(data["line_number"])]
            
        pickle.dumps(self.path.split('/')[-1] + ".pkl")
        return function_data


def get_import_stats(self, lang):
    if lang == "py":
        most_imported_modules, most_imported_files, most_imported_functions = python_parser.get_import_stats(self.path)
    return most_imported_modules, most_imported_files, most_imported_functions