from flybywire.core import App
from flybywire.dom import h
from flybywire.misc import set_interval, clear_interval
import asyncio

class TimerApp(App):
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

    @asyncio.coroutine
    def on_load(self, event):
        """
        Triggers when the application first loads in the browser
        """
        self.task = set_interval(self.tick, 1)

    @asyncio.coroutine
    def on_close(self, event):
        """
        Triggers when the application window is closed
        """
        clear_interval(self.task)


app = TimerApp()
app.start()
