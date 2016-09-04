`flybywire` is an OS-agnostic, declarative UI library for Python based on [Sofi](https://github.com/tryexceptpass/sofi) and inspired by Facebook's [React](https://facebook.github.io/react/) framework. The main goal behind this experiment was to build elegant, interactive UIs in pure Python while leveraging web technologies. Eventually, `flybywire` will use something like [Electron](http://electron.atom.io/) rather than a web browser for greater control over what is rendered.

[![Build Status](https://travis-ci.org/thomasantony/flybywire.svg?branch=master)](https://travis-ci.org/thomasantony/flybywire)
[![PyPI version](https://badge.fury.io/py/flybywire.svg)](https://badge.fury.io/py/flybywire)

Overview
--------
The interface is built using a virtual-DOM layer and sent to the browser over WebSockets. All the view logic is written in pure Python. Instead of providing a set of widgets, `flybywire` allows components to be defined in a declarative manner out of standard HTML tags and CSS using an easy, readable syntax.

As in React, the view is defined as functions of the state. Any changes to the state automatically triggers a redraw of the entire DOM. `flybywire` uses the [virtual-dom](https://github.com/Matt-Esch/virtual-dom) library to update only those parts of the DOM that were actually modified.

Example
-------
This is a really simple example to demonstrate the library in action. It shows simple counter whose value can be controlled by two buttons.

```python
from flybywire.ui import Application, Component
from flybywire.dom import h


def CounterView(count):
    """A simple functional stateless component."""
    return h('h1', str(count))

@Application
class CounterApp(Component):
    def __init__(self):
        """Initialize the application."""
        # super(CounterApp, self).__init__()  # Python 2.7
        super().__init__()
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
```

![flybywire counter demo](https://giant.gfycat.com/HilariousCarefreeAnchovy.gif)
The example can also be found in `examples/counter.py`.


Bugs, features and caveats
--------------------------
- As of now, there is a system in place for some rudimentary DOM event communications. However, slightly more "advanced" features such as doing "event.preventDefault()" for specific events for example, is not available at present. Ideas for exposing this functionality are welcome! I might possibly add back some of the imperative command framework from [Sofi](https://github.com/tryexceptpass/sofi) that I had originally removed from the code.

- Some simple functionality such as focusing a textbox or clearing it after pressing enter cannot be done right now. There might be some simple way of solving this, possibly by injecting some javascript at render-time.

- The server will shut down as soon you close your browser window. This is because there is no option to reset the applicaton state right now without restarting the program.

- Opening multiple browser windows also results in some weirdness. This is again caused by the application state being shared by the all clients. However, this may not be an issue in the future once we move to an architecture based on Electron. Once that happens, there will only ever be one client connected to the server and the server lifecycle will be be tied to that of the actual application window.

About the author
----------------
[Thomas Antony's LinkedIn Profile](https://www.linkedin.com/in/thomasantony)
