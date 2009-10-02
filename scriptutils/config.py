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



class Config(object, SafeConfigParser): #{{{1

    def __init__(self, defaults=None, encoding=None): #{{{2
        SafeConfigParser.__init__(self, defaults)
        self.encoding = encoding or ENCODING

    def encode(self, value): #{{{2
        return encode(value, self.encoding)

    def decode(self, value): #{{{2
        return decode(value, self.encoding)

    def defaults(self): #{{{2
        defaults = {}
        for k, v in SafeConfigParser.defaults(self):
            defaults[Config.decode(self, k)] = Config.decode(self, v)
        return defaults

    def add_section(self, section): #{{{2
        SafeConfigParser.add_section(self, Config.encode(self, section))

    def has_section(self, section): #{{{2
        return SafeConfigParser.has_section(self, Config.encode(self, section))

    def has_option(self, section, option): #{{{2
        return SafeConfigParser.has_option(self, Config.encode(self, section), Config.encode(self, option))

    def options(self, section): #{{{2
        return [Config.decode(self, o) for o in SafeConfigParser.options(self, Config.encode(self, section))]

    def set(self, section, option, value): #{{{2
        section = Config.encode(self, section)
        value = Config.encode(self, value)
        if is_list(value): value = join(value, self.encoding)
        if not Config.has_section(self, section): Config.add_section(self, section)
        SafeConfigParser.set(self, section, option, value)

    def get(self, section, option, default=None): #{{{2
        section = Config.encode(self, section)
        option = Config.encode(self, option)
        if not Config.has_option(self, section, option): return default
        return Config.decode(self, SafeConfigParser.get(self, section, option))

    def getint(self, section, option, default=None): #{{{2
        section = Config.encode(self, section)
        option = Config.encode(self, option)
        if not Config.has_option(self, section, option): return default
        return SafeConfigParser.getint(self, section, option)

    def getboolean(self, section, option, default=None): #{{{2
        section = Config.encode(self, section)
        option = Config.encode(self, option)
        if not Config.has_option(self, section, option): return default
        return SafeConfigParser.getboolean(self, section, option)

    def getfloat(self, section, option, default=None): #{{{2
        section = Config.encode(self, section)
        option = Config.encode(self, option)
        if not Config.has_option(self, section, option): return default
        return SafeConfigParser.getfloat(self, section, option)

    def getlist(self, section, option, default=None, convert=None): #{{{2
        if not Config.has_option(self, section, option): return default
        values = split(Config.get(self, section, option), self.encoding)
        if convert: return [convert(v) for v in values]
        return values

    def update(self, sections): #{{{2
        for section, options in sections.iteritems():
            if not isinstance(options, dict):
                raise ConfigSectionError("Invalid section '%s'" % section)
            for option, value in options.iteritems():
                Config.set(self, section, option, value)

    def items(self, section): #{{{2
        items = []
        for option in self.options(section):
            items.append((option, Config.get(self, section, option)))
        return items



class SingleConfig(Config): #{{{1

    def __init__(self, filename, *args, **kwargs): #{{{2
        self.base = kwargs.pop('base', {})
        Config.__init__(self, *args, **kwargs)
        self.filename = filename
        self.directory = os.path.dirname(self.filename)
        Config.update(self, self.base)
        self.load()

    def load(self): #{{{2
        if os.path.isfile(self.filename):
            SafeConfigParser.read(self, self.filename)
        else:
            self.write()

    def write(self): #{{{2
        directory = os.path.dirname(self.filename)
        if not os.path.isdir(directory): os.makedirs(directory)
        Config.write(self, open(self.filename, 'w'))



class SimpleConfig(SingleConfig): #{{{1

    def __init__(self, filename, *args, **kwargs): #{{{2
        self.main = kwargs.pop('main', 'app:main')
        kwargs['base'] = {self.main: kwargs.pop('base', {})}
        SingleConfig.__init__(self, filename, *args, **kwargs)

    def has_option(self, option): #{{{2
        return SingleConfig.has_option(self, self.main, option)

    def options(self): #{{{2
        return SingleConfig.options(self, self.main)

    def set(self, option, value): #{{{2
        SingleConfig.set(self, self.main, option, value)

    def get(self, option, default=None): #{{{2
        return SingleConfig.get(self, self.main, option, default)

    def getint(self, option, default=None): #{{{2
        return SingleConfig.getint(self, self.main, option, default)

    def getboolean(self, option, default=None): #{{{2
        return SingleConfig.getboolean(self, self.main, option, default)

    def getfloat(self, option, default=None): #{{{2
        return SingleConfig.getfloat(self, self.main, option, default)

    def getlist(self, option, default=None, convert=None): #{{{2
        return SingleConfig.getlist(self, self.main, option, default, convert)

    def update(self, items): #{{{2
        SingleConfig.update(self, {self.main: items})

    def items(self): #{{{2
        return SingleConfig.items(self, self.main)

