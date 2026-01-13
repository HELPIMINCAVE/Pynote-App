import streamlit as st
from src.main.main import add, load_notes, save_notes, delete_note  # Added delete_note

st.set_page_config(page_title="Pynote", page_icon="📝")
st.title("📝 Pynote Streamlit")

# --- SIDEBAR: New Note & Clear All ---
with st.sidebar:
    st.header("New Note")
    title = st.text_input("Title")
    content = st.text_area("Content")
    
    if st.button("Add Note", use_container_width=True):
        if title and content:
            add(title, content)
            st.rerun()
    
    st.divider()
    if st.button("Clear All Notes", type="primary", use_container_width=True):
        save_notes([])
        st.rerun()

# --- MAIN AREA: Display & Delete ---
st.header("Your Notes")
notes = load_notes()

if not notes:
    st.info("No notes found.")
else:
    for note in reversed(notes):
        # We use columns to put the delete button next to the content
        with st.expander(f"📌 {note['title']}"):
            st.write(note['content'])
            
            # Create a unique key for the button using the note ID
            if st.button(f"🗑️ Delete Note {note['id']}", key=f"del_{note['id']}"):
                delete_note(note['id'])
                st.rerun()