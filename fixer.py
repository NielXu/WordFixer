import os
import json
import util
from collections import Counter


# ==================== Classes ====================
class Fixer():
    """
    A useful tool that can do spell check with files.
    """
    def __init__(self,
                root,
                recursive=False,
                fname=None,
                suffix=None):
        """
        Param: root: The root directory that the Fixer will start
                checking
        Param: recursive=True: Recursivly check all the files under the
                given root directory
        Param: fname=None: List like object, only the files in the
                given filenames list will be checked. If None, all
                files will be check
        Param: suffix=None: List like object, only the files with
                the given suffix(extension) will be checked. If None,
                all files will be check. The suffix should be in format
                like .py, .txt or so on
        """
        self.root = root
        self.recursive = recursive
        self.fname = fname
        self.suffix = suffix

    def fix(self,
            replace=False,
            suggest=True):
        """
        Start fixing the files
        Param: repalce=False: Replace the wrong spelling to the
                correct spelling. It is not recommend to use this
                feature since it will modify the files directly. Unless you
                trust the spell checker completely. And also, the fixer
                is not case sensitive.
        Param: suggest=True: Show the wrong spelling on console
                and also the suggested correct spelling
        """
        files = self._scan()
        for file in files:
            self.current_file = file
            lines = self._lines(file)
            if suggest:
                print("====================",file,"====================")
            for line_index in range(0, len(lines)):
                words = util.words(lines[line_index])
                for w in words:
                    if not is_word(w):
                        if suggest:
                            print("wrong:", w, \
                                 "\t@line:", line_index+1, \
                                 "\tsuggest:", correct(w), \
                                 "\tsuggest list:", candidates(w, 5))
            if suggest:
                print("done")

    def _scan(self):
        """
        Scanning files under the given root directory.
        Return: list of filenames
        """
        files = []
        if self.recursive:
            files = util.find(self.root, self.fname, self.suffix)
        else:
            for f in os.listdir(self.root):
                full = os.path.join(self.root, f)
                if os.path.isfile(full):
                    fname, suffix = os.path.splitext(f)
                    if self._in_suffix(suffix) and self._in_fname(fname):
                        files.append(full)
        return files

    def _lines(self, file):
        "Return list that represents every line in the file"
        words = []
        with open(file) as f:
            return f.readlines()

    def _in_suffix(self, suffix):
        "Return True if the suffix is on the list"
        if self.suffix is None:
            return True
        return suffix in self.suffix

    def _in_fname(self, fname):
        "Return True if the file name is on the list"
        if self.fname is None:
            return True
        return fname in self.fname


# ==================== Variables ====================
words_dict = None
counter = None


# ==================== Methods ====================
def is_word(word):
    """
    Check if a single word is a valid English word or not. It does not
    matter if the word is in uppercase or lowercase. However, there
    should be no symbols in the word or it will always return False
    Param: word: The word that will be checked
    Return: True if it is a valid English word, False otherwise
    """
    global words_dict
    if words_dict is None:
        with open("resources/words.json") as f:
            words_dict = json.load(f)
    return word.lower() in words_dict

def rawspell_dist1(word):
    """
    Get a set of words that are one edit distance away from the original
    word. It includes all possible combinations no matteer if the spelling
    is correct or not.
    Param: word: The original word
    Return: A set of words that are one edit distance away from the original
            word
    """
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]   for L, R in splits if R for c in letters]
    inserts    = [L + c + R       for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def rawspell_dist2(word):
    """
    Get a set of words that are two edit distance away from the original
    word. It includes all possible combinations no matteer if the spelling
    is correct or not.
    Param: word: The original word
    Return: A set of words that are two edit distance away from the original
            word
    """
    return set(e2 for e1 in rawspell_dist1(word) \
            for e2 in rawspell_dist1(e1))

def spell_dist1(word):
    """
    Get a set of valid English words that are one edit distance away from
    the original word. Valid English words mean the words that are
    correctly spelling and in the English dictionary
    Param: word: The original word
    Return: A set of words that are one edit distance away from the original
            word
    """
    return set(w for w in rawspell_dist1(word) if is_word(w))

def spell_dist2(word):
    """
    Get a set of valid English words that are two edit distance away from
    the original word. Valid English words mean the words that are
    correctly spelling and in the English dictionary
    Param: word: The original word
    Return: A set of words that are two edit distance away from the original
            word
    """
    return set(w for w in rawspell_dist2(word) if is_word(w))

def P(word):
    """
    Get the probability of word. The probability is related to the frequency
    of the words we use in our daily life.
    """
    global counter
    if counter is None:
        counter = Counter(util.words(open("resources/big.txt").read()))
    return counter[word] / sum(counter.values())

def correct(word):
    """
    Get the most possible correct spelling word according to the given word.
    If the given word is correct, return the original word
    """
    if is_word(word.lower()):
        return word
    c = candidates(word)
    return None if len(c) == 0 else c[0]

def candidates(word, n=None):
    """
    Get the candidates of the word. Candidates mean a list of words that are
    most possible to be the correct spelling.
    Param: word: The word
    Param: n=None: Up to how many words in the list
    Return: A list of possible words, from most possible to least possible
    """
    word = word.lower()
    return sorted((set() or spell_dist1(word) or spell_dist2(word) or [word]),
                    key=P,
                    reverse=True)[:n]

def fix(text):
    """
    Fix the text, check all words and detect if there is any wrong spelling,
    then display on console. This function is different from Fixer.fix()
    since this function workds with text but not files
    """
    words = util.words(text)
    for word in words:
        if not is_word(word):
            print("Wrong:", word,\
                "\tsuggest:", correct(word),\
                "\tsuggest list:", candidates(word, 5))
