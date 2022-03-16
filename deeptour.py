import argparse
import os
import subprocess
from create_summary_tour import create_summary_tour
from create_refine_tour import create_refine_tour
from gitpy import gitpy

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def lang_input(string):
    if string == "py":
        return string
    elif string == "js":
        return string
    elif string == "java":
        return string
    elif string == "cs":
        return string
    else:
        raise OSError("Not a supported language. Choose one of python javascript java c#")


parser = argparse.ArgumentParser()
parser.add_argument('path', type=dir_path)
parser.add_argument('language', type=lang_input)
parser.add_argument('--mode', type=str, default="newest", help="One of most_imported newest oldest")
parser.add_argument('--nsteps', type=int, default=15)



args = parser.parse_args()
project_name = args.path.split('/')[-1]

data_getter = gitpy(args.path)
stats_dict = data_getter.get_function_data(args.language)


summary_tour = create_summary_tour(stats_dict, args.path, args.language, args.mode,args.nsteps)
summary_tour.create_summary_tour()

#refine_tour = create_refine_tour(stats_dict, args.path, args.mode,args.nsteps)
#refine_tour.create_refine_tour()