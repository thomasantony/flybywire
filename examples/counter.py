from flybywire.core import App
from flybywire.dom import h


def CounterView(count):
    """A simple functional stateless component."""
    return h('h1', str(count))


class CounterApp(App):
    def __init__(self):
        """Initialize the application."""
        super().__init__() # in Python 3.5
        self.set_initial_state(0)

    def render(self):
        """Renders view given application state."""
        return h('div',
                    [CounterView(count=self.state),
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
