import db_connection as db
from generals import Generals

generals = Generals()
x = generals.GenRandomCode(size=9)

class Drivers:
    def __init__(self, driver_id = None):
        self.driver_id = driver_id

    def create_drivers_table(self):
            sql_query = """CREATE TABLE IF NOT EXISTS drivers (
                id_number int primary key,
                company_id varchar(20),
                name varchar(255),
                gender varchar(255),
                email varchar(255),
                phone_number int,
                driving_license varchar(255),
                status boolean,
                trips int,
                updated_time timestamp not null default current_timestamp on update current_timestamp,
                created_time timestamp default current_timestamp,
                foreign key (company_id) references admin_users(id)
            )"""
            db.cursor.execute(sql_query)
            db.conn.commit()


    def add_driver(self, metadata):
            metadata = {
                "id_number": "12345678",
                "company_id" :"123",
                "name": "Roadways",
                "gender": "female",
                "email": "machariaandrew1428@gmail.com",
                "phone_number": 254795359098,
                "driving_license": "1234",
                "status": True,
                "trips": 0
            }
            sql_query = """INSERT INTO drivers (id_number, company_id, name, gender, email, phone_number, 
            driving_license, status, trips)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            db.cursor.execute(sql_query, (metadata["id_number"], metadata["company_id"], 
                                        metadata["name"], metadata["gender"], metadata["email"],
                                        metadata["phone_number"], metadata["driving_license"], 
                                        metadata["status"], metadata["trips"]))
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

x = Drivers()
x.create_drivers_table()
x.add_driver(metadata="")
