import ast
import astunparse 
from pathlib import Path
from collections import namedtuple
from collections import OrderedDict

def get_py_function_data(project_path):
        function_data = {}
        for path in Path(project_path).rglob('*.py'):
            ps = str(path)
            with open(path) as sourcefile:
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


                        line_number = 0
                        for num, line in enumerate(sf.split('\n')):
                            if "def" in line and node.name in line:
                                line_number = num

                        function_string = astunparse.unparse(node)
                        if len(function_string) > 512:
                           continue
                        function_data[f'{node.name}'] = {"file_path": ps, "line_number": line_number, "function_string":function_string}
        return function_data



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


def get_import_stats(project_path):
    most_imported_modules = {}
    most_imported_files = {}
    most_imported_functions = {}

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
                        most_imported_functions[func] = 1
                    else:
                        most_imported_functions[func] += 1

    most_imported_files = list(OrderedDict(sorted(most_imported_files.items(), key=lambda item: item[1], reverse=True)).keys())
    most_imported_functions = list(OrderedDict(sorted(most_imported_functions.items(), key=lambda item: item[1], reverse=True)).keys())
    most_imported_modules = list(OrderedDict(sorted(most_imported_modules.items(), key=lambda item: item[1], reverse=True)).keys())

    return most_imported_modules, most_imported_files, most_imported_functions
