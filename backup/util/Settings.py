from collections import MutableMapping
import json, os

class Settings(MutableMapping):

    def __init__(self, filename):
        self.filename = filename
        self.store = {}
        self.read()

    def exists(self):
        return os.path.exists(self.filename)
    
    def read(self):
        if self.exists():
            with open(self.filename, 'r') as f:
                self.store = json.load(f)
        else:
            self.write()

    def write(self):
        with open(self.filename, 'w') as f:
            json.dump(self.store, f, sort_keys=True, indent=2, separators=(',', ': '))

    def __setitem__(self, key, value):
        self.store[key] = value
        self.write()

    def __delitem__(self, key):
        del self.store[key]
        self.write()

    def __getitem__(self, key):
        return self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)
