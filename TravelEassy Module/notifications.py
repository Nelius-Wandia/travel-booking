from generals import Generals
import db_connection as db
generals = Generals()


# Sms static Config
import requests
sms_endpoint_url = 'https://sms.textsms.co.ke/api/services/sendsms'
api_key = "5f7157aa5e206f7f5402ffd5abc79c95"
partner_id = "9064"
sender_id = "TextSMS"

payload = {
    "apikey":api_key,
    "partnerID":partner_id,
    "message":None,
    "shortcode":sender_id,
    "mobile":None
}

class SMS:
    def __init__(self, user_id:str):
        self.user_id = user_id
        self.payload = {
            "apikey":api_key,
            "partnerID":partner_id,
            "message":None,
            "shortcode":sender_id,
            "mobile":None
        }

    def SendInstantSMS(self, phone:list, message:str):
        self.message = message
        for x in phone:
            self.phone = x
            self.payload["mobile"] = phone
            self.payload["message"] = message
            # Create Notification - Add row to Notification Table
            self.CreateSMSNotification() # Sets the notification id @ self.notification_id
            is_sent = self.SendRequest()
            sql_query = """update notifications set status = %s where id = %s"""
            sql_data = [is_sent, self.notification_id]
            db.cursor.execute(sql_query, sql_data)
            db.conn.commit()
            # Update State to Notification Table based on is_sent

    def SendScheduledSMS(self, phone:list, message:str, scheduled_time:str):
        self.message = message
        for x in phone:
            self.phone = x
            self.payload["mobile"] = phone
            self.payload["message"] = message
            self.payload["timeToSend"] = scheduled_time
            # Create Notification - Add row to Notification Table
            self.CreateSMSNotification() # Sets the notification id @ self.notification_id
            is_sent = self.SendRequest()
            sql_query = """update notifications set status = %s where id = %s"""
            sql_data = [is_sent, self.notification_id]
            db.cursor.execute(sql_query, sql_data)
            db.conn.commit()
            # Update State to Notification Table based on is_sent

    def SendRequest(self):
        # sms_api_response = requests.post(sms_endpoint_url, data=self.payload)
        # create algo to verify is sms is sent or not
        return True

    def CreateSMSNotification(self, type="SMS"):
        self.notification_id = self.GenUnique_id()
        sql_query = """insert into notifications (id, company_id, type, destination, message, status) values(%s, %s, %s, %s, %s, %s)"""
        sql_data = [self.notification_id, self.user_id, type, self.phone, self.message, False]
        db.cursor.execute(sql_query, sql_data)
        db.conn.commit()

    def GenUnique_id(self):
        while True:
            code = generals.GenRandomCode(size=10)
            sql_query = """select * from notifications where id = %s"""
            db.cursor.execute(sql_query, [code])
            response = db.cursor.fetchall()
            if not response: return code







# Email Static Config
class Email:
    pass



# System Static Config
pass



# Model testing Environment

# x = SMS(user_id="i&Tenm9PeO")
# x.SendInstantSMS([254795359098], message="Testing Message")