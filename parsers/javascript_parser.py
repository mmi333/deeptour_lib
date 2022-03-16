import esprima

import ast
from pathlib import Path
import re
def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)

def get_js_function_data(project_path):
        function_data = {}
        for path in Path(project_path).rglob('*.js'):
            ps = str(path)
            with open(path) as sourcefile:
                sf = sourcefile.read()
                sf = remove_comments(sf)

                line_number = 0
                split_by_line = sf.split('\n')
                for num, line in enumerate(split_by_line):
                    if "function" in line:
                        line_number = num
                        function_string = re.findall("function(.*?)}", "\n".join(split_by_line[num:]))
                        print(function_string)

                #if len(function_string) > 512:
                #    continue
                #function_data[f'{node.name}'] = {"file_path": ps, "line_number": line_number, "function_string":function_string}
        return function_data
