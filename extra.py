import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", password="Kunal@123")

mycur = mydb.cursor()

mycur.execute("drop database fa;")

print(mycur)