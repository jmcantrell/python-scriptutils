from argparse import ArgumentParser, ArgumentGroup, IndentedHelpFormatter

class Arguments(ArgumentParser):

    def __init__(self, width=None, **kwargs):
        if not width: width = 45
        super(Arguments, self).__init__(**kwargs, add_help_option=None, formatter=IndentedHelpFormatter(max_help_position=width))
        self.add_argument('-h', '--help', action='help', help='Show this help message and exit.')
