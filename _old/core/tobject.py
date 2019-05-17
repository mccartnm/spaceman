"""
Base object for fun event handling
"""

import inspect
import functools

from .utils import emap

class TObject(object):
    """
    In order to utilize the TSignal properly, we have to make
    sure the objects wrap the method with our instance
    """
    def __init__(self, *args, **kwargs):
        for name, method in inspect.getmembers(self):
            if isinstance(method, TSignal):
                #
                # Build a custom signal object for each instance
                # to avoid any overlap
                #
                wrapped = functools.partial(method._func, self)
                setattr(self, name, TSignal(wrapped))

class TSignal(object):
    """
    Decorator for simple pre/post callback setup
    """
    def __init__(self, func):
        self._func = func
        self._pre_events  = []
        self._post_events = []

    def __call__(self, *args, **kwargs):
        """
        When we call the function, we have the pre and post events
        do their bidding.
        """
        for call, a, k in self._pre_events:
            call(*a, *args, **k, **kwargs)

        self._func(*args, **kwargs)

        for call, a, k in self._post_events:
            call(*a, *args, **k, **kwargs)        

    def listen_pre(self, function, *args, **kwargs):
        self._pre_events.append((function, args, kwargs))

    def listen_post(self, function, *args, **kwargs):
        self._post_events.append((function, args, kwargs))

    def stop_listening(self, function):
        """
        Stop using the callback on the provided function
        """
        pre_to_remove = []
        post_to_remove = []
        for e in self._pre_events:
            if e[0] == function:
                pre_to_remove.append(e)

        for e in self._post_events:
            if e[0] == function:
                post_to_remove.append(e)

        emap(lambda x: self._pre_events.remove(x), pre_to_remove)
        emap(lambda x: self._post_events.remove(x), post_to_remove)