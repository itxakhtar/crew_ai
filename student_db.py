import sqlite3
import random

# Connect to SQLite database
connection = sqlite3.connect("student.db")
cursor = connection.cursor()

# Create STUDENT table with detailed columns
cursor.execute("""
CREATE TABLE IF NOT EXISTS STUDENT (
    ROLL_NO INTEGER PRIMARY KEY,
    NAME TEXT NOT NULL,
    DEPARTMENT TEXT NOT NULL,
    SECTION TEXT NOT NULL,
    SEMESTER INTEGER NOT NULL,
    CGPA REAL NOT NULL,
    EMAIL TEXT,
    PHONE TEXT,
    ADDRESS TEXT
)
""")

# Sample student data with extra info
students = [
    ("Ali", "AI", "A", 1, 3.5, "ali@example.com", "03120000001", "Bahawalpur"),
    ("Sara", "Data Science", "B", 2, 3.8, "sara@example.com", "03120000002", "Multan"),
    ("Ahmed", "Software Engineering", "A", 3, 3.2, "ahmed@example.com", "03120000003", "Lahore"),
    ("Hina", "Computer Science", "C", 2, 3.9, "hina@example.com", "03120000004", "Karachi"),
    ("Bilal", "Cyber Security", "B", 1, 3.6, "bilal@example.com", "03120000005", "Islamabad"),
    ("Zara", "AI", "C", 3, 3.7, "zara@example.com", "03120000006", "Faisalabad"),
    ("Usman", "Data Science", "A", 2, 3.4, "usman@example.com", "03120000007", "Sialkot"),
    ("Fatima", "Software Engineering", "B", 1, 3.3, "fatima@example.com", "03120000008", "Bahawalpur"),
    ("Hamza", "Computer Science", "C", 3, 3.8, "hamza@example.com", "03120000009", "Multan"),
    ("Ayesha", "Cyber Security", "A", 2, 3.9, "ayesha@example.com", "03120000010", "Lahore")
]

# Insert students with unique roll numbers, skip duplicates by NAME + DEPARTMENT
used_roll_numbers = set()
for student in students:
    cursor.execute("SELECT 1 FROM STUDENT WHERE NAME=? AND DEPARTMENT=?", (student[0], student[1]))
    if cursor.fetchone():
        continue  # Skip if already exists
    while True:
        roll_no = random.randint(1, 999)
        if roll_no not in used_roll_numbers:
            used_roll_numbers.add(roll_no)
            break
    cursor.execute(
        "INSERT INTO STUDENT (ROLL_NO, NAME, DEPARTMENT, SECTION, SEMESTER, CGPA, EMAIL, PHONE, ADDRESS) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (roll_no, *student)
    )

connection.commit()
print("Database updated & sample data added successfully!")

# Function to search students
def search_students(name=None, department=None, section=None, semester=None, min_cgpa=None, max_cgpa=None, email=None):
    query = "SELECT * FROM STUDENT WHERE 1=1"
    params = []
    if name:
        query += " AND NAME LIKE ?"
        params.append(f"%{name}%")
    if department:
        query += " AND DEPARTMENT LIKE ?"
        params.append(f"%{department}%")
    if section:
        query += " AND SECTION=?"
        params.append(section)
    if semester:
        query += " AND SEMESTER=?"
        params.append(semester)
    if min_cgpa:
        query += " AND CGPA>=?"
        params.append(min_cgpa)
    if max_cgpa:
        query += " AND CGPA<=?"
        params.append(max_cgpa)
    if email:
        query += " AND EMAIL LIKE ?"
        params.append(f"%{email}%")
    cursor.execute(query, params)
    return cursor.fetchall()

# Example: Search by department "AI" and CGPA >= 3.6
results = search_students(department="AI", min_cgpa=3.6)
for r in results:
    print(r)

connection.close()
