import streamlit as st
from pages import word_search_page, other_tool  # import pages

# Sidebar navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose a tool:", ["Word Search", "Other Tool"])

# Launch the selected page
if app_mode == "Word Search":
    word_search_page.app()
elif app_mode == "Other Tool":
    other_tool.app()
