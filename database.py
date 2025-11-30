import sqlite3

# --- Database Setup ---
# conn = sqlite3.connect('attendanc.db', check_same_thread=False) 
# (Make sure you keep check_same_thread=False from the previous fix)
conn = sqlite3.connect('attendanc.db', check_same_thread=False)
cursor = conn.cursor()

# 1. Create Faculty Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS faculty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
''')

# 2. Create Lectures Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS lectures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day TEXT,
        lecture TEXT,
        time TEXT,
        faculty_id INTEGER,
        FOREIGN KEY(faculty_id) REFERENCES faculty(id)
    )
''')

# 3. Create Attendance Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll_no TEXT,
        date TEXT,
        time TEXT,
        lecture TEXT,
        status TEXT,
        emotion TEXT,
        UNIQUE(roll_no, date, lecture)
    )
''')

# 4. Create Admin Table (NEW)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')

# Initialize Default Admin if not exists
cursor.execute("SELECT * FROM admin WHERE username = 'admin'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO admin (username, password) VALUES ('admin', 'admin123')")
    conn.commit()

conn.commit()

# --- Load Faculty and Lectures from DB ---
def load_faculty():
    cursor.execute("SELECT id, name FROM faculty")
    return {row[1]: row[0] for row in cursor.fetchall()}

def load_lectures():
    cursor.execute("SELECT day, lecture, time, faculty.name FROM lectures JOIN faculty ON lectures.faculty_id = faculty.id")
    lecture_schedule = {}
    faculty_schedule = {}
    for row in cursor.fetchall():
        day, lec, time, fac = row
        if day not in lecture_schedule:
            lecture_schedule[day] = {}
            faculty_schedule[day] = {}
        lecture_schedule[day][lec] = time
        faculty_schedule[day][lec] = fac
    return lecture_schedule, faculty_schedule

faculty_dict = load_faculty()
lecture_schedule, faculty_schedule = load_lectures()