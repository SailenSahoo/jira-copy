
import oracledb

def get_db_connection():
    dsn = oracledb.makedsn("your_host", 1521, service_name="your_service")
    connection = oracledb.connect(user="your_user", password="your_password", dsn=dsn)
    return connection
