def escape_html(string):
    escape = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '\'': '&#39;', '\"': '&quot;'}
    for unsafe, safe in escape.items():
        string = string.replace(unsafe, safe)
    return string