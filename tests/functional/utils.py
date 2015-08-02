import os
import subprocess
import shutil
from tempfile import mkdtemp
from pathlib import Path
import sys
import pexpect
import pytest

root = str(Path(__file__).parent.parent.parent.resolve())
bare = os.environ.get('BARE')
enabled = os.environ.get('FUNCTIONAL')


def build_container(tag, dockerfile):
    tmpdir = mkdtemp()
    try:
        with Path(tmpdir).joinpath('Dockerfile').open('w') as file:
            file.write(dockerfile)
        if subprocess.call(['docker', 'build', '--tag={}'.format(tag), tmpdir],
                           cwd=root) != 0:
            raise Exception("Can't build a container")
    finally:
        shutil.rmtree(tmpdir)


def spawn(request, tag, dockerfile, cmd):
    if bare:
        proc = pexpect.spawnu(cmd)
    else:
        tag = 'thefuck/{}'.format(tag)
        build_container(tag, dockerfile)
        proc = pexpect.spawnu('docker run --volume {}:/src --tty=true '
                              '--interactive=true {} {}'.format(root, tag, cmd))
        proc.sendline('pip install /src')
    proc.sendline('cd /')

    proc.logfile = sys.stdout

    request.addfinalizer(proc.terminate)
    return proc


def images(*items):
    if bare:
        return [items[0]]
    else:
        return items


functional = pytest.mark.skipif(
    not enabled,
    reason='Functional tests are disabled by default.')
