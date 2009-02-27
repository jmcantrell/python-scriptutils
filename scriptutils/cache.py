import os.path, pickle

class Cache(object):

    def __init__(self, directory):
        self.directory = directory
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)

    def __delitem__(self, key):
        os.remove(self._get_filename(key))

    def __getitem__(self, key):
        filename = self._get_filename(key)
        if os.path.isfile(filename):
            return pickle.load(open(filename, 'rb'))
        return None

    def __setitem__(self, key, value):
        pickle.dump(value, open(self._get_filename(key), 'wb'))

    def _get_filename(self, key):
        return os.path.join(self.directory, '%s.pkl' % key)

