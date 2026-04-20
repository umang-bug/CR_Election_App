import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("🗳️ Cast Your Vote")

# Initialize Google Sheets Connection
# Ensure you set up your secrets.toml with your sheet URL
conn = st.connection("gsheets", type=GSheetsConnection)

email = st.text_input("Enter your College Email ID", placeholder="e.g. 2024ume001@mnit.ac.in")

if email:
    # 1. Validation Logic
    is_valid = "2024ume" in email.lower() or email == "admin@mnit.ac.in"
    
    if not is_valid:
        st.error("Access Denied: This portal is only for 2024 Mechanical batch students.")
    else:
        # 2. Check for double voting (Fetch existing data from Google Sheets)
        existing_data = conn.read(worksheet="Votes")
        if email in existing_data["Email"].values:
            st.warning("You have already cast your vote! Duplicate entries are not allowed.")
        else:
            st.success("Identity Verified. Select your candidate:")
            
            # 3. The Ballot
            selection = st.radio("Select Candidate", ["Candidate A", "Candidate B", "Candidate C"])
            
            if st.button("Confirm Vote"):
                # Append to Google Sheets
                new_vote = pd.DataFrame([{"Email": email, "Vote": selection}])
                updated_df = pd.concat([existing_data, new_vote], ignore_index=True)
                conn.update(worksheet="Votes", data=updated_df)
                
                st.balloons()
                st.success(f"Thank you! Your vote for {selection} has been recorded anonymously.")