import asyncio
from functools import wraps

def set_interval(fn, interval, args=()):
    """
    Calls a function periodically (assuming there is already an asyncio event
    loop running)

    fn: Function to be called
    interval: Period in seconds
    args: Tuple of arguments to be passed in

    Returns an asyncio.Future object

    Ref: http://stackoverflow.com/a/37512537/538379
    """
    @wraps(fn)
    @asyncio.coroutine
    def repeater():
        while True:
            yield from asyncio.sleep(interval)
            fn(*args)

    loop = asyncio.get_event_loop()
    task = asyncio.Task(repeater())
    return task

def clear_interval(task):
    """
    Stops a periodic function call setup using set_inteval()
    """
    def stopper():
        task.cancel()

    loop = asyncio.get_event_loop()
    loop.call_soon(stopper)
