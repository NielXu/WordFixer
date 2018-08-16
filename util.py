import re
import os


def find(root, fname=None, suffix=None):
    """
    Recursivly find all files that matched from the root directory.
    Param: fname=None: List like object, only the files in the
            given filenames list will be checked. If None, all
            files will match
    Param: suffix=None: List like object, only the files with
            the given suffix(extension) will be checked. If None,
            all files will match. The suffix should be in format
            like .py, .txt or so on
    """
    def _find(dir, l):
        if os.path.isfile(dir):
            l.append(dir)
        else:
            dirs = os.listdir(dir)
            for d in dirs:
                _find(dir+"\\"+d, l)
    def _infname(f, fname):
        if fname is None:
            return True
        return f in fname
    def _insuffix(s, suffix):
        if suffix is None:
            return True
        return s in suffix
    found = []
    files = []
    _find(root, found)
    for f in found:
        n, s = os.path.splitext(os.path.basename(f))
        if _infname(n, fname) and _insuffix(s, suffix):
            files.append(f)
    return files


def find_comment_py(file_dir):
    """
    Find comments in .py file. There are four kinds of comments:
    0. lines that start with #
    1. lines that start with "
    2. lines that start with '
    3. comment blocks
    Return: list of comments
    """
    def _find_in_list(p, l):
        "Find str that starts with the given pattern, return index"
        index = 0
        while index < len(l):
            e = l[index].strip()
            if e.startswith(p):
                return index
            index += 1
    comments = []
    with open(file_dir) as f:
        content = f.readlines()
    lines = [x.strip().replace("\n", "") for x in content]
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("\'\'\'"):
            next_index = index + _find_in_list("\'\'\'", lines[index+1:]) + 2
            find = "\n".join(lines[index:next_index])
            comments.append(find.replace("\'\'\'", ""))
            index = next_index - 1
        if line.startswith("\"\"\""):
            next_index = index + _find_in_list("\"\"\"", lines[index+1:]) + 2
            find = "\n".join(lines[index:next_index])
            comments.append(find.replace("\"\"\"", ""))
            index = next_index - 1
        elif line.startswith("\'"):
            comments.append(line.replace("\'", ""))
        elif line.startswith("\""):
            comments.append(line.replace("\"", ""))
        elif line.startswith("#"):
            comments.append(line.replace("#", ""))
        index += 1
    return comments


def trim(s):
    """
    Remove whitespaces in str and leave only letters
    For instance: trim('examp?le!') -> 'example'
    """
    return "".join(c for c in s if c.isalpha())


def words(s):
    """
    Get all the words from a str, to lowercase
    """
    return re.findall(r'\w+', s.lower())
