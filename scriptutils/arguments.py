from argparse import ArgumentParser, HelpFormatter


class Arguments(ArgumentParser):

    def __init__(self, width=None, **kwargs):
        def get_formatter(*args, **kwargs):
            kwargs['max_help_position'] = width or 45
            return HelpFormatter(*args, **kwargs)
        kwargs['formatter_class'] = get_formatter
        super(Arguments, self).__init__(**kwargs)
