import os
def find_path(filename, search_path):
    result = ''
    for root, dir, files in os.walk(search_path):
        if filename in files:
            result = os.path.join(root, filename)
    return result