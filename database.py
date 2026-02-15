import sqlite3

DB_NAME = "student.db"

# Update only CGPA
def update_student_cgpa(roll_no, new_cgpa):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE STUDENT
        SET CGPA = ?
        WHERE ROLL_NO = ?
    """, (new_cgpa, roll_no))

    conn.commit()
    conn.close()
    print("✔ CGPA updated successfully!")


# Update multiple fields
def update_student_info(roll_no, name=None, department=None, section=None,
                        semester=None, cgpa=None, email=None, phone=None, address=None):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if name:
        cursor.execute("UPDATE STUDENT SET NAME=? WHERE ROLL_NO=?", (name, roll_no))

    if department:
        cursor.execute("UPDATE STUDENT SET DEPARTMENT=? WHERE ROLL_NO=?", (department, roll_no))

    if section:
        cursor.execute("UPDATE STUDENT SET SECTION=? WHERE ROLL_NO=?", (section, roll_no))

    if semester:
        cursor.execute("UPDATE STUDENT SET SEMESTER=? WHERE ROLL_NO=?", (semester, roll_no))

    if cgpa:
        cursor.execute("UPDATE STUDENT SET CGPA=? WHERE ROLL_NO=?", (cgpa, roll_no))

    if email:
        cursor.execute("UPDATE STUDENT SET EMAIL=? WHERE ROLL_NO=?", (email, roll_no))

    if phone:
        cursor.execute("UPDATE STUDENT SET PHONE=? WHERE ROLL_NO=?", (phone, roll_no))

    if address:
        cursor.execute("UPDATE STUDENT SET ADDRESS=? WHERE ROLL_NO=?", (address, roll_no))

    conn.commit()
    conn.close()
    print("✔ Student information updated successfully!")


# Delete a student
def delete_student(roll_no):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM STUDENT WHERE ROLL_NO=?", (roll_no,))
    
    conn.commit()
    conn.close()
    print("✔ Student deleted successfully!")


# Example usage (you can remove this part if not needed)
if __name__ == "__main__":
    update_student_cgpa(101, 3.95)
    update_student_info(101, name="Ahtasham", address="New Bahawalpur")
    delete_student(102)
