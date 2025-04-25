import streamlit as st
from Login import login_page, cookie_controller, clear_cookies
from utils.navbar import navbar

st.set_page_config(initial_sidebar_state="collapsed")

def main():
    
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

        # Log Type Selection Page
        st.markdown('<div id="mammal_log"></div>', unsafe_allow_html=True)
        st.title("Log Type")
        st.write("Select the type of log you want to record:")
        
        st.subheader("Mammal Keeper Log")
        with st.container(border=True):
            if st.button("Feeding Log", use_container_width=True):
                st.switch_page("pages/feeding_log.py")
            
            if st.button("Medical Log", use_container_width=True):
                st.switch_page("pages/medical_log.py")

            if st.button("Enrichment Log", use_container_width=True):
                st.switch_page("pages/enrichment_log.py")

            if st.button("Habitat Cleaning Log", use_container_width=True):
                st.switch_page("pages/habitat_cleaning_log.py")


        st.write("---")

        st.markdown('<div id="herp_log"></div>', unsafe_allow_html=True)
        st.subheader("Watershed/Herpetarium Keeper Log")
        with st.container(border=True):

            filter_option = st.radio("Log Type", ("Watershed", "Herpetarium"), horizontal=True)

            st.session_state["water_herp_log"] = filter_option
            cookie_controller.set("water_herp_log", filter_option)

            if st.button("Feeding Log ", use_container_width=True):
                st.switch_page("pages/water_herp_feeding_log.py")

            if st.button("Medical Log ", use_container_width=True):
                st.switch_page("pages/water_herp_medical_log.py")

            if st.button("Daily Care", use_container_width=True):
                st.switch_page("pages/water_herp_dailycare_log.py")

        # original hex code for the green color #4CAF50

        st.markdown("""
            <a href="#mammal_log">
                <button style="position: fixed; right: 10px; bottom: 400px; padding: 10px; width: 50px; height: 50px; background-color: #0b5394; color: white; border: none; border-radius: 50%; font-size: 20px; cursor: pointer;">
                    🦌
                </button>
            </a>
        """, unsafe_allow_html=True)

        #Button to navigate to Add new reminder section
        st.markdown("""
            <a href="#herp_log">
                <button style="position: fixed; right: 10px; bottom: 340px; padding: 10px; width: 50px; height: 50px; background-color: #0b5394; color: white; border: none; border-radius: 50%; font-size: 20px; cursor: pointer;"> 
                    🐢
                </button>
            </a>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
