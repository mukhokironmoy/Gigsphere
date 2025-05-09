import streamlit as st
import pandas as pd
from auth_utils import get_connection

# Configure the page
st.set_page_config(page_title="GigSphere", layout="wide")

# Initialize session state variables if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'name' not in st.session_state:
    st.session_state.name = None

# Function to handle login
def login(email, password):
    # In a real application, you would hash the password and compare it with the stored hash
    # For simplicity, we're comparing plaintext passwords here
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT user_id, first_name, last_name, user_type, password_hash FROM users WHERE email = %s",
            (email,)
        )
        result = cursor.fetchone()
        
        if result and result[4] == password:  # Simple password check
            st.session_state.logged_in = True
            st.session_state.user_id = result[0]
            st.session_state.user_type = result[3]
            st.session_state.name = f"{result[1]} {result[2]}"
            return True
        return False
    except Exception as e:
        st.error(f"Database error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# Function to handle signup
def signup(first_name, last_name, email, password, user_type, additional_info=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Check if email already exists
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            st.error("Email already registered. Please use a different email.")
            return False
        
        # Use explicit transaction control instead of autocommit
        cursor.execute("BEGIN")
        
        # Insert into users table - Let PostgreSQL generate the user_id
        cursor.execute(
            """
            INSERT INTO users (first_name, last_name, email, password_hash, user_type)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING user_id
            """,
            (first_name, last_name, email, password, user_type)
        )
        user_id = cursor.fetchone()[0]
        
        # Insert into clients or freelancers table using the returned user_id
        if user_type == 'client':
            company_name = additional_info.get('company_name', '')
            business_type = additional_info.get('business_type', '')
            cursor.execute(
                "INSERT INTO clients (client_id, company_name, business_type) VALUES (%s, %s, %s)",
                (user_id, company_name, business_type)
            )
        elif user_type == 'freelancer':
            bio = additional_info.get('bio', '')
            hourly_rate = additional_info.get('hourly_rate', 0)
            experience = additional_info.get('experience', 0)
            cursor.execute(
                "INSERT INTO freelancers (freelancer_id, bio, hourly_rate, experience) VALUES (%s, %s, %s, %s)",
                (user_id, bio, hourly_rate, experience)
            )
        
        # Commit the transaction
        cursor.execute("COMMIT")
        return True
    except Exception as e:
        # Rollback the transaction
        cursor.execute("ROLLBACK")
        st.error(f"Error during signup: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def logout():
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_type = None
    st.session_state.name = None

# Main application UI
def main():
    st.title("GigSphere")
    
    # Display logout button if logged in
    if st.session_state.logged_in:
        st.sidebar.write(f"Logged in as: {st.session_state.name}")
        if st.sidebar.button("Logout"):
            logout()
            st.rerun()
    
    # Check login status
    if not st.session_state.logged_in:
        # Login and signup tabs
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:  # Login tab
            st.header("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login"):
                if login(email, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
        
        with tab2:  # Sign Up tab
            st.header("Sign Up")
            
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name", key="signup_first_name")
                email = st.text_input("Email", key="signup_email")
                user_type = st.selectbox("User Type", ["client", "freelancer"], key="signup_user_type")
            
            with col2:
                last_name = st.text_input("Last Name", key="signup_last_name")
                password = st.text_input("Password", type="password", key="signup_password")
            
            # Additional fields based on user type
            additional_info = {}
            
            if user_type == "client":
                col1, col2 = st.columns(2)
                with col1:
                    company_name = st.text_input("Company Name")
                    additional_info['company_name'] = company_name
                with col2:
                    business_type = st.text_input("Business Type")
                    additional_info['business_type'] = business_type
                    
            elif user_type == "freelancer":
                bio = st.text_area("Bio")
                col1, col2 = st.columns(2)
                with col1:
                    hourly_rate = st.number_input("Hourly Rate ($)", min_value=0.0, value=15.0, step=5.0)
                with col2:
                    experience = st.number_input("Years of Experience", min_value=0, value=1)
                additional_info = {
                    'bio': bio,
                    'hourly_rate': hourly_rate,
                    'experience': experience
                }
            
            if st.button("Sign Up"):
                if signup(first_name, last_name, email, password, user_type, additional_info):
                    st.success("Account created successfully! Please login.")
                else:
                    st.error("Error creating account. Please try again.")
    
    else:  # User is logged in
        # Redirect to the appropriate dashboard
        if st.session_state.user_type == "client":
            st.write("Welcome to your Client Dashboard!")
            # Display featured freelancers
            st.header("Featured Freelancers")
            display_featured_freelancers()
            
            # Recently posted projects
            st.header("Your Recent Projects")
            display_client_projects(st.session_state.user_id)
        
        elif st.session_state.user_type == "freelancer":
            st.write("Welcome to your Freelancer Dashboard!")
            # Display available projects
            st.header("Available Projects")
            display_available_projects()
            
            # Active contracts
            st.header("Your Active Contracts")
            display_freelancer_contracts(st.session_state.user_id)

# Helper functions to display data
def display_featured_freelancers():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT u.first_name, u.last_name, f.bio, f.hourly_rate, f.experience
            FROM users u
            JOIN freelancers f ON u.user_id = f.freelancer_id
            ORDER BY f.experience DESC
            LIMIT 5
        """)
        
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results, columns=['First Name', 'Last Name', 'Bio', 'Hourly Rate ($)', 'Experience (Years)'])
            st.dataframe(df)
        else:
            st.info("No freelancers found.")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def display_client_projects(client_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT title, description, budget, deadline, status, posted_at
            FROM projects
            WHERE client_id = %s
            ORDER BY posted_at DESC
            LIMIT 5
        """, (client_id,))
        
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results, columns=['Title', 'Description', 'Budget ($)', 'Deadline', 'Status', 'Posted At'])
            st.dataframe(df)
            
            if st.button("Post New Project"):
                st.session_state.show_new_project_form = True
            
            if st.session_state.get('show_new_project_form', False):
                st.subheader("Post a New Project")
                with st.form("new_project_form"):
                    project_title = st.text_input("Project Title")
                    project_desc = st.text_area("Project Description")
                    col1, col2 = st.columns(2)
                    with col1:
                        budget = st.number_input("Budget ($)", min_value=0.0, step=100.0)
                    with col2:
                        deadline = st.date_input("Deadline")
                    
                    if st.form_submit_button("Post Project"):
                        try:
                            cursor.execute("""
                                INSERT INTO projects (client_id, title, description, budget, deadline, status)
                                VALUES (%s, %s, %s, %s, %s, 'open')
                            """, (client_id, project_title, project_desc, budget, deadline))
                            conn.commit()
                            st.success("Project posted successfully!")
                            st.session_state.show_new_project_form = False
                            st.rerun()
                        except Exception as e:
                            conn.rollback()
                            st.error(f"Error posting project: {e}")
        else:
            st.info("You haven't posted any projects yet.")
            if st.button("Post Your First Project"):
                st.session_state.show_new_project_form = True
                st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def display_available_projects():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT p.project_id, p.title, p.description, p.budget, p.deadline, 
                   c.company_name, u.first_name, u.last_name
            FROM projects p
            JOIN clients c ON p.client_id = c.client_id
            JOIN users u ON c.client_id = u.user_id
            WHERE p.status = 'open'
            ORDER BY p.posted_at DESC
            LIMIT 10
        """)
        
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results, columns=['Project ID', 'Title', 'Description', 'Budget ($)', 
                                                'Deadline', 'Company', 'Client First Name', 'Client Last Name'])
            
            # Hide the Project ID column from display but keep it for reference
            display_df = df.drop(columns=['Project ID'])
            st.dataframe(display_df)
            
            # Allow submitting proposals
            selected_project = st.selectbox("Select a project to submit proposal", 
                                          options=list(range(len(df))),
                                          format_func=lambda x: df['Title'].iloc[x])
            
            if selected_project is not None:
                with st.form("proposal_form"):
                    st.subheader(f"Submit Proposal for: {df['Title'].iloc[selected_project]}")
                    proposal_text = st.text_area("Your Proposal")
                    bid_amount = st.number_input("Bid Amount ($)", min_value=0.0, step=50.0)
                    
                    if st.form_submit_button("Submit Proposal"):
                        try:
                            cursor.execute("""
                                INSERT INTO proposals (freelancer_id, project_id, proposal_text, bid_amount, status)
                                VALUES (%s, %s, %s, %s, 'approval pending')
                            """, (st.session_state.user_id, df['Project ID'].iloc[selected_project], 
                                  proposal_text, bid_amount))
                            conn.commit()
                            st.success("Proposal submitted successfully!")
                        except Exception as e:
                            conn.rollback()
                            st.error(f"Error submitting proposal: {e}")
        else:
            st.info("No open projects available at the moment.")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def display_freelancer_contracts(freelancer_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT c.contract_id, p.title, c.agreed_price, c.start_date, c.end_date, c.status,
                   u.first_name, u.last_name
            FROM contracts c
            JOIN projects p ON c.project_id = p.project_id
            JOIN clients cl ON c.client_id = cl.client_id
            JOIN users u ON cl.client_id = u.user_id
            WHERE c.freelancer_id = %s
            ORDER BY c.start_date DESC
        """, (freelancer_id,))
        
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results, columns=['Contract ID', 'Project Title', 'Agreed Price ($)', 
                                               'Start Date', 'End Date', 'Status', 
                                               'Client First Name', 'Client Last Name'])
            st.dataframe(df)
        else:
            st.info("You don't have any active contracts.")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()