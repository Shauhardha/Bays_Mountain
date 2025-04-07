import streamlit as st
from datetime import datetime
from utils.notes_utils import get_notes, add_note, search_notes, add_category, add_tag, pin_note, delete_note
from Login import login_page, cookie_controller, clear_cookies
from utils.navbar import navbar, auto_collapse_sidebar
import time

st.set_page_config(initial_sidebar_state="collapsed")

def notes_page():
    '''
    if "user_id" not in st.session_state:
        st.warning("Session expired. Please log in again.")
        st.session_state.logged_in = False  # Flag for login redirection
        st.experimental_rerun()  # Refresh the page to redirect to login
    '''
    
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
        
        user_id = st.session_state["user_id"]
        username = st.session_state["username"]

        auto_collapse_sidebar()
        navbar()
        
        # hide_sidebar_css = """
        #             <style>
        #                 [data-testid="collapsedControl"] {
        #                     display: none;
        #                 }
        #                 [data-testid="stSidebar"] {
        #                     display: none;
        #                 }
        #             </style>
        #         """
        
        # st.markdown(hide_sidebar_css, unsafe_allow_html=True)

        
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

        st.markdown('<div id="search_notes"></div>', unsafe_allow_html=True)
        st.title("Collaborative Notes")
        
        # Section for searching notes
        st.subheader("Search Notes")
        search_query = st.text_input("Search notes by title or content:")

        # Display notes based on search query
        notes = search_notes(search_query,user_id) if search_query else get_notes(user_id)
        
        # Display notes with user and timestamp
        st.subheader("Your Notes")
        with st.container(height=350, border=True):
            if notes:
                for note in notes:
                    note_id, username, title, content, category, is_shared, created_at, updated_at, is_pinned = (
                        note[0],
                        note[1],
                        note[2],
                        note[3],
                        note[4],
                        note[5],
                        note[6],
                        note[7],
                        note[8]
                    )

                    with st.expander(f"{title} (Pinned: {'Yes' if is_pinned else 'No'})"):
                        st.markdown(f"""
                        **Category**: {category if category else "Uncategorized"}  
                        **Content**: {content}  
                        **Shared**: {"Yes" if is_shared else "No"}  
                        **Created by**: {username}  
                        **Created at**: {created_at.strftime('%Y-%m-%d %H:%M:%S') if isinstance(created_at, datetime) else created_at}
                        """)

                        # Create two columns: one for the pin/unpin button and one for the delete button
                        col1, col2 = st.columns([3, 1])  # Adjust column width ratio as needed
                        
                        with col1:
                            if not is_pinned:
                                if st.button(f"Pin Note", key=f"pin_{note_id}"):
                                    pin_note(note_id, True)
                                    st.rerun()
                            else:
                                if st.button(f"Unpin Note", key=f"unpin_{note_id}"):
                                    pin_note(note_id, False)
                                    st.rerun()
                        with col2:
                            # Delete button
                            if st.button(f"Delete Note", key=f"delete_{note_id}"):
                                delete_note(note_id)  # Call the delete_note function
                                st.success("Note deleted successfully!")
                                time.sleep(1)
                                st.rerun()  # Refresh the page to update the notes list 
            else:
                st.info("No notes available.")

        st.write("---") 

        st.markdown('<div id="add_new_notes"></div>', unsafe_allow_html=True)
        st.subheader("Add New Notes")
        with st.form('Notes From',clear_on_submit=True):
            st.text_input("Your Username:", value=username, disabled=True)
            
            title = st.text_input("Note Title:")
            category = st.selectbox("Category", ["Work", "Personal"])
            
            # Rich text editor for note content
            #new_note = st_quill(toolbar=None, key="Note Content:")
            new_note = st.text_area("Note:", height=200)
            is_shared = st.checkbox("Share this note with others?", value=False)
            
            # Add tags functionality
            tags_input = st.text_input("Add tags (comma-separated):")
            tags = tags_input.split(",") if tags_input else []

            submitted = st.form_submit_button("Add Note")

            if submitted:
                if not title or not new_note:
                    st.error("Please fill out all fields before adding the note.")
                else:
                    # Add the note to the database
                    note_id = add_note(user_id, title, new_note, category, is_shared)
                    
                    # Add tags to the database
                    for tag in tags:
                        add_tag(note_id, tag.strip())

                    st.success("Note added successfully!")
                    time.sleep(1)
                    st.rerun()  # Refresh the page to show updated notes


        #Button to navigate to search reminder section
        st.markdown("""
            <a href="#search_notes">
                <button style="position: fixed; right: 10px; bottom: 400px; padding: 10px; width: 50px; height: 50px; background-color: #0b5394; color: white; border: none; border-radius: 50%; font-size: 20px; cursor: pointer;">
                    🔍
                </button>
            </a>
        """, unsafe_allow_html=True)

        #Button to navigate to Add new reminder section
        st.markdown("""
            <a href="#add_new_notes">
                <button style="position: fixed; right: 10px; bottom: 340px; padding: 10px; width: 50px; height: 50px; background-color: #0b5394; color: white; border: none; border-radius: 50%; font-size: 20px; cursor: pointer;"> 
                    ➕
                </button>
            </a>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    notes_page()