import grpc
from concurrent import futures
import sistem_kasir_pb2
import sistem_kasir_pb2_grpc
import mysql.connector

class BackendServicer(sistem_kasir_pb2_grpc.BackendServicer):
    def __init__(self):
        # Koneksi ke database MySQL
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",  # Ubah sesuai dengan username MySQL Anda
            password="",  # Ubah sesuai dengan password MySQL Anda
            database="sistem_kasir"  # Nama database yang Anda gunakan
        )
        self.cursor = self.db.cursor()

    def ProcessTransaction(self, request, context):
        try:
            # Query untuk menyimpan transaksi ke tabel sales_data
            query = """
                INSERT INTO sales_data (
                    Retailer, Retailer_ID, Invoice_Date, Region, State, City, 
                    Product, Price_per_Unit, Units_Sold, Total_Sales, 
                    Operating_Profit, Sales_Method
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                request.retailer,
                request.retailer_id,
                request.invoice_date,
                request.region,
                request.state,
                request.city,
                request.product,
                request.price_per_unit,
                request.units_sold,
                request.total_sales,
                request.operating_profit,
                request.sales_method,
            )

            # Eksekusi query
            self.cursor.execute(query, values)
            self.db.commit()

            return sistem_kasir_pb2.Response(
                status="SUCCESS",
                message="Transaction processed and saved to database."
            )
        except Exception as e:
            return sistem_kasir_pb2.Response(
                status="FAILURE",
                message=f"An error occurred: {e}"
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sistem_kasir_pb2_grpc.add_BackendServicer_to_server(BackendServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Backend server running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
