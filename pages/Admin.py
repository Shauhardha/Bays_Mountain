import streamlit as st
from Login import login_page, cookie_controller, clear_cookies
from utils.user_utils import add_user, hash_password, check_email_exists, get_users_det, get_all_users, update_user, authenticate_user, update_password
from utils.navbar import navbar
import pandas as pd
import time

st.set_page_config(initial_sidebar_state="collapsed")

def admin_page():

    if "logged_in" not in st.session_state:
        if cookie_controller.get("logged_in") == True:
            st.session_state["user_id"] = cookie_controller.get("user_id")
            st.session_state["username"] = cookie_controller.get("username")
            st.session_state["role"] = cookie_controller.get("role")
            st.session_state.logged_in = True
        else:
            st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_page()
    else:
        navbar()
        with st.sidebar:
            if st.button("Logout", key="logout_button"):                
                
                # Inject custom CSS to collapse the sidebar -- Need to rework on this
                hide_sidebar_css = """
                    <style>
                        [data-testid="stSidebar"] {
                            display: none;
                        }
                    </style>
                """
                st.markdown(hide_sidebar_css, unsafe_allow_html=True)

                st.session_state.logged_in = False
                clear_cookies()
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.write(
                    f"""
                    <meta http-equiv="refresh" content="0; url=/" />
                    """,
                    unsafe_allow_html=True
                )
                # Add st.stop to ensure no further code execution
                st.stop()
                

            # JavaScript injection for styling
            st.markdown(
                """
                <script>
                const logoutButton = document.querySelector('#logout_button');
                if (logoutButton) {
                    logoutButton.style.marginTop = 'auto'; // Push to bottom
                    logoutButton.style.marginBottom = '20px';
                    logoutButton.style.width = '100%';
                    logoutButton.style.position = 'absolute';
                    logoutButton.style.bottom = '0';
                    logoutButton.style.left = '0';
                }
                </script>
                """,
                unsafe_allow_html=True,
            )
        
        userid_g = st.session_state["user_id"]

        if st.session_state.role != 'admin':
            st.header("Update Your Password")
            with st.container(border=True):
                with st.form('Password update form2',clear_on_submit=True):
                    oldpassword = st.text_input("Old Password", type="password")
                    newpassword = st.text_input("New Password", type="password")
                    repassword = st.text_input("Confirm Password", type="password")
                    
                    user = get_users_det(userid_g)
                    submitted = st.form_submit_button("Save Changes")
                    if submitted:
                        role = authenticate_user(user[0][2], oldpassword)
                        if not oldpassword or not newpassword or not repassword:
                            st.error("Please fill out all the fields.")
                        elif not role:
                            st.error("The old password you entered is incorrect.")
                        elif newpassword != repassword:
                            st.error("The new password and the confirmation password do not match.")
                        else:
                            hashed_password = hash_password(newpassword)
                            update_password(userid_g, hashed_password)
                            st.success(f"Password updated successfully!")
                            time.sleep(1) 
        else:

            st.title("Admin Page")
            st.markdown('<div id="add_users"></div>', unsafe_allow_html=True)
            st.header("Add New User")

            # Form to add a new user
            with st.form('Admin From',clear_on_submit=True):
                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                role = st.selectbox("Role", ["user", "admin","volunteer"])  # Allow admin to assign roles
                active = st.selectbox("Active", ["True", "False"], disabled=True)
                
                #add_user_button = st.button("Add User")
                submitted = st.form_submit_button("Add User")

                if submitted:
                    if username and email and password:
                        if check_email_exists(email):
                            st.error("This email is already in use. Please use a different email.")
                        else:
                            hashed_password = hash_password(password)
                            add_user(username, email, hashed_password, role, active)
                            st.success(f"User {username} added successfully!")
                            time.sleep(1)
                    else:
                        st.error("All fields are required.")

            
            #Section to Update User Details
            st.markdown('<div id="user_details"></div>', unsafe_allow_html=True)
            st.header('Update User Details')
            with st.container( border=True):
                #with st.form('Admin From',clear_on_submit=True):

                # Initialize session state variables if they don't exist
                if 'selected_user_id' not in st.session_state:
                    st.session_state.selected_user_id = None
                if 'email_mod' not in st.session_state:
                    st.session_state.email_mod = ''
                if 'role_mod' not in st.session_state:
                    st.session_state.role_mod = 'user'
                if 'active_mod' not in st.session_state:
                    st.session_state.active_mod = 'True'

                users = get_all_users()  # Returns a list of all users as [(user_id, username, email)]
                #st.write(users)
                user_dict = {user[0]: f"{user[1].upper()} ({user[2]}) -- Active:{user[4]}" for user in users}  # user_id: "username (email)"
                # Create a reverse dictionary to map display string back to user_id
                reverse_user_dict = {v: k for k, v in user_dict.items()}
                user_list = list(user_dict.values())
                assigned_to = st.selectbox("User", options=user_list, index=None, key='assigned_to')

                # Extract the user_id from the selected display name
                selected_user_id = reverse_user_dict.get(assigned_to)
                
                # If a user is selected, display their details in editable fields
                if selected_user_id is not None:
                    user = get_users_det(str(selected_user_id))
                    if user:
                        st.session_state.selected_user_id = selected_user_id
                        st.session_state.email_mod = user[0][2]
                        st.session_state.role_mod = user[0][3]
                        st.session_state.active_mod = str(user[0][4])
                    if st.session_state.selected_user_id:
                        st.text_input("User Name", value=user[0][1], disabled=True)
                        st.session_state.email_mod = st.text_input("Email", value=st.session_state.email_mod)
                        st.session_state.role_mod = st.selectbox("Role", ["user", "admin","volunteer"], index=["user", "admin","volunteer"].index(st.session_state.role_mod))
                        st.session_state.active_mod = st.selectbox("Active", ["True", "False"], index=["True", "False"].index(st.session_state.active_mod))
                    col1, col2 = st.columns([5, 1]) 
                    with col1:
                        submitted = st.button("Save Changes") 
                    with col2:
                        clear_form = st.button("Clear Form", on_click=reset_selectbox)

                    if submitted:
                        update_user(user_id=selected_user_id, email=st.session_state.email_mod, role=st.session_state.role_mod, active=st.session_state.active_mod)
                        alert = st.success("User details updated successfully!")
                        time.sleep(2) # Wait for 3 seconds
                        st.experimental_rerun()
                        submitted.on_click=reset_selectbox
                
            
            #Section where you can update your own password
            st.markdown('<div id="password_change"></div>', unsafe_allow_html=True)
            st.header("Update Your Password")
            with st.container(border=True):
                with st.form('Password update form2',clear_on_submit=True):
                    oldpassword = st.text_input("Old Password", type="password")
                    newpassword = st.text_input("New Password", type="password")
                    repassword = st.text_input("Confirm Password", type="password")
                    
                    user = get_users_det(userid_g)
                    submitted = st.form_submit_button("Save Changes")
                    if submitted:
                        role = authenticate_user(user[0][2], oldpassword)
                        if not oldpassword or not newpassword or not repassword:
                            st.error("Please fill out all the fields.")
                        elif role:
                            st.error("The old password you entered is incorrect.")
                        elif newpassword != repassword:
                            st.error("The new password and the confirmation password do not match.")
                        else:
                            hashed_password = hash_password(newpassword)
                            update_password(userid_g, hashed_password)
                            st.success(f"Password updated successfully!")
                            time.sleep(1)  

            st.header("User List")
            users = get_all_users()
            with st.container(height=250, border=True):
                col1, col2, col3 = st.columns([1, 5, 1])
                with col2:
                    column_names = ["ID", "Username", "Email", "Role", "Active Status"]
                    df_users = pd.DataFrame(users, columns=column_names)
                    st.write(df_users)  

                st.download_button(
                    label="Download CSV",
                    data=df_users.to_csv().encode("utf-8"),
                    file_name="User_Data.csv",
                    mime="text/csv",
                    icon=":material/download:",
                )

            #Button to navigate to add user section
            st.markdown("""
                <a href="#add_users">
                    <button style="position: fixed; right: 10px; bottom: 460px; padding: 10px; width: 50px; height: 50px; background-color: #0b5394; color: white; border: none; border-radius: 50%; font-size: 20px; cursor: pointer;">
                    ➕
                    </button>
                </a>
            """, unsafe_allow_html=True)

            #Button to navigate to add user section
            st.markdown("""
                <a href="#user_details">
                    <button style="position: fixed; right: 10px; bottom: 400px; padding: 10px; width: 50px; height: 50px; background-color: #0b5394; color: white; border: none; border-radius: 50%; font-size: 22px; cursor: pointer;">
                        🧑‍💼
                    </button>
                </a>
            """, unsafe_allow_html=True)

            #Button to navigate to add user section
            st.markdown("""
                <a href="#password_change">
                    <button style="position: fixed; right: 10px; bottom: 340px; padding: 10px; width: 50px; height: 50px; background-color: #0b5394; color: white; border: none; border-radius: 50%; font-size: 20px; cursor: pointer;">
                        🔏
                    </button>
                </a>
            """, unsafe_allow_html=True)

def reset_selectbox():
    st.session_state.assigned_to = None

if __name__ == "__main__":
    admin_page()
