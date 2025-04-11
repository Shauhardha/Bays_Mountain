import streamlit as st
from Login import login_page, cookie_controller, clear_cookies
from utils.navbar import navbar
from streamlit_free_text_select import st_free_text_select
import uuid
from utils.feeding_utils import add_feedinglog, add_medslog
from datetime import datetime
import time

st.set_page_config(initial_sidebar_state="collapsed")

def feeding_log():
    
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

        if 'filter_option' not in st.session_state:
            st.session_state.filter_option = "Group"
    
        # Check if the form was submitted and reset session state if necessary
        if 'form_submitted' in st.session_state and st.session_state.form_submitted:
            # Clear session state values for the form inputs only when the form is submitted
            st.session_state["individual_name"] = ""
            st.session_state["leftover_food"] = None
            st.session_state["individual_notes"] = ""

            st.session_state.animal_key = get_unique_key("animal_select")
            #st.session_state.food_key = get_unique_key("food_select")
            st.session_state["food_key"] = ""
            
            st.session_state["nb_amount_fed"] = None
            st.session_state["chicken_amount_fed"] = None
            st.session_state["prey_amount_fed"] = None
            st.session_state["fruits_amount_fed"] = None
            st.session_state["veg_amount_fed"] = None
            st.session_state["fish_amount_fed"] = None
            st.session_state["mazuri_amount_fed"] = None
            st.session_state["amount_fed"] = None

            st.session_state.observation_key = get_unique_key("observation_select")

            st.session_state["group_notes"] = ""
            if "deer_feed_scoops" in st.session_state:
                st.session_state["deer_feed_scoops"] = None
            
            st.session_state["meds_added"] = None
            st.session_state["med_type"] = ""
            st.session_state["dose"] = 0

            st.session_state["log_time"] = datetime.now().time()
            
            # Reset the form submission flag to prevent continuous resetting
            st.session_state.form_submitted = False
            st.rerun()  # Refresh the page to clear the form

        if st.button("Back", use_container_width=False):
            st.switch_page("pages/ethogram_form.py")
        
        col1, col2 = st.columns([1, 0.5])

        with col1:
            st.title("Feeding Log")

        with col2:
            filter_option = st.radio("Feeding Type", ["Group", "Individual"], horizontal=True, index=["Group", "Individual"].index(st.session_state.filter_option))
 
        with st.container(border=True): 
            if filter_option == "Individual":
                st.subheader("Individual Feedings")
            else:
                st.subheader("Group Feedings")
            
            if "animal_key" not in st.session_state:
                st.session_state.animal_key = "animal_select"

            if "observation_key" not in st.session_state:
                st.session_state.observation_key = "observation_select"
            
            # if "food_key" not in st.session_state:
            #     st.session_state.food_key = "food_select"              
            
            animal_group = st_free_text_select(label="Animal Type *", options=["Bobcat","Deer","Red Fox","River Otter","Wolf"],
                index=None,
                format_func=lambda x: x.capitalize(),
                placeholder="Select or enter an animal",
                disabled=False,
                delay=300,
                label_visibility="visible",
                key=st.session_state.animal_key,
            )
            
            if filter_option == "Individual":
                individual_name = st.text_input("Enter Animal Name *", key="individual_name")
            else:
                individual_name = "All"
            
            # food_type = st_free_text_select(label="Select Food Type *", options=["Chicken", "Whole Prey", "Fruits", "Fresh Vegetables"],
            #     index=None,
            #     format_func=lambda x: x.capitalize(),
            #     placeholder="Select or enter a food",
            #     disabled=False,
            #     delay=300,
            #     label_visibility="visible",
            #     key=st.session_state.food_key,
            # )

            st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
            st.write("What did you feed? (Weight per animal in lbs)")
            col1, col2 = st.columns([0.75, 0.75])

            with col1:
                with st.container(border=False):
                    
                    nb_amount_fed = st.number_input("Nebraska Brand", value=None, step=.5, format="%.2f", placeholder="Enter the amount fed...", min_value=0.0, max_value=20.0, key="nb_amount_fed")

                    chicken_amount_fed = st.number_input("Chicken", value=None, step=.5, format="%.2f", placeholder="Enter the amount fed...", min_value=0.0, max_value=20.0, key="chicken_amount_fed")

                    prey_amount_fed = st.number_input("Whole Prey", value=None, step=.5, format="%.2f", placeholder="Enter the amount fed...", min_value=0.0, max_value=20.0, key="prey_amount_fed")

                    fruits_amount_fed = st.number_input("Fresh Fruits", value=None, step=.5, format="%.2f", placeholder="Enter the amount fed...", min_value=0.0, max_value=20.0, key="fruits_amount_fed")

            with col2:
                with st.container(border=False):

                    veg_amount_fed = st.number_input("Fresh Vegetables", value=None, step=.5, format="%.2f", placeholder="Enter the amount fed...", min_value=0.0, max_value=20.0, key="veg_amount_fed")

                    fish_amount_fed = st.number_input("Fish", value=None, step=.5, format="%.2f", placeholder="Enter the amount fed...", min_value=0.0, max_value=20.0, key="fish_amount_fed")

                    mazuri_amount_fed = st.number_input("Mazuri Omnivore", value=None, step=.5, format="%.2f", placeholder="Enter the amount fed...", min_value=0.0, max_value=20.0, key="mazuri_amount_fed")

                    amount_fed = st.number_input("Other Food", value=None, step=.5, format="%.2f", placeholder="Enter the amount fed...", min_value=0.0, max_value=20.0, key="amount_fed")

                    if amount_fed:
                        food_type = st.text_input('What "Other Food" were given?', key="food_key")


            st.write("---")
            observation_type = st_free_text_select(label="Select Observation Type *", options=["DVE","DPE"],
                index=None,
                format_func=lambda x: x.upper(),
                placeholder="Select or enter the observation",
                disabled=False,
                delay=300,
                label_visibility="visible",
                key=st.session_state.observation_key,
            )
            
            leftover_food = st.number_input("Enter Leftover Food", value=None, step=.5, format="%.2f", placeholder="Enter the leftover amount...", min_value=0.0, max_value=20.0, key="leftover_food")   
            
            if leftover_food == "": leftover_food = "0"

            if animal_group == "Deer":
                deer_feed_scoops = st.selectbox("Deer Feed Scoops", ["3","3.5","4","4.5","5","5.5","6"], key="deer_feed_scoops", index=None)
                #st.number_input("Enter Number of Deer Feed Scoops", min_value=0, step=1, key="deer_feed_scoops", value=None)
            else:
                deer_feed_scoops = 0

            meds_added = st.selectbox("Was Medication Added to Food?", ["Yes", "No"], key="meds_added", index=None)
            
            if meds_added == "Yes":
                med_type = st.text_input("Enter Medication Type *", key="med_type")
                dose = st.number_input("Enter Medication Dosage *", value=None, key="dose")
                encounter_type = "Feeding"
                administration_type = "Oral"
            else:
                meds_added = "No"
                encounter_type = None
                med_type = None
                dose = None
                administration_type = None

            individual_notes = st.text_area("Notes", key="individual_notes")

            st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
            log_time = st.time_input("Log Time", key="log_time", step=300)
            st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

            formatted_log_time = log_time.strftime("%H:%M:%S")

            med_log_id = 0

            submitted = st.button("Submit Feeding Log")                
            
            if submitted:
                if filter_option == "Individual" and not individual_name:
                    st.error("Please fill out the name of the Animal.")
                    return

                if not animal_group:
                    st.error("Please fill out Animal Type before submitting the feeding log.")
                    return
                
                if not amount_fed and not nb_amount_fed and not chicken_amount_fed and not prey_amount_fed and not fruits_amount_fed and not veg_amount_fed and not fish_amount_fed and not mazuri_amount_fed:
                    st.error("Please fill out Amount Fed for any food type before submitting the feeding log.")
                    return
                
                if not nb_amount_fed:
                    nb_amount_fed = "0"
                if not chicken_amount_fed:
                    chicken_amount_fed = "0"
                if not prey_amount_fed:
                    prey_amount_fed = "0"
                if not fruits_amount_fed:
                    fruits_amount_fed = "0"
                if not veg_amount_fed:
                    veg_amount_fed = "0"
                if not fish_amount_fed:
                    fish_amount_fed = "0"
                if not mazuri_amount_fed:
                    mazuri_amount_fed = "0"
                if not amount_fed:
                    amount_fed = "0"
                    food_type = "No Other Food Type"
                else:
                    if not food_type:
                        st.error("Please fill out Food Type before submitting the feeding log.")
                        return
                
                total_food_quantity = float(nb_amount_fed) + float(chicken_amount_fed) + float(prey_amount_fed) + float(fruits_amount_fed) + float(veg_amount_fed) + float(fish_amount_fed) + float(mazuri_amount_fed) + float(amount_fed)
                
                if not observation_type:
                    st.error("Please fill out Observation Type before submitting the feeding log.")
                    return

                if meds_added == "Yes":
                    if not med_type:  
                        st.error("Please fill out the medication.")
                        return
                    if not dose:  # Ensure both fields are filled
                        st.error("Please fill out the dosage.")
                        return

                    meds_taken=True

                    # Add medication log
                    med_log_id = add_medslog(
                        user_id, 
                        formatted_time, 
                        animal_group, 
                        individual_name, 
                        encounter_type, 
                        med_type, 
                        dose, 
                        administration_type, 
                        meds_taken,
                        formatted_log_time
                    )

                # Add feeding log (med_log_id is None if no meds were added)

                
                add_feedinglog(user_id, formatted_time, animal_group, individual_name, food_type, amount_fed, observation_type, leftover_food, deer_feed_scoops, meds_added, individual_notes, med_log_id,
                    nb_amount_fed, chicken_amount_fed, prey_amount_fed, fruits_amount_fed, veg_amount_fed, fish_amount_fed, mazuri_amount_fed, total_food_quantity, formatted_log_time)

                st.success("Individual feeding log submitted successfully!")
                time.sleep(1)
                st.session_state.filter_option = filter_option
                st.session_state.form_submitted = True
                st.rerun()
            

