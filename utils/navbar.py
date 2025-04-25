import streamlit as st

def navbar():
    # Sidebar navigation
    username = st.session_state["username"]

    st.sidebar.status

    st.sidebar.markdown(f"<p style='font-size:25px; font-weight:bold; font-family:'Calibri';'>{username}</p>",unsafe_allow_html=True)
    st.sidebar.page_link('app.py', label=f'🏠 Home')
    st.sidebar.page_link('pages/notes.py', label='✍ Notes')
    st.sidebar.page_link('pages/calendar.py', label='📅 Calendar')
    st.sidebar.page_link('pages/ethogram_form.py', label='📝 Ethogram Form')
    st.sidebar.page_link('pages/Data_Visualization.py', label='📈 Data Visualization')
    if "role" in st.session_state and st.session_state["role"] == "admin":
        st.sidebar.page_link('pages/Admin.py', label='💻 Admin')
    #    st.sidebar.page_link('pages/habitat.py', label='🦊 Animal & Habitat')
    else:
        st.sidebar.page_link('pages/Admin.py', label='👨‍🌾 User')
    

    st.markdown(
        """
       <style>
       [data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 250px;
           max-width: 250px;
       }
       """,
        unsafe_allow_html=True,
    )
    
def auto_collapse_sidebar():
    st.markdown(
        """
        <script>
            window.addEventListener("load", function () {
                let sidebar = parent.document.querySelector("section[data-testid='stSidebar']");
                if (sidebar && sidebar.getAttribute("aria-expanded") === "true") {
                    sidebar.querySelector('button[aria-label="Close sidebar"]').click();
                }
            });
        </script>
        """,
        unsafe_allow_html=True,
    )
