import streamlit as st
from Login import login_page, cookie_controller, clear_cookies
from utils.navbar import navbar
from datetime import datetime
import time
from utils.feeding_utils import add_watershed_feeding_log, add_herp_feeding_log

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
                st.session_state["location_key"] = None
                st.session_state["watershed_food_key"] = []
                st.session_state["other_food_input"] = ""
                st.session_state["amount_fed"] = None
                st.session_state["indv_no_eat_key"] = ""
                st.session_state["watershed_notes_key"] = ""
                
                st.session_state.water_form_submitted = False
                st.rerun() 

            with st.container(border=True):
                location = st.selectbox("Pond/Tank Location", ["Pond 1", "Pond 2", "Pond 3", "Tank 1", "Tank 2", "Tank 3", "Tank 4", "Tank 5", "Tank 6"], key="location_key", index=None)

                watershed_food = st.multiselect(
                    "Food Items Fed",
                    ["Silverside", "Shrimp", "Krill cubes", "Bloodworm cubes", "Pellets", "Other"],
                    help="You can choose multiple items.",
                    key="watershed_food_key"
                )

                if "Other" in watershed_food:
                    other_food = st.text_input('Please specify the "Other" food item(s):', key="other_food_input")

                amount_fed = st.number_input("Total Food Amount", value=None, step=0.5, format="%.2f", placeholder="Enter the amount fed...", key="amount_fed")

                indv_no_eat = st.text_input('Which individuals did not eat?', key="indv_no_eat_key")

                watershed_notes = st.text_area("Notes", key="watershed_notes_key")

                submitted = st.button("Submit Feeding Log")

                if submitted:
                    if not location:
                        st.warning("Please select Pond/Tank Location")
                        return
                    
                    if not watershed_food:
                        st.warning("Please select the food items fed")
                        return
                    
                    if "Other" in watershed_food:
                        if not other_food:
                            st.warning('Please specify the "Other" food item(s)')
                            return
                        
                    if not amount_fed:
                        amount_fed = 0

                    if not indv_no_eat:
                        indv_no_eat = "None"

                    if not watershed_notes:
                        watershed_notes = "None"
                        
                    for item in watershed_food:
                        if item == "Other":
                            other_food_name = other_food
                        else:
                            other_food_name = "None"
                        
                        add_watershed_feeding_log(user_id, formatted_time, location, item, other_food_name, amount_fed, indv_no_eat, watershed_notes)

                    st.success("Feeding log submitted successfully!")
                    time.sleep(1)
                    st.session_state.water_form_submitted = True
                    st.rerun()

        elif filter_option == "Herpetarium":

            st.title("Herpetarium Feeding Log")
            
            if 'herp_form_submitted' in st.session_state and st.session_state.herp_form_submitted:
                st.session_state["animal_key"] = None
                st.session_state["herpetarium_food_key"] = []
                st.session_state["herp_other_food_input"] = ""
                st.session_state["herp_amount_fed"] = None
                st.session_state["herp_indv_no_eat_key"] = ""
                st.session_state["herp_notes_key"] = ""
                
                st.session_state.herp_form_submitted = False
                st.rerun() 

            with st.container(border=True):
                animal = st.selectbox("Animal Type", ["Snakes", "Frogs/Salamanders/Lizards", "Turtles (inside)", "Turtles (outside)"], key="animal_key", index=None)

                herpetarium_food = st.multiselect(
                    "Food Items Fed",
                    ["Mice", "Worms", "Crickets", "Turtle food (pre-mix)", "Fresh fruit", "Other"],
                    help="You can choose multiple items.",
                    key="herpetarium_food_key"
                )

                if "Other" in herpetarium_food:
                    herp_other_food = st.text_input('Please specify the "Other" food item(s):', key="herp_other_food_input")

                herp_amount_fed = st.number_input("Total Food Amount", value=None, step=0.5, format="%.2f", placeholder="Enter the amount fed...", key="herp_amount_fed")

                herp_indv_no_eat = st.text_input('Which individuals did not eat?', key="herp_indv_no_eat_key")

                herp_notes = st.text_area("Notes", key="herp_notes_key")

                submitted = st.button("Submit Feeding Log")

                if submitted:
                    if not animal:
                        st.warning("Please select the Animal Type")
                        return
                    
                    if not herpetarium_food:
                        st.warning("Please select the food items fed")
                        return
                    
                    if "Other" in herpetarium_food:
                        if not herp_other_food:
                            st.warning('Please specify the "Other" food item(s)')
                            return
                        
                    if not herp_amount_fed:
                        herp_amount_fed = "0"

                    if not herp_indv_no_eat:
                        herp_indv_no_eat = "None"

                    if not herp_notes:
                        herp_notes = "None"
                        
                    for item in herpetarium_food:
                        if item == "Other":
                            herpother_food_name = herp_other_food
                        else:
                            herpother_food_name = "None"
                        
                        add_herp_feeding_log(user_id, formatted_time, animal, item, herpother_food_name, herp_amount_fed, herp_indv_no_eat, herp_notes)
                    
                    st.success("Feeding log submitted successfully!")
                    time.sleep(1)
                    st.session_state.herp_form_submitted = True
                    st.rerun()
                        

if __name__ == "__main__":
    watershed_herpetarium_fed_log()