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
                company_id INT,
                gender VARCHAR(255),
                name VARCHAR(255) NOT NULL,
                id_number INT NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone_number INT NOT NULL,
                driving_license VARCHAR(20) NOT NULL,
                status VARCHAR(255) NOT NULL,
                trips VARCHAR(255) NOT NULL,
                ratings INT NOT NULL,

                updated_at TIMESTAMP
            )"""
            db.cursor.execute(sql_query)
            db.conn.commit()
            # print("Drivers table created successfully")
            # print(f"Error creating drivers table: {err}")

    def add_driver(self, metadata):
        # try:
            sql_query = "INSERT INTO drivers (name, email, license_number) VALUES (%s, %s, %s)"
            db.cursor.execute(sql_query, (metadata["name"], metadata["license_number"]))
            db.conn.commit()
            print("Driver added successfully")
        # except mysql.connector.Error as err:
        #     print(f"Error adding driver: {err}")

    def edit_driver(self, driver_id, metadata):
        # try:
            sql_query = "UPDATE drivers SET name = %s, license_number = %s WHERE id = %s"
            db.cursor.execute(sql_query, (metadata["name"], metadata["license_number"], driver_id))
            db.conn.commit()
            print("Driver updated successfully")
        # except mysql.connector.Error as err:
        #     print(f"Error editing driver: {err}")

    def update_driver_details(self, driver_id, metadata):
        # try:
            sql_query = "UPDATE drivers SET license_number = %s WHERE id = %s"
            db.cursor.execute(sql_query, (metadata["license_number"], driver_id))
            db.conn.commit()
            print("Driver details updated successfully")
        # except mysql.connector.Error as err:
        #     print(f"Error updating driver details: {err}")

    def delete_driver(self, driver_id):
        # try:
            sql_query = "DELETE FROM drivers WHERE id = %s"
            db.cursor.execute(sql_query, (driver_id,))
            db.conn.commit()
            print("Driver deleted successfully")
        # except mysql.connector.Error as err:
        #     print(f"Error deleting driver: {err}")


# # Testing the module
# if __name__ == "__main__":
#     drivers = Drivers()
#     drivers.create_drivers_table()  # Create the drivers table if not exists

#     # Example usage:
#     drivers.add_driver("John Doe", "ABC123")  # Add a new driver
#     drivers.edit_driver(1, "Jane Doe")  # Edit driver with id 1
#     drivers.update_driver_details(1, "XYZ789")  # Update details for driver with id 1
#     drivers.delete_driver(2)  # Delete driver with id 2