def get_unique_key(base_key):
        return f"{base_key}_{uuid.uuid4().hex[:6]}"
          
if __name__ == "__main__":
    feeding_log()



#Alternate code for Food amount

            # st.session_state.nb_amount_key = get_unique_key("nb_amount_select") 
            # st.session_state.chkn_amount_key = get_unique_key("chkn_amount_select")  
            # st.session_state.prey_amount_key = get_unique_key("prey_amount_select")  
            # st.session_state.fruits_amount_key = get_unique_key("fruits_amount_select") 
            # st.session_state.veg_amount_key = get_unique_key("veg_amount_select")  
            # st.session_state.fish_amount_key = get_unique_key("fish_amount_select") 
            # st.session_state.mazuri_amount_key = get_unique_key("mazuri_amount_select") 
            # st.session_state.amount_key = get_unique_key("amount_select")


            # if "food_key" not in st.session_state:
            #     st.session_state.food_key = "food_select"
            
            # if "observation_key" not in st.session_state:    
            #     st.session_state.observation_key = "observation_select"

            # if "nb_amount_key" not in st.session_state:
            #     st.session_state.nb_amount_key = "nb_amount_select" 

            # if "chkn_amount_key" not in st.session_state:
            #     st.session_state.chkn_amount_key = "chkn_amount_select"  

            # if "prey_amount_key" not in st.session_state:
            #     st.session_state.prey_amount_key = "prey_amount_select"  

            # if "fruits_amount_key" not in st.session_state:
            #     st.session_state.fruits_amount_key = "fruits_amount_select" 
                
            # if "veg_amount_key" not in st.session_state:
            #     st.session_state.veg_amount_key = "veg_amount_select"  

            # if "fish_amount_key" not in st.session_state:
            #     st.session_state.fish_amount_key = "fish_amount_select" 

            # if "mazuri_amount_key" not in st.session_state:
            #     st.session_state.mazuri_amount_key = "mazuri_amount_select" 
            
            # if "amount_key" not in st.session_state:
            #     st.session_state.amount_key = "amount_select"  

            # food_type = st_free_text_select(label="Select Food Type *", options=["Chicken", "Whole Prey", "Fruits", "Fresh Vegetables"],
            #     index=None,
            #     format_func=lambda x: x.capitalize(),
            #     placeholder="Select or enter a food",
            #     disabled=False,
            #     delay=300,
            #     label_visibility="visible",
            #     key=st.session_state.food_key,
            # )

            # col1, col2 = st.columns([1, 0.5])

            # with col1:
            #     with st.container(border=True):
            #         st.write("What did you feed? (Weight per animal in lbs)")

            #         nb_amount_fed = st_free_text_select(label="Nebraska Brand", options=["0.25","0.5","0.75","1","1.25","1.5","1.75","2","5","10","15","20"],
            #             index=None,
            #             format_func=lambda x: x.lower(),
            #             placeholder="Select or enter the amount fed",
            #             disabled=False,
            #             delay=300,
            #             label_visibility="visible",
            #             key=st.session_state.nb_amount_key,
            #         )

            #         chicken_amount_fed = st_free_text_select(label="Chicken", options=["0.25","0.5","0.75","1","1.25","1.5","1.75","2","5","10","15","20"],
            #             index=None,
            #             format_func=lambda x: x.lower(),
            #             placeholder="Select or enter the amount fed",
            #             disabled=False,
            #             delay=300,
            #             label_visibility="visible",
            #             key=st.session_state.chkn_amount_key,
            #         )

            #         prey_amount_fed = st_free_text_select(label="Whole Prey", options=["0.25","0.5","0.75","1","1.25","1.5","1.75","2","5","10","15","20"],
            #             index=None,
            #             format_func=lambda x: x.lower(),
            #             placeholder="Select or enter the amount fed",
            #             disabled=False,
            #             delay=300,
            #             label_visibility="visible",
            #             key=st.session_state.prey_amount_key,
            #         )

            #         fruits_amount_fed = st_free_text_select(label="Fresh Fruits", options=["0.25","0.5","0.75","1","1.25","1.5","1.75","2","5","10","15","20"],
            #             index=None,
            #             format_func=lambda x: x.lower(),
            #             placeholder="Select or enter the amount fed",
            #             disabled=False,
            #             delay=300,
            #             label_visibility="visible",
            #             key=st.session_state.fruits_amount_key,
            #         )

            #         veg_amount_fed = st_free_text_select(label="Fresh Vegetables", options=["0.25","0.5","0.75","1","1.25","1.5","1.75","2","5","10","15","20"],
            #             index=None,
            #             format_func=lambda x: x.lower(),
            #             placeholder="Select or enter the amount fed",
            #             disabled=False,
            #             delay=300,
            #             label_visibility="visible",
            #             key=st.session_state.veg_amount_key,
            #         )

            #         fish_amount_fed = st_free_text_select(label="Fish", options=["0.25","0.5","0.75","1","1.25","1.5","1.75","2","5","10","15","20"],
            #             index=None,
            #             format_func=lambda x: x.lower(),
            #             placeholder="Select or enter the amount fed",
            #             disabled=False,
            #             delay=300,
            #             label_visibility="visible",
            #             key=st.session_state.fish_amount_key,
            #         )

            #         mazuri_amount_fed = st_free_text_select(label="Mazuri Omnivore", options=["0.25","0.5","0.75","1","1.25","1.5","1.75","2","5","10","15","20"],
            #             index=None,
            #             format_func=lambda x: x.lower(),
            #             placeholder="Select or enter the amount fed",
            #             disabled=False,
            #             delay=300,
            #             label_visibility="visible",
            #             key=st.session_state.mazuri_amount_key,
            #         )

            #         amount_fed = st_free_text_select(label="Other Food", options=["0.25","0.5","0.75","1","1.25","1.5","1.75","2","5","10","15","20"],
            #             index=None,
            #             format_func=lambda x: x.lower(),
            #             placeholder="Select or enter the amount fed",
            #             disabled=False,
            #             delay=300,
            #             label_visibility="visible",
            #             key=st.session_state.amount_key,
            #         )

            #         if amount_fed:
            #             food_type = st.text_input("Enter Other Food given", key="food_key") 