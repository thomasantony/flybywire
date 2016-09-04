
class Component(object):
"""Decorator used to define a component."""

    def __init__(self):
        self._state = None

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
        if isinstance(self.state, dict) and isinstance(new_state, dict):
            # Merge into dictionary if state is a dictionary (similar to React)
            self._state.update(new_state)
        else:
            self._state = new_state

        self.render()
