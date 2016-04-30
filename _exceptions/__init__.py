# -*- coding: utf-8 -*-


class ExceptionWithFormat(Exception):
    def __init__(self, backend=None, *args, **kwargs):
        super(ExceptionWithFormat, self).__init__(backend, *args, **kwargs)
        self.backend = None
        if backend:
            self.backend = backend

    def __repr__(self):
        if self.backend and type(self.backend) is str:
            return unicode(self.backend.title()) + self.__class__.__name__
        return super(ExceptionWithFormat, self).__repr__()

    def __str__(self):
        return self.__repr__()
