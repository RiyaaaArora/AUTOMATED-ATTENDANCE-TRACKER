import streamlit as st
import pandas as pd
import sqlite3
import os
# Import dependencies
from database import cursor, conn

def admin_panel():
    st.markdown("""
    <style>
    .admin-header {
        background: linear-gradient(90deg, #4CAF50, #FFFFFF);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .admin-card {
        background: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    if not st.session_state.admin_logged_in:
        st.markdown('<div class="admin-header">🔒 Admin Login</div>', unsafe_allow_html=True)
        with st.form("admin_login"):
            admin_id = st.text_input("Admin ID")
            admin_pass = st.text_input("Admin Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                # CHECK DB FOR CREDENTIALS
                cursor.execute("SELECT password FROM admin WHERE username = ?", (admin_id,))
                result = cursor.fetchone()
                
                if result and result[0] == admin_pass:
                    st.session_state.admin_logged_in = True
                    st.session_state.admin_option = None
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
    else:
        st.markdown('<div class="admin-header">🛠️ Admin Panel - Manage System Data</div>', unsafe_allow_html=True)
        
        # --- TOP ROW: LOGOUT & CHANGE PASSWORD ---
        col_main1, col_main2 = st.columns([1, 1])
        with col_main1:
            if st.button("Logout"):
                st.session_state.admin_logged_in = False
                st.session_state.admin_option = None
                st.rerun()
        
        # --- CHANGE PASSWORD SECTION ---
        with st.expander("🔐 Change Admin Password"):
            with st.form("change_pass_form"):
                current_user = st.text_input("Confirm Username", value="admin")
                new_pass = st.text_input("New Password", type="password")
                confirm_pass = st.text_input("Confirm New Password", type="password")
                
                if st.form_submit_button("Update Password"):
                    if new_pass == confirm_pass and new_pass != "":
                        cursor.execute("UPDATE admin SET password = ? WHERE username = ?", (new_pass, current_user))
                        conn.commit()
                        st.success("Password updated successfully! Please login again.")
                        st.session_state.admin_logged_in = False # Force logout to test new pass
                        st.rerun()
                    else:
                        st.error("Passwords do not match or are empty.")
        # Load faculties
        cursor.execute("SELECT id, name FROM faculty")
        faculties = cursor.fetchall()
        
        # Options as "keys" (buttons) for Manage Students, Faculty, Lectures
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📚 Manage Students", key="manage_students"):
                st.session_state.admin_option = "students"
        with col2:
            if st.button("👨‍🏫 Manage Faculty", key="manage_faculty"):
                st.session_state.admin_option = "faculty"
        with col3:
            if st.button("📖 Manage Lectures", key="manage_lectures"):
                st.session_state.admin_option = "lectures"
        
        # Display selected option details only if an option is selected
        if st.session_state.admin_option:
            option = st.session_state.admin_option
            
            if option == "students":
                st.markdown('<div class="admin-card">', unsafe_allow_html=True)
                st.subheader("Manage Students")
                
                # List existing students
                cursor.execute("SELECT name, roll_no FROM attendance GROUP BY name, roll_no")
                persons = cursor.fetchall()
                if persons:
                    df_persons = pd.DataFrame(persons, columns=["Name", "Roll No"])
                    st.table(df_persons)
                
                # Add New Student
                with st.expander("Add New Student"):
                    with st.form("add_person"):
                        new_name = st.text_input("Name")
                        new_roll = st.text_input("Roll No")
                        submitted = st.form_submit_button("Add Student")
                        if submitted and new_name and new_roll:
                            st.success(f"Student {new_name} ({new_roll}) added. Upload photo in 'Add New Face' mode.")
                
                # Edit/Delete Student
                if persons:
                    with st.expander("Edit/Delete Student"):
                        # FIX: Sort the dropdown list numerically using the sorting logic we added earlier
                        student_list = [f"{p[0]} ({p[1]})" for p in persons]
                        edit_person = st.selectbox("Select Student to Edit/Delete", student_list)
                        
                        if edit_person:
                            name, roll = edit_person.split(" (")
                            roll = roll.rstrip(")")
                            
                            new_name_edit = st.text_input("New Name", value=name, key=f"edit_name_{roll}")
                            new_roll_edit = st.text_input("New Roll No", value=roll, key=f"edit_roll_{roll}")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Update Student", key=f"update_person_{roll}"):
                                    if new_name_edit and new_roll_edit:
                                        try:
                                            # FIX: Added try-except block to handle duplicate Roll Numbers
                                            cursor.execute("UPDATE attendance SET name = ?, roll_no = ? WHERE name = ? AND roll_no = ?", (new_name_edit, new_roll_edit, name, roll))
                                            conn.commit()
                                            
                                            # Rename photo file if roll no changed
                                            old_path = os.path.join("Photos", f"{name}_{roll}.jpg")
                                            new_path = os.path.join("Photos", f"{new_name_edit}_{new_roll_edit}.jpg")
                                            if os.path.exists(old_path):
                                                os.rename(old_path, new_path)
                                                
                                            st.success("Student updated successfully.")
                                            st.rerun()
                                        except sqlite3.IntegrityError:
                                            st.error(f"Error: Roll Number {new_roll_edit} already exists or has conflicting attendance records. You cannot merge two students this way.")
                                    else:
                                        st.error("Name and Roll No cannot be empty.")
                            with col2:
                                if st.button("Delete Student", key=f"delete_person_{roll}"):
                                    cursor.execute("DELETE FROM attendance WHERE name = ? AND roll_no = ?", (name, roll))
                                    conn.commit()
                                    photo_path = os.path.join("Photos", f"{name}_{roll}.jpg")
                                    if os.path.exists(photo_path):
                                        os.remove(photo_path)
                                    st.success("Student deleted.")
                                    st.rerun()
                            
                st.markdown('</div>', unsafe_allow_html=True)
            
            elif option == "faculty":
                st.markdown('<div class="admin-card">', unsafe_allow_html=True)
                st.subheader("Manage Faculty")
                
                # List existing faculty
                if faculties:
                    df_fac = pd.DataFrame(faculties, columns=["ID", "Name"])
                    st.table(df_fac)
                
                # Add New Faculty
                with st.expander("Add New Faculty"):
                    with st.form("add_faculty"):
                        fac_name = st.text_input("Faculty Name")
                        submitted = st.form_submit_button("Add Faculty")
                        if submitted and fac_name:
                            try:
                                cursor.execute("INSERT INTO faculty (name) VALUES (?)", (fac_name,))
                                conn.commit()
                                st.success("Faculty added.")
                                st.rerun()
                            except sqlite3.IntegrityError:
                                st.error("Faculty with this name already exists.")
                
                # Edit/Delete Faculty
                if faculties:
                    with st.expander("Edit/Delete Faculty"):
                        edit_fac = st.selectbox("Select Faculty to Edit/Delete", [f"{f[1]} (ID: {f[0]})" for f in faculties])
                        if edit_fac:
                            fac_id = int(edit_fac.split("(ID: ")[1].rstrip(")"))
                            new_name = st.text_input("New Name", key=f"new_name_{fac_id}")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Update Faculty", key=f"update_{fac_id}"):
                                    if new_name:
                                        cursor.execute("UPDATE faculty SET name = ? WHERE id = ?", (new_name, fac_id))
                                        conn.commit()
                                        st.success("Faculty updated.")
                                        st.rerun()
                                    else:
                                        st.error("New name cannot be empty.")
                            with col2:
                                if st.button("Delete Faculty", key=f"delete_{fac_id}"):
                                    cursor.execute("DELETE FROM faculty WHERE id = ?", (fac_id,))
                                    conn.commit()
                                    st.success("Faculty deleted.")
                                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 3. LECTURES
            elif option == "lectures":
                st.markdown('<div class="admin-card">', unsafe_allow_html=True)
                st.subheader("Manage Lectures")
                
                # List existing lectures
                cursor.execute("SELECT lectures.id, day, lecture, time, faculty.name FROM lectures JOIN faculty ON lectures.faculty_id = faculty.id")
                lectures = cursor.fetchall()
                if lectures:
                    df_lec = pd.DataFrame(lectures, columns=["ID", "Day", "Lecture", "Time", "Faculty"])
                    st.table(df_lec)
                
                # Add New Lecture
                with st.expander("Add New Lecture"):
                    with st.form("add_lecture"):
                        day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
                        lec_name = st.text_input("Lecture Name")
                        time = st.text_input("Time (HH:MM)")
                        fac_id = st.selectbox("Faculty", [f"{f[1]} (ID: {f[0]})" for f in faculties] if faculties else [])
                        
                        if st.form_submit_button("Add Lecture"):
                            if lec_name and time and fac_id:
                                fac_id_num = int(fac_id.split("(ID: ")[1].rstrip(")"))
                                
                                # FIX: Check if lecture exists BEFORE inserting
                                cursor.execute("SELECT COUNT(*) FROM lectures WHERE day = ? AND time = ?", (day, time))
                                count = cursor.fetchone()[0]
                                
                                if count > 0:
                                    st.error(f"⚠️ A lecture already exists on {day} at {time}. Cannot add duplicate.")
                                else:
                                    cursor.execute("INSERT INTO lectures (day, lecture, time, faculty_id) VALUES (?, ?, ?, ?)", (day, lec_name, time, fac_id_num))
                                    conn.commit()
                                    st.success(f"✅ Lecture '{lec_name}' added successfully at {time}.")
                                    st.rerun()
                            else:
                                st.error("Please fill in all fields.")
                
            
                
                # Edit/Delete Lecture
                if lectures:
                    with st.expander("Edit/Delete Lecture"):
                        edit_lec = st.selectbox("Select Lecture to Edit/Delete", [f"{l[2]} (ID: {l[0]})" for l in lectures])
                        if edit_lec:
                            lec_id = int(edit_lec.split("(ID: ")[1].rstrip(")"))
                            new_day = st.selectbox("New Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], key=f"new_day_{lec_id}")
                            new_lec = st.text_input("New Lecture Name", key=f"new_lec_{lec_id}")
                            new_time = st.text_input("New Time", key=f"new_time_{lec_id}")
                            new_fac = st.selectbox("New Faculty", [f"{f[1]} (ID: {f[0]})" for f in faculties] if faculties else [], key=f"new_fac_{lec_id}")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("Update Lecture", key=f"update_lec_{lec_id}"):
                                    if new_lec and new_time and new_fac:
                                        new_fac_id = int(new_fac.split("(ID: ")[1].rstrip(")"))
                                        cursor.execute("UPDATE lectures SET day = ?, lecture = ?, time = ?, faculty_id = ? WHERE id = ?", (new_day, new_lec, new_time, new_fac_id, lec_id))
                                        conn.commit()
                                        st.success("Lecture updated.")
                                        st.rerun()
                                    else:
                                        st.error("All fields must be filled.")
                            with col2:
                                if st.button("Delete Lecture", key=f"delete_lec_{lec_id}"):
                                    cursor.execute("DELETE FROM lectures WHERE id = ?", (lec_id,))
                                    conn.commit()
                                    st.success("Lecture deleted.")
                                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)