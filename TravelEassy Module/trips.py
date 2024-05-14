import db_connection as db
from generals import Generals
from buses import Buses
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
        origin varchar(255),
        destination varchar(255),
        seat_occupation varchar(20),
        price int,
        message longtext,
        state boolean,
        updated_time timestamp not null default current_timestamp on update current_timestamp,
        created_time timestamp default current_timestamp,
        foreign key (company_id) references admin_users(id),
        foreign key (bus_id) references buses(id)
        )"""
        db.cursor.execute(sql_query)
        db.conn.commit()

    def CreateTrip(self, metadata):
        # metadata = {
        #     "company_id": "ebBZ6l)RWm",
        #     "bus_id": "u(Szt",
        #     "driver_id": "cwiejcoiwe",
        #     "origin": {
        #         "address": "Nairobi",
        #         "datetime": "12-12-2024"
        #     },
        #     "destination": {
        #         "address": "Kisumu",
        #         "datetime": "12-12-2024"
        #     },
        #     "seat_config": "0:89",
        #     "price": 4500,
        #     "message": "lorem ipsum"
        # }
        self.trip_id = self.GetUniqueTrip()
        sql_query = """insert into trips(id, company_id, bus_id, driver_id, origin, destination, seat_occupation, price, message, state) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        sql_data = [self.trip_id, metadata["company_id"], metadata["bus_id"], metadata["driver_id"], json.dumps(metadata["origin"]), json.dumps(metadata["destination"]), metadata["seat_config"], metadata["price"], metadata["message"], False]
        db.cursor.execute(sql_query, sql_data)
        db.conn.commit()

    def FetchTrips(self, user_id=""):
        sql_query = """select * from trips where company_id = %s"""
        db.cursor.execute(sql_query, [user_id])
        trips = db.cursor.fetchall()

        export_data = []
        unit_trip_data = ["trip_id", "origin_addr", "origin_time", "destination_addr", "destination_time", "seat_occupation", "price", "message", "plate_no", "drivers_name"]
        for trip in trips:
            origin_addr = json.loads(trip[4])["address"]
            origin_datetime = json.loads(trip[4])["datetime"]
            destination_addr = json.loads(trip[5])["address"]
            destination_datetime = json.loads(trip[5])["datetime"]
            unit_trip_data = [trip[0], origin_addr, origin_datetime, destination_addr, destination_datetime, trip[6], trip[7], trip[8]]
            bus = Buses(bus_id=trip[2])
            bus.GetBusDetails()

            unit_trip_data.append(bus.plate_number)
            unit_trip_data.append("Andrew Macharia")
            export_data.append(unit_trip_data)

        return export_data

    def BookTicket(self):
        pass

    def GetUniqueTrip(self):
        while True:
            trip_id = generals.GenRandomCode(size=10)
            sql_query = """select * from buses where id = %s"""
            db.cursor.execute(sql_query, [trip_id])
            if not db.cursor.fetchall(): return trip_id

x = Trips()
# x.CreateTripTable()
# x.CreateTrip("")
print(x.FetchTrips(user_id="ebBZ6l)RWm"))
