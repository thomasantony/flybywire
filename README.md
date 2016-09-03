`flybywire` is an OS-agnostic, declarative UI library for Python based on [Sofi](https://github.com/tryexceptpass/sofi) and inspired by Facebook's [React](https://facebook.github.io/react/) javascript library. The main motivation behind this library was to be able to build elegant, interactive UIs in pure Python while leveraging having the flexibility to leverage web technology. Eventually, we will switch to something like [Electron](http://electron.atom.io/) rather than using a web browser.

[![Build Status](https://travis-ci.org/thomasantony/flybywire.svg?branch=master)](https://travis-ci.org/thomasantony/flybywire)
[![PyPI version](https://badge.fury.io/py/flybywire.svg)](https://badge.fury.io/py/flybywire)

## Overview
The interface is built using a virtual-DOM layer and rendered using HTML/CSS in a browser over `websockets` while all the view logic is written in pure Python . Instead of providing a set of widgets, `flybywire` allows you to build components in a declarative manner out of standard HTML tags and CSS.

As in React, the view is described as pure functions of the state. Any changes to the state automatically triggers a redraw of the entire window. `flybywire` uses the [virtual-dom](https://github.com/Matt-Esch/virtual-dom) library to update only those parts of the window that were actually modified.

## Example

This is a really simple example to demonstrate the library in action. It shows simple counter that increments it's value every second, with it's box getting progressively bigger.

```python
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
```

The example can also be found in `examples/auto_counter.py`.

## Bugs, "features" and caveats

- As of now, it is not possible to bind DOM events through the virtual DOM layer. This drastically limits the "interactive" part of the library. This is the highest priority feature under development as of now.

- The server is setup to shut down as soon you close your browser window. This is because there is no option to reset the applicaton state right now without restarting the program. This can result in some weird behavior if you open up a new window.

- Opening multiple browser windows also results in some weirdness. This is again caused by there being only one global application state per server. However, this may not be an issue in the future once we move to an architecture based on Electron. Hopefully, then the server lifecycle will be be tied to that of the actual application window.

## About the author
[Thomas Antony's LinkedIn Profile](https://www.linkedin.com/in/thomasantony)

<!--
[![Build Status](https://travis-ci.org/thomasantony/simplepipe.svg?branch=master)](https://travis-ci.org/thomasantony/simplepipe)
[![PyPI version](https://badge.fury.io/py/simplepipe.svg)](https://badge.fury.io/py/simplepipe)
-->
