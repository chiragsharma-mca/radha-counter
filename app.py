import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Radha Naam Counter", 
    page_icon="🕉️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== ADVANCED PREMIUM CSS ====================
st.markdown("""
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&family=Yatra+One&display=swap');

    /* Hide Streamlit Default Top-bar & Footer for Native App Look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* App Background - Soft Creamy Spiritual Tint */
    .stApp {
        background: linear-gradient(180deg, #FFFDF9 0%, #FFF5E4 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Custom Title Styling with Spiritual Font */
    .spiritual-title {
        font-family: 'Yatra One', cursive;
        color: #FF6F00;
        font-size: 42px;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(255, 111, 0, 0.2);
        margin-top: 10px;
        margin-bottom: 0px;
    }
    
    .subtitle {
        text-align: center;
        color: #8D6E63;
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 35px;
    }

    /* Premium Card Containers */
    .custom-card {
        background: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0px 10px 25px rgba(255, 111, 0, 0.1);
        border: 1px solid #FFE0B2;
        margin-bottom: 20px;
    }

    /* Modern Gradient Buttons */
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #FF8F00 0%, #FF6F00 100%) !important;
        color: white !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        font-size: 18px !important;
        width: 100%;
        border: none !important;
        padding: 12px !important;
        box-shadow: 0px 6px 15px rgba(255, 111, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #FF6F00 0%, #E65100 100%) !important;
        box-shadow: 0px 8px 20px rgba(230, 81, 0, 0.5) !important;
        transform: translateY(-2px);
    }
    
    /* GIANT GLOWING ROUND "SHRI RADHA" BUTTON */
    .round-btn div[data-testid="stButton"] > button {
        background: radial-gradient(circle, #FFA000 0%, #FF6F00 70%, #E65100 100%) !important;
        color: #FFFFFF !important;
        width: 230px !important;
        height: 230px !important;
        border-radius: 50% !important;
        font-family: 'Yatra One', cursive !important;
        font-size: 42px !important;
        border: 6px solid #FFF3E0 !important;
        box-shadow: 0px 0px 30px rgba(255, 111, 0, 0.6), inset 0px 0px 15px rgba(255, 255, 255, 0.4) !important;
        margin: 15px auto !important;
        display: block !important;
    }
    .round-btn div[data-testid="stButton"] > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0px 0px 40px rgba(255, 111, 0, 0.9), inset 0px 0px 20px rgba(255, 255, 255, 0.6) !important;
    }

    /* Red Logout/Action Button */
    .btn-red div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #E53935 0%, #C62828 100%) !important;
        box-shadow: 0px 6px 15px rgba(211, 47, 47, 0.3) !important;
    }
    .btn-red div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #D32F2F 0%, #B71C1C 100%) !important;
        box-shadow: 0px 8px 20px rgba(183, 28, 28, 0.5) !important;
    }

    /* Giant Counter Display */
    .counter-display {
        text-align: center;
        font-size: 85px;
        font-weight: 800;
        color: #2C1810;
        margin-top: -15px;
        margin-bottom: 10px;
        text-shadow: 2px 2px 0px #FFE0B2;
    }
    
    /* Section Headers */
    h2, h3 {
        color: #E65100 !important;
        font-weight: 700 !important;
        text-align: center;
    }
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
                  ('admin', 'Male', 25, 'admin251095', 'chirag_25'))
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
    
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:20px; margin-bottom:20px;'>अपना रोल चुनें / Select Role</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        if st.button("🔒 ADMIN PANEL"): navigate_to("admin_login")
        st.write("")
        if st.button("🧘 NORMAL USER"): navigate_to("user_login")
    st.markdown("</div>", unsafe_allow_html=True)

def admin_login_page():
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("2>Admin Sign In</h2>", unsafe_allow_html=True)
    u = st.text_input("Admin Username", placeholder="Enter admin ID")
    p = st.text_input("Admin Password", type="password", placeholder="Enter password")
    st.write("")
    if st.button("LOGIN AS ADMIN"):
        conn = sqlite3.connect("radha_counter_web.db")
        if conn.execute("SELECT * FROM users WHERE username=? AND dob=? AND role='admin'", (u, p)).fetchone():
            st.session_state.current_user = u
            navigate_to("admin_dashboard")
        else: st.error("❌ Galat Admin Credentials!")
        conn.close()
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("← Back to Home"): navigate_to("home")

def user_login_page():
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h2>User Login</h2>", unsafe_allow_html=True)
    u = st.text_input("Username (Aapka Naam)", placeholder="Jaise: Chirag")
    p = st.text_input("Password (DOB: DDMMYYYY)", type="password", placeholder="Jaise: 09022023")
    st.write("")
    if st.button("LOGIN"):
        conn = sqlite3.connect("radha_counter_web.db")
        if conn.execute("SELECT * FROM users WHERE username=? AND dob=? AND role='user'", (u, p)).fetchone():
            st.session_state.current_user = u
            navigate_to("counter_page")
        else: st.error("❌ Wrong Username ya Password!")
        conn.close()
    
    st.markdown("<p style='text-align: center; margin-top:20px; font-weight:600; color:#555;'>New User?</p>", unsafe_allow_html=True)
    if st.button("✨ Register New Account"): navigate_to("register_page")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("← Back to Home"): navigate_to("home")

def register_page():
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h2>Create New Account</h2>", unsafe_allow_html=True)
    with st.form("reg_form"):
        name = st.text_input("Full Name", placeholder="Aapka Pura Naam")
        gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=5, max_value=120, step=1)
        dob = st.text_input("DOB (Format: 09022023)", placeholder="8 digits without slash")
        st.write("")
        if st.form_submit_button("REGISTER NOW"):
            if not name or not dob or len(dob) != 8:
                st.error("⚠️ Please enter correct details! It should be 8 digits .")
            else:
                try:
                    conn = sqlite3.connect("radha_counter_web.db")
                    conn.execute("INSERT INTO users (username, gender, age, dob) VALUES (?, ?, ?, ?)", (name, gender, age, dob))
                    conn.commit(); conn.close()
                    st.success(f"🎉 Registered! Login ID: {name}, Pass: {dob}")
                except sqlite3.IntegrityError: st.error("⚠️ Is naam ka user pehle se hai!")
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("← Back to Login"): navigate_to("user_login")

def counter_page():
    st.markdown(f"<div class='spiritual-title' style='font-size:32px;'>जय श्री कृष्ण, {st.session_state.current_user}!</div>", unsafe_allow_html=True)
    st.write("")
    
    # Glowing Round Button inside a Card
    st.markdown("<div class='custom-card' style='background: linear-gradient(180deg, #FFFFFF 0%, #FFFDF5 100%);'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown('<div class="round-btn">', unsafe_allow_html=True)
        if st.button("श्री राधा"):
            if st.session_state.count == 0: st.session_state.start_time = datetime.now()
            st.session_state.count += 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown(f"<div class='counter-display'>{st.session_state.count}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Auto Save & Logout
    col_btn1, col_btn2, col_btn3 = st.columns([1, 4, 1])
    with col_btn2:
        st.markdown('<div class="btn-red">', unsafe_allow_html=True)
        if st.button("🔴 LOGOUT & SAVE SESSION"):
            if st.session_state.count > 0:
                end_time = datetime.now()
                s_date = st.session_state.start_time.strftime("%Y-%m-%d")
                s_time = st.session_state.start_time.strftime("%H:%M:%S")
                e_time = end_time.strftime("%H:%M:%S")
                conn = sqlite3.connect("radha_counter_web.db")
                conn.execute("INSERT INTO reports (username, session_date, start_time, end_time, total_count) VALUES (?, ?, ?, ?, ?)",
                             (st.session_state.current_user, s_date, s_time, e_time, st.session_state.count))
                conn.commit(); conn.close()
            st.session_state.current_user = None; st.session_state.count = 0; st.session_state.start_time = None
            navigate_to("home")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-bottom:15px;'>📊 My Previous Reports</h3>", unsafe_allow_html=True)
    conn = sqlite3.connect("radha_counter_web.db")
    df = pd.read_sql_query(f"SELECT session_date as Date, start_time as Start, end_time as End, total_count as Count FROM reports WHERE username='{st.session_state.current_user}' ORDER BY id DESC", conn)
    conn.close()
    if not df.empty: st.dataframe(df, use_container_width=True, hide_index=True)
    else: st.info("Still there is no session Let's start from today!")
    st.markdown("</div>", unsafe_allow_html=True)

def admin_dashboard():
    st.markdown("<div class='spiritual-title' style='color:#D32F2F; font-size:36px;'>Admin Control Panel</div>", unsafe_allow_html=True)
    st.write("")
    
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["👥 Registered Users", "📈 All Counter Reports"])
    conn = sqlite3.connect("radha_counter_web.db")
    with tab1:
        st.dataframe(pd.read_sql_query("SELECT username as Username, gender as Gender, age as Age, dob as Password FROM users WHERE role!='admin' ORDER BY id DESC", conn), use_container_width=True, hide_index=True)
    with tab2:
        st.dataframe(pd.read_sql_query("SELECT username as User, session_date as Date, start_time as Start, end_time as End, total_count as Count FROM reports ORDER BY id DESC", conn), use_container_width=True, hide_index=True)
    conn.close()
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<div class="btn-red">', unsafe_allow_html=True)
        if st.button("🔴 Admin Logout"): st.session_state.current_user = None; navigate_to("home")
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== ROUTER ====================
if st.session_state.page == 'home': home_page()
elif st.session_state.page == 'admin_login': admin_login_page()
elif st.session_state.page == 'user_login': user_login_page()
elif st.session_state.page == 'register_page': register_page()
elif st.session_state.page == 'counter_page': counter_page()
elif st.session_state.page == 'admin_dashboard': admin_dashboard()
