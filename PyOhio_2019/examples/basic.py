#!/usr/bin/env python3
# coding=utf-8
"""A simple example demonstrating the following:
    1) How to add a command
    2) How to add help for that command
    3) Persistent history
    4) How to run an initialization script at startup
    5) How to add custom command aliases using the alias command
"""
import cmd2
from cmd2 import style

CUSTOM_CATEGORY = 'My Custom Commands'


class BasicApp(cmd2.Cmd):
    def __init__(self):
        super().__init__(multiline_commands=['echo'],
                         persistent_history_file='cmd2_history.dat',
                         startup_script='startup.txt',
                         use_ipython=True)

        self.intro = style('Welcome to PyOhio 2019 and cmd2!', fg='red', bg='white', bold=True) + ' 😀'

        # Allow access to your application in py and ipy via self
        self.locals_in_py = True

        # Set the default category name
        self.default_category = 'cmd2 Built-in Commands'

    @cmd2.with_category(CUSTOM_CATEGORY)
    def do_intro(self, _):
        """Display the intro banner"""
        self.poutput(self.intro)

    @cmd2.with_category(CUSTOM_CATEGORY)
    def do_echo(self, arg):
        """Example of a multiline command"""
        self.poutput(arg)


if __name__ == '__main__':
    app = BasicApp()
    app.cmdloop()
