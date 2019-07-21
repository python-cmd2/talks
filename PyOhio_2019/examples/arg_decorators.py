#!/usr/bin/env python3
# coding=utf-8
"""An example demonstrating how use one of cmd2's argument parsing decorators"""
import argparse
import os

import cmd2


class ArgparsingApp(cmd2.Cmd):
    def __init__(self):
        super().__init__(use_ipython=True)
        self.intro = 'cmd2 has awesome decorators to make it easy to use Argparse to parse command arguments'

    cat_parser = cmd2.Cmd2ArgumentParser(description='concatenate and print files', epilog='See "man cat"')
    flag_group = cat_parser.add_mutually_exclusive_group()
    flag_group.add_argument('-o', '--output_file', help='output written to this file',
                            completer_method=cmd2.Cmd.path_complete)
    flag_group.add_argument('-p', '--paged', action='store_true', help='display using a pager')

    cat_parser.add_argument('files_to_cat', nargs=argparse.ONE_OR_MORE, help='files to concatinate',
                            completer_method=cmd2.Cmd.path_complete)

    @cmd2.with_argparser(cat_parser)
    def do_cat(self, args: argparse.Namespace) -> None:
        """concatenate and print files"""
        shell_command = '!cat ' + ' '.join(args.files_to_cat)
        if args.paged:
            shell_command += ' | ' + self.pager
        elif args.output_file:
            shell_command += ' > {}'.format(os.path.expanduser(args.output_file))
        self.poutput('Running shell command {!r}'.format(shell_command))
        self.onecmd_plus_hooks(shell_command)
        self.poutput('')

    pow_parser = argparse.ArgumentParser()
    pow_parser.add_argument('base', type=int)
    pow_parser.add_argument('exponent', type=int, choices=range(-5, 6))

    @cmd2.with_argparser(pow_parser)
    def do_pow(self, args: argparse.Namespace) -> None:
        """Raise an integer to a small integer exponent, either positive or negative."""
        self.poutput('{} ** {} == {}'.format(args.base, args.exponent, args.base ** args.exponent))


if __name__ == '__main__':
    app = ArgparsingApp()
    app.cmdloop()
