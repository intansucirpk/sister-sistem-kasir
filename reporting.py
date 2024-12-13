import grpc
import common_pb2
import common_pb2_grpc


def main():
    backend_port = "50051"  # Port backend server

    # Log port yang digunakan
    print(f"[INFO] Menghubungkan ke Backend server di port {backend_port}...")

    with grpc.insecure_channel(f"localhost:{backend_port}") as channel:
        stub = common_pb2_grpc.BackendStub(channel)

        print("Pilih jenis laporan:")
        print("1. Harian")
        print("2. Mingguan")

        pilihan = input("Masukkan pilihan (1/2): ")
        periode = "harian" if pilihan == "1" else "mingguan"

        # Kirim permintaan laporan
        request = common_pb2.LaporanRequest(periode=periode)
        response = stub.AmbilLaporan(request)

        if response.laporan:
            print(f"\n[LAPORAN] Laporan {periode.capitalize()}:")
            for item in response.laporan:
                print(item)
        else:
            print(f"\n[TIDAK ADA DATA] Tidak ada transaksi pada periode {periode.capitalize()}.")


if __name__ == "__main__":
    print("[INFO] Client dimulai...")
    main()
