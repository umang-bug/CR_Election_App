import streamlit as st

st.set_page_config(page_title="MECH CR Elections 2026", page_icon="⚙️", layout="wide")

# Custom CSS for a "Cool" look
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #003366; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚙️ Mechanical Engineering | Class of 2028")
st.header("Academic Year 2026-27 CR Elections")

st.info("Welcome to the official voting portal for the 3rd Year Class Representative.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Elections Rules")
    st.write("* Only emails containing **'2024ume'** are eligible.")
    st.write("* Voting is strictly anonymous.")
    st.write("* Each student has exactly **one vote**.")

with col2:
    st.subheader("Timeline")
    st.warning("Polls Close: Tonight at 11:59 PM")
    if st.button("View Candidates"):
        st.switch_page("pages/1_Candidates.py")
