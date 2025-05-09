import streamlit as st
import pandas as pd
from auth_utils import get_connection

# Page configuration
st.set_page_config(page_title="Freelancer Dashboard", layout="wide")

# Check if user is logged in and is a freelancer
if not st.session_state.get('logged_in', False) or st.session_state.get('user_type', '') != 'freelancer':
    st.error("Please login as a freelancer to access this page")
    st.stop()

# Main freelancer dashboard
st.title("Freelancer Dashboard")
st.write(f"Welcome back, {st.session_state.name}!")

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Available Projects", "My Proposals", "Active Contracts", "Submissions"])

# Available Projects Tab
with tab1:
    st.header("Browse Available Projects")
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT p.project_id, p.title, p.description, p.budget, p.deadline, 
                   u.first_name, u.last_name, c.company_name, p.status, p.posted_at
            FROM projects p
            JOIN clients c ON p.client_id = c.client_id
            JOIN users u ON c.client_id = u.user_id
            WHERE p.status = 'open'
            ORDER BY p.posted_at DESC
        """)
        
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results, columns=['Project ID', 'Title', 'Description', 'Budget ($)', 
                                               'Deadline', 'Client First Name', 'Client Last Name', 
                                               'Company', 'Status', 'Posted At'])
            
            # Hide Project ID column from display but keep it for reference
            display_df = df.drop(columns=['Project ID'])
            st.dataframe(display_df)
            
            # Allow submitting proposals
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
                                    VALUES (%s, %s, %s, %s, 'pending')
                                """, (st.session_state.user_id, project_id, proposal_text, bid_amount))
                                conn.commit()
                                st.success("Proposal submitted successfully!")
                                st.rerun()
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

# My Proposals Tab
with tab2:
    st.header("My Submitted Proposals")
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT p.proposal_id, p.proposal_text, p.bid_amount, p.status, p.submitted_at,
                   proj.title, proj.budget, proj.deadline, c.company_name
            FROM proposals p
            JOIN projects proj ON p.project_id = proj.project_id
            JOIN clients c ON proj.client_id = c.client_id
            WHERE p.freelancer_id = %s
            ORDER BY p.submitted_at DESC
        """, (st.session_state.user_id,))
        
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results, columns=['Proposal ID', 'Proposal Text', 'Bid Amount ($)', 
                                               'Status', 'Submitted At', 'Project Title', 
                                               'Project Budget ($)', 'Deadline', 'Company'])
            
            # Format the dataframe for better display
            display_df = df[['Project Title', 'Company', 'Bid Amount ($)', 
                            'Project Budget ($)', 'Status', 'Submitted At']]
            st.dataframe(display_df)
            
            # Allow viewing full proposal details
            proposal_idx = st.selectbox("Select a proposal to view details", 
                                      options=list(range(len(df))),
                                      format_func=lambda x: f"{df['Project Title'].iloc[x]} - {df['Status'].iloc[x]}")
            
            if proposal_idx is not None:
                st.subheader(f"Proposal Details: {df['Project Title'].iloc[proposal_idx]}")
                st.write(f"**Status:** {df['Status'].iloc[proposal_idx]}")
                st.write(f"**Bid Amount:** ${df['Bid Amount ($)'].iloc[proposal_idx]}")
                st.write(f"**Submitted At:** {df['Submitted At'].iloc[proposal_idx]}")
                st.write("**Proposal Text:**")
                st.write(df['Proposal Text'].iloc[proposal_idx])
                
                # Allow withdrawing proposals that are still pending
                if df['Status'].iloc[proposal_idx].lower() == 'pending':
                    if st.button("Withdraw Proposal"):
                        try:
                            cursor.execute("""
                                UPDATE proposals
                                SET status = 'withdrawn'
                                WHERE proposal_id = %s
                            """, (df['Proposal ID'].iloc[proposal_idx],))
                            conn.commit()
                            st.success("Proposal withdrawn successfully!")
                            st.rerun()
                        except Exception as e:
                            conn.rollback()
                            st.error(f"Error withdrawing proposal: {e}")
        else:
            st.info("You haven't submitted any proposals yet.")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Active Contracts Tab
with tab3:
    st.header("Active Contracts")
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT c.contract_id, c.start_date, c.end_date, c.payment_amount, c.status,
                   p.title as project_title, cl.company_name
            FROM contracts c
            JOIN projects p ON c.project_id = p.project_id
            JOIN clients cl ON p.client_id = cl.client_id
            WHERE c.freelancer_id = %s AND c.status = 'active'
            ORDER BY c.start_date DESC
        """, (st.session_state.user_id,))
        
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results, columns=['Contract ID', 'Start Date', 'End Date', 
                                               'Payment Amount ($)', 'Status', 'Project Title', 'Company'])
            
            # Display active contracts
            display_df = df[['Project Title', 'Company', 'Payment Amount ($)', 'Start Date', 'End Date']]
            st.dataframe(display_df)
            
            # Show details for selected contract
            contract_idx = st.selectbox("Select a contract to view details", 
                                     options=list(range(len(df))),
                                     format_func=lambda x: f"{df['Project Title'].iloc[x]} - {df['Company'].iloc[x]}")
            
            if contract_idx is not None:
                contract_id = df['Contract ID'].iloc[contract_idx]
                st.subheader(f"Contract Details: {df['Project Title'].iloc[contract_idx]}")
                st.write(f"**Company:** {df['Company'].iloc[contract_idx]}")
                st.write(f"**Payment:** ${df['Payment Amount ($)'].iloc[contract_idx]}")
                st.write(f"**Start Date:** {df['Start Date'].iloc[contract_idx]}")
                st.write(f"**End Date:** {df['End Date'].iloc[contract_idx]}")
                
                # Get milestones for this contract
                cursor.execute("""
                    SELECT milestone_id, title, description, due_date, amount, status
                    FROM milestones
                    WHERE contract_id = %s
                    ORDER BY due_date
                """, (contract_id,))
                
                milestones = cursor.fetchall()
                if milestones:
                    st.subheader("Milestones")
                    milestone_df = pd.DataFrame(milestones, 
                                             columns=['Milestone ID', 'Title', 'Description', 
                                                     'Due Date', 'Amount ($)', 'Status'])
                    st.dataframe(milestone_df[['Title', 'Due Date', 'Amount ($)', 'Status']])
                else:
                    st.info("No milestones defined for this contract.")
        else:
            st.info("You don't have any active contracts at the moment.")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Submissions Tab
