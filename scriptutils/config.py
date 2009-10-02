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



class Config(object): #{{{1

    def __init__(self, defaults=None, encoding=None): #{{{2
        self.encoding = encoding
        self.parser = SafeConfigParser(defaults)

    def encode(self, value): #{{{2
        return encode(value, self.encoding)

    def decode(self, value): #{{{2
        return decode(value, self.encoding)

    def defaults(self): #{{{2
        return self.decode(self.parser.defaults())

    def sections(self): #{{{2
        return self.decode(self.parser.sections())

    def add_section(self, section): #{{{2
        self.parser.add_section(self.encode(section))

    def has_section(self, section): #{{{2
        return self.parser.has_section(self.encode(section))

    def has_option(self, section, option): #{{{2
        return self.parser.has_option(self.encode(section), self.encode(option))

    def options(self, section): #{{{2
        return self.decode(self.parser.options(self.encode(section)))

    def read(self, filenames): #{{{2
        self.parser.read(filenames)

    def readfp(self, fp, filename=None): #{{{2
        self.parser.readfp(fp, filename)

    def get(self, section, option, default=None, getter=None): #{{{2
        section = self.encode(section)
        option = self.encode(option)
        if not getter: getter = self.parser.get
        if not self.has_option(section, option): return default
        return self.decode(getter(section, option))

    def getint(self, section, option, default=None): #{{{2
        return self.get(section, option, default, self.parser.getint)

    def getboolean(self, section, option, default=None): #{{{2
        return self.get(section, option, default, self.parser.getboolean)

    def getfloat(self, section, option, default=None): #{{{2
        return self.get(section, option, default, self.parser.getfloat)

    def getlist(self, section, option, default=None, convert=None): #{{{2
        if not self.has_option(section, option): return default
        values = split(self.get(section, option), self.encoding)
        if convert: return [convert(v) for v in values]
        return values

    def set(self, section, option, value): #{{{2
        section = self.encode(section)
        value = self.encode(value)
        if is_list(value): value = join(value, self.encoding)
        if not self.has_section(section): self.add_section(section)
        self.parser.set(section, option, value)

    def write(self, fo): #{{{2
        self.parser.write(fo)

    def remove_option(self, section, option): #{{{2
        return self.parser.remove_option(section, option)

    def remove_section(self, section): #{{{2
        return self.parser.remove_section(section)

    def update(self, sections): #{{{2
        for section, options in sections.iteritems():
            if not isinstance(options, dict):
                raise ConfigSectionError("Invalid section '%s'" % section)
            for option, value in options.iteritems():
                self.set(section, option, value)

    def items(self, section): #{{{2
        return [(o, self.get(section, o)) for o in self.options(section)]



class SingleConfig(Config): #{{{1

    def __init__(self, filename, base=None, **kwargs): #{{{2
        self.filename = filename
        self.base = base or {}
        super(SingleConfig, self).__init__(**kwargs)
        self.directory = os.path.dirname(self.filename)
        self.update(self.base)
        self.load()

    def load(self): #{{{2
        if os.path.isfile(self.filename):
            super(SingleConfig, self).read(self.filename)
        else:
            self.write()

    def write(self, fo=None): #{{{2
        if not fo:
            if not os.path.isdir(self.directory): os.makedirs(directory)
            fo = open(self.filename, 'w')
        super(SingleConfig, self).write(fo)



class SimpleConfig(object): #{{{1

    def __init__(self, filename, base=None, main=None, **kwargs): #{{{2
        self.main = main or 'app:main'
        self.config = SingleConfig(filename, base={self.main: base or {}}, **kwargs)

    def encode(self, value): #{{{2
        return self.config.encode(value)

    def decode(self, value): #{{{2
        return self.config.decode(value)

    def has_option(self, option): #{{{2
        return self.config.has_option(self.main, option)

    def options(self): #{{{2
        return self.config.options(self.main)

    def get(self, option, default=None): #{{{2
        return self.config.get(self.main, option, default)

    def getint(self, option, default=None): #{{{2
        return self.config.getint(self.main, option, default)

    def getboolean(self, option, default=None): #{{{2
        return self.config.getboolean(self.main, option, default)

    def getfloat(self, option, default=None): #{{{2
        return self.config.getfloat(self.main, option, default)

    def getlist(self, option, default=None, convert=None): #{{{2
        return self.config.getlist(self.main, option, default, convert)

    def set(self, option, value): #{{{2
        self.config.set(self.main, option, value)

    def update(self, items): #{{{2
        self.config.update({self.main: items})

    def items(self): #{{{2
        return self.config.items(self.main)

    def load(self): #{{{2
        self.config.load()

    def write(self): #{{{2
        self.config.write()
