#!/usr/bin/env python3
# coding=utf-8
"""An example demonstrating how to use a couple of cmd2's argument parsing decorators.
"""
import argparse
import os
from typing import List

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

    # TODO: Show off all of the following:
    # - Argument types
    #   - Integer arguments
    # - Tab Completion:
    #   - Choices
    pprint_parser = argparse.ArgumentParser()
    pprint_parser.add_argument('-p', '--piglatin', action='store_true', help='atinLay')
    pprint_parser.add_argument('-s', '--shout', action='store_true', help='N00B EMULATION MODE')
    pprint_parser.add_argument('-r', '--repeat', type=int, help='output [n] times')

    @cmd2.with_argparser_and_unknown_args(pprint_parser)
    def do_unknown_print(self, args: argparse.Namespace, unknown: List[str]) -> None:
        """Print the options and argument list this options command was called with."""
        self.poutput('unknown_print was called with the following\n\toptions: {!r}\n\targuments: {}'.format(args,
                                                                                                            unknown))


if __name__ == '__main__':
    app = ArgparsingApp()
    app.cmdloop()
