from flask import Flask, render_template, request
import mysql.connector
import grpc
import common_pb2
import common_pb2_grpc

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Ganti dengan password MySQL Anda
    'database': 'kasir_terdistribusi'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    print(f"[INFO] Memproses permintaan GET/POST untuk halaman utama (page={page})")

    try:
        # Koneksi ke database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Hitung total data untuk pagination
        cursor.execute("SELECT COUNT(*) FROM barang")
        total_data = cursor.fetchone()[0]

        # Menghitung total halaman
        total_pages = (total_data + per_page - 1) // per_page

        # Ambil data dengan limit dan offset
        cursor.execute(
            "SELECT id_barang, nama_barang, stok, harga FROM barang LIMIT %s OFFSET %s",
            (per_page, offset)
        )
        data_barang = cursor.fetchall()

        print(f"[INFO] Data barang berhasil diambil, total data: {total_data}")
    except mysql.connector.Error as err:
        print(f"[ERROR] Koneksi database gagal: {err}")
        data_barang = []
        total_pages = 1
    finally:
        if conn.is_connected():
            conn.close()

    if request.method == 'POST':
        try:
            id_barang = int(request.form['id_barang'])
            jumlah = int(request.form['jumlah'])

            # Koneksi ke server gRPC (Backend)
            print("[INFO] Menghubungkan ke Backend gRPC server di port 50051...")
            with grpc.insecure_channel("localhost:50051") as channel:
                stub = common_pb2_grpc.BackendStub(channel)
                transaksi = common_pb2.TransactionRequest(id_barang=id_barang, jumlah=jumlah)
                response = stub.ProsesTransaksi(transaksi)

            print(f"[SUCCESS] Transaksi diproses: {response.message}, Total Harga: {response.total_harga}")
            return render_template(
                'result.html',
                message=response.message,
                total_harga=response.total_harga,
                diskon=response.diskon,
            )
        except Exception as e:
            print(f"[ERROR] Terjadi kesalahan saat memproses transaksi: {e}")
            return render_template('index.html', error="Terjadi kesalahan saat memproses transaksi.")

    return render_template(
        'index.html',
        page=page,
        total_pages=total_pages,
        data_barang=data_barang,
    )

@app.route('/tambah_stok', methods=['POST'])
def tambah_stok():
    try:
        id_barang = int(request.form['id_barang'])
        jumlah_tambah = int(request.form['jumlah_tambah'])

        print("[INFO] Menghubungkan ke Stok Barang gRPC server di port 50052...")
        with grpc.insecure_channel("localhost:50052") as channel:
            stub = common_pb2_grpc.StokBarangStub(channel)
            tambah_stok_request = common_pb2.StokUpdateRequest(
                id_barang=id_barang, jumlah_terjual=-jumlah_tambah
            )  # negative to add stock
            response = stub.UpdateStok(tambah_stok_request)

        print(f"[SUCCESS] Stok berhasil diperbarui: {response.message}")

        # Ambil data barang terbaru setelah stok ditambah
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT id_barang, nama_barang, stok, harga FROM barang")
        data_barang = cursor.fetchall()
        conn.close()

        return render_template('index.html', message=response.message, data_barang=data_barang)
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat menambah stok: {e}")
        return render_template('index.html', error="Terjadi kesalahan saat menambah stok.")

if __name__ == "__main__":
    flask_port = 5000
    print(f"[INFO] Flask server berjalan di http://localhost:{flask_port}")
    app.run(host="localhost", port=flask_port, debug=True)
