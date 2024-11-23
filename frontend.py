import grpc
import kasir_pb2
import kasir_pb2_grpc

def run():
    # Membuat channel dan stub untuk menghubungi server gRPC
    channel = grpc.insecure_channel('localhost:50051')
    stub = kasir_pb2_grpc.BackendStub(channel)

    # Mempersiapkan data transaksi
    item = "Barang A"
    jumlah = 2
    harga_per_unit = 100000  # Harga per unit barang A

    # Mengecek stok terlebih dahulu
    stok_request = kasir_pb2.StockQuery(item=item)
    try:
        stok_response = stub.CheckStock(stok_request)
        print(f"Stok untuk {item}: {stok_response.stok}")

        if stok_response.stok >= jumlah:
            # Mengirimkan transaksi ke server jika stok cukup
            transaksi = kasir_pb2.TransactionRequest(
                item=item,
                jumlah=jumlah,
                harga_per_unit=harga_per_unit
            )

            response = stub.ProcessTransaction(transaksi)
            print(f"Total Harga: {response.total_harga}")
            print(f"Diskon: {response.diskon}")
            print(f"Pajak: {response.pajak}")
            print(f"Harga Akhir: {response.harga_akhir}")
            print(f"Pesan: {response.message}")

            # Mengirimkan informasi ke server untuk update stok
            stok_update = kasir_pb2.StockUpdateRequest(item=item, jumlah=jumlah)
            response_stok = stub.UpdateStock(stok_update)
            print(response_stok.message)
        else:
            print(f"Stok tidak cukup untuk {item}!")
    except grpc.RpcError as e:
        print(f"Error saat berkomunikasi dengan server: {e}")

if __name__ == '__main__':
    run()
