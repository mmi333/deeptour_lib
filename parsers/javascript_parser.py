import esprima

import subprocess
from pathlib import Path
import re
import json
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
import json

def get_json(obj):
  return json.loads(
    json.dumps(obj, default=lambda o: getattr(o, '__dict__', str(o)))
  )

def get_js_function_data(project_path):
    cnt = 0
    function_data = {}
    for path in Path(project_path).rglob('*.js'):
        ps = str(path)
        function_name = ''
        function_string = ''
        if "node_modules" in ps or "eslint" in ps or "libraries" in ps or "docs" in ps:
            continue
        with open(path) as sourcefile:
            sf = sourcefile.read()
            line_num = 0
            sf = remove_comments(sf)
            try:
                    parser = esprima.parseScript(sf)
            except:
                    continue
            for node in parser.body:
                if node.type == "FunctionDeclaration":
                    with open('parsers/jsast.json', 'w', encoding='utf-8') as f:
                        json.dump(get_json(node), f, ensure_ascii=False, indent=4)

                    p = subprocess.Popen(['node', 'parsers/javascript_parser.js'], stdout=subprocess.PIPE)
                    out = p.stdout.read()
                    function_string = out.decode().replace("\n", "")
                    function_name = function_string.split(" ")[1]
                    for line_number, line in enumerate(sf.split('\n')):
                        if function_name in line :
                            line_num = line_number

                    function_name = function_name[:function_name.find('(')]

                    if len(function_string) > 512:
                        continue
                    function_data[f'{function_name}'] = {"file_path": ps, "line_number": line_num, "function_string":function_string}
    return function_data
