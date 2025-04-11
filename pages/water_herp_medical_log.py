import streamlit as st
from Login import login_page, cookie_controller, clear_cookies
from utils.navbar import navbar
from datetime import datetime
from utils.medical_utils import add_watershed_med_log, add_herp_med_log
import time

st.set_page_config(initial_sidebar_state="collapsed")

def watershed_herpetarium_med_log():

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
                st.session_state.logged_in = False
                clear_cookies()
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.write(
                    """
                    <meta http-equiv="refresh" content="0; url=/" />
                    """,
                    unsafe_allow_html=True
                )
                st.stop()

        user_id = st.session_state["user_id"]
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        if "water_herp_log" not in st.session_state:
            st.session_state["water_herp_log"] = cookie_controller.get("water_herp_log")
    
        filter_option = st.session_state["water_herp_log"]

        if st.button("Back", use_container_width=False):
                st.switch_page("pages/ethogram_form.py")

        if filter_option == "Watershed":
            st.title("Watershed Medical Log")
            label = "Individual Name"
        elif filter_option == "Herpetarium":
            st.title("Herpetarium Medical Log")
            label = "Animal Name"

        if 'form_submitted' in st.session_state and st.session_state.form_submitted:
            st.session_state["individual_key"] = ""
            st.session_state["observation_key"] = ""
            st.session_state["intervention_key"] = ""
            st.session_state["notes_key"] = ""

            st.session_state["log_time"] = datetime.now().time()
            
            st.session_state.form_submitted = False
            st.rerun() 

        with st.container(border=True):
            
            individual = st.text_input(f"{label}*", key="individual_key")

            observation = st.text_input('Observation*', key="observation_key")
            
            intervention = st.text_input('Intervention*', key="intervention_key")

            notes = st.text_area("Notes", key="notes_key")

            st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
            log_time = st.time_input("Log Time", key="log_time", step=300)
            st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

            formatted_log_time = log_time.strftime("%H:%M:%S")

            submitted = st.button("Submit Medical Log")

            if submitted:
                if not individual:
                    st.warning(f"Please select the {label}")
                    return
                
                if not observation:
                    st.warning("Please enter the observation")
                    return
                
                if not intervention:
                    st.warning("Please enter the applied intervention")
                    return
                
                if filter_option == "Watershed":
                    add_watershed_med_log(user_id, formatted_time, individual, observation, intervention, notes, formatted_log_time)
                elif filter_option == "Herpetarium":
                    add_herp_med_log(user_id, formatted_time, individual, observation, intervention, notes, formatted_log_time)

                st.success("Medical log submitted successfully!")
                time.sleep(1)
                st.session_state.form_submitted = True
                st.rerun()


if __name__ == "__main__":
    watershed_herpetarium_med_log()