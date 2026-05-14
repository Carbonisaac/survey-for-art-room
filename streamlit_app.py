import streamlit as st
import os
from shillelagh.backends.apsw.db import connect

st.title("Art Room Survey")

# Link to your sheet from secrets.toml
sheet_url = st.secrets["private_gsheets_url"]["url"]

# Create connection
conn = connect(
    ":memory:", 
    adapter_kwargs={
        "gsheetsapi": {
            "service_account_info": st.secrets["gcp_service_account"].to_dict()
        }
    }
)

# The Form questions
with st.form("survey_form"):
    year_level = st.selectbox("What year level are you?", ["10", "11", "12", "Staff Member"])

    # Question 1: Priorities
    priorities = st.multiselect(
        "Which of the following art supplies or equipment would you use most often? (Select at least 1)",
        ["Digital drawing tablets", "Wood burners", "Traditional painting", "3D/Pottery", "Textiles/Fashion", "Printmaking", "Photography", "Music creation"]
    )
    
    # Question 2: Atmosphere
    vibe = st.radio(
        "What kind of 'vibe' or atmosphere do you think would help you be most creative?",
        ["Collaborative (Open space)", "Focused (Quiet zones)", "Inspiring (Art-covered walls)", "Minimalist (Clean/High-tech)"]
    )
    
    # Question 3: Functional features
    feature = st.selectbox(
        "Aside from art supplies, what functional feature is most important to you?",
        ["Comfortable seating", "Adjustable lighting", "Better storage", "Resources"]
    )
    
    # Question 4: Open Suggestion
    dream_feature = st.text_input("If you could add one 'dream feature' to the art room, what would it be?")
    
    submit = st.form_submit_button("Submit Data")

# Handling the submission
if submit:
    # 1. Validation Check: Make sure no fields are empty
    if not year_level or not priorities or not vibe or not feature or not dream_feature:
        st.error("Please answer all questions before submitting!")
    
    else:
        # 2. If everything is filled out, run the database code
        try:
            cursor = conn.cursor()
            
            # Convert the list of priorities into one string
            priorities_str = ", ".join(priorities)
            
            # Your SQL query (Ensure your Google Sheet headers match these names exactly)
            query = f'INSERT INTO "{sheet_url}" (year, priorities, atmosphere, feature, dream) VALUES ("{year_level}", "{priorities_str}", "{vibe}", "{feature}", "{dream_feature}")'
            
            cursor.execute(query)
            st.success("Thank you! Your response has been recorded.")
        except Exception as e:
            st.error(f"An error occurred while saving: {e}")

