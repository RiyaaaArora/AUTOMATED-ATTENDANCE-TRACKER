import streamlit as st
import os
# --- Ensure Photos Folder Exists ---
if not os.path.exists("Photos"):
    os.makedirs("Photos")

# --- Page Config ---
st.set_page_config(page_title="Advanced Attendance System", page_icon="face", layout="wide")

# ============================
# 🎨 CUSTOM SIDEBAR DESIGN
# ============================

st.markdown("""
<style>

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E90FF, #F01E2C);
    padding: 20px;
}

.sidebar-title {
    color: white;
    font-size: 28px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 20px;
}

.menu-btn {
    background-color: rgba(255,255,255,0.15);
    padding: 12px 18px;
    margin-top: 10px;
    border-radius: 10px;
    color: white;
    font-size: 18px;
    cursor: pointer;
    border: 1px solid rgba(255,255,255,0.3);
    text-align: left;
    transition: 0.2s;
}

.menu-btn:hover {
    background-color: rgba(255,255,255,0.3);
    transform: translateX(6px);
}

.menu-btn-selected {
    background-color: white !important;
    color: #1E90FF !important;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# --- Initialize session_state attributes ---
if "camera_active" not in st.session_state:
    st.session_state.camera_active = False
if "selected_person" not in st.session_state:
    st.session_state.selected_person = None