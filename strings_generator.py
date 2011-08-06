#!/usr/bin/python

import subprocess
import os

from redis_search import ScoredIndexSearch

strings_command = "/usr/bin/strings"

class StringsGenerator(object):

    def __init__(self, directory):
        self.index = ScoredIndexSearch()
        self.directory = directory

    def strings(self, f):
        strings = ''
        nul_f = open(os.devnull, 'w')
        p = subprocess.Popen([strings_command, f], stdout=subprocess.PIPE, stderr = nul_f)
        for s in p.stdout:
            strings += s + " "
        nul_f.close()
        self.index.add_indexed_item(f, strings)

    def dir_strings(self):
        for r,d,files in os.walk(self.directory):
            for f in files:
                print f
                self.strings(os.path.join(r,f))

    def search(self, string):
        return self.index.search(string)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        sys.exit("Directory needed.")
    sg = StringsGenerator(sys.argv[1])
    response = raw_input("Generate database? (y/N) ")
    if response == 'y':
        sg.dir_strings()
        print("Database generated.")
    else:
        print("We assume that the database has already been generated.")
    print("Search in the database using sg.search('query')")
