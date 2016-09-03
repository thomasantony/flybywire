from flybywire.core import App
from flybywire.dom import h
from flybywire.misc import set_interval, clear_interval
import asyncio

class AutoCounterApp(App):
    def __init__(self):
        """Initialize the application."""
        # super().__init__() # in Python 3.5
        super(AutoCounterApp, self).__init__()
        self.register('load', self.onload)
        # self.register('close', self.onclose)

        self.set_initial_state(0)
        self.task = None

    def render(self):
        """Renders view given application state."""
        count = self.state

        return h('div', str(count), style = {
                'textAlign': 'center',
                'lineHeight': str(100 + count) + 'px',
                'border': '1px solid red',
                'width': str(100 + count) + 'px',
                'height': str(100 + count) + 'px'
        })

    def tick(self):
        """Increments counter."""
        self.set_state(self.state + 1)

    @asyncio.coroutine
    def onload(self, event):
        """
        'Load' event handler with application logic
        """
        self.task = set_interval(self.tick, 1)

    @asyncio.coroutine
    def onclose(self, event):
        """
        Cancel the period task that was setup
        """
        clear_interval(self.task)


app = AutoCounterApp()
app.start()
