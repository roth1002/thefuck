from thefuck.specific.archlinux import get_pkgfile, archlinux_env
from thefuck import shells


def match(command, settings):
    return 'not found' in command.stderr and get_pkgfile(command.script)


def get_new_command(command, settings):
    packages = get_pkgfile(command.script)

    formatme = shells.and_('{} -S {}', '{}')
    return [formatme.format(pacman, package, command.script)
            for package in packages]

enabled_by_default, pacman = archlinux_env()
