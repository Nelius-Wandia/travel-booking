import db_connection as db
from generals import Generals
import json

generals = Generals()

class Trips:
    def __init__(self, trip_id=None):
        self.trip_id = trip_id

    def CreateTripTable(self):
        sql_query = """create table if not exists trips(
        id varchar(10),
        company_id varchar(50),
        bus_id varchar(20),
        driver_id  varchar(20),
        origin varchar(20),
        destination varchar(20),
        seat_occupation varchar(20),
        price int,
        state boolean,
        updated_time timestamp not null default current_timestamp on update current_timestamp,
        created_time timestamp default current_timestamp,
        foreign key (company_id) references admin_users(id),
        foreign key (bus_id) references buses(id)
        )"""
        db.cursor.execute(sql_query)
        db.conn.commit()

    def CreateTrip(self, metadata):
        metadata = {
            "company_id": "ebBZ6l)RWm",
            "bus_id": "u(Szt",
            "driver_id": "cwiejcoiwe",
            "origin": "Nairobi",
            "destination": "Kisumu",
            "seat_config": "0:89",
            "price": 4500
        }
        self.trip_id = self.GetUniqueTrip()
        sql_query = """insert into trips(id, company_id, bus_id, driver_id, origin, destination, seat_occupation, price, state) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        sql_data = [self.trip_id, metadata["company_id"], metadata["bus_id"], metadata["driver_id"], metadata["origin"], metadata["destination"], metadata["seat_config"], metadata["price"], False]
        db.cursor.execute(sql_query, sql_data)
        db.conn.commit()

    def FetchTrips(self, user_id=""):
        sql_query = """select * from trips where company_id = %s"""
        db.cursor.execute()

    def GetUniqueTrip(self):
        while True:
            trip_id = generals.GenRandomCode(size=10)
            sql_query = """select * from buses where id = %s"""
            db.cursor.execute(sql_query, [trip_id])
            if not db.cursor.fetchall(): return trip_id

x = Trips()
# x.CreateTripTable()
x.CreateTrip("")

