# from datetime import datetime
# from typing import List
# from fastapi import APIRouter, Depends, HTTPException
# from pydantic import BaseModel
# from login import get_current_user, get_db_connection

# router_data = APIRouter(
#     prefix="/data",
#     tags=["data"],
# )

# # temperature
# class Temperature(BaseModel):
#     messzeitpunkt: datetime
#     temperatur: float
#     sensorNr: int

# @router_data.get("/temperature", response_model=List[Temperature])
# async def get_temperature(sensorNr: int = None):
#     con, cursor = get_db_connection()
#     if sensorNr:
#         cursor.execute(
#             "SELECT * FROM temperaturmessung WHERE sensorNr = %s", (sensorNr,)
#         )
#     else:
#         cursor.execute("SELECT * FROM temperaturmessung")
#     res = cursor.fetchall()
#     cursor.close()
#     con.close()
#     return res

# @router_data.post("/temperature")
# async def post_temperature(
#     temperature: float,
#     sensorNr: int,
# ):
#     con, cursor = get_db_connection()
#     try:
#         cursor.execute(
#             """
#             INSERT INTO temperaturmessung (messzeitpunkt, temperatur, sensorNr)
#             VALUES (CURDATE(), %s, %s)
#             """,
#             (temperature, sensorNr),
#         )
#         con.commit()
#         return {"message": "Temperature added"}
#     except Exception as e:
#         con.rollback()
#         raise HTTPException(status_code=400, detail=str(e))
#     finally:
#         cursor.close()
#         con.close()

# @router_data.post("/sql")
# async def execute_sql(sql: str, current_user: dict = Depends(get_current_user)):
#     con, cursor = get_db_connection()
#     try:
#         cursor.execute(sql)
#         res = cursor.fetchall()
#     except Exception as e:
#         cursor.close()
#         con.close()
#         raise HTTPException(status_code=400, detail=str(e))
#     cursor.close()
#     con.close()
#     return res

# #sensor
# class Sensor(BaseModel):
#     sensorNr: int
#     adresse: str
#     maxTemperature: float
#     herstellerID: int | None = None
#     serverschrankID: int | None = None

# @router_data.get("/sensor", response_model=List[Sensor])
# async def get_sensor(sensorNr: int = None):
#     con, cursor = get_db_connection()
#     if sensorNr:
#         cursor.execute("SELECT * FROM sensor WHERE sensorNr = %s", (sensorNr,))
#     else:
#         cursor.execute("SELECT * FROM sensor")
#     res = cursor.fetchall()
#     cursor.close()
#     con.close()
#     return res


# @router_data.post("/sensor")
# async def post_sensor(
#     sensor: Sensor, current_user: dict = Depends(get_current_user)
# ):
#     con, cursor = get_db_connection()
#     try:
#         cursor.execute(
#             """
#             INSERT INTO sensor (adresse, maxTemperature, herstellerID, serverschrankID)
#             VALUES (%s, %s, %s, %s)
#             """,
#             (
#                 sensor.adresse,
#                 sensor.maxTemperature,
#                 sensor.herstellerID,
#                 sensor.serverschrankID,
#             ),
#         )
#         con.commit()
#         cursor.close()
#         con.close()
#         return {"message": "Sensor added"}
#     except Exception as e:
#         cursor.close()
#         con.close()
#         raise HTTPException(status_code=400, detail=str(e))

# @router_data.patch("/sensor")
# async def patch_sensor(
#     sensor: Sensor, current_user: dict = Depends(get_current_user)
# ):
#     con, cursor = get_db_connection()
#     try:
#         cursor.execute(
#             """
#             UPDATE sensor
#             SET adresse = %s, maxTemperature = %s, herstellerID = %s, serverschrankID = %s
#             WHERE sensorNr = %s
#             """,
#             (
#                 sensor.adresse,
#                 sensor.maxTemperature,
#                 sensor.herstellerID,
#                 sensor.serverschrankID,
#                 int(sensor.sensorNr),
#             ),
#         )
    
#     # write log eintragsnummer	zeitstempel	alteMaxTemperatur	neueMaxTemperatur	anmeldename	sensorNr
#         cursor.execute(
#             """
#             INSERT INTO log (zeitstempel, alteMaxTemperatur, neueMaxTemperatur, anmeldename, sensorNr)
#             SELECT NOW(), maxTemperature, %s, %s, %s
#             FROM sensor
#             WHERE sensorNr = %s
#             """,
#             (sensor.maxTemperature, current_user["anmeldename"], sensor.sensorNr, sensor.sensorNr),
#         )
#         con.commit()
#     except Exception  as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
#     cursor.close()
#     con.close()
#     return {"message": "Sensor updated"}

# # hersteller
# class Hersteller(BaseModel):
#     name: str


# # @router_data.post("/hersteller")
# # async def post_hersteller(
# #     hersteller: Hersteller, current_user: dict = Depends(get_current_user)
# # ):
# #     con, cursor = get_db_connection()
# #     cursor.execute(
# #         """
# #         INSERT INTO hersteller (name)
# #         VALUES (%s)
# #         """,
# #         (hersteller.name,),
# #     )
# #     con.commit()
# #     cursor.close()
# #     con.close()
# #     return {"message": "Hersteller added"}


# #log: eintragsnummer	zeitstempel	alteMaxTemperatur	neueMaxTemperatur	anmeldename	sensorNr



# #hersteller
# @router_data.get("/hersteller")
# async def get_hersteller(herstellerID: int = None):
#     con, cursor = get_db_connection()
#     if herstellerID:
#         cursor.execute(
#             "SELECT * FROM hersteller WHERE herstellerID = %s", (herstellerID,)
#         )
#     else:
#         cursor.execute("SELECT * FROM hersteller")
#     res = cursor.fetchall()
#     cursor.close()
#     con.close()
#     return res

# #logs eintragsnummer	zeitstempel	alteMaxTemperatur	neueMaxTemperatur	anmeldename	sensorNr
# class Log(BaseModel):
#     eintragsnummer: int
#     zeitstempel: datetime
#     anmeldename: str
#     sensorNr: int
#     alteMaxTemperatur: float
#     neueMaxTemperatur: float


# # get logs from time period or all logs    
# @router_data.get("/logs", response_model=List[Log])
# async def get_log(start: str = None, end: str = None, current_user: dict = Depends(get_current_user)):
#     if not current_user["adminRolle"] == 1:
#         raise HTTPException(status_code=401, detail="Unauthorized")
    
#     con, cursor = get_db_connection()
#     if start and end:
#         start_date = datetime.fromisoformat(start.replace("Z", "+00:00"))
#         end_date = datetime.fromisoformat(end.replace("Z", "+00:00"))
#         cursor.execute(
#             "SELECT * FROM log WHERE zeitstempel BETWEEN %s AND %s",
#             (start_date, end_date),
#         )
#     else:
#         cursor.execute("SELECT * FROM log")
#     res = cursor.fetchall()
#     cursor.close()
#     con.close()
#     return res