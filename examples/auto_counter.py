from flybywire.core import App
from flybywire.dom import h

import asyncio

class AutoCounterApp(App):
    def __init__(self):
        """Initialize the application."""
        # super().__init__() # in Python 3.5
        super(AutoCounterApp, self).__init__()
        self.register('load', self.onload)

        # Initialize application state
        self.set_initial_state(0)

    def render(self):
        """Renders view given application state."""
        count = self.state
        # Equivalent to :
        #   <div style="textAlign: center; ...">{count}</div>
        return h('div', str(count), style = {
                'textAlign': 'center',
                'lineHeight': str(100 + count) + 'px',
                'border': '1px solid red',
                'width': str(100 + count) + 'px',
                'height': str(100 + count) + 'px'
        })

    @asyncio.coroutine
    def onload(self, event):
        """
        'Load' event handler with application logic
        """
        while True:
            yield from asyncio.sleep(1)
            # Increment counter and trigger redraw
            self.set_state(self.state + 1)

app = AutoCounterApp()
app.start()
