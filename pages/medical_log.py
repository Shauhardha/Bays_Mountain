import streamlit as st
from Login import login_page, cookie_controller, clear_cookies
from utils.medical_utils import add_injury_log, add_sedation_log, add_medslog, add_medslog_main, add_vetlog
from utils.navbar import navbar
from streamlit_free_text_select import st_free_text_select
import uuid
import datetime
import time

st.set_page_config(initial_sidebar_state="collapsed")

def medical_log_page():
    
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

        if 'form_submitted' in st.session_state and st.session_state.form_submitted:
            st.session_state.animal_key = get_unique_key("animal_select")
            st.session_state["animal_name"] = ""
            st.session_state.encounter_key = get_unique_key("encounter_select")
            
            st.session_state.injury_tie = "No"
            st.session_state["injury_type"] = None
            st.session_state["injury_description"] = ""
            st.session_state.exam_key = get_unique_key("exam_select")

            st.session_state.sedation = "No"
            #st.session_state["sedation_medication"] = ""
            st.session_state.sedation_medication_key = get_unique_key("sedation_medication_select")
            st.session_state["sed_dose"] = ""
            st.session_state["sedation_kit"] = ""
            st.session_state.sed_administration_key = get_unique_key("sed_admin_select")
            st.session_state["time_in"] = datetime.datetime.now().time()
            st.session_state["time_out"] = datetime.datetime.now().time()

            st.session_state.vet_notified = "No"
            st.session_state["vet_response"] = ""

            st.session_state.meds_tie = "No"
            st.session_state["Meloxicam"] = None
            st.session_state["Cephalexin"] = None
            st.session_state["Gabapentin"] = None
            st.session_state["Bravecto"] = None
            st.session_state["Intercepter"] = None

            st.session_state["mel_dose"] = ""
            st.session_state["cep_dose"] = ""
            st.session_state["gap_dose"] = ""
            st.session_state["brav_dose"] = ""
            st.session_state["int_dose"] = ""

            st.session_state["meds_type"] = ""
            # st.session_state.meds_type_key = get_unique_key("meds_type_select")
            st.session_state["med_dose"] = ""
            st.session_state.encounter_key = get_unique_key("encounter_select")
            st.session_state["meds_taken"] = None

            st.session_state["med_log_notes"] = ""

            st.session_state["log_time"] = datetime.datetime.now().time()

            st.session_state.form_submitted = False
            st.rerun()

        
        if 'vet_form_submitted' in st.session_state and st.session_state.vet_form_submitted:
            st.session_state.vetlog_animal_key = get_unique_key("vetlog_animal_select")
            st.session_state["vet_animal_name"] = ""
            
            #st.session_state["vet_type"] = ""
            st.session_state["vet_name"] = ""
            st.session_state["check_type"] = ""
            st.session_state.check_key = get_unique_key("check_select")
            st.session_state["vet_location"] = None
            st.session_state["vet_exam_notes"] = ""

            st.session_state["vet_log_time"] = datetime.datetime.now().time()

            st.session_state.vet_form_submitted = False
            st.rerun()


        st.markdown('<div id="medical_log"></div>', unsafe_allow_html=True)

        if st.button("Back", use_container_width=False):
            st.switch_page("pages/ethogram_form.py")

        st.title("Medical Log") 

        with st.container(border=True):
            if "animal_key" not in st.session_state:
                st.session_state.animal_key = "animal_select"
            
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


            # Animal name and encounter type
            animal_name = st.text_input("Animal Name:", key="animal_name")
            #encounter_type = st.selectbox("Encounter Type:", ["", "Routine Check", "Emergency", "Follow-up"], key="encounter_type")

            if "encounter_key" not in st.session_state:
                st.session_state.encounter_key = "encounter_select"
            
            encounter_type = st_free_text_select(
                label="Encounter Type",
                options=["Medication","Vaccination","Routine Check", "Emergency", "Follow-up"],     #"Vet-Visit",
                index=None,
                format_func=lambda x: x.capitalize(),
                placeholder="Select or enter an animal",
                disabled=False,
                delay=300,
                key=st.session_state.encounter_key, 
                label_visibility="visible",
            )

            #Injury Section
            injury = st.radio("Medication tied to Injury?", horizontal=True, options=["No", "Yes"], key="injury_tie")

            vet_notified = "No"
            vet_response = "None"

            if injury == "Yes":
                with st.container(border=True):
                    injury_type = st.selectbox("Injury Type:", ["New", "Old"], index=None, key="injury_type")
                    injury_description = st.text_area("Injury Description:", key="injury_description")

                    if "exam_key" not in st.session_state:
                        st.session_state.exam_key = "exam_select"
                    examination_type = st_free_text_select(
                        label="Examination Type",
                        options=["PE","VE"],
                        index=None,
                        format_func=lambda x: x.upper(),
                        placeholder="Select or enter Examination Type",
                        disabled=False,
                        delay=300,
                        key=st.session_state.exam_key, 
                        label_visibility="visible",
                    )
                    #Vet Notified
                    vet_notified = st.radio("Vet Notified?", horizontal=True, options=["No", "Yes"], key="vet_notified")

                    if vet_notified == "Yes":
                        vet_response = st.text_input("Vet Response", key="vet_response")
                    else:
                        vet_response = "None"

            #Animal Sedation
            sedated = st.radio("Was Animal Sedated?", horizontal=True, options=["No", "Yes"], key="sedation")

            if sedated == "Yes":
                with st.container(border=True):
                    
                    #sedation_medication = st.text_input("Sedation Medication used", key="sedation_medication")
                    if "sedation_medication_key" not in st.session_state:
                        st.session_state.sedation_medication_key = "sedation_medication_select"
                    sedation_medication = st_free_text_select(
                        label="Sedation Medication Used",
                        options=["BAM Sedation","BAM Reversal"],
                        index=None,
                        format_func=lambda x: x.capitalize(),
                        placeholder="Select or enter Sedation Medication Used",
                        disabled=False,
                        delay=300,
                        key=st.session_state.sedation_medication_key, 
                        label_visibility="visible",
                    )
                    
                    sed_dose = st.text_input("Sedation Dose:", key="sed_dose")
                    sedation_kit = st.text_input("Sedation Kit used", key="sedation_kit")

                    if "sed_administration_key" not in st.session_state:
                        st.session_state.sed_administration_key = "sed_admin_select"
                    sed_administration_type = st_free_text_select(
                        label="Sedation Administration Method",
                        options=["Oral","Dart Gun", "Hand"],
                        index=None,
                        format_func=lambda x: x.capitalize(),
                        placeholder="Select or enter Sedation Administration Method",
                        disabled=False,
                        delay=300,
                        key=st.session_state.sed_administration_key, 
                        label_visibility="visible",
                    )

                    time_administered = st.time_input("Set Administered Time", key="time_in", step=300)

                    response_time = st.time_input("Set Response Time", key="time_out", step=300)

                    time_administered_dt = datetime.datetime.combine(datetime.date.today(), time_administered)
                    response_time_dt = datetime.datetime.combine(datetime.date.today(), response_time)

                    # Check if response_time is greater than time_administered
                    if response_time_dt < time_administered_dt:
                        st.error("❌ 'Time Out' must be **greater** than 'Time In'. Please enter a valid time.")

                    formatted_time_in = time_administered.strftime("%H:%M:%S")
                    formatted_time_out = response_time.strftime("%H:%M:%S")

            
            #Medication Section
            medication = st.radio("Did you administer Medication?", horizontal=True, options=["No", "Yes"], key="meds_tie")

            if medication == "Yes":
                with st.container(border=True):
                    #meds_type = st.text_input("Medication Type:", key="meds_type")

                    
                    
                    Meloxicam = st.checkbox('Meloxicam', key="Meloxicam")
                    if Meloxicam:
                        buff, buff2 = st.columns([1,1])
                        mel_dose = buff.text_input("Meloxicam Dose:", key="mel_dose")

                    Cephalexin = st.checkbox('Cephalexin', key="Cephalexin")
                    if Cephalexin:
                        buff, buff2 = st.columns([1,1])
                        cep_dose = buff.text_input("Cephalexin Dose:", key="cep_dose")

                    Gabapentin = st.checkbox('Gabapentin', key="Gabapentin")
                    if Gabapentin:
                        buff, buff2 = st.columns([1,1])
                        gap_dose = buff.text_input("Gabapentin Dose:", key="gap_dose")

                    Bravecto = st.checkbox('Bravecto', key="Bravecto")
                    if Bravecto:
                        buff, buff2 = st.columns([1,1])
                        brav_dose = buff.text_input("Bravecto Dose:", key="brav_dose")

                    Intercepter = st.checkbox('Intercepter', key="Intercepter")
                    if Intercepter:
                        buff, buff2 = st.columns([1,1])
                        int_dose = buff.text_input("Intercepter Dose:", key="int_dose")
                    
                    ifOther = st.checkbox('Other', key="ifOther")
                    if ifOther:
                        buff, buff2 = st.columns([1,1])
                        meds_type = buff.text_input("Medication Type:", key="med_type")
                        meds_dose = buff.text_input("Medication Dose:", key="med_dose")
                    
                    # if "meds_type_key" not in st.session_state:
                    #     st.session_state.meds_type_key = "meds_type_select"
                    # meds_type = st_free_text_select(
                    #     label="Medication Type:",
                    #     options=["Meloxicam","Cephalexin", "Gabapentin", "Bravecto", "Intercepter"],
                    #     index=None,
                    #     format_func=lambda x: x.capitalize(),
                    #     placeholder="Select or enter Medication Type",
                    #     disabled=False,
                    #     delay=300,
                    #     key=st.session_state.meds_type_key, 
                    #     label_visibility="visible",
                    # )

                    if "administration_key" not in st.session_state:
                        st.session_state.administration_key = "admin_select"
                    administration_type = st_free_text_select(
                        label="Administration Route",
                        options=["Oral", "IM", "Dart Gun"],
                        index=None,
                        format_func=lambda x: x.upper(),
                        placeholder="Select or enter Meds Administration Route",
                        disabled=False,
                        delay=300,
                        key=st.session_state.administration_key, 
                        label_visibility="visible",
                    )

                    meds_taken = st.selectbox("Did animal take medication:", ["Yes", "No"], index=None, key="meds_taken") 

            injury_description = st.text_area("Medical Log Notes and Findings:", key="med_log_notes")

            st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
            log_time = st.time_input("Log Time", key="log_time", step=300)
            st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

            formatted_log_time = log_time.strftime("%H:%M:%S")

            injury_id = 0
            sedation_id = 0
            medication_id = 0
            
            if st.button("Submit Medical Log"):
                if not animal_group:
                    st.error("Please fill out Animal Type before submitting the medical log.")
                    return
                if not animal_name:
                    st.error("Please fill out Animal Name before submitting the medical log.")
                    return
                if not encounter_type:
                    st.error("Please fill out Encounter Type before submitting the medical log.")
                    return
                
                if injury == "Yes":
                    if not injury_type:
                        st.error("Please fill out Injury Type.")
                        return
                    if not injury_description:
                        st.error("Please fill out Injury Description.")
                        return
                    if not examination_type:
                        st.error("Please fill out Examination Type.")
                        return
                    
                    if vet_notified == "Yes":
                        if not vet_response:
                            st.error("Please fill out Vet Response.")
                            return
                    
                    injury_id = add_injury_log(user_id, formatted_time, animal_group, animal_name, encounter_type, injury_type, injury_description, examination_type, formatted_log_time)

                    

                if sedated == "Yes":
                    if not sedation_medication:
                        st.error("Please fill out Medication used for Sedation.")
                        return
                    if not sed_dose:
                        st.error("Please fill out Sedation Dosage.")
                        return
                    if not sed_administration_type:
                        st.error("Please fill out Sedation Administration Route.")
                        return
                    
                    sedation_id = add_sedation_log(
                                        user_id, formatted_time, animal_group, animal_name, 
                                        encounter_type, sedation_medication, sed_dose, sedation_kit, 
                                        sed_administration_type, formatted_time_in, formatted_time_out, formatted_log_time
                                    )
                    
                if medication == "Yes":
                    if Meloxicam and not mel_dose:
                        st.error("Please fill out Meloxicam dosage.")
                        return
                    elif not Meloxicam:
                        mel_dose = "0"
                    
                    if Cephalexin and not cep_dose:
                        st.error("Please fill out Cephalexin dosage.")
                        return
                    elif not Cephalexin:
                        cep_dose = "0"
                    
                    if Gabapentin and not gap_dose:
                        st.error("Please fill out Gabapentin dosage.")
                        return
                    elif not Gabapentin:
                        gap_dose = "0"
                    
                    if Bravecto and not brav_dose:
                        st.error("Please fill out Bravecto dosage.")
                        return
                    elif not Bravecto:
                        brav_dose = "0"
                    
                    if Intercepter and not int_dose:
                        st.error("Please fill out Intercepter dosage.")
                        return
                    elif not Intercepter:
                        int_dose = "0"
                    
                    if ifOther and not meds_type:
                        if not meds_type:
                            st.error("Please fill out the other Medication used.")
                            return
                        if not meds_dose:
                            st.error("Please fill out the other Medication Dosage.")
                            return
                    elif not ifOther:
                        meds_type = "None"
                        meds_dose = "0"
                    if not administration_type:
                        st.error("Please fill out Sedation Administration Route.")
                        return
                    if not meds_taken:
                        st.error("Please fill out if animal took the medication.")
                        return
                    
                    medication_id = add_medslog(
                                        user_id, formatted_time, animal_group, animal_name, encounter_type, 
                                        meds_type, meds_dose, administration_type, meds_taken,
                                        Meloxicam,Cephalexin,Gabapentin,Bravecto,Intercepter,
                                        mel_dose,cep_dose,gap_dose,brav_dose,int_dose,ifOther, formatted_log_time
                                    )
                    
                    
                add_medslog_main(
                    user_id, formatted_time, animal_group, animal_name, encounter_type, 
                    injury, injury_id, sedated, sedation_id, 
                    vet_notified, vet_response, medication, medication_id, injury_description, formatted_log_time)

                st.success("Medical log submitted successfully!")
                time.sleep(1)
                st.session_state.form_submitted = True
                st.rerun()       
        
        
        st.write("---")
        st.markdown('<div id="vet_log"></div>', unsafe_allow_html=True)
        st.title("Vet Log")

        with st.container(border=True):

            if "vetlog_animal_key" not in st.session_state:
                st.session_state.vetlog_animal_key = "vetlog_animal_select"
            vet_animal_group = st_free_text_select(
                label="Animal Type:",
                options=["Bobcat", "Deer", "Red Fox", "River Otter", "Wolf"],
                index=None,
                format_func=lambda x: x.capitalize(),
                placeholder="Select or enter Animal Type",
                disabled=False,
                delay=300,
                key=st.session_state.vetlog_animal_key, 
                label_visibility="visible",
            )
            # Animal name and encounter type
            vet_animal_name = st.text_input("Animal Name:", key="vet_animal_name")
            
            #vet_type = st.text_input("Vet Intervention Type:", key="vet_type")
            vet_name = st.text_input("Vet Name:", key="vet_name")
            
            if "check_key" not in st.session_state:
                st.session_state.check_key = "check_select"
            vet_check = st_free_text_select(
                label="Vet Check Type:",
                options=["Yearly Assessment","Quaterly Assessment","Operation","Injury Check"],
                index=None,
                format_func=lambda x: x.capitalize(),
                placeholder="Select or enter Vet Check Type",
                disabled=False,
                delay=300,
                key=st.session_state.check_key, 
                label_visibility="visible",
            )
            location = st.selectbox("Vet Examination Location:", ["On-Site", "Took-to-vet"], index=None, key="vet_location")
            vet_exam_notes = st.text_area("Examination Notes:", key="vet_exam_notes")

            st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
            vet_log_time = st.time_input("Log Time", key="vet_log_time", step=300)
            st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

            formatted_vet_log_time = vet_log_time.strftime("%H:%M:%S")
            
            if st.button("Submit Vet Data", key="submit_vet"): 
                
                if not vet_animal_group:
                    st.error("Please fill out Animal Type before submitting the medical log.")
                    return
                if not vet_animal_name:
                    st.error("Please fill out Animal Name before submitting the medical log.")
                    return
                if not vet_name:
                    st.error("Please fill out Vet Name.")
                    return
                if not vet_check:
                    st.error("Please fill out Vet Check Type.")
                    return
                if not location:
                    st.error("Please fill out Vet Examination Location.")
                    return 
                if not vet_exam_notes:
                    st.error("Please fill out Vet Examination Notes. If there is not significant notes then type 'NSF'")
                    return 
                
                add_vetlog(user_id, formatted_time, vet_animal_group, vet_animal_name, vet_name, vet_check, location, vet_exam_notes, formatted_vet_log_time)
                
                st.success("Vet log submitted successfully!")
                time.sleep(1)
                st.session_state.vet_form_submitted = True
                st.rerun()


        #Button to navigate to search reminder section
        st.markdown("""
            <a href="#medical_log">
                <button style="position: fixed; right: 10px; bottom: 400px; padding: 10px; width: 50px; height: 50px; background-color: #4CAF50; color: white; border: none; border-radius: 50%; font-size: 22px; cursor: pointer;">
                    ➕
                </button>
            </a>
        """, unsafe_allow_html=True)

        #Button to navigate to Add new reminder section
        st.markdown("""
            <a href="#vet_log">
                <button style="position: fixed; right: 10px; bottom: 340px; padding: 10px; width: 50px; height: 50px; background-color: #4CAF50; color: white; border: none; border-radius: 50%; font-size: 22px; cursor: pointer;">
                    👨‍⚕️
                </button>
            </a>
        """, unsafe_allow_html=True)
        
    
def get_unique_key(base_key):
        return f"{base_key}_{uuid.uuid4().hex[:6]}"

if __name__ == "__main__":
    medical_log_page()
