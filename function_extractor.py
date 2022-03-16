import re
import os
from datetime import datetime
import ast
from collections import namedtuple
from pathlib import Path
import collections
import esprima

def get_functions_by_date(blame_string, lang):
    regex_string = {"py" : ['def'], "js": ["function", "=>"], "java": "", "cs": ""}
    functions_sorted_by_date = {}

    for line in blame_string.split('\n'):
        pm = re.findall(regex_string[lang] + " (.*?)\(", line)
        if pm != []:
            date = re.findall('(\d+[-/]\d+[-/]\d+)', line)[0]
            
            if pm[0].strip() == '':
                continue
            functions_sorted_by_date[pm[0].strip()] = datetime.strptime(date, '%Y-%m-%d')
    functions_sorted_by_date = collections.OrderedDict(sorted(functions_sorted_by_date.items(), key=lambda p: p[1], reverse=True))
    return functions_sorted_by_date

def get_imports(path):
    Import = namedtuple("Import", ["module", "name", "alias"])
    module = []
    with open(path) as fh:        
        root = ast.parse(fh.read(), path)

        for node in ast.iter_child_nodes(root):
            if isinstance(node, ast.Import):
                module = []
            elif isinstance(node, ast.ImportFrom):  
                try:
                    module = node.module.split('.')
                except:
                    pass
            else:
                continue

            for n in node.names:
                yield Import(module, n.name.split('.'), n.asname)


def get_function_stats(blame_string, project_path):
    functions_sorted_by_date = get_functions_by_date(blame_string)

    most_imported_modules = {}
    most_imported_files = {}
    most_imported_functions = {}
    function_and_file = {}

    project_name = project_path.split('/')[-1]

    for path in Path(project_path).rglob('*.py'):
        ps = str(path)
        with open(path) as sourcefile:
            sf = sourcefile.read()
            gi = get_imports(path)
            
            if gi == None:
                continue
            for imp in gi: 
                module_list = getattr(imp, 'module')
                if project_name in module_list:
                    for i in module_list[:-1]:
                        if i not in most_imported_modules.keys():
                            most_imported_modules[i] = 1
                        else:
                            most_imported_modules[i] += 1

                    file_path = project_path + "/" + "/".join(module_list)


                    if file_path not in most_imported_files.keys():
                        most_imported_files[file_path] = 1
                    else:
                        most_imported_files[file_path] += 1



                    func = getattr(imp, 'name')[0]
                    if func not in most_imported_functions.keys():
                        function_and_file[func] = file_path
                        most_imported_functions[func] = 1
                    else:
                        most_imported_functions[func] += 1

    most_imported_files = list(collections.OrderedDict(sorted(most_imported_files.items(), key=lambda item: item[1], reverse=True)).keys())
    most_imported_functions = list(collections.OrderedDict(sorted(most_imported_functions.items(), key=lambda item: item[1], reverse=True)).keys())
    most_imported_modules = list(collections.OrderedDict(sorted(most_imported_modules.items(), key=lambda item: item[1], reverse=True)).keys())

    return most_imported_files, most_imported_functions, most_imported_modules


def get_function_data(most_imported_functions, function_and_file, functions_sorted_by_date):
        function_data = {}
        for function, file_path in function_and_file.items():
            if not os.path.exists(file_path + ".py"):
                continue
            with open(file_path + ".py") as sourcefile:
                sf = sourcefile.read()

                tree = ast.parse(sf)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if not len(node.body):
                            continue

                        if not isinstance(node.body[0], ast.Expr):
                            continue

                        if not hasattr(node.body[0], 'value') or not isinstance(node.body[0].value, ast.Str):
                            continue
                        node.body = node.body[1:]


                        if node.name in most_imported_functions:
                            line_number = 0
                            for num, line in enumerate(sf.split('\n')):
                                if "def" in line and node.name in line:
                                    line_number = num

                            function_string = ast.unparse(node)
                            if len(function_string) > 512:
                                continue
                            function_date = str(functions_sorted_by_date[node.name]).split()[0]
                            function_data[f'{node.name}'] = f'{file_path}.py\n{line_number}\n{function_date}\n{function_string}'
        return function_data




