import grpc
import sistem_kasir_pb2
import sistem_kasir_pb2_grpc

def input_transaction():
    # Membuat saluran komunikasi ke server Backend
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = sistem_kasir_pb2_grpc.BackendStub(channel)

        # Meminta input dari pengguna
        retailer = input("Masukkan nama retailer: ")
        retailer_id = int(input("Masukkan ID retailer: "))
        invoice_date = input("Masukkan tanggal invoice (YYYY-MM-DD): ")
        region = input("Masukkan wilayah/region: ")
        state = input("Masukkan nama negara bagian (state): ")
        city = input("Masukkan nama kota: ")
        product = input("Masukkan nama produk: ")
        price_per_unit = float(input("Masukkan harga per unit produk: "))
        units_sold = int(input("Masukkan jumlah unit yang terjual: "))
        total_sales = price_per_unit * units_sold
        operating_profit = float(input("Masukkan keuntungan operasi: "))
        sales_method = input("Masukkan metode penjualan (e.g., Online, Offline): ")

        # Membuat objek transaksi
        transaction = sistem_kasir_pb2.Transaction(
            retailer=retailer,
            retailer_id=retailer_id,
            invoice_date=invoice_date,
            region=region,
            state=state,
            city=city,
            product=product,
            price_per_unit=price_per_unit,
            units_sold=units_sold,
            total_sales=total_sales,
            operating_profit=operating_profit,
            sales_method=sales_method
        )

        # Mengirim transaksi ke server Backend
        response = stub.ProcessTransaction(transaction)

        # Menampilkan respons dari server Backend
        print(f"\nStatus: {response.status}")
        print(f"Message: {response.message}")

if __name__ == "__main__":
    input_transaction()
