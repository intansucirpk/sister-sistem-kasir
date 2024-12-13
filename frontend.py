import grpc
import common_pb2
import common_pb2_grpc


def main():
    backend_port = "50051"  # Port backend server

    # Log port yang digunakan
    print(f"[INFO] Menghubungkan ke Backend server di port {backend_port}...")

    with grpc.insecure_channel(f"localhost:{backend_port}") as channel:
        stub = common_pb2_grpc.BackendStub(channel)

        # Input transaksi
        print("[INFO] Mengirim permintaan transaksi...")
        transaksi = common_pb2.TransactionRequest(id_barang=1, jumlah=2)
        response = stub.ProsesTransaksi(transaksi)

        # Hasil transaksi
        if response.success:
            print(
                f"[SUCCESS] Transaksi berhasil: {response.message}\n"
                f"Total Harga: {response.total_harga}\n"
                f"Diskon: {response.diskon}\n"
            )
        else:
            print(f"[ERROR] Transaksi gagal: {response.message}")


if __name__ == "__main__":
    print("[INFO] Client dimulai...")
    main()
