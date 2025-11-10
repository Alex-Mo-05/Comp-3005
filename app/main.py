
import os
import sys
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime


# This function allows the python script to connect to the database hosted on your local machine
def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            dbname='comp3005',
            user="postgres",
            password="12345",
        )
        return conn
    except Exception as e:
        print(f"[ERROR] Failed to connect to database: {e}")
        sys.exit(1)

# This function retrieves all students and displays them
def getAllStudents(conn):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT student_id, first_name, last_name, email, enrollment_date FROM students ORDER BY student_id;")
            rows = cur.fetchall()
            print("\n[RESULT] All students:")
            for r in rows:
                print(f"  - ID {r['student_id']}: {r['first_name']} {r['last_name']} | {r['email']} | enrolled {r['enrollment_date']}\n")
            return rows
    except Exception as e:
        print(f"[ERROR] getAllStudents failed: {e}")
        return []

# This function adds a student requiring the first_name, last_name, email, and enrollment date parameters
def addStudent(conn, first_name, last_name, email, enrollment_date=None):
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
                RETURNING student_id;
                """,
                (first_name, last_name, email, enrollment_date),
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            print(f"[OK] addStudent: inserted ID {new_id} ({first_name} {last_name})\n")
            return new_id
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] addStudent failed: {e}")
        return None

# This function updates a students email based on the student id selected, if a non valid id is selected the function will do nothing and return to the main menu
def updateStudentEmail(conn):
    student_id = input("\nWhat is the id the student you want to edit: ")
    with conn.cursor() as cur:

        cur.execute("SELECT 1 FROM students WHERE student_id = %s;", (student_id,))
        if cur.fetchone() is not None:
            new_email = input("What is the new student email: ")

            try:
                cur.execute(
                    "UPDATE students SET email = %s WHERE student_id = %s;",
                    (new_email, student_id),
                )

                conn.commit()
                print(f"[OK] updateStudentEmail: ID {student_id} -> {new_email}\n")
                return True
            except Exception as e:
                conn.rollback()
                print(f"[ERROR] updateStudentEmail failed: {e}")
                return False

        else:
            print("Unable to find student with id {student_id} please try again. \n")
            return False


# This function deletes a student from the database, if a non valid student id is selected the user will be returned to the main menu
def deleteStudent(conn):
    student_id = input("\nWhat is the id the student you want to delete: ")
    with conn.cursor() as cur:

        cur.execute("SELECT 1 FROM students WHERE student_id = %s;", (student_id,))
        if cur.fetchone() is not None:
            try:
                cur.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
                if cur.rowcount == 0:
                    print(f"[WARN] deleteStudent: no student with ID {student_id}")
                    conn.rollback()
                    return False
                conn.commit()
                print(f"[OK] deleteStudent: removed ID {student_id}\n")
                return True
            except Exception as e:
                conn.rollback()
                print(f"[ERROR] deleteStudent failed: {e}\n")
                return False
    
        else:
            print("Unable to find student please try again. \n")
            return False

# Control flow of the project, including the main menu prompts
def main():
    conn = get_connection()
    while True:
        action = input("Please select an action: \n1) Show all students \n2) Add a new student\n3) Update student's email\n4) Delete student \n5) Exit Application: \nAction: ")
        if action == "1":
            getAllStudents(conn)
        elif action == "2":
            fname = input("\nWhat is the first name of the new student: ")
            lname = input("What is the last name of the new student: ")
            nmail = input("What is the email of the new student: ")
            dat = input("Date of enrolment of the new student format(YYYY-mm-dd): ")
            addStudent(
                conn,
                first_name=fname,
                last_name=lname,
                email=nmail,
                enrollment_date=datetime.strptime(dat, "%Y-%m-%d"),
            )
        
        elif action == "3":
            updateStudentEmail(conn)
        
        elif action == "4":
            deleteStudent(conn)

        elif action == "5":
            print("Closing session")
            conn.close()
            exit()

        else: 
            print("Please select an option from the menu using their numbers \n")

    

    

        



    

if __name__ == "__main__":
    main()

