import sqlite3

connection = sqlite3.connect("student.db")
cursor = connection.cursor()

# Drop old table (only if you don't need old data)
cursor.execute("DROP TABLE IF EXISTS STUDENT")

# Create new table with EMAIL
cursor.execute("""
CREATE TABLE STUDENT (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT,
    CLASS TEXT,
    SECTION TEXT,
    MARKS INTEGER,
    EMAIL TEXT
)
""")

# Insert data with email
students = [
    ("Ali", "AI", "A", 85, "ali@example.com"),
    ("Kamil", "Data Science", "B", 90, "kamil@example.com"),
    ("Muzamil", "Software Engineering", "B", 90, "muzamil@example.com"),
    ("Daoud", "Data Science", "B", 90, "daoud@example.com"),
    ("Saad", "Computer Science", "B", 90, "saad@example.com"),
    ("Tanveer", "Information Technology", "B", 90, "tanveer@example.com")
]

for s in students:
    cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS, EMAIL) VALUES (?, ?, ?, ?, ?)", s)

connection.commit()

# Fetch all
cursor.execute("SELECT * FROM STUDENT")
rows = cursor.fetchall()
for row in rows:
    print(row)

connection.close()
