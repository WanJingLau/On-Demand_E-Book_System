#check & replace to 2 single quote
def check_single_quote(string):
    if string.find("'") != -1:
        return string.replace("'", "''")
    else:
        return string
#check & replace spacing with _
def check_spacing(string):
    if string.find(" ") != -1:
        return string.replace(" ", "_")
    else:
        return string
#check & remove ?
def check_question_mark(string):
    if string.find("?") != -1:
        return string.replace("?", "")
    else:
        return string

def check_front_end_space(string):
    newstring = string.lstrip()
    return newstring.rstrip()