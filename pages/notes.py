import streamlit as st
from datetime import datetime
from utils.notes_utils import get_notes, add_note, search_notes, add_category, add_tag, pin_note, delete_note
from Login import login_page
from utils.navbar import navbar
#from streamlit_quill import st_quill

def notes_page():
    '''
    if "user_id" not in st.session_state:
        st.warning("Session expired. Please log in again.")
        st.session_state.logged_in = False  # Flag for login redirection
        st.experimental_rerun()  # Refresh the page to redirect to login
    '''
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False  # Default to not logged in
    
    if not st.session_state.logged_in:
        login_page()
    else:
        
        user_id = st.session_state["user_id"]
        username = st.session_state["username"]

        navbar()
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
        notes = search_notes(search_query,str(user_id)) if search_query else get_notes(str(user_id))
        
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
                    st.rerun()  # Refresh the page to show updated notes


        #Button to navigate to search reminder section
        st.markdown("""
            <a href="#search_notes">
                <button style="position: fixed; right: 20px; bottom: 400px; padding: 10px 20px; width: 168px; background-color: #4CAF50; color: white; border: none; border-radius: 25px; font-size: 16px; cursor: pointer;">
                    Search Notes
                </button>
            </a>
        """, unsafe_allow_html=True)

        #Button to navigate to Add new reminder section
        st.markdown("""
            <a href="#add_new_notes">
                <button style="position: fixed; right: 20px; bottom: 350px; padding: 10px 20px; width: 168px; background-color: #4CAF50; color: white; border: none; border-radius: 25px; font-size: 16px; cursor: pointer;">
                    Add New Notes
                </button>
            </a>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    notes_page()