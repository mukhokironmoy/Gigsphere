import streamlit as st
import pandas as pd
from auth_utils import get_connection

# Page configuration
st.set_page_config(page_title="Client Dashboard", layout="wide")

# Check if user is logged in and is a client
if not st.session_state.get('logged_in', False) or st.session_state.get('user_type', '') != 'client':
    st.error("Please login as a client to access this page")
    st.stop()

# Main client dashboard
st.title("Client Dashboard")
st.write(f"Welcome back, {st.session_state.name}!")

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Projects", "Proposals", "Contracts", "Invoices"])

# Projects Tab
with tab1:
    st.header("Your Projects")
    
    # Add new project button
    if st.button("+ Post New Project"):
        st.session_state.show_project_form = True
    
    # New project form
    if st.session_state.get('show_project_form', False):
        st.subheader("Post a New Project")
        with st.form("project_form"):
            project_title = st.text_input("Project Title")
            project_desc = st.text_area("Project Description")
            col1, col2 = st.columns(2)
            with col1:
                budget = st.number_input("Budget ($)", min_value=0.0, step=100.0)
            with col2:
                deadline = st.date_input("Deadline")
            
            if st.form_submit_button("Post Project"):
                conn = get_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO projects (client_id, title, description, budget, deadline, status)
                        VALUES (%s, %s, %s, %s, %s, 'open')
                    """, (st.session_state.user_id, project_title, project_desc, budget, deadline))
                    conn.commit()
                    st.success("Project posted successfully!")
                    st.session_state.show_project_form = False
                except Exception as e:
                    conn.rollback()
                    st.error(f"Error posting project: {e}")
                finally:
                    cursor.close()
                    conn.close()
    
    # Display existing projects
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT project_id, title, description, budget, deadline, status, posted_at
            FROM projects
            WHERE client_id = %s
            ORDER BY posted_at DESC
        """, (st.session_state.user_id,))
        
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results, columns=['Project ID', 'Title', 'Description', 'Budget ($)', 
                                               'Deadline', 'Status', 'Posted At'])
            st.dataframe(df)
            
            # Allow selecting a project to view details or update
            project_ids = df['Project ID'].tolist()
            project_titles = df['Title'].tolist()
            project_options = [f"{id} - {title}" for id, title in zip(project_ids, project_titles)]
            
            selected_project = st.selectbox("Select a project to manage", options=project_options)
            
            if selected_project:
                selected_id = selected_project.split(" - ")[0]
                st.subheader(f"Managing Project: {selected_project.split(' - ', 1)[1]}")
                
                # Create management options
                option = st.radio("Choose action:", ["View Proposals", "Update Status"])
                
                if option == "View Proposals":
                    # Fetch proposals for this project
                    cursor.execute("""
                        SELECT p.proposal_id, u.first_name, u.last_name, p.proposal_text, 
                               p.bid_amount, p.submitted_at, p.status, f.freelancer_id
                        FROM proposals p
                        JOIN freelancers f ON p.freelancer_id = f.freelancer_id
                        JOIN users u ON f.freelancer_id = u.user_id
                        WHERE p.project_id = %s
                    """, (selected_id,))
                    
                    proposals = cursor.fetchall()
                    if proposals:
                        prop_df = pd.DataFrame(proposals, columns=['Proposal ID', 'First Name', 'Last Name', 
                                                                'Proposal Text', 'Bid Amount ($)', 
                                                                'Submitted At', 'Status', 'Freelancer ID'])
                        
                        # Hide Freelancer ID from display
                        display_prop_df = prop_df.drop(columns=['Freelancer ID'])
                        st.dataframe(display_prop_df)
                        
                        # Allow accepting a proposal
                        proposal_idx = st.selectbox("Select proposal to accept:", 
                                                  options=list(range(len(prop_df))),
                                                  format_func=lambda x: f"{prop_df['First Name'].iloc[x]} {prop_df['Last Name'].iloc[x]} - ${prop_df['Bid Amount ($)'].iloc[x]}")
                        
                        if st.button("Accept Proposal"):
                            proposal_id = prop_df['Proposal ID'].iloc[proposal_idx]
                            freelancer_id = prop_df['Freelancer ID'].iloc[proposal_idx]
                            bid_amount = prop_df['Bid Amount ($)'].iloc[proposal_idx]
                            
                            # Update proposal status
                            cursor.execute("UPDATE proposals SET status = 'accepted' WHERE proposal_id = %s", 
                                           (proposal_id,))
                            
                            # Mark other proposals as rejected
                            cursor.execute("""
                                UPDATE proposals 
                                SET status = 'rejected' 
                                WHERE project_id = %s AND proposal_id != %s
                            """, (selected_id, proposal_id))
                            
                            # Create a contract
                            cursor.execute("""
                                INSERT INTO contracts 
                                (client_id, freelancer_id, project_id, proposal_id, agreed_price, start_date, status)
                                VALUES (%s, %s, %s, %s, %s, CURRENT_DATE, 'active')
                            """, (st.session_state.user_id, freelancer_id, selected_id, proposal_id, bid_amount))
                            
                            # Update project status
                            cursor.execute("UPDATE projects SET status = 'in progress' WHERE project_id = %s", 
                                           (selected_id,))
                            
                            conn.commit()
                            st.success("Proposal accepted and contract created!")
                            st.rerun()
                    else:
                        st.info("No proposals received for this project yet.")
                
                elif option == "Update Status":
                    new_status = st.selectbox("Select new status:", 
                                             options=["open", "in progress", "completed", "cancelled"])
                    
                    if st.button("Update Status"):
                        cursor.execute("UPDATE projects SET status = %s WHERE project_id = %s", 
                                      (new_status, selected_id))
                        conn.commit()
                        st.success(f"Project status updated to {new_status}")
                        st.rerun()
        else:
            st.info("You haven't posted any projects yet.")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Proposals Tab
