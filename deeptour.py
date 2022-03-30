import argparse
import os
import subprocess
from create_summary_tour import create_summary_tour
from create_refine_if_defect_tour import create_refine_if_defect_tour
from create_java_to_cs_tour import create_java_to_cs_tour
from gitpy import gitpy

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


parser = argparse.ArgumentParser()
parser.add_argument('path', type=dir_path)
parser.add_argument('--mode', type=str, default="newest", help="One of newest oldest")
parser.add_argument('--nsteps', type=int, default=15)



args = parser.parse_args()
project_name = args.path.split('/')[-1]

data_getter = gitpy(args.path)
stats_dict, lang = data_getter.get_function_data()

import_info = []
if lang == 'py':
    most_imported_modules, most_imported_files, most_imported_functions = data_getter.get_import_stats(lang)
    import_info = [most_imported_modules, most_imported_files, most_imported_functions]



summary_tour = create_summary_tour(stats_dict, args.path, lang, args.mode,args.nsteps, import_info)
summary_tour.create_summary_tour()


refine_if_defect_tour = create_refine_if_defect_tour(stats_dict, args.path, lang, args.mode,args.nsteps)
refine_if_defect_tour.create_refine_if_defect_tour()

java_to_cs_tour = create_java_to_cs_tour(stats_dict, args.path, lang, args.mode,args.nsteps)
java_to_cs_tour.create_java_to_cs_tour()
