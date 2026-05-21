"""Module untuk representasi perangkat jaringan."""

import random


class DeviceTimeoutError(Exception):
    """Exception untuk timeout koneksi."""
    pass


class AuthenticationError(Exception):
    """Exception untuk gagal autentikasi."""
    pass


class NetworkDevice:
    """
    Parent class perangkat jaringan.
    """

    def __init__(self, hostname, ip_address):
        """
        Inisialisasi perangkat jaringan.

        Args:
            hostname (str): Nama perangkat
            ip_address (str): IP Address perangkat
        """

        self.hostname = hostname
        self.ip_address = ip_address
        self.status = "UNKNOWN"

    def check_status(self):
        """
        Simulasi pengecekan perangkat.
        """

        # Simulasi timeout
        if random.randint(1, 100) <= 20:
            raise DeviceTimeoutError(
                "Destination Host Unreachable"
            )

        # Simulasi auth gagal
        if random.randint(1, 100) <= 20:
            raise AuthenticationError(
                "Kredensial SSH ditolak"
            )

        return "PING OK"


class RouterDevice(NetworkDevice):
    """Class Router."""

    def check_status(self):
        """
        Mengecek status router.
        """

        parts = self.hostname.split("-")
        short_name = f"{parts[0]}{parts[2]}"

        print(f"Mengecek Router-{short_name}...")

        base_status = super().check_status()

        routes = random.randint(10, 50)

        result = (
            f"[SUCCESS] {base_status} | "
            f"Routing OSPF | Routes: {routes}"
        )

        self.status = result

        return result


class SwitchDevice(NetworkDevice):
    """Class Switch."""

    def check_status(self):
        """
        Mengecek status switch.
        """

        parts = self.hostname.split("-")
        short_name = f"{parts[0]}{parts[2]}"

        print(f"Mengecek Switch-{short_name}...")

        base_status = super().check_status()

        vlan = random.randint(2, 10)

        result = (
            f"[SUCCESS] {base_status} | "
            f"STP Forwarding | VLAN: {vlan}"
        )

        self.status = result

        return result
