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
            "company_id" :"DeR#G#DCbc",
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
        # print("Driver added successfully")

        
    def edit_driver(self, driver_id, metadata):
        # Extract relevant fields from metadata
        name = metadata.get("name")
        gender = metadata.get("gender")
        id_number = metadata.get("id_number")
        phone_number = metadata.get("phone_number")
        email = metadata.get("email")
        license_number = metadata.get("driving_license")

        # Check if any of the fields are provided for update
        if not any([name, gender, id_number, phone_number, email, license_number]):
            print("No fields provided for update.")
            return

        # Construct SQL query for updating provided fields
        sql_query = "UPDATE drivers SET "
        update_values = []

        if name:
            sql_query += "name = %s, "
            update_values.append(name)
        if gender:
            sql_query += "gender = %s, "
            update_values.append(gender)
        if id_number:
            sql_query += "id_number = %s, "
            update_values.append(id_number)
        if phone_number:
            sql_query += "phone_number = %s, "
            update_values.append(phone_number)
        if email:
            sql_query += "email = %s, "
            update_values.append(email)
        if license_number:
            sql_query += "driving_license = %s, "
            update_values.append(license_number)

        # Remove trailing comma and space from SQL query
        sql_query = sql_query.rstrip(", ")

        # Add WHERE clause for specific driver_id
        sql_query += " WHERE id_number = %s"
        update_values.append(driver_id)

        # Execute the update query
        db.cursor.execute(sql_query, tuple(update_values))
        db.conn.commit()



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
