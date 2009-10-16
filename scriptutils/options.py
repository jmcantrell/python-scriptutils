from optparse import OptionParser, OptionGroup, IndentedHelpFormatter

class Options(object, OptionParser):

    def __init__(self, usage=None, width=None):
        if not usage: usage = 'Usage: %prog [options]'
        if not width: width = 35
        super(Options, self).__init__()
        OptionParser.__init__(self, usage, add_help_option=None,
                formatter=IndentedHelpFormatter(max_help_position=width))

    def add_option_group(self, name):
        group = OptionGroup(self, name)
        super(Options, self).add_option_group(group)
        return group
