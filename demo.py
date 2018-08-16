# Setup directory
import os
dir = os.getcwd() + "\\resources\\"


import fixer
# Try to correct a wrong word using fixer.correct()
print(fixer.correct("corect"))      # Ouput: correct
print(fixer.correct("incoerrct"))   # Output: incorrect

# Get words that probably the right one
print(fixer.candidates("corect"))        # Output: correct
print(fixer.candidates("incoerrct"))     # Output: incorrect

# Fix a string, results print on console
fixer.fix("Thsi is a sentnce taht full of mistakes")

# Initialize new fixer
# rt1.txt and rt2.txt are files that contain some random texts for testing
# Some words are spelled incorrectly in order to test the fixer
f = fixer.Fixer(dir,                    # The root dir
                recursive=True,         # Recursively check all the files
                fname=["rt1", "rt2"])   # Only certain files will be checked
# Start fixing files, results print on console
f.fix()


import util
# print all files under resources folder
print(util.find(dir))
# print files with given filenames
print(util.find(dir, fname=["rt1"]))
# print files with given extensions
print(util.find(dir, suffix=[".txt"]))

print(util.trim("exam?ple!"))    # output: example
print(util.words("Separate words from sentence"))
# Output: ['separate', 'words', 'from', 'sentence']

# Find all the comments in a py file, here use corrector.py as an example
examplepy = util.find(dir, fname=["corrector"])[0]
print(util.find_comment_py(examplepy))
