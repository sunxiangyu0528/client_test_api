import time

import pytest
from _pytest.capture import CaptureManager


def manual_step(info):
    capture_manager = CaptureManager("no")
    capture_manager.suspend_global_capture(in_=True)

    while True:
        result = input(info + "  Result:").lower()

        if result in ['fail', 'block', 'j', 'l']:
            comments = input('Comments:')
            if comments:
                break
        elif result in ['pass', 'k']:
            break

    capture_manager.resume_global_capture()

    if result == 'fail' or result == 'j':
        pytest.fail(comments)
    elif result == 'block' or result == 'l':
        pytest.skip(comments)