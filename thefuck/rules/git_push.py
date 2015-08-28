from thefuck import utils
from thefuck.specific.git import git_support


@git_support
def match(command, settings):
    return ('push' in command.script
            and 'set-upstream' in command.stderr)


@git_support
def get_new_command(command, settings):
    return command.stderr.split('\n')[-3].strip()
