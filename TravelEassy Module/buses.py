import db_connection as db
from generals import Generals

generals = Generals()

class Buses:
    def __init__(self, bus_id:str=""):
        self.bus_id = bus_id

    def CreateBusTable(self):
        sql_query = """create table Buses (
        id varchar(20) primary key,
        company_id varchar(100),
        license_plate varchar(10),
        no_seats int,
        model varchar(100),
        color varchar(100),
        arrangement varchar(100),
        no_trips int,
        status boolean,
        updated_time timestamp not null default current_timestamp on update current_timestamp,
        created_time timestamp default current_timestamp,
        foreign key (company_id) references admin_users(id)
        )"""
        db.cursor.execute(sql_query)
        db.conn.commit()

    def AddBus(self, metadata):
        bus_id = generals.GenRandomCode(size=5)
        sql_query = """insert into buses (id, company_id, license_plate, no_seats, model, color, arrangement, no_trips, status) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        sql_data = [bus_id, metadata["company_id"], metadata["license_plate"], metadata["no_seats"], metadata["model"], metadata["color"], metadata["arrangement"], 0, False]

        db.cursor.execute(sql_query, sql_data)
        db.conn.commit()

    def UpdateBus(self, metadata):
        # metadata = {
        #     "bus_id": bus_id,
        #     "license_plate": license,
        #     "no_seats": no_seats,
        #     "model": model,
        #     "color": colour,
        #     "arrangement": seat_config
        # }
        print(metadata)
        sql_query = """update buses set license_plate = %s, no_seats = %s, model = %s, color = %s, arrangement = %s where id = %s"""
        sql_data = [metadata["license_plate"], metadata["no_seats"], metadata["model"], metadata["color"], metadata["arrangement"], metadata["bus_id"]]
        db.cursor.execute(sql_query, sql_data)
        db.conn.commit()

    def DeleteBus(self):
        sql_query = """delete from buses where id = %s"""
        db.cursor.execute(sql_query, [self.bus_id])
        db.conn.commit()

    def BookFully(self):
        sql_query = """select status from buses where id = %s"""
        db.cursor.execute(sql_query, [self.bus_id])
        response = db.cursor.fetchall()
        if not response: return False

        status = response[0][0]
        if status: return False

        sql_query = """update buses set no_trips = no_trips + 1, status = %s where id = %s"""
        db.cursor.execute(sql_query, [True, self.bus_id])
        db.conn.commit()

        return True

    def ArriveDestination(self):
        sql_query = """update buses set status = %s where id = %s"""
        db.cursor.execute(sql_query, [False, self.bus_id])
        db.conn.commit()

    def GetAllBuses(self, user_id=""):
        sql_query = """select * from buses where company_id = %s"""
        db.cursor.execute(sql_query, [user_id])
        return db.cursor.fetchall()

bus = Buses()
# bus.CreateBusTable()
# bus.AddBus("h")
# print(bus.BookFully())
# bus.ArriveDestination()
# print(bus.GetAllBuses(user_id="x7p@9OYV@f"))
# bus.DeleteBus()