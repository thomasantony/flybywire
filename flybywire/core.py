"""
Module: flybywire.core

Contains the 'App' class which forms the base class for any Application built
using this framework.
"""
import os
import abc
import json
import asyncio
import logging
import webbrowser

from autobahn.asyncio.websocket import WebSocketServerFactory, WebSocketServerProtocol

class App(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.interface = FBWEventProcessor()
        self.server = FBWEventServer(processor=self.interface)
        self._state = None
        self._callbacks = {}
        logging.basicConfig(
            format="%(asctime)s [%(levelname)s] - %(funcName)s: %(message)s",
            level=logging.INFO
        )

        # Setup callback to initialize DOM when the client connects
        self.register('init', self._oninit)
        self.register('domevent', self._process_domevent)
        # self.register('shutdown', self._shutdown)

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
        content = self.render().to_dict()
        vdom = content['dom']
        self.remote_render(vdom)

    @asyncio.coroutine
    def _oninit(self, event):
        """Trigger render() when app initializes."""
        content = self.render().to_dict()
        vdom = content['dom']
        self.update_callbacks(content['callbacks'])
        # Send init command to create initial DOM
        self.interface.dispatch({ 'name': 'init', 'vdom': json.dumps(vdom)})

    def update_callbacks(self, callbacks):
        """Updates internal list with callbacks found in the dom."""
        if callbacks != self._callbacks:
            self._callbacks.update(callbacks)

    @asyncio.coroutine
    def _process_domevent(self, event):
        """Routes DOM events to the right callback function."""
        if event['callback'] in self._callbacks:
            cb_func, cb_self = self._callbacks[event['callback']]
            if cb_self is not None:
                cb_func(cb_self, event['event_obj'])
            else:
                cb_func(event['event_obj'])
        else:
            logging.error('Callback '+event['callback']+' not found.')

    #
    # def _shutdown(self, event):
    #     """Shuts down the server."""
    #     exit(0)

    def start(self, autobrowse=True):
        """Start the application."""
        self.server.start(autobrowse)

    def register(self, event, callback, selector=None):
        """Register event callback"""

        self.interface.register(event, callback, selector)

    def unregister(self, event, callback, selector=None):
        """Register event callback"""

        self.interface.unregister(event, callback, selector)

    def remote_render(self, vdom):
        """Converts given vdom to JSON and sends it to browser for rendering."""
        content = self.render().to_dict()
        vdom = content['dom']
        self._callbacks.update(content['callbacks'])
        self.interface.dispatch({ 'name': 'render', 'vdom': json.dumps(vdom)})


class FBWEventProcessor(object):
    """Event handler providing hooks for callback functions"""

    handlers = { 'init': { '_': [] },
                 'load': { '_': [] },
                 'close': { '_': [] },
                 'domevent': {'_': []},
               }

    def register(self, event, callback, selector=None):
        if event not in self.handlers:
            self.handlers[event] = { '_': [] }

        if selector:
            key = str(id(callback))
        else:
            key = '_'

        if key not in self.handlers[event]:
            self.handlers[event][key] = list()

        self.handlers[event][key].append(callback)

        # if (event not in ('init', 'load', 'close', 'shutdown')
        #    and len(self.handlers[event].keys()) > 1):
        #     capture = False
        #     if selector is None:
        #         selector = 'html'
        #         capture = True
        #
        #     self.dispatch({ 'name': 'subscribe', 'event': event, 'selector': selector, 'capture': capture, 'key': str(id(callback)) })

    def unregister(self, event, callback, selector=None):
        if event not in self.handlers:
            return

        if selector is None:
            self.handlers[event]['_'].remove(callback)
        else:
            self.handlers[event].pop(str(id(callback)))

        # if event not in ('init', 'load', 'close'):
        #     self.dispatch({ 'name': 'unsubscribe', 'event': event, 'selector': selector, 'key': str(id(callback)) })

    def dispatch(self, command):
        self.protocol.sendMessage(bytes(json.dumps(command), 'utf-8'), False)

    @asyncio.coroutine
    def process(self, protocol, event):
        self.protocol = protocol
        eventtype = event['event']
        logging.info('Event triggered : '+eventtype)
        if eventtype in self.handlers:
            # Check for local handler
            if 'key' in event:
                key = event['key']

                if key in self.handlers[eventtype]:
                    for handler in self.handlers[eventtype][key]:
                        if callable(handler):
                            yield from handler(event)

            # Check for global handler
            for handler in self.handlers[eventtype]['_']:
                if callable(handler):
                    yield from handler(event)


class FBWEventProtocol(WebSocketServerProtocol):
    """Websocket event handler which dispatches events to FBWEventProcessor"""

    def onConnect(self, request):
        logging.info("Client connecting: %s" % request.peer)

    def onOpen(self):
        logging.info("WebSocket connection open")

    @asyncio.coroutine
    def onMessage(self, payload, isBinary):
        if isBinary:
            logging.debug("Binary message received: {} bytes".format(len(payload)))
        else:
            logging.debug("Text message received: {}".format(payload.decode('utf-8')))
            body = json.loads(payload.decode('utf-8'))

            if 'event' in body:
                yield from self.processor.process(self, body)

    def onClose(self, wasClean, code, reason):
        logging.info("WebSocket connection closed: {}".format(reason))

        # Stop server when browser exists
        loop = asyncio.get_event_loop()
        loop.stop()
        # Stop all pending tasks
        for task in asyncio.Task.all_tasks():
            task.cancel()
        exit(0)


class FBWEventServer(object):
    """Websocket event server"""

    def __init__(self, hostname=u"127.0.0.1", port=9000, processor=None):

        self.hostname = hostname
        self.port = port
        self.processor = processor

        factory = WebSocketServerFactory(u"ws://" + hostname + u":" + str(port))
        protocol = FBWEventProtocol
        protocol.processor = processor
        protocol.app = self

        factory.protocol = protocol

        self.loop = asyncio.get_event_loop()
        self.server = self.loop.create_server(factory, '0.0.0.0', port)

    def stop(self):
        self.loop.stop()

    def start(self, autobrowse=True):
        self.loop.run_until_complete(self.server)

        try:
            path = os.path.dirname(os.path.realpath(__file__))
            if autobrowse:
                webbrowser.open('file:///' + os.path.join(path, 'static/main.html'))
            self.loop.run_forever()

        except KeyboardInterrupt:
            pass

        finally:
            self.server.close()
            self.loop.close()

    def __repr__(self):
        return "<EventServer(%s, %s)>" % (self.hostname, self.port)

    def __str__(self):
        return repr(self)
