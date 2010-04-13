import os, pickle

class Cache(object):

    def __init__(self, directory, **kwargs):
        self.data = dict(**kwargs)
        self.directory = directory

    def __contains__(self, key):
        if key in self.data:
            return True
        if os.path.isfile(self._filename(key)):
            return True
        return False

    def __delitem__(self, key):
        if key in self.data:
            del(self.data[key])
        fn = self._filename(key)
        if os.path.isfile(fn):
            os.remove(fn)

    def __getitem__(self, key):
        if key not in self.data:
            fn = self._filename(key)
            if os.path.isfile(fn):
                self.data[key] = pickle.load(open(fn, 'rb'))
            else:
                self.data[key] = None
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def _filename(self, key):
        return os.path.join(self.directory, '%s.pkl' % key)

    def get(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    def set(self, key, value):
        self[key] = value

    def dump(self):
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)
        for key, value in self.data.items():
            pickle.dump(value, open(self._filename(key), 'wb'))
