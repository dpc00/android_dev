'''
Created on Jul 28, 2016

@author: libraryuser
'''

class FileCmp(dict):
    def __init__(self, run, f2):
        super(FileCmp, self).__init__()
        self['file1'] = run
        self['file2'] = f2

    def __missing__(self, key):
        if key == 'match':
            self.scan()
            return self[key]
        else:
            return None

    def scan(self):
        run = self['file1']
        f2 = self['file2']
        self['match'] = True
        if run['mtime'] != f2['mtime']:
            self['match'] = False
        elif run['size'] != f2['size']:
            self['match'] = False
