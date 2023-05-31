import mysql.connector
connect = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='movieclub'
)

driver_path = r'C:\Users\artea\Downloads\chromedriver_win32\chromedriver'