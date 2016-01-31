import shlex
from subprocess import Popen, PIPE


def system_call(cmd, **kwargs):
    """
    Wraps the rather ugly subprocess.Popen call.

    `cmd` a string with the system call to be made, may also
    contain pipes, for example:

    system_call('ls -la | grep foo')
    """
    cmds = cmd.split('|')
    previous = None
    for cmd in cmds:
        stdin = getattr(previous, 'stdout', None)
        stdout = kwargs.pop('stdout', PIPE)
        stderr = kwargs.pop('stderr', PIPE)
        previous = Popen(shlex.split(cmd),
                         stdin=stdin,
                         stdout=stdout,
                         stderr=stderr,
                         **kwargs)

    out, err = previous.communicate()
    if err:
        raise OSError(err)
    elif out:
        return out.strip()
    return ''
