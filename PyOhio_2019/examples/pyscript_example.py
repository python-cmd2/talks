#!/usr/bin/env python
# coding=utf-8
"""A sample application for how Python scripting can provide conditional control flow of a cmd2 application"""
import os

import cmd2
from cmd2 import style


class CmdLineApp(cmd2.Cmd):
    """ Example cmd2 application to showcase conditional control flow in Python scripting within cmd2 aps. """

    def __init__(self):
        # Enable the optional ipy command if IPython is installed by setting use_ipython=True
        super().__init__(use_ipython=True)
        self._set_prompt()
        self.intro = 'Built-in Python scripting is a killer feature ...'

        # Add cwd accessor to Python environment used by pyscripts
        self.py_locals['cwd'] = self.cwd

    def _set_prompt(self):
        """Set prompt so it displays the current working directory."""
        self._cwd = os.getcwd()
        self.prompt = style('{!r} $ '.format(self._cwd), fg='cyan')

    def postcmd(self, stop: bool, line: str) -> bool:
        """Hook method executed just after a command dispatch is finished.

        :param stop: if True, the command has indicated the application should exit
        :param line: the command line text for this command
        :return: if this is True, the application will exit after this command and the postloop() will run
        """
        """Override this so prompt always displays cwd."""
        self._set_prompt()
        return stop

    def cwd(self):
        """Read-only property used by the pyscript to obtain cwd"""
        return self._cwd

    @cmd2.with_argument_list
    def do_cd(self, arglist):
        """Change directory.
    Usage:
        cd <new_dir>
        """
        # Expect 1 argument, the directory to change to
        if not arglist or len(arglist) != 1:
            self.perror("cd requires exactly 1 argument")
            self.do_help('cd')
            return

        # Convert relative paths to absolute paths
        path = os.path.abspath(os.path.expanduser(arglist[0]))

        # Make sure the directory exists, is a directory, and we have read access
        out = ''
        err = None
        data = None
        if not os.path.isdir(path):
            err = '{!r} is not a directory'.format(path)
        elif not os.access(path, os.R_OK):
            err = 'You do not have read access to {!r}'.format(path)
        else:
            try:
                os.chdir(path)
            except Exception as ex:
                err = '{}'.format(ex)
            else:
                out = 'Successfully changed directory to {!r}\n'.format(path)
                self.stdout.write(out)
                data = path

        if err:
            self.perror(err)
        self.last_result = data

    # Enable tab completion for cd command
    def complete_cd(self, text, line, begidx, endidx):
        return self.path_complete(text, line, begidx, endidx, path_filter=os.path.isdir)

    dir_parser = cmd2.Cmd2ArgumentParser()
    dir_parser.add_argument('-l', '--long', action='store_true', help="display in long format with one item per line")

    @cmd2.with_argparser_and_unknown_args(dir_parser)
    def do_dir(self, args, unknown):
        """List contents of current directory."""
        # No arguments for this command
        if unknown:
            self.perror("dir does not take any positional arguments:")
            self.do_help('dir')
            return

        # Get the contents as a list
        contents = os.listdir(self._cwd)

        fmt = '{} '
        if args.long:
            fmt = '{}\n'
        for f in contents:
            self.stdout.write(fmt.format(f))
        self.stdout.write('\n')

        self.last_result = contents


if __name__ == '__main__':
    import sys
    c = CmdLineApp()
    sys.exit(c.cmdloop())
