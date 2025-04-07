import streamlit as st
import pandas as pd
from datetime import date
from utils.calendar_utils import get_users, add_reminder, get_reminders, update_reminder, delete_reminder
from utils.calendar_utils import get_all_reminders, search_reminders, get_assigned_reminders, search_assigned_reminders
from Login import login_page, cookie_controller, clear_cookies
from utils.navbar import navbar
import time
from streamlit_calendar import calendar

st.set_page_config(initial_sidebar_state="collapsed")

def calendar_page():
    
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
        if "user_id" in st.session_state:
            user_id = st.session_state["user_id"]
            username = st.session_state["username"]

        navbar()
        with st.sidebar:
            if st.button("Logout", key="logout_button"):                
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
                st.stop()

        st.title("Calendar & Reminders")

        # Ensure user is logged in
        if "user_id" not in st.session_state:
            st.warning("Please log in to access the calendar.")
            return

        # Initialize editing state
        if "editing_reminder" not in st.session_state:
            st.session_state.editing_reminder = None

        # Fetch all users (for assigning reminders)
        users = get_users()  # Returns a list of all users as [(user_id, username, email)]
        user_dict = {user[0]: f"{user[1].upper()} ({user[2]})" for user in users}  # user_id: "username (email)"
        user_dict_name = {user[0]: user[1].upper() for user in users}  # user_id: "username "
        user_list = list(user_dict.values())

        #--------------------Calendar Section-------------------------
        # Fetch reminders for the logged-in user
        reminders_t = get_all_reminders('')
        
        # Define a priority-to-color mapping
        priority_colors = {"High": "red", "Medium": "orange", "Low": "green"}

        # Create events from reminders
        events = [
            {
                "title": f"{reminder[4].capitalize()} : {reminder[2]}",  # title
                "color": priority_colors.get(reminder[5], "gray"),  # priority -> color
                "start": reminder[1].strftime("%Y-%m-%d")  # date as string
            }
            for reminder in reminders_t
        ]
        st.markdown('<div id="calendar"></div>', unsafe_allow_html=True)
        # Display calendar with reminders
        st.subheader("Calendar") # Pass the reminders grouped by date
        with st.container(border=True):
            calendar(events=events, custom_css="""
                .fc-event-past {
                    opacity: 0.8;
                }
                .fc-event-time {
                    font-style: italic;
                }
                .fc-event-title {
                    font-weight: 700;
                }
                .fc-toolbar-title {
                    font-size: 1.3rem !important; /* Force the font size to apply */
                }
                .fc-event-title {
                    font-size: 0.6rem !important; /* Force the font size to apply */
                }
            """)

        #---------------------Search Reminder Section--------------------
        st.markdown('<div id="search_reminder"></div>', unsafe_allow_html=True)    
        st.subheader("Search Reminder")
        search_query = st.text_input("Search reminder by title or description:")
        

        # Display reminders
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Your Reminders")
        with col2:
            filter_option = st.radio("", ("Assigned BY You", "Assigned TO You"), horizontal=True)

        # Display notes based on search query
        if filter_option == "Assigned BY You":
            reminders = search_reminders(search_query, user_id) if search_query else get_reminders(user_id)
        else:
            reminders = search_assigned_reminders(search_query, user_id) if search_query else get_assigned_reminders(user_id)
        
        st.markdown("""
            <p style="color: grey; font-size: 13px; margin-top: 0; margin-bottom: 0;">
                Users must go to "Add a Reminder" section after clicking the Edit button
            </p>
        """, unsafe_allow_html=True)
        with st.container(height=300, border=True):
            if not reminders:
                st.info("No reminders set.")
            else:
                for i, reminder in enumerate(reminders):
                    with st.expander(f"{reminder[1]}&nbsp;&nbsp;&nbsp; - &nbsp;&nbsp;&nbsp;{user_dict_name.get(reminder[4], 'Unknown')} : {reminder[2]} (Priority: {reminder[5]})"):  # Indexes based on query order
                        st.write(f"Date: {reminder[1]}")
                        st.write(f"Description: {reminder[3]}")
                        if filter_option == "Assigned BY You":
                            st.write(f"Assigned To: {user_dict.get(reminder[4], 'Unknown')}")
                        else:
                            st.write(f"Assigned By: {user_dict.get(reminder[6], 'Unknown')}")
                        
                        # Edit and delete buttons
                        if filter_option == "Assigned BY You":
                            col1, col2 = st.columns([5, 1]) 
                            with col1:
                                if st.button("Edit ", key=f"edit_{i}"):
                                    st.session_state.editing_reminder = {
                                        "id": reminder[0],
                                        "date": reminder[1],
                                        "title": reminder[2],
                                        "description": reminder[3],
                                        "assigned_to": reminder[4],
                                        "priority": reminder[5]
                                    }
                                    st.rerun()
                            with col2:
                                if st.button("Delete", key=f"delete_{i}"):
                                    delete_reminder(reminder[0])
                                    st.success("Reminder deleted successfully!")
                                    time.sleep(1)
                                    st.rerun()
        

        #--------------------Add a Reminder Section-------------------------
        st.markdown('<div id="add_new_reminder"></div>', unsafe_allow_html=True)

        # Add/Update Reminder Section
        st.header("Add a Reminder")
        reminder = st.session_state.editing_reminder

        # Default values for the form
        default_date = date.today()
        default_title = ""
        default_description = ""
        default_priority = "Medium"

        # Reset form state when "Clear Form" is clicked
        if "clear_form" not in st.session_state:
            st.session_state.clear_form = False

        if st.session_state.clear_form:
            reminder = None  # Reset editing reminder
            st.session_state.clear_form = False  # Reset the state to avoid looping

        # Form for adding or updating a reminder
        with st.form('Notes Form', clear_on_submit=(reminder is None)):
            reminder_date = st.date_input(
                "Select Date", 
                value=reminder["date"] if reminder else default_date
            )
            reminder_title = st.text_input(
                "Reminder Title", 
                value=reminder["title"] if reminder else default_title
            )
            reminder_description = st.text_area(
                "Description", 
                value=reminder["description"] if reminder else default_description
            )

            # Ensure the assigned_to index is valid
            if reminder and user_dict.get(reminder["assigned_to"], "Unknown") in user_list:
                assigned_to_index = user_list.index(user_dict.get(reminder["assigned_to"], "Unknown"))
            else:
                assigned_to_index = 0

            assigned_to = st.selectbox(
                "Assign to User", 
                options=user_list,     
                index=assigned_to_index
            )

            priority = st.radio(
                "Priority Level", 
                options=["High", "Medium", "Low"], 
                index=["High", "Medium", "Low"].index(reminder["priority"]) if reminder else ["High", "Medium", "Low"].index(default_priority)
            )

            col1, col2 = st.columns([5, 1]) 
            with col1:
                submitted = st.form_submit_button("Save Reminder")
            with col2:
                clear_form = st.form_submit_button("Clear Form")

            if clear_form:
                st.session_state.clear_form = True  # Set state to clear the form
                st.rerun()

            if submitted:
                if reminder_title.strip():
                    assigned_to_user_id = user_id if assigned_to == "Self" else [k for k, v in user_dict.items() if v == assigned_to][0]
                    if reminder:  # Update existing reminder
                        update_reminder(
                            reminder_id=reminder["id"],
                            date=reminder_date,
                            title=reminder_title,
                            description=reminder_description,
                            assigned_to=assigned_to_user_id,
                            priority=priority
                        )
                        st.success("Reminder updated successfully!")
                        time.sleep(1)
                        st.session_state.editing_reminder = None
                    else:  # Add new reminder
                        add_reminder(
                            user_id=user_id,
                            date=reminder_date,
                            title=reminder_title,
                            description=reminder_description,
                            assigned_to=assigned_to_user_id,
                            priority=priority
                        )
                        st.success("Reminder added successfully!")
                        time.sleep(1)
                    st.rerun()
                else:
                    st.error("Title cannot be empty.")


        #Button to navigate to Search reminder section
        st.markdown("""
            <a href="#calendar">
                <button style="position: fixed; right: 10px; bottom: 460px; padding: 10px; width: 50px; height: 50px; background-color: #0b5394; color: white; border: none; border-radius: 50%; font-size: 20px; cursor: pointer;">
                    📆
                </button>
            </a>
        """, unsafe_allow_html=True)

        #Button to navigate to Search reminder section
        st.markdown("""
            <a href="#search_reminder">
                <button style="position: fixed; right: 10px; bottom: 400px; padding: 10px; width: 50px; height: 50px; background-color: #0b5394; color: white; border: none; border-radius: 50%; font-size: 20px; cursor: pointer;">
                    🔍
                </button>
            </a>
        """, unsafe_allow_html=True)
        
        #Button to navigate to Add new reminder section
        st.markdown("""
            <a href="#add_new_reminder">
                <button style="position: fixed; right: 10px; bottom: 340px; padding: 10px; width: 50px; height: 50px; background-color: #0b5394; color: white; border: none; border-radius: 50%; font-size: 20px; cursor: pointer;">
                    ➕
                </button>
            </a>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    calendar_page()
