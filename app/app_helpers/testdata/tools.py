import json


def importJson(in_file) -> list:
    with open(in_file) as file:
        return json.load(file)
    print("Import complete.")
    

def exportJson(data, out_file):
    json_str = json.dumps(data, indent=4)
    with open(out_file, "w") as file:
        file.write(json_str)
    print("Export complete.")
