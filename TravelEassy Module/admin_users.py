import db_connection as db

class AdminUser:
    def CreateUserTable(self):
        sql_query = """create table if not exists admin_users(
                id integer primary key,
                company_name text,
                phone integer,
                email text,
                means_type text,
                till_number integer,
                banck_account integer,
                crypto_address text,
                verification text,
                revenue integer,
                total_trips integer,
                logo_url text,
                updated_time text,
                created_time text
                )"""
        db.cursor.execute(sql_query)
        db.conn.commit()









# Cols - (id, company_name, phone, email, means_type, till_number, bank_acc, crypto_addr, verification,
# revenue, total_trips, logo_url, updated_time, created_time)

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
