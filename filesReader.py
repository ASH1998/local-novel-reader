import streamlit as st
import os
import json
import glob

st.set_page_config(layout="wide")

def get_available_series():
    return [d for d in os.listdir('novel_chapters') 
            if os.path.isdir(os.path.join('novel_chapters', d))]

def get_available_chapters(series_name):
    chapter_files = glob.glob(f'novel_chapters/{series_name}/chapter_*.txt')
    chapters = []
    for file in chapter_files:
        chapter_num = int(file.split('chapter_')[-1].replace('.txt', ''))
        chapters.append(chapter_num)
    return sorted(chapters)

def load_progress():
    if os.path.exists('reading_progress.json'):
        with open('reading_progress.json', 'r') as f:
            return json.load(f)
    return {'series': {}}

def save_progress(progress):
    with open('reading_progress.json', 'w') as f:
        json.dump(progress, f)

def load_chapter(series_name, chapter_num):
    try:
        chapter_path = f'novel_chapters/{series_name}/chapter_{chapter_num}.txt'
        with open(chapter_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None

def main():
    st.title("Novel Reader")
    
    # Add sidebar content
    st.sidebar.title("Reading Progress")
    progress = load_progress()
    
    # Get available series
    available_series = get_available_series()
    selected_series = st.sidebar.selectbox("Select Series", available_series)
    
    # Initialize series progress if not exists
    if selected_series not in progress['series']:
        progress['series'][selected_series] = {'last_read': 1, 'max_read': 1}
    
    series_progress = progress['series'][selected_series]
    available_chapters = get_available_chapters(selected_series)
    
    # Initialize session state for series and chapter if not exists
    if 'current_series' not in st.session_state:
        st.session_state.current_series = selected_series
    if 'current_chapter' not in st.session_state:
        st.session_state.current_chapter = series_progress['last_read']
    
    # Update session state if series changes
    if selected_series != st.session_state.current_series:
        st.session_state.current_series = selected_series
        st.session_state.current_chapter = series_progress['last_read']
    
    # Add chapter selectbox in sidebar
    selected_chapter = st.sidebar.selectbox(
        "Select Chapter",
        available_chapters,
        index=available_chapters.index(st.session_state.current_chapter)
    )
    
    # Update current chapter if selection changes
    if selected_chapter != st.session_state.current_chapter:
        st.session_state.current_chapter = selected_chapter
    
    current_chapter = st.session_state.current_chapter
    
    # Calculate progress based on chapter position
    current_index = available_chapters.index(current_chapter)
    total_chapters = len(available_chapters)
    progress_value = (current_index + 1) / total_chapters
    progress_text = f"{progress_value:.1%}"
    
    st.sidebar.progress(progress_value, text=progress_text)
    st.sidebar.metric("Current Chapter", current_chapter)
    st.sidebar.metric("Last Read Chapter", series_progress['last_read'])
    st.sidebar.metric("Max Read Chapter", series_progress['max_read'])
    
    # Main content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Previous Chapter"):
            try:
                current_index = available_chapters.index(current_chapter)
                if current_index > 0:
                    st.session_state.current_chapter = available_chapters[current_index - 1]
                    st.rerun()
            except ValueError:
                st.error("Chapter not found in sequence")
    
    with col2:
        st.write(f"Current Chapter: {current_chapter}")
    
    with col3:
        if st.button("Next Chapter"):
            try:
                current_index = available_chapters.index(current_chapter)
                if current_index < len(available_chapters) - 1:
                    st.session_state.current_chapter = available_chapters[current_index + 1]
                    st.rerun()
            except ValueError:
                st.error("Chapter not found in sequence")
    
    chapter_content = load_chapter(selected_series, current_chapter)
    
    if chapter_content:
        st.markdown("---")
        st.markdown(chapter_content)
        
        # Add bottom navigation buttons
        st.markdown("---")
        bcol1, bcol2, bcol3 = st.columns(3)
        
        with bcol1:
            if st.button("Previous Chapter", key="prev_bottom"):
                try:
                    current_index = available_chapters.index(current_chapter)
                    if current_index > 0:
                        st.session_state.current_chapter = available_chapters[current_index - 1]
                        st.rerun()
                except ValueError:
                    st.error("Chapter not found in sequence")
        
        with bcol2:
            st.write(f"Current Chapter: {current_chapter}")
        
        with bcol3:
            if st.button("Next Chapter", key="next_bottom"):
                try:
                    current_index = available_chapters.index(current_chapter)
                    if current_index < len(available_chapters) - 1:
                        st.session_state.current_chapter = available_chapters[current_index + 1]
                        st.rerun()
                except ValueError:
                    st.error("Chapter not found in sequence")
        
        # Update progress immediately when chapter is found
        series_progress['last_read'] = current_chapter
        series_progress['max_read'] = max(series_progress['max_read'], current_chapter)
        save_progress(progress)
    else:
        st.error("Chapter not found!")
        st.session_state.current_chapter = series_progress['last_read']
        st.rerun()

if __name__ == "__main__":
    main()
