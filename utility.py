def convert_string_to_dict(txt):
    if txt.find(',') != -1:
        splitter = ','
    else:
        splitter = ' '
    return eval("dict(%s)" % ','.join(txt.split(splitter)))

