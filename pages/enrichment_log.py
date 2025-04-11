import streamlit as st
from Login import login_page, cookie_controller, clear_cookies
from utils.navbar import navbar
from streamlit_free_text_select import st_free_text_select
import datetime
import uuid
from utils.enrichment_utils import add_enrichment_log
import time

st.set_page_config(initial_sidebar_state="collapsed")

def enrichment_log():

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
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")


        # Check if the form was submitted and reset session state if necessary
        if 'form_submitted' in st.session_state and st.session_state.form_submitted:
            # Clear the session state values for the form inputs
            st.session_state["individual_name"] = ""
            st.session_state["details"] = ""
            st.session_state["time_in"] = datetime.datetime.now().time()
            st.session_state["time_out"] = datetime.datetime.now().time()
            st.session_state["enrichment_response"] = None

            st.session_state.animal_key = get_unique_key("animal_select")
            st.session_state.observation_key = get_unique_key("observation_select")
            st.session_state.enrichment_key = get_unique_key("enrichment_select")

            st.session_state["log_time"] = datetime.datetime.now().time()
           
            st.session_state.form_submitted = False
            st.rerun()  # Refresh the page to clear the form

        if st.button("Back", use_container_width=False):
            st.switch_page("pages/ethogram_form.py")
        
        st.title("Enrichment Log")

        with st.container(border=True):
            
            if "animal_key" not in st.session_state:
                st.session_state.animal_key = "animal_select"
            if "observation_key" not in st.session_state:    
                st.session_state.observation_key = "observation_select"
            if "enrichment_key" not in st.session_state:    
                st.session_state.enrichment_key = "enrichment_select"

            animal_group = st_free_text_select(
                label="Animal Type",
                options=["Bobcat", "Deer", "Red Fox", "River Otter", "Wolf"],
                index=None,
                format_func=lambda x: x.capitalize(),
                placeholder="Select or enter an animal",
                disabled=False,
                delay=300,
                key=st.session_state.animal_key, 
                label_visibility="visible",
            )   
                
            #st.subheader("Individual Information")
            individual_name = st.text_input("Which Individuals were in the habitat? (If 'All' then leave it empty)", key="individual_name")

            if individual_name == "": individual_name = "All"

            enrichment_type = st_free_text_select(label="Select Enrichment Type", options=["Toys", "Training", "Food", "Interaction (Play)", "Bones"],
                index=None,
                format_func=lambda x: x.capitalize(),
                placeholder="Select or enter the enrichment type",
                disabled=False,
                delay=300,
                label_visibility="visible",
                key=st.session_state.enrichment_key,
            ) 

            #st.subheader("Details and Response")
            details = st.text_area("Enter Details of the Enrichment and Findings", key="details")
            
            #time_in = st.time_input("Set Time In", datetime.time(8, 45), key="time_in")
            time_in = st.time_input("Set Time In", key="time_in", step=300)
            time_out = st.time_input("Set Time Out", key="time_out", step=300) #datetime.datetime.now().time(),

            time_administered_dt = datetime.datetime.combine(datetime.date.today(), time_in)
            response_time_dt = datetime.datetime.combine(datetime.date.today(), time_out)

            # Check if response_time is greater than time_administered
            if response_time_dt < time_administered_dt:
                st.error("❌ 'Time Out' must be **greater** than 'Time In'. Please enter a valid time.")
            
            #response = st.text_area("Enter Response", key="response")

            formatted_time_in = time_in.strftime("%H:%M:%S")
            formatted_time_out = time_out.strftime("%H:%M:%S")

            enrichment_response = st.selectbox("How did the animal respond to the Enrichment with 1 being 'No Response' and 5 being 'Fully Engaged'", ["1","2","3","4","5"], key="enrichment_response", index=None)

            observation_type = st_free_text_select(label="Select Observation Type", options=["DVE","DPE"],
                index=None,
                format_func=lambda x: x.upper(),
                placeholder="Select or enter the observation",
                disabled=False,
                delay=300,
                label_visibility="visible",
                key=st.session_state.observation_key,
            )

            st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
            log_time = st.time_input("Log Time", key="log_time", step=300)
            st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

            formatted_log_time = log_time.strftime("%H:%M:%S")

            if st.button("Submit Enrichment Log"):

                if not animal_group:
                    st.error("Please fill out Animal Type before submitting the enrichment log.")
                    return
                if not enrichment_type:
                    st.error("Please select or enter the Enrichment Type before submitting the enrichment log.")
                    return
                if not details:
                    st.error("Please fill out Enrichment Details before submitting the enrichment log.")
                    return
                if not enrichment_response:
                    st.error("Please select the Enrichment Response before submitting the enrichment log.")
                    return
                if not observation_type:
                    st.error("Please select or enter the Observation Type before submitting the enrichment log.")
                    return
                
                add_enrichment_log(
                    user_id, 
                    formatted_time, 
                    animal_group, 
                    enrichment_response, 
                    individual_name, 
                    enrichment_type, 
                    details, 
                    formatted_time_in, 
                    formatted_time_out,
                    observation_type,
                    formatted_log_time
                )
                
                st.success("Enrichment log submitted successfully!")
                time.sleep(1)
                st.session_state.form_submitted = True
                st.rerun()
                

def get_unique_key(base_key):
        return f"{base_key}_{uuid.uuid4().hex[:6]}"

if __name__ == "__main__":
    enrichment_log()
