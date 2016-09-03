from flybywire.core import App
from flybywire.dom import h

import asyncio
import json
import time

import logging

@asyncio.coroutine
def oninit(event):
    logging.info("MAIN")
    app.load('foo')

@asyncio.coroutine
def onload(event):
    logging.info("LOADED")

    i = 1
    while True:
        yield from asyncio.sleep(1)
        vdom = h('div', {
            'style': {
                'textAlign': 'center',
                'lineHeight': str(100 + i) + 'px',
                'border': '1px solid red',
                'width': str(100 + i) + 'px',
                'height': str(100 + i) + 'px'
            }
        }, str(i))
        app.render(vdom)
        i += 1

    return

logging.basicConfig(format="%(asctime)s [%(levelname)s] - %(funcName)s: %(message)s", level=logging.INFO)

app = App()
app.register('init', oninit)
app.register('load', onload)
# app.register('click', clicked)

app.start()
