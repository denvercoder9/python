"""A very mixed bag

Note-to-self: clean up
"""

import shlex
from collections import Counter
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


def setdefaultattr(obj, name, value):
    """ This is for attribute what dict.setdefault is for dictionary keys """
    return obj.__dict__.setdefault(name, value)


class IdGenerator(Counter):
    """Creates unique ids, optionally with prefix.
    More or less like gensym in lisp """

    def __call__(self, prefix=None):
        self[prefix] += 1
        if prefix is None:
            return self[prefix]
        else:
            return prefix + str(self[prefix])
