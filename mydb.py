import mysql.connector

dataBase = mysql.connector.connect(
    host= 'localhost',
    user="root",
    passwd='saturda1z',

)

#preparing a cursor object

cursorObject = dataBase.cursor()

#create the database

cursorObject.execute('CREATE DATABASE donald')

print ('Database created')