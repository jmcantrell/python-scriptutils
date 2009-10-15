import os, csv
from StringIO import StringIO
from unicodeutils import encode, decode, is_list
from ConfigParser import SafeConfigParser

ENCODING = 'utf-8'

# FUNCTIONS {{{1

def split(value, encoding=None): #{{{2
    if not encoding: encoding = ENCODING
    reader = csv.reader([encode(value, encoding)], dialect=ConfigDialect)
    return [v.strip().decode(encoding) for v in tuple(reader)[0]]

def join(values, encoding=None): #{{{2
    if not encoding: encoding = ENCODING
    strbuf = StringIO()
    writer = csv.writer(strbuf, dialect=ConfigDialect)
    writer.writerow(encode(values, encoding))
    return decode(strbuf.getvalue().strip(), encoding)


# CLASSES {{{1

class ConfigSectionError(Exception): #{{{2
    pass



class ConfigDialect(csv.Dialect): #{{{2

    delimiter = ','
    doublequote = False
    escapechar = '\\'
    lineterminator = '\n'
    quotechar = '"'
    quoting = csv.QUOTE_MINIMAL
    skipinitialspace = True



class Config(object): #{{{2

    def __init__(self, defaults=None, encoding=None):
        self.encoding = encoding
        self.parser = SafeConfigParser(defaults)

    def encode(self, value):
        return encode(value, self.encoding)

    def decode(self, value):
        return decode(value, self.encoding)

    def defaults(self):
        return self.decode(self.parser.defaults())

    def sections(self):
        return self.decode(self.parser.sections())

    def add_section(self, section):
        self.parser.add_section(self.encode(section))

    def has_section(self, section):
        return self.parser.has_section(self.encode(section))

    def has_option(self, section, option):
        return self.parser.has_option(self.encode(section), self.encode(option))

    def options(self, section):
        return self.decode(self.parser.options(self.encode(section)))

    def read(self, filenames):
        self.parser.read(filenames)

    def readfp(self, fp, filename=None):
        self.parser.readfp(fp, filename)

    def getraw(self, section, option, default=None, getter=None):
        section = self.encode(section)
        option = self.encode(option)
        if not getter: getter = self.parser.get
        if not self.has_option(section, option): return default
        return getter(section, option)

    def get(self, section, option, default=None):
        return self.decode(self.getraw(section, option, default))

    def getint(self, section, option, default=None):
        return self.getraw(section, option, default, self.parser.getint)

    def getboolean(self, section, option, default=None):
        return self.getraw(section, option, default, self.parser.getboolean)

    def getfloat(self, section, option, default=None):
        return self.getraw(section, option, default, self.parser.getfloat)

    def getlist(self, section, option, default=None, convert=None):
        if not self.has_option(section, option): return default
        values = split(self.get(section, option), self.encoding)
        if convert: return [convert(v) for v in values]
        return values

    def set(self, section, option, value):
        section = self.encode(section)
        value = self.encode(value)
        if is_list(value): value = join(value, self.encoding)
        if not self.has_section(section): self.add_section(section)
        self.parser.set(section, option, value)

    def write(self, fo):
        self.parser.write(fo)

    def remove_option(self, section, option):
        return self.parser.remove_option(section, option)

    def remove_section(self, section):
        return self.parser.remove_section(section)

    def update(self, sections):
        for section, options in sections.iteritems():
            if not isinstance(options, dict):
                raise ConfigSectionError("Invalid section '%s'" % section)
            for option, value in options.iteritems():
                self.set(section, option, value)

    def items(self, section):
        return [(o, self.get(section, o)) for o in self.options(section)]



class SingleConfig(Config): #{{{2

    def __init__(self, filename, base=None, **kwargs):
        self.filename = filename
        self.base = base or {}
        super(SingleConfig, self).__init__(**kwargs)
        self.directory = os.path.dirname(self.filename)
        self.update(self.base)
        self.load()

    def load(self):
        if os.path.isfile(self.filename):
            super(SingleConfig, self).read(self.filename)
        else:
            self.write()

    def write(self, fo=None):
        if not fo:
            if not os.path.isdir(self.directory):
                os.makedirs(self.directory)
            fo = open(self.filename, 'w')
        super(SingleConfig, self).write(fo)



class SimpleConfig(object): #{{{2

    def __init__(self, filename, base=None, main=None, **kwargs):
        self.main = main or 'app:main'
        self.base = base or {}
        self.config = SingleConfig(filename, base={self.main: self.base}, **kwargs)
        self.filename = self.config.filename
        self.directory = self.config.directory
        self.encoding = self.config.encoding

    def encode(self, value):
        return self.config.encode(value)

    def decode(self, value):
        return self.config.decode(value)

    def has_option(self, option):
        return self.config.has_option(self.main, option)

    def options(self):
        return self.config.options(self.main)

    def get(self, option, default=None):
        return self.config.get(self.main, option, default)

    def getint(self, option, default=None):
        return self.config.getint(self.main, option, default)

    def getboolean(self, option, default=None):
        return self.config.getboolean(self.main, option, default)

    def getfloat(self, option, default=None):
        return self.config.getfloat(self.main, option, default)

    def getlist(self, option, default=None, convert=None):
        return self.config.getlist(self.main, option, default, convert)

    def set(self, option, value):
        self.config.set(self.main, option, value)

    def update(self, items):
        self.config.update({self.main: items})

    def items(self):
        return self.config.items(self.main)

    def load(self):
        self.config.load()

    def write(self):
        self.config.write()
