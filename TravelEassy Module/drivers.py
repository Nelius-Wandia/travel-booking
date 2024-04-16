import db_connection as db
from generals import Generals

generals = Generals()
x = generals.GenRandomCode(size=9)

class Drivers:
    def __init__(self):
        pass

    def create_drivers_table(self):
            sql_query = """CREATE TABLE IF NOT EXISTS drivers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                company_id int,
                gender varchar(255),
                name varchar(255),
                id_number int,
                email varchar(255),
                phone_number int ,
                driving_license varchar,
                status varchar(255),
                trips varchar(255),
                ratings int not null,
                updated_time timestamp not null default current_timestamp on update current_timestamp,
                created_time timestamp default current_timestamp
            )"""
            db.cursor.execute(sql_query)
            db.conn.commit()


    def add_driver(self, metadata):
            sql_query = "INSERT INTO drivers (name, email, license_number) VALUES (%s, %s, %s)"
            db.cursor.execute(sql_query, (metadata["name"], metadata["license_number"]))
            db.conn.commit()
            print("Driver added successfully")

    def edit_driver(self, driver_id, metadata):
            sql_query = "UPDATE drivers SET name = %s, license_number = %s WHERE id = %s"
            db.cursor.execute(sql_query, (metadata["name"], metadata["license_number"], driver_id))
            db.conn.commit()
            print("Driver updated successfully")

    def update_driver_details(self, driver_id, metadata):
            sql_query = "UPDATE drivers SET license_number = %s WHERE id = %s"
            db.cursor.execute(sql_query, (metadata["license_number"], driver_id))
            db.conn.commit()
            print("Driver details updated successfully")

    def delete_driver(self, driver_id):
            sql_query = "DELETE FROM drivers WHERE id = %s"
            db.cursor.execute(sql_query, (driver_id,))
            db.conn.commit()
            print("Driver deleted successfully")
