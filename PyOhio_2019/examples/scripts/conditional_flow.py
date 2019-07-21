# coding=utf-8
# flake8: noqa F821
"""
This is a Python script intended to be used with the "pyscript_example.py" cmd2 example application.

To demonstrate:
    ./pyscript_example.py
    run_pyscript scripts/conditional_flow.py directory_path

Note: The "app" function is defined within the cmd2 embedded Python environment and "cwd" was made
available by adding to the self.py_locals dictionary in pyscript_example.py
"""
import sys

from cmd2 import ansi, style

if len(sys.argv) > 1:
    directory = sys.argv[1]
    print('Using specified directory: {!r}'.format(directory))
else:
    directory = 'foobar'
    print('Using default directory: {!r}'.format(directory))

# Keep track of where we started
original_dir = cwd

# Try to change to the specified directory
cd_result = app('cd {}'.format(directory))

# Conditionally do something based on the results of the last command
if cd_result:
    print('\nContents of directory {!r}:'.format(directory))
    dir_result = app('dir -l')
    print('{}\n'.format(dir_result.data))

    # Change back to where we were
    print('Changing back to original directory: {!r}'.format(original_dir))
    app('cd {}'.format(original_dir))
else:
    # cd command failed, print a warning
    print('Failed to change directory to {!r}'.format(directory))
    ansi.ansi_aware_write(sys.stderr, style(cd_result.stderr, fg='red'))
