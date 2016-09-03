from flybywire.core import App
from flybywire.dom import h
from flybywire.misc import set_interval, clear_interval
import asyncio

class TimerApp(App):
    def __init__(self):
        """Initialize the application."""
        super().__init__()
        self.register('load', self.onload)
        self.register('close', self.onclose)

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
    def onload(self, event):
        """
        'Load' event handler with application logic
        """
        self.task = set_interval(self.tick, 1)

    @asyncio.coroutine
    def onclose(self, event):
        """
        Stop the timer when app closes
        """
        clear_interval(self.task)


app = TimerApp()
app.start()
