"""Module untuk mengelola perangkat jaringan."""

from tabulate import tabulate
from net_ops.device import DeviceTimeoutError, AuthenticationError


class NetworkManager:
    """
    Controller untuk mengelola perangkat jaringan.
    """

    def __init__(self):
        """Inisialisasi list perangkat dan riwayat."""
        self.registered_devices = []
        self.task_history = []

    def add_device(self, device):
        """
        Menambahkan perangkat ke inventory.
        """

        # Validasi IP duplikat
        for d in self.registered_devices:
            if d.ip_address == device.ip_address:
                print("Error: IP Address sudah digunakan!")
                return

        self.registered_devices.append(device)

        print(f"[SUCCESS] Perangkat baru diregistrasi: "
              f"{device.hostname}")

    def check_all_devices(self, device_type=None):
        """
        Melakukan pengecekan perangkat.
        """

        if not self.registered_devices:
            print("Inventory kosong!")
            return

        table_data = []

        for device in self.registered_devices:

            # Filter tipe perangkat
            if (
                device_type == "router" and
                device.__class__.__name__ != "RouterDevice"
            ):
                continue

            if (
                device_type == "switch" and
                device.__class__.__name__ != "SwitchDevice"
            ):
                continue

            try:
                # Pengecekan status perangkat
                status = device.check_status()

            except DeviceTimeoutError as e:

                status = "[FAILED] (DeviceTimeoutError)"

                print(f"[ERROR] DeviceTimeoutError: {e}")

                print(
                    ">> ACTION: "
                    "Cek koneksi kabel fisik / "
                    "Port link status..."
                )

            except AuthenticationError as e:

                status = "[FAILED] (AuthenticationError)"

                print(f"[ERROR] AuthenticationError: {e}")

                print(
                    ">> ACTION: "
                    "Kirim permintaan reset "
                    "kredensial ke Admin..."
                )

            else:
                print(status)

            # Simpan ke tabel
            table_data.append([
                device.ip_address,
                device.hostname,
                status
            ])

            # =========================
            # AUTO SAVE AUDIT LOG
            # =========================

            # Data untuk riwayat (dengan IP)
            history_data = (
                f"{device.hostname}|"
                f"{device.ip_address}|"
                f"{status}"
            )

            # Data untuk file txt (tanpa IP)
            log_data = f"{device.hostname}|{status}"

            # Simpan ke list riwayat
            self.task_history.append(history_data)

            # Simpan ke file audit log
            with open("network_audit_log.txt", "a") as file:
                file.write(log_data + "\n")

            print(
                ">> (Sistem otomatis menyimpan "
                "baris log ke dalam "
                "'network_audit_log.txt')"
            )

        print("\n=== HASIL PENGECEKAN ===\n")

        print(tabulate(
            table_data,
            headers=["IP Address", "Hostname", "Status"],
            tablefmt="grid"
        ))

    def show_history(self):
        """Menampilkan riwayat pengecekan."""

        if not self.task_history:
            print("Belum ada riwayat.")
            return

        print("\n=== RIWAYAT ===")

        for data in self.task_history:
            print(data)

    def find_failed_devices(self):
        """
        Generator mencari perangkat gagal.
        """

        for history in self.task_history:

            if (
                "[FAILED]" in history or
                "[ERROR]" in history
            ):
                yield history

    # =========================
    # FILE I/O READ
    # =========================
    def read_audit_log(self):
        """
        Membaca seluruh isi audit log.
        """

        try:
            with open("network_audit_log.txt", "r") as file:
                logs = file.readlines()

            return logs

        except FileNotFoundError:
            print("File audit log belum tersedia.")
            return []

    # =========================
    # FILTER + LAMBDA
    # =========================
    def filter_failed_logs(self):
        """
        Menyaring log gagal menggunakan
        filter() dan lambda.
        """

        logs = self.read_audit_log()

        failed_logs = list(filter(
            lambda line:
            "[FAILED]" in line or "[ERROR]" in line,
            logs
        ))

        return failed_logs

    # =========================
    # LAPORAN INSIDEN
    # =========================
    def print_incident_report(self):
        """
        Menampilkan laporan insiden jaringan.
        """

        print("\n--- MENYUSUN LAPORAN INSIDEN JARINGAN ---")

        print("Membaca file database "
              "'network_audit_log.txt'...")

        failed_logs = self.filter_failed_logs()

        print("Menerapkan Lambda Filter...")

        print("\n>> HASIL FILTER PERANGKAT BERMASALAH:")

        if not failed_logs:
            print("[INFO] Tidak ada perangkat bermasalah.")
            return

        nomor = 1

        for log in failed_logs:

            # Pisahkan hostname dan status
            parts = log.strip().split("|")

            hostname = parts[0]
            status = parts[1]

            # Hapus label FAILED dari status
            status = status.replace(
                "[FAILED] ",
                ""
            )

            print(
                f"{nomor}. "
                f"[FAILED] "
                f"{hostname} "
                f"{status}"
            )

            nomor += 1

        print(
            f"\n[INFO] Laporan selesai dicetak. "
            f"Total: {len(failed_logs)} "
            "insiden tercatat di database."
        )
