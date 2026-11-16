"""Bound concurrent local Docker builds across Parsarium worker processes."""

from contextlib import contextmanager
import fcntl
import os
from pathlib import Path
import tempfile
import time


SLOTS = 3
LOCKS = Path(tempfile.gettempdir()) / f"parsarium-docker-build-slots-{os.getuid()}"


@contextmanager
def docker_build_slot():
    LOCKS.mkdir(parents=True, exist_ok=True)
    while True:
        for index in range(SLOTS):
            handle = (LOCKS / str(index)).open("w")
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                handle.close()
                continue
            try:
                yield
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)
                handle.close()
            return
        time.sleep(0.5)
