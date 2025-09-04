import time
from contextlib import contextmanager


@contextmanager
def timer(label: str):
    start = time.time()
    try:
        yield
    finally:
        dur = (time.time() - start) * 1000
        print(f"{label} took {dur:.1f} ms")
