from datetime import datetime

# CLASS 1: KENDARAAN
class Kendaraan:

    jumlah_kendaraan = 0

    def __init__(self, kode, nama, jenis, harga_per_hari):
        self.kode = kode
        self.nama = nama
        self.jenis = jenis
        self.__harga_per_hari = 0
        self.harga_per_hari = harga_per_hari
        self.__tersedia = True

        Kendaraan.jumlah_kendaraan += 1

    # PROPERTY
    @property
    def harga_per_hari(self):
        return self.__harga_per_hari

    # SETTER
    @harga_per_hari.setter
    def harga_per_hari(self, harga):
        if harga <= 0:
            raise ValueError("Harga harus lebih dari 0")
        self.__harga_per_hari = float(harga)

    @property
    def tersedia(self):
        return self.__tersedia

    def ubah_status(self, status):
        self.__tersedia = status

    def tampilkan_info(self):
        status = "Tersedia" if self.tersedia else "Sedang disewa"

        return (
            f"{self.kode:<8} | {self.nama:<18} | "
            f"{self.jenis:<10} | "
            f"Rp{self.harga_per_hari:,.0f} | {status}"
        )

    # CLASS METHOD
    @classmethod
    def dari_data(cls, data):
        return cls(
            data["kode"],
            data["nama"],
            data["jenis"],
            data["harga_per_hari"]
        )

    # STATIC METHOD
    @staticmethod
    def format_rupiah(nominal):
        return f"Rp{nominal:,.0f}".replace(",", ".")

# CLASS 2: SISTEM RENTAL
class SistemRental:

    def __init__(self, nama_usaha):
        self.nama_usaha = nama_usaha
        self.__kendaraan = {}
        self.__transaksi = {}
        self.__nomor_transaksi = 1

    def tambah_kendaraan(self, kendaraan):
        if kendaraan.kode in self.__kendaraan:
            print("Kode kendaraan sudah digunakan.")
            return

        self.__kendaraan[kendaraan.kode] = kendaraan
        print("Kendaraan berhasil ditambahkan.")

    def tampilkan_kendaraan(self, hanya_tersedia=False):
        print("\n===== DAFTAR KENDARAAN =====")
        print("-" * 85)

        for kendaraan in self.__kendaraan.values():
            if not hanya_tersedia or kendaraan.tersedia:
                print(kendaraan.tampilkan_info())

        print("-" * 85)

    def sewa_kendaraan(self, kode, nama_penyewa, lama_hari):

        kendaraan = self.__kendaraan.get(kode)

        if kendaraan is None:
            print("Kendaraan tidak ditemukan.")
            return

        if not kendaraan.tersedia:
            print("Kendaraan sedang disewa.")
            return

        if not self.validasi_lama_sewa(lama_hari):
            print("Lama sewa minimal 1 hari.")
            return

        if not nama_penyewa.strip():
            print("Nama penyewa tidak boleh kosong.")
            return

        total = kendaraan.harga_per_hari * lama_hari

        nomor = f"TRX{self.__nomor_transaksi:03d}"
        self.__nomor_transaksi += 1

        self.__transaksi[nomor] = {
            "kendaraan": kendaraan,
            "nama_penyewa": nama_penyewa,
            "lama_hari": lama_hari,
            "total": total,
            "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "status": "Aktif"
        }

        kendaraan.ubah_status(False)

        print("\n===== PENYEWAAN BERHASIL =====")
        print("Nomor Transaksi :", nomor)
        print("Nama Penyewa    :", nama_penyewa)
        print("Kendaraan       :", kendaraan.nama)
        print("Lama Sewa       :", lama_hari, "hari")
        print("Total Biaya     :", Kendaraan.format_rupiah(total))

    def kembalikan_kendaraan(self, nomor_transaksi):

        transaksi = self.__transaksi.get(nomor_transaksi.upper())

        if transaksi is None:
            print("Nomor transaksi tidak ditemukan.")
            return

        if transaksi["status"] == "Selesai":
            print("Kendaraan sudah dikembalikan.")
            return

        transaksi["kendaraan"].ubah_status(True)
        transaksi["status"] = "Selesai"

        print("\nPengembalian berhasil!")
        print("Kendaraan :", transaksi["kendaraan"].nama)
        print("Pembayaran:", Kendaraan.format_rupiah(
            transaksi["total"]
        ))

    def tampilkan_transaksi(self):

        print("\n===== RIWAYAT TRANSAKSI =====")

        if not self.__transaksi:
            print("Belum ada transaksi.")
            return

        for nomor, data in self.__transaksi.items():
            print(
                nomor, "|",
                data["nama_penyewa"], "|",
                data["kendaraan"].nama, "|",
                data["lama_hari"], "hari |",
                Kendaraan.format_rupiah(data["total"]), "|",
                data["status"]
            )

    # STATIC METHOD
    @staticmethod
    def validasi_lama_sewa(lama_hari):
        return (
            isinstance(lama_hari, int)
            and not isinstance(lama_hari, bool)
            and lama_hari >= 1
        )

# PROGRAM UTAMA
def jalankan_program():

    rental = SistemRental("Rental Kendaraan Maju Jaya")

    # OBJECT KENDARAAN
    data_kendaraan = [
        {
            "kode": "M001",
            "nama": "Honda Beat",
            "jenis": "Motor",
            "harga_per_hari": 75000
        },
        {
            "kode": "M002",
            "nama": "Yamaha NMAX",
            "jenis": "Motor",
            "harga_per_hari": 120000
        },
        {
            "kode": "M003",
            "nama": "Toyota Avanza",
            "jenis": "Mobil",
            "harga_per_hari": 350000
        },
        {
            "kode": "M004",
            "nama": "Honda Brio",
            "jenis": "Mobil",
            "harga_per_hari": 300000
        }
    ]

    for data in data_kendaraan:
        kendaraan = Kendaraan.dari_data(data)
        rental.tambah_kendaraan(kendaraan)

    # MENU PROGRAM
    while True:

        print("\n================================")
        print("  SISTEM RENTAL KENDARAAN")
        print("  RENTAL MAJU JAYA")
        print("================================")
        print("1. Lihat Semua Kendaraan")
        print("2. Lihat Kendaraan Tersedia")
        print("3. Sewa Kendaraan")
        print("4. Pengembalian Kendaraan")
        print("5. Riwayat Transaksi")
        print("6. Keluar")
        print("================================")

        pilihan = input("Pilih Menu (1-6): ")

        if pilihan == "1":
            rental.tampilkan_kendaraan()

        elif pilihan == "2":
            rental.tampilkan_kendaraan(True)

        elif pilihan == "3":

            rental.tampilkan_kendaraan(True)

            kode = input("Masukkan Kode Kendaraan: ").upper()
            nama = input("Nama Penyewa: ")

            try:
                lama = int(input("Lama Sewa (hari): "))
                rental.sewa_kendaraan(kode, nama, lama)
            except ValueError:
                print("Input lama sewa harus berupa angka.")

        elif pilihan == "4":

            nomor = input("Masukkan Nomor Transaksi: ")
            rental.kembalikan_kendaraan(nomor)

        elif pilihan == "5":
            rental.tampilkan_transaksi()

        elif pilihan == "6":
            print("Terima kasih telah menggunakan sistem rental.")
            break

        else:
            print("Pilihan tidak valid!")

# MENJALANKAN PROGRAM
if __name__ == "__main__":
    jalankan_program()