import json


def convert_value_post(request):
    table_input = request.POST.get("table_input")
    if table_input is None:
        return {}
    parsed_input = json.loads(table_input)
    converted = convert_value_input(parsed_input)
    return converted


def convert_value_input(parsed_input):
    converted = {}
    for item in parsed_input:
        if item.get("value") == "":
            continue
        command = {item.get("name"): item.get("value")}
        converted.update(command)
    return converted