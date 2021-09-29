import ftplib
from decouple import config

FTP_HOST = "ftp.dlptest.com"
FTP_USER = config("USERNAME")
FTP_PASS = config("PASSWORD")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import ftplib

    FTP_HOST = "ftp.dlptest.com"

    FTP_USER = "dlpuser"

    FTP_PASS = "rNrKYTX9g7z3RgJRmxWuGHbeu"

    ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
