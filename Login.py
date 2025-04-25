import streamlit as st
from utils.user_utils import authenticate_user, get_user_details
import time
#from utils.cookies_manage import cookie_controller
from streamlit_cookies_controller import CookieController
#from streamlit_local_storage import LocalStorage

cookie_controller = CookieController()
# cookie_controller = LocalStorage()

def login_page():
    st.title("Login")
    email = st.text_input("UserName")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        role = authenticate_user(email, password)
        user = get_user_details(email)
        if role:
            st.success("Login successful!")
            st.session_state["user_id"] = user[0][0]
            st.session_state["username"] = user[0][1]
            st.success(f"Welcome, {st.session_state['username']}!")
            st.session_state.logged_in = True
            st.session_state.role = role
            
            cookie_controller.set("user_id", user[0][0])
            cookie_controller.set("username", user[0][1])
            cookie_controller.set("logged_in", True)
            cookie_controller.set("role", role)
            
            time.sleep(1)
            st.query_params = {"page": "main"}
            st.rerun()
        else:
            st.error("Invalid email or password.")

def clear_cookies():
    cookie_controller.remove("user_id")
    cookie_controller.remove("username")
    cookie_controller.remove("role")
    cookie_controller.remove("logged_in")
    # cookie_controller.deleteAll()
