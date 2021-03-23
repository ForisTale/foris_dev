def escape_js(string):
    escape = {'&': '\\u0026', '<': '\\u003c', '>': '\\u003e', '\u2028': '\\u2028', '\u2029': '\\u2029'}
    for unsafe, safe in escape.items():
        string = string.replace(unsafe, safe)
    return string