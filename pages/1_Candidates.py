import streamlit as st

st.title("👥 Candidate Profiles")

# Candidate Data
candidates = [
    {"name": "Candidate A", "tagline": "Innovation & Unity", "bio": "Focusing on better lab equipment access.", "img": "https://via.placeholder.com/150"},
    {"name": "Candidate B", "tagline": "Transparency First", "bio": "Improving communication between faculty and students.", "img": "https://via.placeholder.com/150"},
    {"name": "Candidate C", "tagline": "Efficiency in Action", "bio": "Streamlining event approvals and attendance.", "img": "https://via.placeholder.com/150"}
]

cols = st.columns(len(candidates))

for i, person in enumerate(candidates):
    with cols[i]:
        st.image(person["img"], use_column_width=True)
        st.subheader(person["name"])
        st.caption(f"*{person['tagline']}*")
        with st.expander("View Manifesto"):
            st.write(person["bio"])