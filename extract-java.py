import json
import os
from tree_sitter import Language, Parser


java_language = Language('./build/my-languages.so', 'java')


java_parser = Parser()
java_parser.set_language(java_language)


exclude_function_names = {
    "main", "toString", "write", "get", "accept", "create", "dispose", "run", "add", 
    "_init", "getValue", "update", "setUp", "getName", "setName", "load", 
    "clear", "read", "init", "setValue", "parse", "equals", "getOffset", "getWidth", "execute", "getData",
    "clone","setId","getValues","getMessage","getDescription","getPath","setPrice","start","close"
}
exclude_function_names = {name.lower() for name in exclude_function_names}

def get_functions(code, parser, language):
    code_bytes = bytes(code, "utf8")
    tree = parser.parse(code_bytes)
    query = language.query("""(method_declaration) @method""")
    
    functions = []
    for node, _ in query.captures(tree.root_node):
        name_node = node.child_by_field_name('name')
        func_name = name_node.text.decode('utf8') if name_node else ''
        
        if func_name.lower().startswith(("get", "set")):
            continue
        if func_name.lower() in exclude_function_names:
            continue
        
        start_byte = node.start_byte
        end_byte = node.end_byte
        func_code = code_bytes[start_byte:end_byte].decode('utf8')
        
        if func_code.count("\n") + 1 < 10:
            functions.append((func_name, func_code))
    
    return functions



os.makedirs("./java", exist_ok=True)
output_path = "./java/java_function.jsonl"


sample_limit = 3000
sample_count = 0
with open("java.jsonl", "r", encoding="utf-8") as infile, \
     open(output_path, "w", encoding="utf-8") as outfile:
    
    for line in infile:
        if sample_count >= sample_limit:
            break
        
        data = json.loads(line)
        java_code = data.get("content")
        if not java_code:
            continue
        
        functions = get_functions(java_code, java_parser, java_language)
        for func_name, func_code in functions:
            entry = {
                "function_name": func_name,
                "code": func_code
            }
            outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")
        
        sample_count += 1

print("extract 3000 sample to java_function.jsonl")
