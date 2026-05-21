"""Program utama untuk Network Automation Task Simulator."""

from net_ops.device import RouterDevice, SwitchDevice
from net_ops.manager import NetworkManager


def tampilkan_header():
    """Menampilkan header informasi program."""
    print("=== NETWORK AUTOMATION TASK SIMULATOR ===")
    print("Nama  : Fandika Nugraha")
    print("NPM   : 25782097 ")
    print("Lab   : Session 8")
    print("Topik : Data Persistence (File I/O) & Lambda Functions")


def tampilkan_menu():
    """Menampilkan menu utama program."""
    print("\n1. Tambah Perangkat Jaringan")
    print("2. Cek Status Router")
    print("3. Cek Status Switch")
    print("4. Lihat Riwayat Automasi")
    print("5. Cari Perangkat Bermasalah")
    print("6. Cetak Laporan Insiden Jaringan")
    print("7. Keluar")


# =========================
# CLOSURE
# =========================
def hostname_factory(kode_lokasi):
    """
    Membuat fungsi generator hostname berbasis lokasi.

    Args:
        kode_lokasi (str): Kode lokasi (contoh: GKB)

    Returns:
        function: Fungsi untuk menghasilkan hostname
    """

    def generate_name(tipe_perangkat, id_perangkat):
        """
        Menghasilkan hostname dengan format:
        <LOKASI>-<TIPE>-<ID>

        Args:
            tipe_perangkat (str): Jenis perangkat (router/switch)
            id_perangkat (str): ID perangkat

        Returns:
            str: Hostname perangkat
        """
        return f"{kode_lokasi}-{tipe_perangkat.upper()}-{id_perangkat}"

    return generate_name


# Inisialisasi closure
gkb_namer = hostname_factory("GKB")


def main():
    """
    Fungsi utama untuk menjalankan program.
    """
    tampilkan_header()

    # Inisialisasi controller
    manager = NetworkManager()

    while True:
        tampilkan_menu()
        pilihan = input("Masukkan pilihan(1/2/3/4/5/6/7): ")

        if pilihan == "1":

            tipe = (
                input(">> Masukkan tipe perangkat (Router/Switch): ")
                .strip()
                .lower()
            )

            id_perangkat = input(">> Masukkan ID: ").strip()

            ip = input(">> Masukkan IP Address: ").strip()

            # Generate hostname otomatis
            hostname = gkb_namer(tipe, id_perangkat)

            # Membuat object sesuai tipe
            if tipe == "router":
                device = RouterDevice(hostname, ip)

            elif tipe == "switch":
                device = SwitchDevice(hostname, ip)

            else:
                print("Tipe tidak valid!")
                continue

            # Menambahkan perangkat
            manager.add_device(device)

        elif pilihan == "2":
            manager.check_all_devices("router")

        elif pilihan == "3":
            manager.check_all_devices("switch")

        elif pilihan == "4":
            manager.show_history()

        elif pilihan == "5":

            print("\n--- MENCARI PERANGKAT BERMASALAH ---")

            gen = manager.find_failed_devices()

            try:
                while True:
                    data = next(gen)
                    print(f"Ditemukan error: {data}")

                    input(
                        ">> Tekan [ENTER] "
                        "untuk mencari error berikutnya..."
                    )

            except StopIteration:
                print(
                    "[INFO] Pencarian selesai. "
                    "Tidak ada perangkat bermasalah lainnya."
                )

        elif pilihan == "6":
            manager.print_incident_report()

        elif pilihan == "7":
            print("Keluar Program...")
            break

        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()
