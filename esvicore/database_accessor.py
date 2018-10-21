import builtins


class File(object):
    """A basic file-like object."""

    def __init__(self, path, *args, **kwargs):
        self._file = builtins.open(path, *args, **kwargs)

    def read(self, n_bytes = -1):
        # TODO Here I will lock the DB (or wait until it is unlocked first)
        data = self._file.read(n_bytes)
        # TODO Here I will unlock the DB
        return data

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_val, e_tb):
        self._file.close()
        self._file = None


def open(path, *args, **kwargs):
    return File(path, *args, **kwargs)