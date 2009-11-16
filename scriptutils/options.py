from optparse import OptionParser, OptionGroup, IndentedHelpFormatter

class Options(object, OptionParser):

    def __init__(self, usage=None, args=None, width=None):
        if not usage: usage = 'Usage: %prog [options]'
        if args: usage += ' %s' % args.strip()
        if not width: width = 45
        super(Options, self).__init__()
        OptionParser.__init__(self, usage, add_help_option=None, formatter=IndentedHelpFormatter(max_help_position=width))
        self.add_option('-h', '--help', action='help', help='Show this help message and exit.')

    def add_option_group(self, name):
        group = OptionGroup(self, name)
        super(Options, self).add_option_group(group)
        return group
