import mysql.connector
conn = mysql.connector.connect(
            host="127.0.0.1",   # Replace with your database host
            user="Andrew",   # Replace with your database username
            password="andrew",   # Replace with your database password
            database="traveazzy"    # Replace with your database name
        )
cursor = conn.cursor()