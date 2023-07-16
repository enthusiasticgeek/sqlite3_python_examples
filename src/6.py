#!/usr/bin/env python3
"""
The program continues to simulate the RIGHT JOIN and FULL OUTER JOIN operations using alternative techniques. The approach for the FULL OUTER JOIN is to combine a LEFT JOIN with a separate query to include unmatched rows from the left table.

Please note that while these techniques simulate the behavior of RIGHT JOIN and FULL OUTER JOIN, they may not be as efficient as the native implementations available in other database systems.
"""
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
                print(f"ID: {row[0]}, Student ID: {row[1]}")

            # Perform JOIN operations

            # Inner Join - Students and Courses
            cursor.execute("SELECT students.name, courses.name FROM students INNER JOIN courses ON students.id = courses.student_id")
            rows = cursor.fetchall()
            print("\nInner Join - Students and Courses:")
            for row in rows:
                print(f"Student Name: {row[0]}, Course Name: {row[1]}")

            # Left Join - Students and Courses
            cursor.execute("SELECT students.name, courses.name FROM students LEFT JOIN courses ON students.id = courses.student_id")
            rows = cursor.fetchall()
            print("\nLeft Join - Students and Courses:")
            for row in rows:
                print(f"Student Name: {row[0]}, Course Name: {row[1]}")

            # Cross Join - Students and Courses (Cartesian Product)
            cursor.execute("SELECT students.name, courses.name FROM students CROSS JOIN courses")
            rows = cursor.fetchall()
            print("\nCross Join - Students and Courses:")
            for row in rows:
                print(f"Student Name: {row[0]}, Course Name: {row[1]}")

            # Self-Join - Students and Courses
            cursor.execute("SELECT s.name, c.name FROM students s, courses c WHERE s.id = c.student_id")
            rows = cursor.fetchall()
            print("\nSelf-Join - Students and Courses:")
            for row in rows:
                print(f"Student Name: {row[0]}, Course Name: {row[1]}")

            # Full Outer Join - Students and Courses (Simulated)
            cursor.execute("SELECT students.name, courses.name FROM students LEFT JOIN courses ON students.id = courses.student_id UNION SELECT students.name, NULL FROM students WHERE students.id NOT IN (SELECT student_id FROM courses)")
            rows = cursor.fetchall()
            print("\nFull Outer Join - Students and Courses:")
            for row in rows:
                print(f"Student Name: {row[0]}, Course Name: {row[1]}")

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

    # Retrieve data from the tables and perform join operations
    database.retrieve_data()

    # Close the database connection
    database.close_connection()


if __name__ == "__main__":
    main()

