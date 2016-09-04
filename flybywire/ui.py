import abc
from .core import FBWApp

def Application(cls):
    def create_fbw_app(*args, **kwargs):
        root = cls(*args, **kwargs)
        return FBWApp(root)

    #TODO: Figure out way to fix __name__ and __doc__ in resulting instance
    return create_fbw_app

class Component(object):
    """Class defining a UI component."""
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        self._state = None
        self._observers = []

    @abc.abstractmethod
    def render():
        """Applications must implement this method."""
        raise NotImplementedError()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, _):
        raise RuntimeError('Use the set_state() or set_initial_state() '+\
                           'to modify the state')

    def set_initial_state(self, state):
        """Sets the application state without triggering a redraw."""
        # Helps initialize state before client is connected
        self._state = state

    def set_state(self, new_state):
        """Set new state and trigger redraw."""
        # Merge into dictionary if state is a dictionary (similar to React)
        if isinstance(self.state, dict) and isinstance(new_state, dict):
            self._state.update(new_state)
        else:
            self._state = new_state

        self.notify_observers()

    def add_observer(self, observer):
        """
        Sets up observer who is triggered whenever the state is changed
        """
        self._observers.append(observer)

    def notify_observers(self):
        """
        Notifies observers that the component state has changed
        """
        for obs in self._observers:
            obs()

    def remove_observer(self, callback):
        """
        Removes an observer
        """
        self._observers.remove(observer)

    def on_load(self):
        """
        Load event handler
        """
        pass

    def on_close(self):
        """
        Close event handler
        """
        pass
