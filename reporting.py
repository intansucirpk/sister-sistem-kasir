import grpc
import kasir_pb2
import kasir_pb2_grpc
from datetime import datetime

def run():
    # Membuat channel dan stub untuk menghubungi server gRPC
    channel = grpc.insecure_channel('localhost:50051')  # Ganti dengan alamat server Anda
    stub = kasir_pb2_grpc.BackendStub(channel)

    # Mengambil laporan transaksi antara tanggal tertentu
    start_date = "2024-11-01"
    end_date = "2024-11-30"

    # Membuat request untuk transaksi antara start_date dan end_date
    transaksi_request = kasir_pb2.TransactionQuery(start_date=start_date, end_date=end_date)
    
    try:
        # Mengirim request dan menerima response dari server gRPC
        transaksi_response = stub.GetTransactionReport(transaksi_request)

        # Menampilkan laporan transaksi
        print(f"Laporan Penjualan dari {start_date} hingga {end_date}")
        print("====================================")
        
        # Iterasi melalui transaksi yang ada dalam response
        for transaksi in transaksi_response.transaksi:
            print(f"ID Transaksi: {transaksi.id}")
            print(f"Item: {transaksi.item}")
            print(f"Jumlah: {transaksi.jumlah}")
            print(f"Harga Akhir: {transaksi.harga_akhir}")
            print(f"Tanggal: {transaksi.tanggal_transaksi}")
            print("-" * 40)
    except grpc.RpcError as e:
        print(f"Error saat mengambil laporan: {e}")

if __name__ == '__main__':
    run()
