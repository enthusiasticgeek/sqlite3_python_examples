#!/usr/bin/env python3
# In memory db
import sqlite3

class StudentDatabase:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(':memory:')
            print("Connected to the in-memory database")
        except sqlite3.Error as e:
            print(f"An error occurred while connecting to the database: {e}")

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS students
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               name TEXT,
                               age INTEGER)''')
            print("Table created successfully")
        except sqlite3.Error as e:
            print(f"An error occurred while creating the table: {e}")

    def insert_data(self, name, age):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
            self.conn.commit()
            print("Data inserted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred while inserting data: {e}")

    def retrieve_data(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving data: {e}")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Connection closed")


def main():
    # Create an instance of StudentDatabase
    database = StudentDatabase()

    # Connect to the in-memory database
    database.connect()

    # Create a table
    database.create_table()

    # Insert data into the table
    database.insert_data('John Doe', 20)
    database.insert_data('Jane Smith', 22)
    database.insert_data('Alex Johnson', 21)

    # Retrieve data from the table
    database.retrieve_data()

    # Close the database connection
    database.close_connection()


if __name__ == "__main__":
    main()

