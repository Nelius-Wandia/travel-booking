from generals import Generals
import db_connection as db
import json

generals = Generals()

class AdminUser:
    def __init__(self, user_id=None):
        self.user_id = user_id

    def CreateUserTable(self):
        sql_query = """create table if not exists admin_users(
                id varchar(20) primary key,
                company_name varchar(50),
                phone integer,
                email varchar(50),
                means_type varchar(10),
                password varchar(12),
                till_number integer,
                bank_account integer,
                crypto_address varchar(50),
                verification varchar(10),
                revenue integer,
                total_trips integer,
                logo_url varchar(50),
                updated_time timestamp not null default current_timestamp on update current_timestamp,
                created_time timestamp default current_timestamp
                )"""
        db.cursor.execute(sql_query)
        db.conn.commit()

    def DeleteUserTable(self):
        sql_query = """drop table if exists admin_users"""
        db.cursor.execute(sql_query)
        db.conn.commit()

    def CreateUser(self, metadata):
        if not self.is_present(metadata["phone"], metadata["email"]): return False
        self.verification = generals.GenRandomCode(size=5)
        verification = {
            "code": self.verification,
            "state": False
        }
        verification = json.dumps(verification)
        sql_query = """
            insert into admin_users (id, company_name, phone, email, means_type, password, till_number, bank_account, crypto_address, verification, revenue, total_trips, logo_url, updated_time, created_time)
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
        
        sql_data = (generals.GenRandomCode(size=5), metadata["company_name"], metadata["phone"], metadata["email"], metadata["means_type"], generals.GetPasswordHash(metadata["password"]), metadata["till_number"], metadata["bank_account"], metadata["crypto_address"], verification, 0, 0, self.SaveLogo(metadata["logo"]), generals.GetCurrentTime(), generals.GetCurrentTime())
        db.cursor.execute(sql_query, sql_data)
        db.conn.commit()
        return True
            
    def is_present(self, phone, email):
        sql_query = """select * from admin_users where phone = %s or email = %s"""
        db.cursor.execute(sql_query, (phone, email))
        response = db.cursor.fetchall()
        if not response: return False
        return True

    def SaveLogo(self, img_file):
        # Returns the file name
        # Use 16 Character unique identifier
        return img_file
    
    def AuthenticateUser(self, username, password):
        sql_query = """select * from admin_users where email = %s"""
        db.cursor.execute(sql_query, [username])
        response = db.cursor.fetchall()
        if not response: return False
        user_password = response[0][5]
        if not generals.VerifyHash(user_password, password): return False
        return True

    def SetUserState(self, state):
        sql_query = """select verification from admin_users where id = %s"""
        db.cursor.execute(sql_query, (self.user_id,))
        response = db.cursor.fetchall()
        if not response: return False
        verification = json.loads(response[0][0])
        ver_data = {
            "code": verification["code"],
            "state": state
        }
        ver_data = json.dumps(ver_data)
        print(ver_data)
        sql_query = """update admin_users set verification = %s where id = %s"""
        print(self.user_id)
        db.cursor.execute(sql_query, (ver_data,self.user_id,))
        db.conn.commit()
        return True
    

# Models Testing Code #
metadata = {
    "company_name": "ionextech",
    "phone": 254795359098,
    "email": "machariaandrew1428@gmail.com",
    "means_type": "Roadways",
    "password": "1234",
    "till_number": "1234",
    "bank_account": "1234",
    "crypto_address": "1234",
    "logo": "logo"
}
user = AdminUser()
# user.CreateUser(metadata)
user.CreateUserTable()
# print(user.GetAdminTable())
# print(user.AuthenticateUser("machariaandrew1428@gmail.com", "1234"))
# print(user.SetUserState(False))
# End of Model Testing #


# Cols - (id, company_name, phone, email, means_type, till_number, bank_acc, crypto_addr, verification(json), revenue, total_trips, logo_url, updated_time, created_time)

# FUNCTIONS
# Rules(Each function takes its own parameters)
# Rules(Init set the user id)
# - CreateUser - (Create new user account)
# - AuthenticateUser - (Allow access based on email/phone and password)
# - VerifyUser - (Verify user based input verification code)
# - ControlUser - (Enable/Disable User Account)
# - UpdateProfile - (Update user profile profile)
# - DeleteUser - (Delete user account)
# - IncreamentTrips - (Increament number of trips for the user)
# - NotifyUser - (Notify user by sms/email address)
# - SetUserdetails - (Set user details)
# - CreateUserTable - (Create user table)
# - DeleteUserTable - (Delete user table)
