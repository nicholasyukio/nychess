# This file will the implemented in the future
# The purpose is to store the game info in a MySQL database

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")

""" Database table and columns:

Table games:
Columns: id, game_id, start_time, last_update_time, game_history, game_situation


 """