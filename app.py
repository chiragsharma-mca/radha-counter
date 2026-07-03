import streamlit as st
import sqlite3
from datetime import datetime, timezone, timedelta
import pandas as pd

# ==================== INDIAN TIMEZONE (IST) SETUP ====================
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST)

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Radha Naam Counter", 
    page_icon="🕉️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== GUARANTEED ROUND BUTTON CSS ====================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&family=Yatra+One&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(180deg, #FFFDF9 0%, #FFF5E4 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    .spiritual-title {
        font-family: 'Yatra One', cursive;
        color: #FF6F00;
        font-size: 42px;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(255, 111, 0, 0.2);
        margin-top: 10px;
    }
    
    .subtitle {
        text-align: center;
        color: #8D6E63;
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 25px;
    }

    .form-container {
        max-width: 400px;
        margin: 0 auto;
        background: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0px 10px 25px rgba(255, 111, 0, 0.1);
        border: 1px solid #FFE0B2;
    }

    /* 1. NORMAL BUTTONS (Login, Register, Admin etc.) */
    button[kind="secondary"], button[kind="secondaryFormSubmit"], button[kind="primaryFormSubmit"] {
        background: linear-gradient(135deg, #FF8F00 0%, #FF6F00 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        width: 100% !important;
        height: 48px !important;
        border: none !important;
        box-shadow: 0px 4px 10px rgba(255, 111, 0, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #FF6F00 0%, #E65100 100%) !important;
        transform: translateY(-2px) !important;
    }
    
    /* 2. GUARANTEED GIANT ROUND "SHRI RADHA" BUTTON (PRIMARY TYPE) */
    button[kind="primary"] {
        background: radial-gradient(circle, #FFA000 0%, #FF6F00 70%, #E65100 100%) !important;
        color: #FFFFFF !important;
        width: 260px !important;
        height: 260px !important;
        border-radius: 50% !important;
        font-family: 'Yatra One', cursive, sans-serif !important;
        font-size: 45px !important;
        font-weight: bold !important;
        border: 8px solid #FFF3E0 !important;
        box-shadow: 0px 10px 30px rgba(255, 111, 0, 0.6), inset 0px 0px 15px rgba(255, 255, 255, 0.4) !important;
        margin: 15px auto !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 !important;
        transition: transform 0.1s ease !important;
    }
    button[kind="primary"]:hover {
        transform: scale(1.04) !important;
        box-shadow: 0px 15px 40px rgba(255, 111, 0, 0.8) !important;
    }

    /* Counter Display (Theek Button Ke Niche) */
    .counter-display {
        text-align: center;
        font-size: 65px;
        font-weight: 800;
        color: #2C1810;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    /* Custom Table/Grid Design */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        font-size: 14px;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
    }
    .custom-table th {
        background-color: #FF8F00;
        color: white;
        text-align: left;
        padding: 12px 15px;
        font-weight: 600;
    }
    .custom-table td {
        padding: 12px 15px;
        border-bottom: 1px solid #FFE0B2;
        color: #444;
        background-color: #FFFFFF;
    }
    .custom-table tr:hover td {
        background-color: #FFF3E0;
    }
    
    h2, h3 { color: #E65100 !important; text-align: center; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# ==================== DATABASE SETUP ====================
def setup_db():
    conn = sqlite3.connect("radha_counter_web.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE, gender TEXT, age INTEGER, dob TEXT, role TEXT DEFAULT 'user')''')
    c.execute('''CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT, session_date TEXT, start_time TEXT, end_time TEXT, total_count INTEGER)''')
    
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, gender, age, dob, role) VALUES (?, ?, ?, ?, ?)",
                  ('admin', 'Male', 25, 'admin123', 'admin'))
    conn.commit()
    conn.close()

setup_db()

# ==================== SESSION STATE ====================
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'count' not in st.session_state: st.session_state.count = 0
if 'start_time' not in st.session_state: st.session_state.start_time = None

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ==================== VIEWS & PAGES ====================
def home_page():
    st.markdown("<div class='spiritual-title'>जय श्री राधा रानी</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>— SPIRITUAL COUNTING APP —</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    st.markdown("<h3>Select Role</h3>", unsafe_allow_html=True)
    if st.button("🔒 ADMIN PANEL"): navigate_to("admin_login")
    st.write("")
    if st.button("🧘 NORMAL USER"): navigate_to("user_login")
    st.markdown("</div>", unsafe_allow_html=True)

def admin_login_page():
    st.markdown("<div class='spiritual-title'>Admin Access</div>", unsafe_allow_html=True)
    st.write("")
    
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    u = st.text_input("Admin Username", placeholder="Enter ID")
    p = st.text_input("Admin Password", type="password", placeholder="Enter Password")
    st.write("")
    if st.button("LOGIN AS ADMIN"):
        conn = sqlite3.connect("radha_counter_web.db")
        if conn.execute("SELECT * FROM users WHERE username=? AND dob=? AND role='admin'", (u, p)).fetchone():
            st.session_state.current_user = u
            # Check if using default password, force reset
            if p == 'admin123':
                navigate_to("admin_reset_password")
            else:
                navigate_to("admin_dashboard")
        else: st.error("❌ Galat Admin Credentials!")
        conn.close()
    
    st.write("")
    if st.button("← Back to Home"): navigate_to("home")
    st.markdown("</div>", unsafe_allow_html=True)

def admin_reset_password_page():
    st.markdown("<div class='spiritual-title'>Update Password</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Please change your default password to continue.</div>", unsafe_allow_html=True)
    st.write("")
    
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    new_pass = st.text_input("Enter New Password", type="password")
    confirm_pass = st.text_input("Confirm New Password", type="password")
    st.write("")
    
    if st.button("UPDATE PASSWORD"):
        if not new_pass or not confirm_pass:
            st.error("⚠️ Password fields cannot be empty!")
        elif new_pass == 'admin123':
            st.error("⚠️ Please choose a different password than default!")
        elif new_pass != confirm_pass:
            st.error("⚠️ Passwords do not match!")
        else:
            conn = sqlite3.connect("radha_counter_web.db")
            conn.execute("UPDATE users SET dob=? WHERE username=? AND role='admin'", (new_pass, st.session_state.current_user))
            conn.commit(); conn.close()
            st.success("✅ Password Updated Successfully!")
            navigate_to("admin_dashboard")
            
    st.write("---")
    if st.button("← Logout"): st.session_state.current_user = None; navigate_to("home")
    st.markdown("</div>", unsafe_allow_html=True)

def user_login_page():
    st.markdown("<div class='spiritual-title'>User Login</div>", unsafe_allow_html=True)
    st.write("")
    
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    u = st.text_input("Username (Name)", placeholder="Jaise: Chirag")
    p = st.text_input("Password (DOB)", type="password", placeholder="Jaise: 09022023")
    st.write("")
    if st.button("LOGIN"):
        conn = sqlite3.connect("radha_counter_web.db")
        if conn.execute("SELECT * FROM users WHERE username=? AND dob=? AND role='user'", (u, p)).fetchone():
            st.session_state.current_user = u
            navigate_to("counter_page")
        else: st.error("❌ Wrong Username ya Password!")
        conn.close()
    
    st.write("---")
    if st.button("✨ Register New Account"): navigate_to("register_page")
    st.write("")
    if st.button("← Back to Home"): navigate_to("home")
    st.markdown("</div>", unsafe_allow_html=True)

def register_page():
    st.markdown("<div class='spiritual-title'>Registration</div>", unsafe_allow_html=True)
    st.write("")
    
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    with st.form("reg_form"):
        name = st.text_input("Full Name", placeholder="Aapka Naam")
        gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=5, max_value=120, step=1)
        dob = st.text_input("DOB (Format: 09022023)", placeholder="8 digits")
        st.write("")
        if st.form_submit_button("REGISTER NOW"):
            if not name or not dob or len(dob) != 8:
                st.error("⚠️ Sahi details bharein! DOB 8 digits.")
            else:
                try:
                    conn = sqlite3.connect("radha_counter_web.db")
                    conn.execute("INSERT INTO users (username, gender, age, dob) VALUES (?, ?, ?, ?)", (name, gender, age, dob))
                    conn.commit(); conn.close()
                    st.success(f"🎉 Registered! Login ID: {name}, Pass: {dob}")
                except sqlite3.IntegrityError: st.error("⚠️ Is naam ka user pehle se hai!")
    
    st.write("")
    if st.button("← Back to Login"): navigate_to("user_login")
    st.markdown("</div>", unsafe_allow_html=True)

def counter_page():
    st.markdown(f"<div class='spiritual-title' style='font-size:32px;'>जय श्री कृष्ण, {st.session_state.current_user}!</div>", unsafe_allow_html=True)
    st.write("")
    
    # 1. GUARANTEED GIANT ROUND BUTTON (Using type="primary")
    if st.button("श्री राधा", type="primary"):
        if st.session_state.count == 0: 
            st.session_state.start_time = get_ist_now()
        st.session_state.count += 1
        st.rerun()
        
    # 2. COUNTER NUMBER (Theek Niche)
    st.markdown(f"<div class='counter-display'>{st.session_state.count}</div>", unsafe_allow_html=True)
    
    # 3. LOGOUT & SAVE BUTTON
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button("🔴 LOGOUT & SAVE SESSION"):
            if st.session_state.count > 0:
                end_time = get_ist_now()
                s_date = st.session_state.start_time.strftime("%Y-%m-%d")
                s_time = st.session_state.start_time.strftime("%I:%M:%S %p")
                e_time = end_time.strftime("%I:%M:%S %p")
                conn = sqlite3.connect("radha_counter_web.db")
                conn.execute("INSERT INTO reports (username, session_date, start_time, end_time, total_count) VALUES (?, ?, ?, ?, ?)",
                             (st.session_state.current_user, s_date, s_time, e_time, st.session_state.count))
                conn.commit(); conn.close()
            st.session_state.current_user = None; st.session_state.count = 0; st.session_state.start_time = None
            navigate_to("home")

    st.write("---")
    st.markdown("<h3>📊 My Previous Reports</h3>", unsafe_allow_html=True)
    
    conn = sqlite3.connect("radha_counter_web.db")
    rows = conn.execute("SELECT session_date, start_time, end_time, total_count FROM reports WHERE username=? ORDER BY id DESC", (st.session_state.current_user,)).fetchall()
    conn.close()
    
    if rows:
        html = "<table class='custom-table'><tr><th>Date</th><th>Start Time</th><th>End Time</th><th>Total Count</th></tr>"
        for row in rows:
            html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td><b>{row[3]}</b></td></tr>"
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("Abhi tak koi session save nahi hua hai. Aaj se shuruaat karein!")

def admin_dashboard():
    st.markdown("<div class='spiritual-title' style='color:#D32F2F; font-size:36px;'>Admin Control Panel</div>", unsafe_allow_html=True)
    st.write("")
    
    tab1, tab2 = st.tabs(["👥 Registered Users", "📈 All Counter Reports"])
    
    conn = sqlite3.connect("radha_counter_web.db")
    
    with tab1:
        users = conn.execute("SELECT username, gender, age, dob FROM users WHERE role!='admin' ORDER BY id DESC").fetchall()
        if users:
            u_html = "<table class='custom-table'><tr><th>Username</th><th>Gender</th><th>Age</th><th>Password (DOB)</th></tr>"
            for u in users:
                u_html += f"<tr><td>{u[0]}</td><td>{u[1]}</td><td>{u[2]}</td><td>{u[3]}</td></tr>"
            u_html += "</table>"
            st.markdown(u_html, unsafe_allow_html=True)
        else:
            st.write("No users registered yet.")

    with tab2:
        reports = conn.execute("SELECT username, session_date, start_time, end_time, total_count FROM reports ORDER BY id DESC").fetchall()
        if reports:
            r_html = "<table class='custom-table'><tr><th>User</th><th>Date</th><th>Start Time</th><th>End Time</th><th>Count</th></tr>"
            for r in reports:
                r_html += f"<tr><td><b>{r[0]}</b></td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td><b>{r[4]}</b></td></tr>"
            r_html += "</table>"
            st.markdown(r_html, unsafe_allow_html=True)
        else:
            st.write("No reports generated yet.")
            
    conn.close()
    
    st.write("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔴 Admin Logout"): st.session_state.current_user = None; navigate_to("home")

# ==================== ROUTER ====================
if st.session_state.page == 'home': home_page()
elif st.session_state.page == 'admin_login': admin_login_page()
elif st.session_state.page == 'admin_reset_password': admin_reset_password_page()
elif st.session_state.page == 'user_login': user_login_page()
elif st.session_state.page == 'register_page': register_page()
elif st.session_state.page == 'counter_page': counter_page()
elif st.session_state.page == 'admin_dashboard': admin_dashboard()
