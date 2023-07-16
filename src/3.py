#!/usr/bin/env python3
# In memory db - foreign key 
import sqlite3

class StudentDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            print("Connected to the database")
        except sqlite3.Error as e:
            print(f"An error occurred while connecting to the database: {e}")

    def create_tables(self):
        try:
            cursor = self.conn.cursor()

            # Create the students table
            cursor.execute('''CREATE TABLE IF NOT EXISTS students
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               name TEXT,
                               age INTEGER)''')

            # Create the courses table
            cursor.execute('''CREATE TABLE IF NOT EXISTS courses
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               name TEXT,
                               student_id INTEGER,
                               FOREIGN KEY (student_id) REFERENCES students(id))''')

            print("Tables created successfully")
        except sqlite3.Error as e:
            print(f"An error occurred while creating the tables: {e}")

    def insert_student(self, name, age):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
            self.conn.commit()
            print("Student inserted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred while inserting student: {e}")

    def insert_course(self, name, student_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO courses (name, student_id) VALUES (?, ?)", (name, student_id))
            self.conn.commit()
            print("Course inserted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred while inserting course: {e}")

    def retrieve_data(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

            cursor.execute("SELECT * FROM courses")
            rows = cursor.fetchall()
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Student ID: {row[2]}")
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving data: {e}")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Connection closed")


def main():
    # Create an instance of StudentDatabase
    database = StudentDatabase('example.db')

    # Connect to the database
    database.connect()

    # Create tables
    database.create_tables()

    # Insert student data
    database.insert_student('John Doe', 20)
    database.insert_student('Jane Smith', 22)

    # Insert course data
    database.insert_course('Mathematics', 1)
    database.insert_course('Physics', 1)
    database.insert_course('Chemistry', 2)

    # Retrieve data from the tables
    database.retrieve_data()

    # Close the database connection
    database.close_connection()


if __name__ == "__main__":
    main()

