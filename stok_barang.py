import grpc
from concurrent import futures
import time
import kasir_pb2
import kasir_pb2_grpc
import mysql.connector

class StokBarang(kasir_pb2_grpc.BackendServicer):

    def __init__(self):
        # Koneksi ke database MySQL untuk stok barang
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sister_sistem_kasir"
        )
        self.cursor = self.db.cursor()

    def CheckStock(self, request, context):
        """Mengecek stok barang"""
        item = request.item
        self.cursor.execute("SELECT stok FROM stok_barang WHERE nama_barang = %s", (item,))
        result = self.cursor.fetchone()
        
        if result:
            stok = result[0]
            return kasir_pb2.StockResponse(item=item, stok=stok, message="Stok ditemukan")
        else:
            return kasir_pb2.StockResponse(item=item, stok=0, message="Barang tidak ditemukan")

    def UpdateStock(self, request, context):
        """Memperbarui stok barang setelah transaksi"""
        item = request.item
        jumlah = request.jumlah
        self.cursor.execute("SELECT stok FROM stok_barang WHERE nama_barang = %s", (item,))
        result = self.cursor.fetchone()
        
        if result:
            stok = result[0] - jumlah
            if stok < 0:
                return kasir_pb2.StockUpdateResponse(message="Stok tidak cukup")
            self.cursor.execute("UPDATE stok_barang SET stok = %s WHERE nama_barang = %s", (stok, item))
            self.db.commit()
            return kasir_pb2.StockUpdateResponse(message="Stok berhasil diperbarui")
        else:
            return kasir_pb2.StockUpdateResponse(message="Barang tidak ditemukan")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kasir_pb2_grpc.add_BackendServicer_to_server(StokBarang(), server)
    server.add_insecure_port('[::]:50052')  # Server akan berjalan di port 50052
    print("Stok Barang Server berjalan di port 50052...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
