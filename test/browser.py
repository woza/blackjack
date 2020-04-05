# Test stub for browser module
import json
import os.path
import sys

class folder:
    def __init__(self, path):
        with open('test.input.0') as src:
            file_system = json.load(src)

        logger = open('/tmp/browser.log', 'w')
        logger.write(str(file_system)+"\n")
        self.path = path
        logger.write("PATH '%s'\n" % path)
        bits = [x for x in self.path.split('/') if len(x) >0]
        logger.write("BITS " + str(bits)+"\n")
        self.contents = file_system['/']
        for b in bits:
            logger.write("B " + str(b)+"\n")
            self.contents = self.contents[b]
        logger.write("CONTENTS " + str(self.contents)+"\n")
            
    def fetch_contents(self):
        return self.contents

    def subfolders(self):
        return []

    def file_names(self):
        return self.contents
    
