import os, os.path, csv
from StringIO import StringIO
from unicodeutils import encode, decode, is_list
from ConfigParser import SafeConfigParser

ENCODING = 'utf-8'

def split(value, encoding=None):
    if not encoding: encoding = ENCODING
    reader = csv.reader([encode(value, encoding)], dialect=ConfigDialect)
    return [v.strip().decode(encoding) for v in tuple(reader)[0]]

def join(values, encoding=None):
    if not encoding: encoding = ENCODING
    strbuf = StringIO()
    writer = csv.writer(strbuf, dialect=ConfigDialect)
    writer.writerow(encode(values, encoding))
    return decode(strbuf.getvalue().strip(), encoding)

class ConfigSectionError(Exception): pass

class ConfigDialect(csv.Dialect): #{{{1

    delimiter = ','
    doublequote = False
    escapechar = '\\'
    lineterminator = '\n'
    quotechar = '"'
    quoting = csv.QUOTE_MINIMAL
    skipinitialspace = True



class Config(SafeConfigParser): #{{{1

    def __init__(self, defaults=None, main=None, encoding=None):
        SafeConfigParser.__init__(self, defaults)
        self.encoding = encoding or ENCODING
        self.main = main or 'app:main'

    def encode(self, value):
        return encode(value, self.encoding)

    def decode(self, value):
        return decode(value, self.encoding)

    def defaults(self):
        defaults = {}
        for k, v in SafeConfigParser.defaults(self):
            defaults[self.decode(k)] = self.decode(v)
        return defaults

    def add_section(self, section):
        SafeConfigParser.add_section(self, self.encode(section))

    def has_section(self, section):
        return SafeConfigParser.has_section(self, self.encode(section))

    def has_option(self, section, option):
        return SafeConfigParser.has_option(self, self.encode(section), self.encode(option))

    def options(self, section):
        return [self.decode(o) for o in SafeConfigParser.options(self, self.encode(section))]

    def set(self, section, option, value):
        section = self.encode(section)
        value = self.encode(value)
        if is_list(value): value = join(value, self.encoding)
        if not self.has_section(section): self.add_section(section)
        SafeConfigParser.set(self, section, option, value)

    def get(self, section, option, default=None):
        section = self.encode(section)
        option = self.encode(option)
        if not self.has_option(section, option): return default
        return self.decode(SafeConfigParser.get(self, section, option))

    def getint(self, section, option, default=None):
        section = self.encode(section)
        option = self.encode(option)
        if not self.has_option(section, option): return default
        return SafeConfigParser.getint(self, section, option)

    def getboolean(self, section, option, default=None):
        section = self.encode(section)
        option = self.encode(option)
        if not self.has_option(section, option): return default
        return SafeConfigParser.getboolean(self, section, option)

    def getfloat(self, section, option, default=None):
        section = self.encode(section)
        option = self.encode(option)
        if not self.has_option(section, option): return default
        return SafeConfigParser.getfloat(self, section, option)

    def getlist(self, section, option, default=None, convert=None):
        if not self.has_option(section, option): return default
        values = split(self.get(section, option), self.encoding)
        if convert: return [convert(v) for v in values]
        return values

    def update(self, sections):
        for section, options in sections.iteritems():
            if not isinstance(options, dict):
                raise ConfigSectionError("Invalid section '%s'" % section)
            for option, value in options.iteritems():
                self.set(section, option, value)

    def items(self, section):
        items = []
        for option in self.options(section):
            items.append((option, self.get(section, option)))
        return items



class SingleConfig(Config): #{{{1

    def __init__(self, filename, base, *args, **kwargs):
        Config.__init__(self, *args, **kwargs)
        self.filename = filename
        self.directory = os.path.dirname(self.filename)
        self.update(base)
        self.load()

    def load(self):
        if os.path.isfile(self.filename):
            self.read(self.filename)
        else:
            self.write()

    def write(self):
        directory = os.path.dirname(self.filename)
        if not os.path.isdir(directory): os.makedirs(directory)
        Config.write(self, open(self.filename, 'w'))
