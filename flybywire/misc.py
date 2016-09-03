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
    """
    @wraps(fn)
    def repeater(future):
        while not future.cancelled():
            yield from asyncio.sleep(interval)
            fn(*args)

    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    asyncio.ensure_future(repeater(future))
    return future

def clear_interval(task):
    """
    Stops a periodic function call setup using set_inteval()
    """
    loop = asyncio.get_event_loop()
    loop.call_soon_threadsafe(task.cancel)
