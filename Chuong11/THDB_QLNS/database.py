import pyodbc


def connect_db():
    drivers = [
        (
            "ODBC Driver 18 for SQL Server",
            [
                "DRIVER={ODBC Driver 18 for SQL Server};"
                "SERVER=.;"
                "DATABASE=QUANLYNHANSU;"
                "Trusted_Connection=yes;"
                "TrustServerCertificate=yes;",
                "DRIVER={ODBC Driver 18 for SQL Server};"
                "SERVER=.;"
                "DATABASE=QUANLYNHANSU;"
                "Trusted_Connection=yes;"
                "Encrypt=no;",
            ],
        ),
        (
            "ODBC Driver 17 for SQL Server",
            [
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=.;"
                "DATABASE=QUANLYNHANSU;"
                "Trusted_Connection=yes;"
                "TrustServerCertificate=yes;",
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=.;"
                "DATABASE=QUANLYNHANSU;"
                "Trusted_Connection=yes;"
                "Encrypt=no;",
            ],
        ),
        (
            "SQL Server",
            [
                "DRIVER={SQL Server};"
                "SERVER=.;"
                "DATABASE=QUANLYNHANSU;"
                "Trusted_Connection=yes;",
            ],
        ),
    ]

    last_error = None
    for _, connection_strings in drivers:
        for connection_string in connection_strings:
            try:
                return pyodbc.connect(connection_string)
            except Exception as exc:
                last_error = exc

    raise ConnectionError(
        "Khong ket noi duoc SQL Server. Kiem tra SQL Server local, database QUANLYNHANSU "
        "va ODBC Driver 17/18 hoac SQL Server driver tren may."
    ) from last_error
