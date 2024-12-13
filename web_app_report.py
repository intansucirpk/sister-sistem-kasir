from flask import Flask, render_template, request, redirect, url_for
import grpc
import common_pb2
import common_pb2_grpc

app = Flask(__name__, template_folder='templates2')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        periode = request.form['periode']
        print(f"[INFO] Periode laporan dipilih: {periode}")
        
        # Redirect to the result page with the selected period
        return redirect(url_for('hasil_laporan', periode=periode, page=1))

    print("[INFO] Halaman form laporan (GET)")
    return render_template('report.html')

@app.route('/hasil_laporan')
def hasil_laporan():
    periode = request.args.get('periode')
    current_page = int(request.args.get('page', 1))
    
    print(f"[INFO] Mengambil laporan periode '{periode}' untuk halaman {current_page}")
    
    try:
        # Connect to gRPC server (Backend)
        print("[INFO] Menghubungkan ke Backend gRPC server di port 50051...")
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = common_pb2_grpc.BackendStub(channel)
            laporan_request = common_pb2.LaporanRequest(periode=periode)
            response = stub.AmbilLaporan(laporan_request)
        
        laporan = response.laporan
        print(f"[SUCCESS] Laporan berhasil diambil. Total item laporan: {len(laporan)}")

        items_per_page = 10
        total_pages = min((len(laporan) // items_per_page) + (1 if len(laporan) % items_per_page > 0 else 0), 3)
        
        # Paginate laporan list (slice the report list for the current page)
        start = (current_page - 1) * items_per_page
        end = start + items_per_page
        laporan = laporan[start:end]
        
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat mengambil laporan: {e}")
        laporan = []
        total_pages = 1

    return render_template('hasil_laporan.html', laporan=laporan, total_pages=total_pages, current_page=current_page)

if __name__ == "__main__":
    flask_port = 50054
    print(f"[INFO] Flask server berjalan di http://localhost:{flask_port}")
    app.run(host="localhost", port=flask_port, debug=True)
