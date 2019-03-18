import logging
import threading


def run_in_thread(fn):
    def run(*k, **kw):
        def wrapper():
            try:
                fn(*k, **kw)
            except Exception as e:
                logging.exception("Error in thread")
        t = threading.Thread(target=wrapper)
        t.start()
    return run