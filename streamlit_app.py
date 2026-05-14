import streamlit as st
from shillelagh.backends.apsw.db import connect

st.title("Art Room Survey")

# Link to your sheet from secrets.toml
sheet_url = st.secrets["private_gsheets_url"]["url"]

# Create connection
# We add .to_dict() to the end of the service account info
conn = connect(":memory:", adapter_kwargs={
    "gsheetsapi": {
        "service_account_info": st.secrets["gcp_service_account"].to_dict()
    }
})

# The Form questions
with st.form("survey_form"):
    year_level = st.selectbox("What year level are you?", ["10", "11", "12", "Staff Member"])

    # Question 1: Priorities (Multiselect is better here since they pick 3)
    priorities = st.multiselect(
        "Which of the following art supplies or equipment would you use most often? (Select up to 3)",
        ["Digital drawing tablets", "Traditional painting", "3D/Pottery", "Textiles/Fashion", "Printmaking", "Photography", "Music creation"]
    )
    
    # Question 2: Atmosphere
    vibe = st.radio(
        "What kind of 'vibe' or atmosphere do you think would help you be most creative?",
        ["Collaborative (Open space)", "Focused (Quiet zones)", "Inspiring (Art-covered walls)", "Minimalist (Clean/High-tech)"]
    )
    
    # Question 3: Functional features
    feature = st.selectbox(
        "Aside from art supplies, what functional feature is most important to you?",
        ["Comfortable seating", "Adjustable lighting", "Better storage/lockers", "Resource Library"]
    )
    
    # Question 4: Open Suggestion
    dream_feature = st.text_input("If you could add one 'dream feature' to the art room, what would it be?")
    
    submit = st.form_submit_button("Submit Data")

if submit:
    # ... (your form inputs are above here) ...

if submit:
    # 1. Validation Check: Make sure no fields are empty
    if not year_level or not priorities or not vibe or not feature or not dream_feature:
        st.error("Please answer all questions before submitting!")
    
    else:
        # 2. If everything is filled out, run the database code
        cursor = conn.cursor()
        
        # Convert the list of priorities into one string
        priorities_str = ", ".join(priorities)
        
        # Your SQL query
        query = f"INSERT INTO '{sheet_url}' (year, priorities, atmosphere, feature, dream) VALUES ('{year_level}', '{priorities_str}', '{vibe}', '{feature}', '{dream_feature}')"
        
        cursor.execute(query)
        st.success("Thank you! Your response has been recorded.")
    cursor = conn.cursor()
    # Convert list to string for SQL storage
    priorities_str = ", ".join(priorities)
    
    # Updated query to match your new variables
    query = f"INSERT INTO '{sheet_url}' (year, priorities, atmosphere, feature, dream) VALUES ('{year_level}', '{priorities_str}', '{vibe}', '{feature}', '{dream_feature}')"

    cursor.execute(query)
    st.success("Thank you for completing this survey!")
