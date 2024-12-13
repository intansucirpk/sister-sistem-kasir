import grpc
from concurrent import futures
import mysql.connector
import common_pb2
import common_pb2_grpc


class StokBarangService(common_pb2_grpc.StokBarangServicer):
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="kasir_terdistribusi"
        )
        print("[INFO] Terhubung ke database 'kasir_terdistribusi'.")

    def UpdateStok(self, request, context):
        cursor = self.conn.cursor()
        cursor.execute("SELECT stok FROM barang WHERE id_barang = %s", (request.id_barang,))
        barang = cursor.fetchone()
        if not barang or barang[0] < request.jumlah_terjual:
            return common_pb2.StokUpdateResponse(success=False, message="Stok tidak cukup")

        cursor.execute(
            "UPDATE barang SET stok = stok - %s WHERE id_barang = %s",
            (request.jumlah_terjual, request.id_barang),
        )
        self.conn.commit()
        return common_pb2.StokUpdateResponse(success=True, message="Stok diperbarui")

    def AddStok(self, request, context):
        cursor = self.conn.cursor()
        cursor.execute("SELECT stok FROM barang WHERE id_barang = %s", (request.id_barang,))
        barang = cursor.fetchone()
        if not barang:
            return common_pb2.AddStokResponse(success=False, message="Barang tidak ditemukan")

        cursor.execute(
            "UPDATE barang SET stok = stok + %s WHERE id_barang = %s",
            (request.jumlah_tambah, request.id_barang),
        )
        self.conn.commit()
        return common_pb2.AddStokResponse(success=True, message="Stok berhasil ditambahkan")


def serve():
    server_port = "50052"

    # Log port yang digunakan
    print(f"[INFO] Server gRPC Stok Barang berjalan di port {server_port}.")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    common_pb2_grpc.add_StokBarangServicer_to_server(StokBarangService(), server)
    server.add_insecure_port(f"[::]:{server_port}")
    server.start()
    print(f"[SUCCESS] Stok Barang berjalan dan mendengarkan permintaan di port {server_port}.")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
