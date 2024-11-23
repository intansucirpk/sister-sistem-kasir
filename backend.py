import grpc
from concurrent import futures
import time
import kasir_pb2
import kasir_pb2_grpc
import mysql.connector
from mysql.connector import Error

# Koneksi ke database MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Sesuaikan dengan user MySQL Anda
            password='',  # Sesuaikan dengan password MySQL Anda
            database='sister_sistem_kasir'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

class Backend(kasir_pb2_grpc.BackendServicer):
    # Implementasi RPC: ProcessTransaction
    def ProcessTransaction(self, request, context):
        item = request.item
        jumlah = request.jumlah
        harga_per_unit = request.harga_per_unit
        
        # Hitung total harga, diskon, pajak, dan harga akhir
        total_harga = harga_per_unit * jumlah
        diskon = 0.1 * total_harga  # Contoh diskon 10%
        pajak = 0.05 * total_harga  # Contoh pajak 5%
        harga_akhir = total_harga - diskon + pajak
        
        # Masukkan transaksi ke database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO transaksi (item, jumlah, harga_per_unit, total_harga, diskon, pajak, harga_akhir) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (item, jumlah, harga_per_unit, total_harga, diskon, pajak, harga_akhir)
            )
            connection.commit()
            cursor.close()
            connection.close()

        return kasir_pb2.TransactionResponse(
            total_harga=total_harga,
            diskon=diskon,
            pajak=pajak,
            harga_akhir=harga_akhir,
            message="Transaksi berhasil diproses"
        )

    # Implementasi RPC: UpdateStock
    def UpdateStock(self, request, context):
        item = request.item
        jumlah = request.jumlah
        
        # Update stok barang di database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE stok_barang SET stok = stok - %s WHERE nama_barang = %s", (jumlah, item))
            connection.commit()
            cursor.close()
            connection.close()
        
        return kasir_pb2.StockUpdateResponse(message=f"Stok untuk {item} telah diperbarui.")

    # Implementasi RPC: CheckStock
    def CheckStock(self, request, context):
        item = request.item
        
        # Mengecek stok barang di database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT stok FROM stok_barang WHERE nama_barang = %s", (item,))
            stok = cursor.fetchone()
            cursor.close()
            connection.close()
        
        if stok:
            return kasir_pb2.StockResponse(item=item, stok=stok[0], message="Stok tersedia")
        else:
            return kasir_pb2.StockResponse(item=item, stok=0, message="Barang tidak ditemukan")

    # Implementasi RPC: GetTransactionReport
    def GetTransactionReport(self, request, context):
        """Mengambil laporan transaksi berdasarkan tanggal"""
        start_date = request.start_date
        end_date = request.end_date
        connection = get_db_connection()
        
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id, item, jumlah, harga_akhir, tanggal_transaksi
                FROM transaksi
                WHERE tanggal_transaksi BETWEEN %s AND %s
            """, (start_date, end_date))
            result = cursor.fetchall()
            cursor.close()
            connection.close()

            transaksi_list = []
            for row in result:
                transaksi = kasir_pb2.Transaction(
                    id=row[0],
                    item=row[1],
                    jumlah=row[2],
                    harga_akhir=row[3],
                    tanggal_transaksi=row[4].strftime('%Y-%m-%d %H:%M:%S')  # Format tanggal
                )
                transaksi_list.append(transaksi)

            return kasir_pb2.TransactionReport(transaksi=transaksi_list)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kasir_pb2_grpc.add_BackendServicer_to_server(Backend(), server)
    server.add_insecure_port('[::]:50051')
    print("Server berjalan di port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
