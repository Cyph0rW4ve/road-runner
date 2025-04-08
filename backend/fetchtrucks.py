import mysql.connector

def fetch_trucks(truck_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user='root',
        password='1234',
        database='road_runner'
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT fuel_tank, liters_per_100km FROM trucks WHERE brand = %s", (truck_name,))
    myresult = mycursor.fetchall()

    fuel_tank = myresult[0][0]
    consumption = myresult[0][1]

    return [fuel_tank, consumption]