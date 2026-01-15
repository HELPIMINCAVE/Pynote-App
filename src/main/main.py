import streamlit as st
import pandas as pd
import sys
import os

# Ensure the root directory is in your path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from src.main.main import add, load_notes, save_notes, delete_note
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.stop()

st.set_page_config(page_title="Pynote Pro", page_icon="📝")
st.title("📝 Pynote Streamlit")

# --- SIDEBAR: Add & Export ---
with st.sidebar:
    st.header("New Note")
    title_in = st.text_input("Title")
    content_in = st.text_area("Content")
    if st.button("Add Note", use_container_width=True):
        if title_in and content_in:
            add(title_in, content_in)
            st.success("Note added!")
            st.rerun()
    
    st.divider()
    st.header("Backup & Export")
    notes = load_notes()
    
    if notes:
        # Convert notes to Dataframe for CSV export
        df = pd.DataFrame(notes)
        
        # 1. Export as CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export as .CSV",
            data=csv,
            file_name='pynote_export.csv',
            mime='text/csv',
            use_container_width=True
        )
        
        # 2. Export as TXT
        txt_content = "=== PYNOTE EXPORT ===\n\n"
        for n in notes:
            ts = n.get('timestamp', 'No date')
            txt_content += f"TITLE: {n['title']}\nDATE: {ts}\nCONTENT: {n['content']}\n{'-' * 20}\n"
        
        st.download_button(
            label="📄 Export as .TXT",
            data=txt_content,
            file_name='pynote_export.txt',
            mime='text/plain',
            use_container_width=True
        )
    
    st.divider()
    st.subheader("Danger Zone")
    if st.button("Clear All Notes", type="primary", use_container_width=True):
        save_notes([])
        st.rerun()

# --- MAIN AREA: Search & Display ---
search_query = st.text_input("🔍 Search notes...", "").lower()

if not notes:
    st.info("No notes found. Create one in the sidebar!")
else:
    # Filter notes for search
    filtered = [
        n for n in notes
        if search_query in n['title'].lower() or search_query in n['content'].lower()
    ]
    
    for note in reversed(filtered):
        # We display the timestamp in the expander title
        timestamp = note.get('timestamp', 'New Note')
        with st.expander(f"📌 {note['title']} ({timestamp})"):
            st.write(note['content'])
            
            # Delete Button
            if st.button(f"🗑️ Delete Note", key=f"del_{note['id']}"):
                delete_note(note['id'])
                st.rerun()