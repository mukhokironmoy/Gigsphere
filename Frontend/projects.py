import streamlit as st
import pandas as pd
from auth_utils import get_connection

# Page configuration
st.set_page_config(page_title="Browse Projects", layout="wide")

# Check if user is logged in
if not st.session_state.get('logged_in', False):
    st.error("Please login to access this page")
    st.stop()

# Main projects page
st.title("Browse Projects")

# Create filters
st.sidebar.header("Filters")
status_filter = st.sidebar.multiselect(
    "Project Status",
    ["open", "in progress", "completed", "cancelled"],
    default=["open"]
)

min_budget = st.sidebar.number_input("Min Budget ($)", min_value=0, value=0, step=100)
max_budget = st.sidebar.number_input("Max Budget ($)", min_value=0, value=10000, step=100)

# Construct SQL query based on filters
query = """
    SELECT p.project_id, p.title, p.description, p.budget, p.deadline, 
           u.first_name, u.last_name, c.company_name, p.status, p.posted_at
    FROM projects p
    JOIN clients c ON p.client_id = c.client_id
    JOIN users u ON c.client_id = u.user_id
    WHERE p.status IN %s AND p.budget >= %s
"""

params = [tuple(status_filter), min_budget]

# Add max budget filter if it's not 0
if max_budget > 0:
    query += " AND p.budget <= %s"
    params.append(max_budget)

query += " ORDER BY p.posted_at DESC"

# Execute query and display results
conn = get_connection()
cursor = conn.cursor()
try:
    cursor.execute(query, params)
    results = cursor.fetchall()
    
    if results:
        df = pd.DataFrame(results, columns=['Project ID', 'Title', 'Description', 'Budget ($)', 
                                           'Deadline', 'Client First Name', 'Client Last Name', 
                                           'Company', 'Status', 'Posted At'])
        
        # Add a column that shows days until deadline
        df['Days to Deadline'] = (pd.to_datetime(df['Deadline']) - pd.Timestamp.now().normalize()).dt.days
        
        # Hide Project ID from display
        display_df = df.drop(columns=['Project ID'])
        
        st.dataframe(display_df)
        
        # If user is a freelancer, allow them to submit proposals
        if st.session_state.get('user_type') == 'freelancer':
            project_idx = st.selectbox("Select a project to submit proposal", 
                                      options=list(range(len(df))),
                                      format_func=lambda x: f"{df['Title'].iloc[x]} - ${df['Budget ($)'].iloc[x]}")
            
            if project_idx is not None:
                project_id = df['Project ID'].iloc[project_idx]
                
                # Check if already submitted a proposal for this project
                cursor.execute("""
                    SELECT COUNT(*) FROM proposals 
                    WHERE freelancer_id = %s AND project_id = %s
                """, (st.session_state.user_id, project_id))
                
                already_applied = cursor.fetchone()[0] > 0
                
                if already_applied:
                    st.warning("You have already submitted a proposal for this project.")
                elif df['Status'].iloc[project_idx] != 'open':
                    st.warning("This project is no longer accepting proposals.")
                else:
                    st.subheader(f"Submit Proposal for: {df['Title'].iloc[project_idx]}")
                    with st.form("proposal_form"):
                        proposal_text = st.text_area("Your Proposal")
                        bid_amount = st.number_input("Bid Amount ($)", 
                                                   min_value=0.0, 
                                                   max_value=float(df['Budget ($)'].iloc[project_idx]),
                                                   step=10.0)
                        
                        if st.form_submit_button("Submit Proposal"):
                            try:
                                cursor.execute("""
                                    INSERT INTO proposals (freelancer_id, project_id, proposal_text, bid_amount, status)
                                    VALUES (%s, %s, %s, %s, 'approval pending')
                                """, (st.session_state.user_id, project_id, proposal_text, bid_amount))
                                conn.commit()
                                st.success("Proposal submitted successfully!")
                            except Exception as e:
                                conn.rollback()
                                st.error(f"Error submitting proposal: {e}")
    else:
        st.info("No projects found matching your filters.")
except Exception as e:
    st.error(f"Error: {e}")
finally:
    cursor.close()
    conn.close()