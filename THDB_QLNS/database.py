import pyodbc


def connect_db():
    drivers = [
        "ODBC Driver 18 for SQL Server",
        "ODBC Driver 17 for SQL Server",
        "SQL Server",
    ]

    last_error = None
    for driver in drivers:
        connection_string = (
            f"DRIVER={{{driver}}};"
            "SERVER=.;"
            "DATABASE=QUANLYNHANSU;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        try:
            return pyodbc.connect(connection_string)
        except Exception as exc:
            last_error = exc

    raise ConnectionError(
        "Khong ket noi duoc SQL Server. Kiem tra ten SERVER, database QUANLYNHANSU, "
        "hoac cai ODBC Driver 17/18 for SQL Server."
    ) from last_error
