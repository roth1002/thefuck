import re
from thefuck.specific.sudo import sudo_support


@sudo_support
def match(command, settings):
    return ('rm' in command.script
            and 'is a directory' in command.stderr.lower())


@sudo_support
def get_new_command(command, settings):
    arguments = '-rf'
    if 'hdfs' in command.script:
        arguments = '-r'
    return re.sub('\\brm (.*)', 'rm ' + arguments + ' \\1', command.script)
