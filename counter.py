from vdom4py import vDom

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
    # app.register('click', buttonclicked, selector='button')
    yield from asyncio.sleep(5)
    vdom = {"t":3,"tn":"DIV","p":{"style":{"textAlign":"center","lineHeight":"110px","border":"1px solid red","width":"110px","height":"100px"}},"c":[{"t":1,"x":"10"}]}
    app.render(vdom)
    logging.info('Sending new vdom')
    return
#
# @asyncio.coroutine
# def clicked(event):
#     logging.info("CLICKED!")
#
# @asyncio.coroutine
# def buttonclicked(event):
#     if ('id' in event['event_object']['target']):
#         logging.info("BUTTON " + event['event_object']['target']['id'] + " CLICKED!")
#     else:
#         logging.info("BUTTON " + event['event_object']['target']['innerText'] + " CLICKED!")

logging.basicConfig(format="%(asctime)s [%(levelname)s] - %(funcName)s: %(message)s", level=logging.INFO)

app = vDom()
app.register('init', oninit)
app.register('load', onload)
# app.register('click', clicked)

app.start()
