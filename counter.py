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
    i = 1
    while True:
        yield from asyncio.sleep(1)
        vdom = {"t":3,"tn":"DIV","p":{"style":{"textAlign":"center","lineHeight":str(100+i)+"px","border":"1px solid red","width":str(100+i)+"px","height":str(100+i)+"px"}},"c":[{"t":1,"x":str(i)}]}
        app.render(vdom)
        i += 1

    return

logging.basicConfig(format="%(asctime)s [%(levelname)s] - %(funcName)s: %(message)s", level=logging.INFO)

app = vDom()
app.register('init', oninit)
app.register('load', onload)
# app.register('click', clicked)

app.start()
