#!/usr/bin/python

import subprocess
import os

from redis_search import ScoredIndexSearch

class StringsGenerator(object):

    def __init__(self, directory):
        self.index = ScoredIndexSearch()
        self.directory = directory


    def strings(self, f):
        strings = ''
        nul_f = open(os.devnull, 'w')
        p = subprocess.Popen(["/usr/bin/strings" , f], stdout=subprocess.PIPE,\
                stderr = nul_f)
        for s in p.stdout:
            strings += s + " "
        nul_f.close()
        return f, strings

    def dir_strings(self):
        for r,d,files in os.walk(self.directory):
            for f in files:
                file_name, strings = self.strings(os.path.join(r,f))
                self.index.add_indexed_item(file_name, strings)

    def search(self, string):
        return self.index.search(string)



if __name__ == '__main__':
    directory = "/path/to/your/dir"
    sg = StringsGenerator(directory)
    response = raw_input("Generate database? (y/N) ")
    if response == 'y':
        sg.dir_strings()
        print("Db generated.")
    print("Search in the database using sg.search('query')")
