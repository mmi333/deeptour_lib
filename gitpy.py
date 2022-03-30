from git import Repo
import time
import ast
import os
from parsers import python_parser
from parsers import javascript_parser 
from parsers import java_parser 

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

    def argmax(self, iterable):
        return max(enumerate(iterable), key=lambda x: x[1])[0]

    def get_function_data(self):



        py_function_data = python_parser.get_py_function_data(self.path)
        js_function_data = javascript_parser.get_js_function_data(self.path)
        java_function_data = java_parser.get_java_function_data(self.path)
        function_data_list = [py_function_data, js_function_data, java_function_data]
        function_data_list_ind = self.argmax([len(x) for x in function_data_list])
        lang = ["py", "js", "java"][function_data_list_ind]
        function_data = function_data_list[function_data_list_ind]
        print("Detected language: " + lang)


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
        return function_data, lang


    def get_import_stats(self, lang):
        if lang == "py":
            most_imported_modules, most_imported_files, most_imported_functions = python_parser.get_import_stats(self.path)
        return most_imported_modules, most_imported_files, most_imported_functions