with tab4:
    st.header("Project Submissions")
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Get contracts that need submissions
        cursor.execute("""
            SELECT c.contract_id, p.title as project_title, c.end_date, 
                   cl.company_name, m.milestone_id, m.title as milestone_title
            FROM contracts c
            JOIN projects p ON c.project_id = p.project_id
            JOIN clients cl ON p.client_id = cl.client_id
            LEFT JOIN milestones m ON c.contract_id = m.contract_id AND m.status = 'in progress'
            WHERE c.freelancer_id = %s AND c.status = 'active'
            ORDER BY m.due_date, c.end_date
        """, (st.session_state.user_id,))
        
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results, columns=['Contract ID', 'Project Title', 'End Date', 
                                               'Company', 'Milestone ID', 'Milestone Title'])
            
            # Format the selection options
            display_options = []
            for i in range(len(df)):
                if pd.notna(df['Milestone ID'].iloc[i]):
                    display_options.append(f"{df['Project Title'].iloc[i]} - {df['Milestone Title'].iloc[i]}")
                else:
                    display_options.append(f"{df['Project Title'].iloc[i]} - Final Submission")
            
            submission_idx = st.selectbox("Select a project or milestone to submit work", 
                                       options=list(range(len(df))),
                                       format_func=lambda x: display_options[x])
            
            if submission_idx is not None:
                is_milestone = pd.notna(df['Milestone ID'].iloc[submission_idx])
                
                submission_type = "Milestone" if is_milestone else "Project"
                submission_title = (df['Milestone Title'].iloc[submission_idx] if is_milestone 
                                  else df['Project Title'].iloc[submission_idx])
                
                st.subheader(f"Submit {submission_type}: {submission_title}")
                
                with st.form("submission_form"):
                    title = st.text_input("Submission Title")
                    description = st.text_area("Description")
                    file_upload = st.file_uploader("Upload Files", accept_multiple_files=True)
                    notes = st.text_area("Additional Notes for Client")
                    
                    if st.form_submit_button("Submit Work"):
                        try:
                            # Start a transaction
                            conn.autocommit = False
                            
                            # Insert submission record
                            cursor.execute("""
                                INSERT INTO submissions (contract_id, milestone_id, title, description, notes, status)
                                VALUES (%s, %s, %s, %s, %s, 'pending review')
                                RETURNING submission_id
                            """, (
                                df['Contract ID'].iloc[submission_idx], 
                                df['Milestone ID'].iloc[submission_idx] if is_milestone else None,
                                title, description, notes
                            ))
                            
                            submission_id = cursor.fetchone()[0]
                            
                            # Handle file uploads if present
                            if file_upload:
                                for file in file_upload:
                                    # Save file to storage (placeholder - implement your file storage logic)
                                    file_path = f"uploads/{submission_id}_{file.name}"
                                    
                                    # Record file in database
                                    cursor.execute("""
                                        INSERT INTO submission_files (submission_id, file_name, file_path)
                                        VALUES (%s, %s, %s)
                                    """, (submission_id, file.name, file_path))
                            
                            # Update milestone status if this is a milestone submission
                            if is_milestone:
                                cursor.execute("""
                                    UPDATE milestones
                                    SET status = 'submitted'
                                    WHERE milestone_id = %s
                                """, (df['Milestone ID'].iloc[submission_idx],))
                            
                            conn.commit()
                            st.success("Work submitted successfully!")
                            st.rerun()
                        except Exception as e:
                            conn.rollback()
                            st.error(f"Error submitting work: {e}")
                        finally:
                            conn.autocommit = True
        else:
            st.info("You don't have any active projects requiring submissions.")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()