with tab2:
    st.header("Received Proposals")
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT p.proposal_id, pr.title, u.first_name, u.last_name, 
                   p.proposal_text, p.bid_amount, p.submitted_at, p.status
            FROM proposals p
            JOIN projects pr ON p.project_id = pr.project_id
            JOIN freelancers f ON p.freelancer_id = f.freelancer_id
            JOIN users u ON f.freelancer_id = u.user_id
            WHERE pr.client_id = %s
            ORDER BY p.submitted_at DESC
        """, (st.session_state.user_id,))
        
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results, columns=['Proposal ID', 'Project Title', 'First Name', 'Last Name', 
                                               'Proposal Text', 'Bid Amount ($)', 'Submitted At', 'Status'])
            st.dataframe(df)
        else:
            st.info("You haven't received any proposals yet.")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Contracts Tab
with tab3:
    st.header("Your Contracts")
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT c.contract_id, p.title, u.first_name, u.last_name, 
                   c.agreed_price, c.start_date, c.end_date, c.status
            FROM contracts c
            JOIN projects p ON c.project_id = p.project_id
            JOIN freelancers f ON c.freelancer_id = f.freelancer_id
            JOIN users u ON f.freelancer_id = u.user_id
            WHERE c.client_id = %s
            ORDER BY c.start_date DESC
        """, (st.session_state.user_id,))
        
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results, columns=['Contract ID', 'Project Title', 'Freelancer First Name', 
                                               'Freelancer Last Name', 'Agreed Price ($)', 
                                               'Start Date', 'End Date', 'Status'])
            st.dataframe(df)
            
            # Allow selecting a contract to manage
            contract_idx = st.selectbox("Select contract to manage:", 
                                      options=list(range(len(df))),
                                      format_func=lambda x: f"{df['Project Title'].iloc[x]} - {df['Freelancer First Name'].iloc[x]} {df['Freelancer Last Name'].iloc[x]}")
            
            if contract_idx is not None:
                contract_id = df['Contract ID'].iloc[contract_idx]
                
                # Show submissions for this contract
                st.subheader("Submissions")
                cursor.execute("""
                    SELECT s.submission_id, s.description, s.submitted_at, s.approved
                    FROM submissions s
                    WHERE s.contract_id = %s
                    ORDER BY s.submitted_at DESC
                """, (contract_id,))
                
                submissions = cursor.fetchall()
                if submissions:
                    sub_df = pd.DataFrame(submissions, columns=['Submission ID', 'Description', 
                                                              'Submitted At', 'Approved'])
                    st.dataframe(sub_df)
                    
                    # Allow approving a submission
                    sub_idx = st.selectbox("Select submission to review:", 
                                         options=list(range(len(sub_df))),
                                         format_func=lambda x: f"{sub_df['Description'].iloc[x][:30]}... ({sub_df['Submitted At'].iloc[x]})")
                    
                    if sub_idx is not None:
                        submission_id = sub_df['Submission ID'].iloc[sub_idx]
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Approve Submission"):
                                # Add client remarks
                                remarks = st.text_area("Add remarks (optional):")
                                
                                cursor.execute("""
                                    UPDATE submissions 
                                    SET approved = TRUE, client_remarks = %s
                                    WHERE submission_id = %s
                                """, (remarks, submission_id))
                                conn.commit()
                                st.success("Submission approved!")
                        
                        with col2:
                            if st.button("Request Changes") and not sub_df['Approved'].iloc[sub_idx]:
                                remarks = st.text_area("Provide feedback:")
                                
                                cursor.execute("""
                                    UPDATE submissions 
                                    SET client_remarks = %s
                                    WHERE submission_id = %s
                                """, (remarks, submission_id))
                                conn.commit()
                                st.success("Feedback submitted!")
                else:
                    st.info("No submissions for this contract yet.")
                
                # Add option to mark contract as completed
                if df['Status'].iloc[contract_idx] == 'active':
                    if st.button("Mark Contract as Completed"):
                        cursor.execute("""
                            UPDATE contracts 
                            SET status = 'completed', end_date = CURRENT_DATE
                            WHERE contract_id = %s
                        """, (contract_id,))
                        
                        # Also update the project status
                        cursor.execute("""
                            UPDATE projects
                            SET status = 'completed'
                            WHERE project_id = (SELECT project_id FROM contracts WHERE contract_id = %s)
                        """, (contract_id,))
                        
                        conn.commit()
                        st.success("Contract marked as completed!")
                        st.rerun()
        else:
            st.info("You don't have any contracts yet.")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Invoices Tab
with tab4:
    st.header("Your Invoices")
    st.info("💡 Invoicing functionality coming soon!")