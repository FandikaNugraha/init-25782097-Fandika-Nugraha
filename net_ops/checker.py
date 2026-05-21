"""
Module: checker.py
Deskripsi: Berisi fungsi simulasi status perangkat dengan Exception Handling.
"""

import random


def check_router_status():
    """
    Menghasilkan status router secara acak dengan simulasi kegagalan koneksi.
    """
    # Simulasi peluang 20%
    if random.randint(1, 100) <= 20:
        raise ConnectionError(
            "Connection Timeout: Destination Host Unreachable")

    status = ["UP", "DOWN"]
    return random.choice(status)


def check_switch_status():
    """
    Menghasilkan status switch secara acak dengan simulasi kegagalan koneksi.
    """
    if random.randint(1, 100) <= 20:
        raise ConnectionError(
            "Connection Timeout: Destination Host Unreachable")

    status = ["UP", "DOWN"]
    return random.choice(status)
