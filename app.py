import streamlit as st

st.title("Word Search Solver")

st.write("Upload or type a list of words and analyze them here.")

uploaded_file = st.file_uploader("Upload your dictionary (.txt)", type=["txt"])

if uploaded_file:
    words = [line.strip() for line in uploaded_file.readlines()]
    st.write(f"Loaded {len(words)} words.")
    st.write(sorted(words)[:20])  # Show a preview of the first 20 words
else:
    st.info("Upload a .txt file containing one word per line.")
