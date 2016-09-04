from flybywire.core import FBWApp
from flybywire.ui import Component
from flybywire.dom import h
from flybywire.misc import set_interval, clear_interval

class TimerApp(Component):
    def __init__(self):
        """Initialize the application."""
        super().__init__()

        self.set_initial_state({'secondsElapsed': 0})
        self.task = None

    def render(self):
        """Renders view given application state."""
        count = self.state['secondsElapsed']
        return h('div', 'Seconds Elapsed: '+str(count))

    def tick(self):
        """Increments counter."""
        count = self.state['secondsElapsed']
        self.set_state({'secondsElapsed': count + 1})

    def on_load(self):
        """
        Triggers when the application first loads in the browser
        """
        print('On load triggered')
        self.task = set_interval(self.tick, 1)

    def on_close(self):
        """
        Triggers when the application window is closed
        """
        print('On close triggered')
        clear_interval(self.task)

app = FBWApp(TimerApp())
app.start()
