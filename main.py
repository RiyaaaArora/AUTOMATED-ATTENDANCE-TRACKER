# Import all modules
from config import *
from database import *
from utils import *
from face_utils import *
from emotion_utils import *
from ui_functions import *
from admin import *

# --- Main Logic ---
if __name__ == "__main__":

# Attractive title for the front dashboard
    st.markdown("<h1 style='text-align: center; color: #4CAF50; font-family: Arial, sans-serif;'>Lecture Lens</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555;'>DAV University, Jalandhar</h3>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 🎯 SIDEBAR MENU (ONLY ADMIN PANEL)
    # -------------------------------------------------------------
    st.sidebar.markdown("<div class='sidebar-title'>📌 Navigation</div>", unsafe_allow_html=True)

    # Only Admin Panel in sidebar
    if st.sidebar.button("⚙️ Admin Panel", key="Admin Panel", use_container_width=True,
                         help="Go to Admin Panel",
                         type="secondary"):
        st.session_state.app_mode = "Admin Panel"

    # Initialize selected mode to "Home"
    if "app_mode" not in st.session_state:
        st.session_state.app_mode = "Home"

    app_mode = st.session_state.app_mode
    # -------------------------------------------------------------

    # ---- Run selected mode ----
    if app_mode == "Home":
        # Attractive Home Page Content
        st.markdown("""
        <div style='text-align: center; margin-top: 50px;'>
            <h2 style='color: #2196F3; font-family: Arial, sans-serif;'>Welcome to Lecture Lens!</h2>
            <p style='font-size: 18px; color: #666; margin-bottom: 30px;'>Your Smart Attendance Tracking Solution for DAV University, Jalandhar</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mode Buttons on Dashboard
        st.markdown("<h3 style='text-align: center; color: #333;'>Select a Mode to Get Started:</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("😀 Mark Attendance", key="btn_recognize", use_container_width=True):
                st.session_state.app_mode = "Recognize Face & Emotion"
            st.markdown("<p style='text-align: center; color: #666;'>Mark attendance with face and emotion detection.</p>", unsafe_allow_html=True)
            
            if st.button("➕ Add New Face", key="btn_add", use_container_width=True):
                st.session_state.app_mode = "Add New Face"
            st.markdown("<p style='text-align: center; color: #666;'>Register a new student.</p>", unsafe_allow_html=True)
        
        with col2:
            if st.button("⏳ Close Attendance", key="btn_close", use_container_width=True):
                st.session_state.app_mode = "Close Attendance"
            st.markdown("<p style='text-align: center; color: #666;'>End the current attendance session.</p>", unsafe_allow_html=True)
            
            if st.button("📄 View Records", key="btn_records", use_container_width=True):
                st.session_state.app_mode = "View Records"
            st.markdown("<p style='text-align: center; color: #666;'>Check attendance records.</p>", unsafe_allow_html=True)
        
        with col3:
            if st.button("📊 View Attendance Summary", key="btn_summary", use_container_width=True):
                st.session_state.app_mode = "View Attendance Summary"
            st.markdown("<p style='text-align: center; color: #666;'>See summary analytics.</p>", unsafe_allow_html=True)
            
            if st.button("🗓️ View Timetable", key="btn_timetable", use_container_width=True):
                st.session_state.app_mode = "View Timetable"
            st.markdown("<p style='text-align: center; color: #666;'>View class schedules.</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: center; margin-top: 40px;'>
            <p style='font-size: 16px; color: #888;'>Click on a mode above to proceed. Use the sidebar for Admin Panel.</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif app_mode == "Recognize Face & Emotion":
        recognize_face()
        if st.button("🔙 Back to Home", key="back_home_recognize"):
            st.session_state.app_mode = "Home"
            st.rerun()  # Force rerun to update immediately
        
    elif app_mode == "Add New Face":
        add_new_face()
        if st.button("🔙 Back to Home", key="back_home_add"):
            st.session_state.app_mode = "Home"
            st.rerun()
        
    elif app_mode == "Close Attendance":
        close_attendance()
        if st.button("🔙 Back to Home", key="back_home_close"):
            st.session_state.app_mode = "Home"
            st.rerun()
        
    elif app_mode == "View Records":
        view_attendance_records()
        if st.button("🔙 Back to Home", key="back_home_records"):
            st.session_state.app_mode = "Home"
            st.rerun()
        
    elif app_mode == "View Attendance Summary":
        view_attendance_summary()
        if st.button("🔙 Back to Home", key="back_home_summary"):
            st.session_state.app_mode = "Home"
            st.rerun()
        
    elif app_mode == "View Timetable":
        view_timetable()
        if st.button("🔙 Back to Home", key="back_home_timetable"):
            st.session_state.app_mode = "Home"
            st.rerun()
        
    elif app_mode == "Admin Panel":
        admin_panel()
        if st.button("🔙 Back to Home", key="back_home_admin"):
            st.session_state.app_mode = "Home"
            st.session_state.admin_logged_in = False  
            st.rerun()