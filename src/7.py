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

            # Group By and Having - Average age by course
            cursor.execute("SELECT courses.name, AVG(students.age) FROM students JOIN courses ON students.id = courses.student_id GROUP BY courses.name HAVING AVG(students.age) > 20")
            rows = cursor.fetchall()
            print("Average age by course (Having age > 20):")
            for row in rows:
                print(f"Course Name: {row[0]}, Average Age: {row[1]}")

            print("\n")

            # Union - Students and Courses
            cursor.execute("SELECT name FROM students UNION SELECT name FROM courses")
            rows = cursor.fetchall()
            print("Union of student names and course names:")
            for row in rows:
                print(f"Name: {row[0]}")

            print("\n")

            # Except - Students not enrolled in any course
            cursor.execute("SELECT name FROM students EXCEPT SELECT students.name FROM students JOIN courses ON students.id = courses.student_id")
            rows = cursor.fetchall()
            print("Students not enrolled in any course:")
            for row in rows:
                print(f"Name: {row[0]}")

            print("\n")

            # Intersect - Students enrolled in both Math and Physics courses
            cursor.execute("SELECT students.name FROM students JOIN courses ON students.id = courses.student_id WHERE courses.name = 'Mathematics' INTERSECT SELECT students.name FROM students JOIN courses ON students.id = courses.student_id WHERE courses.name = 'Physics'")
            rows = cursor.fetchall()
            print("Students enrolled in both Math and Physics courses:")
            for row in rows:
                print(f"Name: {row[0]}")

            print("\n")

            # Subquery - Students younger than the average age
            cursor.execute("SELECT name FROM students WHERE age < (SELECT AVG(age) FROM students)")
            rows = cursor.fetchall()
            print("Students younger than the average age:")
            for row in rows:
                print(f"Name: {row[0]}")

            print("\n")

            # EXISTS - Students with enrolled courses
            cursor.execute("SELECT name FROM students WHERE EXISTS (SELECT 1 FROM courses WHERE students.id = courses.student_id)")
            rows = cursor.fetchall()
            print("Students with enrolled courses:")
            for row in rows:
                print(f"Name: {row[0]}")

            print("\n")

            # Case - Displaying course names with age conditions
            cursor.execute("SELECT courses.name, CASE WHEN students.age < 18 THEN 'Under 18' WHEN students.age >= 18 AND students.age < 25 THEN '18-24' ELSE '25+' END AS age_group FROM students JOIN courses ON students.id = courses.student_id")
            rows = cursor.fetchall()
            print("Course names with age groups:")
            for row in rows:
                print(f"Course Name: {row[0]}, Age Group: {row[1]}")

        except sqlite3.Error as e:
            print(f"An error occurred while retrieving data: {e}")

    def update_student(self, student_id, name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE students SET name = ? WHERE id = ?", (name, student_id))
            self.conn.commit()
            print("Student updated successfully")
        except sqlite3.Error as e:
            print(f"An error occurred while updating student: {e}")

    def delete_student(self, student_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            self.conn.commit()
            print("Student deleted successfully")
        except sqlite3.Error as e:
            print(f"An error occurred while deleting student: {e}")

    def replace_student(self, name, age):
        try:
            cursor = self.conn.cursor()
            cursor.execute("REPLACE INTO students (name, age) VALUES (?, ?)", (name, age))
            self.conn.commit()
            print("Student replaced successfully")
        except sqlite3.Error as e:
            print(f"An error occurred while replacing student: {e}")

    def execute_transaction(self):
        try:
            cursor = self.conn.cursor()

            # Begin the transaction
            cursor.execute("BEGIN")

            # Insert new student
            cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", ("New Student", 21))

            # Update an existing student
            cursor.execute("UPDATE students SET age = ? WHERE name = ?", (22, "John Doe"))

            # Delete a student
            cursor.execute("DELETE FROM students WHERE name = ?", ("Jane Smith",))

            # Commit the transaction
            cursor.execute("COMMIT")

            print("Transaction executed successfully")
        except sqlite3.Error as e:
            # Rollback the transaction in case of any error
            cursor.execute("ROLLBACK")
            print(f"An error occurred while executing the transaction: {e}")

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

    # Retrieve data from the tables and perform various operations
    database.retrieve_data()

    # Update a student
    database.update_student(1, "John Smith")

    # Delete a student
    database.delete_student(2)

    # Replace a student
    database.replace_student("Alex Johnson", 23)

    # Execute a transaction
    database.execute_transaction()

    # Close the database connection
    database.close_connection()


if __name__ == "__main__":
    main()


