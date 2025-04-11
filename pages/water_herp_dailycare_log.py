import streamlit as st
from Login import login_page, cookie_controller, clear_cookies
from utils.navbar import navbar
from datetime import datetime
from utils.enrichment_utils import add_watershed_care_log, add_herp_care_log
import time

st.set_page_config(initial_sidebar_state="collapsed")

def watershed_herpetarium_fed_log():

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

            st.title("Watershed Feeding Log")

            if 'water_form_submitted' in st.session_state and st.session_state.water_form_submitted:
                st.session_state["location"] = []
                st.session_state["pond1_dailycare"] = []
                # st.session_state["pond2_dailycare"] = []
                # st.session_state["pond3_dailycare"] = []
                # st.session_state["tank1_dailycare"] = []
                # st.session_state["tank2_dailycare"] = []
                # st.session_state["tank3_dailycare"] = []
                # st.session_state["tank4_dailycare"] = []
                # st.session_state["tank5_dailycare"] = []
                # st.session_state["tank6_dailycare"] = []
                st.session_state["other_care_input"] = ""
                st.session_state["watershed_notes_key"] = ""

                st.session_state["log_time"] = datetime.now().time()
                
                st.session_state.water_form_submitted = False
                st.rerun() 

            with st.container(border=True):
                #location = st.selectbox("Pond/Tank Location", ["Pond 1", "Pond 2", "Pond 3", "Tank 1", "Tank 2", "Tank 3", "Tank 4", "Tank 5", "Tank 6"], key="location_key", index=None)

                input_dict = {}

                st.subheader("Daily Care Performed")

                location = st.multiselect(
                    "Pond/Tank Location",
                    ["Pond 1", "Pond 2", "Pond 3", "Tank 1", "Tank 2", "Tank 3", "Tank 4", "Tank 5", "Tank 6"],
                    help="You can choose multiple items.",
                    key="location"
                )
                
                pond1_dailycare = st.multiselect(
                    "Daily Care Type",
                    ["Daily check", "Glass cleaning", "Waste removal", "Water change", "Gravel clean/change", "Other"],
                    help="You can choose multiple items.",
                    key="pond1_dailycare"
                )

                if pond1_dailycare: input_dict['Pond 1'] = pond1_dailycare

                # pond2_dailycare = st.multiselect(
                #     "Pond 2",
                #     ["Daily check", "Glass cleaning", "Waste removal", "Water change", "Gravel clean/change", "Other"],
                #     help="You can choose multiple items.",
                #     key="pond2_dailycare"
                # )

                # if pond2_dailycare: input_dict['Pond 2'] = pond2_dailycare

                # pond3_dailycare = st.multiselect(
                #     "Pond 3",
                #     ["Daily check", "Glass cleaning", "Waste removal", "Water change", "Gravel clean/change", "Other"],
                #     help="You can choose multiple items.",
                #     key="pond3_dailycare"
                # )

                # if pond3_dailycare: input_dict['Pond 3'] = pond3_dailycare

                # tank1_dailycare = st.multiselect(
                #     "Tank 1",
                #     ["Daily check", "Glass cleaning", "Waste removal", "Water change", "Gravel clean/change", "Other"],
                #     help="You can choose multiple items.",
                #     key="tank1_dailycare"
                # )

                # if tank1_dailycare: input_dict['Tank 1'] = tank1_dailycare

                # tank2_dailycare = st.multiselect(
                #     "Tank 2",
                #     ["Daily check", "Glass cleaning", "Waste removal", "Water change", "Gravel clean/change", "Other"],
                #     help="You can choose multiple items.",
                #     key="tank2_dailycare"
                # )

                # if tank2_dailycare: input_dict['Tank 2'] = tank2_dailycare

                # tank3_dailycare = st.multiselect(
                #     "Tank 3",
                #     ["Daily check", "Glass cleaning", "Waste removal", "Water change", "Gravel clean/change", "Other"],
                #     help="You can choose multiple items.",
                #     key="tank3_dailycare"
                # )

                # if tank3_dailycare: input_dict['Tank 3'] = tank3_dailycare

                # tank4_dailycare = st.multiselect(
                #     "Tank 4",
                #     ["Daily check", "Glass cleaning", "Waste removal", "Water change", "Gravel clean/change", "Other"],
                #     help="You can choose multiple items.",
                #     key="tank4_dailycare"
                # )

                # if tank4_dailycare: input_dict['Tank 4'] = tank4_dailycare

                # tank5_dailycare = st.multiselect(
                #     "Tank 5",
                #     ["Daily check", "Glass cleaning", "Waste removal", "Water change", "Gravel clean/change", "Other"],
                #     help="You can choose multiple items.",
                #     key="tank5_dailycare"
                # )

                # if tank5_dailycare: input_dict['Tank 5'] = tank5_dailycare

                # tank6_dailycare = st.multiselect(
                #     "Tank 6",
                #     ["Daily check", "Glass cleaning", "Waste removal", "Water change", "Gravel clean/change", "Other"],
                #     help="You can choose multiple items.",
                #     key="tank6_dailycare"
                # )

                # if tank6_dailycare: input_dict['Tank 6'] = tank6_dailycare

                # #if "Other" in watershed_dailycare:
                if "Other" in pond1_dailycare: # or "Other" in pond2_dailycare or "Other" in pond3_dailycare or "Other" in tank1_dailycare or "Other" in tank2_dailycare or "Other" in tank3_dailycare or "Other" in tank4_dailycare or "Other" in tank5_dailycare or "Other" in tank6_dailycare:    
                    other_care = st.text_input('Please specify the "Other" care performed:', key="other_care_input")

                watershed_notes = st.text_area("Notes", key="watershed_notes_key")

                st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
                log_time = st.time_input("Log Time", key="log_time", step=300)
                st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

                formatted_log_time = log_time.strftime("%H:%M:%S")

                submitted = st.button("Submit Feeding Log")

                if submitted:
                    if not location:
                        st.warning("Please select the Pond/Tank Location")
                        return
                    
                    
                    if not pond1_dailycare: # and not pond2_dailycare and not pond3_dailycare and not tank1_dailycare and not tank2_dailycare and not tank3_dailycare and not tank4_dailycare and not tank5_dailycare and not tank6_dailycare:
                        st.warning("Please fill the Pond/Tank Location and the daily care performed")
                        return
                
                    
                    if "Other" in pond1_dailycare: # or "Other" in pond2_dailycare or "Other" in pond3_dailycare or "Other" in tank1_dailycare or "Other" in tank2_dailycare or "Other" in tank3_dailycare or "Other" in tank4_dailycare or "Other" in tank5_dailycare or "Other" in tank6_dailycare:
                        if not other_care:
                            st.warning('Please specify the "Other" care performed')
                            return
                        
                    if not watershed_notes:
                        watershed_notes = "None"

                    #for location, selected_items in input_dict.items():
                    for loc in location:                       
                        for item in pond1_dailycare:
                            if item == "Other":
                                watershed_care_name = other_care
                            else:
                                watershed_care_name = "None"

                            add_watershed_care_log(user_id, formatted_time, loc, item, watershed_care_name, watershed_notes, formatted_log_time)
                        
                    st.success("Daily Care log submitted successfully!")
                    time.sleep(1)
                    st.session_state.water_form_submitted = True
                    st.rerun()

        elif filter_option == "Herpetarium":

            st.title("Herpetarium Feeding Log")
            
            if 'herp_form_submitted' in st.session_state and st.session_state.herp_form_submitted:
                st.session_state["animal_key"] = []
                st.session_state["herpetarium_food1_key"] = []
                # st.session_state["herpetarium_food2_key"] = []
                # st.session_state["herpetarium_food3_key"] = []
                # st.session_state["herpetarium_food4_key"] = []
                st.session_state["herp_other_care_input"] = ""
                st.session_state["herp_indv_no_key"] = ""
                st.session_state["herp_notes_key"] = ""

                st.session_state["log_time"] = datetime.now().time()
                
                st.session_state.herp_form_submitted = False
                st.rerun() 

            with st.container(border=True):
                #animal = st.selectbox("Animal Type", ["Snakes", "Frogs/Salamanders/Lizards", "Turtles (inside)", "Turtles (outside)"], key="animal_key", index=None)

                #input_dict = {}

                st.subheader("Daily Care Performed")

                animal = st.multiselect(
                    "Animal Type",
                    ["Snakes", "Frogs/Salamanders/Lizards", "Turtles (inside)", "Turtles (outside)"],
                    help="You can choose multiple items.",
                    key="animal_key"
                )
                
                options = ["Daily check", "Water change", "Waste removal", "Bedding change", "Pond cleaning", "Weed-eating", "Enrichment", "Other"]
                
                herpetarium_food1 = st.multiselect(
                    "Daily Care Type",
                    options,
                    help="You can choose multiple items.",
                    key="herpetarium_food1_key"
                )

                # if herpetarium_food1: input_dict['Snakes'] = herpetarium_food1

                # herpetarium_food2 = st.multiselect(
                #     "Frogs/Salamanders/Lizards",
                #     options,
                #     help="You can choose multiple items.",
                #     key="herpetarium_food2_key"
                # )

                # if herpetarium_food2: input_dict['Frogs/Salamanders/Lizards'] = herpetarium_food2

                # herpetarium_food3 = st.multiselect(
                #     "Turtles (inside)",
                #     options,
                #     help="You can choose multiple items.",
                #     key="herpetarium_food3_key"
                # )

                # if herpetarium_food3: input_dict['Turtles (inside)'] = herpetarium_food3

                # herpetarium_food4 = st.multiselect(
                #     "Turtles (outside)",
                #     options,
                #     help="You can choose multiple items.",
                #     key="herpetarium_food4_key"
                # )

                # if herpetarium_food4: input_dict['Turtles (outside)'] = herpetarium_food4

                if "Other" in herpetarium_food1: # or "Other" in herpetarium_food2 or "Other" in herpetarium_food3 or "Other" in herpetarium_food4:
                    herp_other_care = st.text_input('Please specify the "Other" care performed:', key="herp_other_care_input")

                enclosures_not_done = st.text_input('Any enclosures not done?', key="herp_indv_no_key")

                herp_notes = st.text_area("Notes", key="herp_notes_key")

                st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
                log_time = st.time_input("Log Time", key="log_time", step=300)
                st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

                formatted_log_time = log_time.strftime("%H:%M:%S")

                submitted = st.button("Submit Feeding Log")

                if submitted:
                    if not animal: # and not herpetarium_food2 and not herpetarium_food3 and not herpetarium_food4:
                        st.warning("Please select the Animal Type")
                        return                    
                    
                    if not herpetarium_food1: # and not herpetarium_food2 and not herpetarium_food3 and not herpetarium_food4:
                        st.warning("Please select the Daily Care Type")
                        return
                    
                    if "Other" in herpetarium_food1: # or "Other" in herpetarium_food2 or "Other" in herpetarium_food3 or "Other" in herpetarium_food4:
                        if not herp_other_care:
                            st.warning('Please specify the "Other" care performed')
                            return
                        
                    if not enclosures_not_done:
                        enclosures_not_done = "None"
                    
                    if not herp_notes:
                        herp_notes = "None"

                    # for animal, selected_items in input_dict.items():
                    for anml in animal:  
                        for item in herpetarium_food1:
                            if item == "Other":
                                herp_care_name = herp_other_care
                            else:
                                herp_care_name = "None"

                            add_herp_care_log(user_id, formatted_time, anml, item, herp_care_name, enclosures_not_done, herp_notes, formatted_log_time)
                        
                    st.success("Daily Care log submitted successfully!")
                    time.sleep(1)
                    st.session_state.herp_form_submitted = True
                    st.rerun()
                        
                        
if __name__ == "__main__":
    watershed_herpetarium_fed_log()