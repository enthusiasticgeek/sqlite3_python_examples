#!/usr/bin/env python3
import sqlite3
import csv

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
                              (id INTEGER PRIMARY KEY,
                               name TEXT,
                               age INTEGER)''')

            # Create the courses table
            cursor.execute('''CREATE TABLE IF NOT EXISTS courses
                              (id INTEGER PRIMARY KEY,
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

    def show_tables(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print("Tables in the database:")
            for table in tables:
                print(table[0])
        except sqlite3.Error as e:
            print(f"An error occurred while showing tables: {e}")

    def describe_table(self, table_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"Columns in table {table_name}:")
            for column in columns:
                print(column[1])
        except sqlite3.Error as e:
            print(f"An error occurred while describing table: {e}")

    def dump_database(self, file_name):
        try:
            cursor = self.conn.cursor()
            with open(file_name, "w") as file:
                for line in self.conn.iterdump():
                    file.write(f"{line}\n")
            print("Database dumped successfully")
        except sqlite3.Error as e:
            print(f"An error occurred while dumping database: {e}")

    def import_csv(self, table_name, csv_file):
        try:
            cursor = self.conn.cursor()
            with open(csv_file, "r") as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    cursor.execute(f"INSERT INTO {table_name} (name, age) VALUES (?, ?)", (row[0], row[1]))
            self.conn.commit()
            print(f"CSV file '{csv_file}' imported into table '{table_name}' successfully")
        except sqlite3.Error as e:
            print(f"An error occurred while importing CSV: {e}")

    def export_csv(self, table_name, csv_file):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            with open(csv_file, "w", newline="") as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(["name", "age"])  # Write header row
                csv_writer.writerows(rows)
            print(f"Table '{table_name}' exported to CSV file '{csv_file}' successfully")
        except sqlite3.Error as e:
            print(f"An error occurred while exporting CSV: {e}")

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

    # Show tables
    database.show_tables()

    # Describe table
    database.describe_table('students')

    # Dump database
    database.dump_database('database_dump.sql')

    # Import CSV
    database.import_csv('students', 'students.csv')

    # Export CSV
    database.export_csv('students', 'exported_students.csv')

    # Close the database connection
    database.close_connection()


if __name__ == "__main__":
    main()

