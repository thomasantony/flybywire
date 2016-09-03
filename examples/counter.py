from flybywire.core import App
from flybywire.dom import h
import asyncio

class CounterApp(App):
    def __init__(self):
        """Initialize the application."""
        super().__init__() # in Python 3.5
        self.set_initial_state(0)
        self.task = None

    def render(self):
        """Renders view given application state."""
        count = self.state

        return h('div',
                    [h('h1', str(count)),
                     h('button', '+', onclick = self.increment),
                     h('button', '-', onclick = self.decrement)]
                )

    def increment(self, e):
        """Increments counter."""
        self.set_state(self.state + 1)

    def decrement(self, e):
        """Decrements counter."""
        self.set_state(self.state - 1)


app = CounterApp()
app.start()
