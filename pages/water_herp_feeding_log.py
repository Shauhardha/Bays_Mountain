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
                st.session_state["location_key"] = []
                st.session_state["pond1_dailycare"] = []
                # st.session_state["pond2_dailycare"] = []
                # st.session_state["pond3_dailycare"] = []
                # st.session_state["tank1_dailycare"] = []
                # st.session_state["tank2_dailycare"] = []
                # st.session_state["tank3_dailycare"] = []
                # st.session_state["tank4_dailycare"] = []
                # st.session_state["tank5_dailycare"] = []
                # st.session_state["tank6_dailycare"] = []
                st.session_state["other_food_input"] = ""
                st.session_state["amount_fed"] = None
                st.session_state["indv_no_eat_key"] = ""
                st.session_state["watershed_notes_key"] = ""

                st.session_state["log_time"] = datetime.now().time()
                
                st.session_state.water_form_submitted = False
                st.rerun() 

            with st.container(border=True):
                # location = st.selectbox("Pond/Tank Location", ["Pond 1", "Pond 2", "Pond 3", "Tank 1", "Tank 2", "Tank 3", "Tank 4", "Tank 5", "Tank 6"], key="location_key", index=None)

                location = st.multiselect(
                    "Pond/Tank Location",
                    ["Pond 1", "Pond 2", "Pond 3", "Tank 1", "Tank 2", "Tank 3", "Tank 4", "Tank 5", "Tank 6"],
                    help="You can choose multiple items.",
                    key="location_key"
                )

                options = ["Silverside", "Shrimp", "Krill cubes", "Bloodworm cubes", "Pellets", "Other"]

                #input_dict = {}

                #st.subheader("Food Items Fed")

                pond1_dailycare = st.multiselect(
                    "Food Items Fed",
                    options,
                    help="You can choose multiple items.",
                    key="pond1_dailycare"
                )

                # if pond1_dailycare: input_dict['Pond 1'] = pond1_dailycare

                # pond2_dailycare = st.multiselect(
                #     "Pond 2",
                #     options,
                #     help="You can choose multiple items.",
                #     key="pond2_dailycare"
                # )

                # if pond2_dailycare: input_dict['Pond 2'] = pond2_dailycare

                # pond3_dailycare = st.multiselect(
                #     "Pond 3",
                #     options,
                #     help="You can choose multiple items.",
                #     key="pond3_dailycare"
                # )

                # if pond3_dailycare: input_dict['Pond 3'] = pond3_dailycare

                # tank1_dailycare = st.multiselect(
                #     "Tank 1",
                #     options,
                #     help="You can choose multiple items.",
                #     key="tank1_dailycare"
                # )

                # if tank1_dailycare: input_dict['Tank 1'] = tank1_dailycare

                # tank2_dailycare = st.multiselect(
                #     "Tank 2",
                #     options,
                #     help="You can choose multiple items.",
                #     key="tank2_dailycare"
                # )

                # if tank2_dailycare: input_dict['Tank 2'] = tank2_dailycare

                # tank3_dailycare = st.multiselect(
                #     "Tank 3",
                #     options,
                #     help="You can choose multiple items.",
                #     key="tank3_dailycare"
                # )

                # if tank3_dailycare: input_dict['Tank 3'] = tank3_dailycare

                # tank4_dailycare = st.multiselect(
                #     "Tank 4",
                #     options,
                #     help="You can choose multiple items.",
                #     key="tank4_dailycare"
                # )

                # if tank4_dailycare: input_dict['Tank 4'] = tank4_dailycare

                # tank5_dailycare = st.multiselect(
                #     "Tank 5",
                #     options,
                #     help="You can choose multiple items.",
                #     key="tank5_dailycare"
                # )

                # if tank5_dailycare: input_dict['Tank 5'] = tank5_dailycare

                # tank6_dailycare = st.multiselect(
                #     "Tank 6",
                #     options,
                #     help="You can choose multiple items.",
                #     key="tank6_dailycare"
                # )

                # if tank6_dailycare: input_dict['Tank 6'] = tank6_dailycare

                if "Other" in pond1_dailycare: # or "Other" in pond2_dailycare or "Other" in pond3_dailycare or "Other" in tank1_dailycare or "Other" in tank2_dailycare or "Other" in tank3_dailycare or "Other" in tank4_dailycare or "Other" in tank5_dailycare or "Other" in tank6_dailycare:
                    other_food = st.text_input('Please specify the "Other" food item(s):', key="other_food_input")

                amount_fed = st.number_input("Total food amount fed per Location", value=None, step=0.5, format="%.2f", placeholder="Enter the amount fed...", key="amount_fed")

                indv_no_eat = st.text_input('Which individuals did not eat?', key="indv_no_eat_key")

                watershed_notes = st.text_area("Notes", key="watershed_notes_key")

                st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
                log_time = st.time_input("Log Time", key="log_time", step=300)
                st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

                formatted_log_time = log_time.strftime("%H:%M:%S")

                submitted = st.button("Submit Feeding Log")

                if submitted:
                    if not pond1_dailycare: # and not pond2_dailycare and not pond3_dailycare and not tank1_dailycare and not tank2_dailycare and not tank3_dailycare and not tank4_dailycare and not tank5_dailycare and not tank6_dailycare:
                        st.warning("Please select the food items fed for the Pond/Tank Location")
                        return
                    
                    # if not watershed_food:
                    #     st.warning("Please select the food items fed")
                    #     return
                    
                    if "Other" in pond1_dailycare: # or "Other" in pond2_dailycare or "Other" in pond3_dailycare or "Other" in tank1_dailycare or "Other" in tank2_dailycare or "Other" in tank3_dailycare or "Other" in tank4_dailycare or "Other" in tank5_dailycare or "Other" in tank6_dailycare:
                        if not other_food:
                            st.warning('Please specify the "Other" food item(s)')
                            return
                        
                    if not amount_fed:
                        amount_fed = 0

                    if not indv_no_eat:
                        indv_no_eat = "None"

                    if not watershed_notes:
                        watershed_notes = "None"
                        
                    for loc in location:     
                        for item in pond1_dailycare:
                            if item == "Other":
                                other_food_name = other_food
                            else:
                                other_food_name = "None"
                            
                            add_watershed_feeding_log(user_id, formatted_time, loc, item, other_food_name, amount_fed, indv_no_eat, watershed_notes, formatted_log_time)

                    st.success("Feeding log submitted successfully!")
                    time.sleep(1)
                    st.session_state.water_form_submitted = True
                    st.rerun()

        elif filter_option == "Herpetarium":

            st.title("Herpetarium Feeding Log")
            
            if 'herp_form_submitted' in st.session_state and st.session_state.herp_form_submitted:
                st.session_state["animal_key"] = None
                st.session_state["herpetarium_food1_key"] = []
                st.session_state["herpetarium_food2_key"] = []
                st.session_state["herpetarium_food3_key"] = []
                st.session_state["herpetarium_food4_key"] = []
                st.session_state["herp_other_food_input"] = ""
                st.session_state["herp_amount_fed"] = None
                st.session_state["herp_indv_no_eat_key"] = ""
                st.session_state["herp_notes_key"] = ""

                st.session_state["log_time"] = datetime.now().time()
                
                st.session_state.herp_form_submitted = False
                st.rerun() 

            with st.container(border=True):
                #animal = st.selectbox("Animal Type", ["Snakes", "Frogs/Salamanders/Lizards", "Turtles (inside)", "Turtles (outside)"], key="animal_key", index=None)

                input_dict = {}

                st.subheader("Food Items Fed")
                
                herpetarium_food1 = st.multiselect(
                    "Snakes",
                    ["Mice", "Worms", "Crickets", "Turtle food (pre-mix)", "Fresh fruit", "Other"],
                    help="You can choose multiple items.",
                    key="herpetarium_food1_key"
                )

                if herpetarium_food1: input_dict['Snakes'] = herpetarium_food1

                herpetarium_food2 = st.multiselect(
                    "Frogs/Salamanders/Lizards",
                    ["Mice", "Worms", "Crickets", "Turtle food (pre-mix)", "Fresh fruit", "Other"],
                    help="You can choose multiple items.",
                    key="herpetarium_food2_key"
                )

                if herpetarium_food2: input_dict['Frogs/Salamanders/Lizards'] = herpetarium_food2

                herpetarium_food3 = st.multiselect(
                    "Turtles (inside)",
                    ["Mice", "Worms", "Crickets", "Turtle food (pre-mix)", "Fresh fruit", "Other"],
                    help="You can choose multiple items.",
                    key="herpetarium_food3_key"
                )

                if herpetarium_food3: input_dict['Turtles (inside)'] = herpetarium_food3

                herpetarium_food4 = st.multiselect(
                    "Turtles (outside)",
                    ["Mice", "Worms", "Crickets", "Turtle food (pre-mix)", "Fresh fruit", "Other"],
                    help="You can choose multiple items.",
                    key="herpetarium_food4_key"
                )

                if herpetarium_food4: input_dict['Turtles (outside)'] = herpetarium_food4

                if "Other" in herpetarium_food1 or "Other" in herpetarium_food2 or "Other" in herpetarium_food3 or "Other" in herpetarium_food4:
                    herp_other_food = st.text_input('Please specify the "Other" food item(s):', key="herp_other_food_input")

                herp_amount_fed = st.number_input("Total Food Amount", value=None, step=0.5, format="%.2f", placeholder="Enter the amount fed...", key="herp_amount_fed")

                herp_indv_no_eat = st.text_input('Which individuals did not eat?', key="herp_indv_no_eat_key")

                herp_notes = st.text_area("Notes", key="herp_notes_key")

                st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
                log_time = st.time_input("Log Time", key="log_time", step=300)
                st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

                formatted_log_time = log_time.strftime("%H:%M:%S")

                submitted = st.button("Submit Feeding Log")

                if submitted:
                    if not herpetarium_food1 and not herpetarium_food2 and not herpetarium_food3 and not herpetarium_food4:
                        st.warning("Please select the Animal Type")
                        return
                    
                    # if not herpetarium_food:
                    #     st.warning("Please select the food items fed")
                    #     return
                    
                    if "Other" in herpetarium_food1 or "Other" in herpetarium_food2 or "Other" in herpetarium_food3 or "Other" in herpetarium_food4:
                        if not herp_other_food:
                            st.warning('Please specify the "Other" food item(s)')
                            return
                        
                    if not herp_amount_fed:
                        herp_amount_fed = "0"

                    if not herp_indv_no_eat:
                        herp_indv_no_eat = "None"

                    if not herp_notes:
                        herp_notes = "None"
                        
                    for animal, selected_items in input_dict.items():
                        for item in selected_items:
                            if item == "Other":
                                herpother_food_name = herp_other_food
                            else:
                                herpother_food_name = "None"
                            
                            add_herp_feeding_log(user_id, formatted_time, animal, item, herpother_food_name, herp_amount_fed, herp_indv_no_eat, herp_notes, formatted_log_time)
                    
                    st.success("Feeding log submitted successfully!")
                    time.sleep(1)
                    st.session_state.herp_form_submitted = True
                    st.rerun()
                        

if __name__ == "__main__":
    watershed_herpetarium_fed_log()