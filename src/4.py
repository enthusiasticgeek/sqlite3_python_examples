#!/usr/bin/env python3
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

            # Select all students
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            print("All students:")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

            print("\n")

            # Select courses for a specific student
            student_id = 1
            cursor.execute("SELECT * FROM courses WHERE student_id = ?", (student_id,))
            rows = cursor.fetchall()
            print(f"Courses for student with ID {student_id}:")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Student ID: {row[2]}")

            print("\n")

            # Select distinct ages of students
            cursor.execute("SELECT DISTINCT age FROM students")
            rows = cursor.fetchall()
            print("Distinct ages of students:")
            for row in rows:
                print(f"Age: {row[0]}")

            print("\n")

            # Select students with age between 20 and 25
            cursor.execute("SELECT * FROM students WHERE age BETWEEN 20 AND 25")
            rows = cursor.fetchall()
            print("Students with age between 20 and 25:")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

            print("\n")

            # Select students with names in a list
            names = ['John Doe', 'Jane Smith']
            cursor.execute("SELECT * FROM students WHERE name IN ({})".format(','.join(['?'] * len(names))), tuple(names))
            rows = cursor.fetchall()
            print("Students with names in the list:")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

            print("\n")

            # Select students with names containing 'Joh'
            keyword = 'Joh'
            cursor.execute("SELECT * FROM students WHERE name LIKE ?", (f'%{keyword}%',))
            rows = cursor.fetchall()
            print(f"Students with names containing '{keyword}':")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

            print("\n")

            # Select students with NULL age
            cursor.execute("SELECT * FROM students WHERE age IS NULL")
            rows = cursor.fetchall()
            print("Students with NULL age:")
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
    database = StudentDatabase('example.db')

    # Connect to the database
    database.connect()

    # Create tables
    database.create_tables()

    # Insert student data
    database.insert_student('John Doe', 20)
    database.insert_student('Jane Smith', 22)
    database.insert_student('Alex Johnson', 25)
    database.insert_student('Sarah Brown', None)

    # Insert course data
    database.insert_course('Mathematics', 1)
    database.insert_course('Physics', 1)
    database.insert_course('Chemistry', 2)
    database.insert_course('Biology', 3)
    database.insert_course('English', 4)

    # Retrieve data using different SQLite operations
    database.retrieve_data()

    # Close the database connection
    database.close_connection()


if __name__ == "__main__":
    main()

