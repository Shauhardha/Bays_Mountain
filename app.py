import streamlit as st
from utils.notes_utils import get_notes_app
from utils.calendar_utils import get_all_reminders
from Login import login_page, cookie_controller, clear_cookies
from utils.navbar import navbar
#from utils.cookies_manage import cookie_controller, clear_cookies

# Set page configuration early
#st.set_page_config(initial_sidebar_state="collapsed")

def main():
    # if "logged_in" not in st.session_state: 
    #     st.session_state.logged_in = False  # Default to not logged in

    if "logged_in" not in st.session_state:
        if cookie_controller.get("logged_in") == True: 
            st.session_state["user_id"] = cookie_controller.get("user_id")
            st.session_state["username"] = cookie_controller.get("username")
            st.session_state["role"] = cookie_controller.get("role")
            st.session_state.logged_in = True
        else:
            st.session_state.logged_in = False

    # Prevent resetting session state on refresh
    if not st.session_state.get("logged_in", False):
        login_page()
        return
    
    query_params = st.query_params                    # experimental_get_query_params (Removed this because its outdated)
    page = query_params.get("page", ["main"])[0]

    dashboard()


def dashboard():
    """
    Main dashboard showing notes.
    """
    navbar()

    user_id = st.session_state["user_id"]

    
    st.title("BaysTrack Dashboard")
    # Wrap the notes content inside the white-bordered container
    col1, col2 = st.columns([1, 1])
    with col1:
        fil1, fil2 = st.columns([1, 0.7])
        with fil1: 
            st.header("Notes")
        with st.container(height=300, border=True):
            notes = get_notes_app(str(user_id))
            if notes:
                for note in notes:
                    st.markdown(f"<p style='font-size:12.5px;'>{note[2]} - {note[3]} {note[9]}</p>", unsafe_allow_html=True)
                    st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
            else:
                st.write("No notes available.")

    with col2:  
        fil1, fil2 = st.columns([1, 0.7])
        with fil1:
            st.header("Reminders")    
        with fil2:
            filter_option = st.radio("Reminders", options=("All", "Self"), horizontal=True, label_visibility="collapsed")
        with st.container(height=300, border=True):
            if filter_option == "All":
                var = ''
                reminders = get_all_reminders(var)
            else:
                reminders = get_all_reminders(user_id)
            if reminders:
                for reminder in reminders:
                    st.markdown(
                        f"<p style='font-size:12.5px;'>{reminder[1]}&nbsp;&nbsp;&nbsp; - &nbsp;&nbsp;&nbsp;"
                        f"{reminder[4].capitalize()} : {reminder[2]} (Priority: {reminder[5]})</p>",
                        unsafe_allow_html=True,
                    )
                    st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
            else:
                st.write("No reminders available.")

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
            # st.rerun()
            

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

if __name__ == "__main__":
    main()
