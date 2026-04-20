import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("📊 Election Statistics")

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Votes")

total_students = 120  # Total strength of M1 batch
votes_cast = len(df)
turnout = (votes_cast / total_students) * 100

st.metric("Total Votes Cast", votes_cast)
st.progress(votes_cast / total_students)
st.write(f"Voter Turnout: **{turnout:.1f}%**")

# Display a fun chart of voting times or just turnout
# (Don't show the 'Vote' column results to keep the lead secret!)