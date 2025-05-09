import streamlit as st
import pandas as pd
from auth_utils import get_connection

# Page configuration
st.set_page_config(page_title="My Profile", layout="wide")

# Check if user is logged in
if not st.session_state.get('logged_in', False):
    st.error("Please login to access this page")
    st.stop()

# Main profile page
st.title("My Profile")

# Get user data
conn = get_connection()
cursor = conn.cursor()
try:
    # Get basic user info
    cursor.execute("""
        SELECT first_name, last_name, email, user_type
        FROM users
        WHERE user_id = %s
    """, (st.session_state.user_id,))
    
    user_info = cursor.fetchone()
    if user_info:
        first_name, last_name, email, user_type = user_info
        
        # Display profile info
        col1, col2 = st.columns(2)
        with col1:
            st.header("Personal Information")
            st.write(f"**Name:** {first_name} {last_name}")
            st.write(f"**Email:** {email}")
            st.write(f"**Account Type:** {user_type.capitalize()}")
            
            # Edit profile button
            if st.button("Edit Profile"):
                st.session_state.show_edit_form = True
        
        # Display additional info based on user type
        with col2:
            if user_type == 'client':
                cursor.execute("""
                    SELECT company_name, business_type
                    FROM clients
                    WHERE client_id = %s
                """, (st.session_state.user_id,))
                
                client_info = cursor.fetchone()
                if client_info:
                    company_name, business_type = client_info
                    
                    st.header("Company Information")
                    st.write(f"**Company Name:** {company_name}")
                    st.write(f"**Business Type:** {business_type}")
            
            elif user_type == 'freelancer':
                cursor.execute("""
                    SELECT bio, portfolio, experience, hourly_rate
                    FROM freelancers
                    WHERE freelancer_id = %s
                """, (st.session_state.user_id,))
                
                freelancer_info = cursor.fetchone()
                if freelancer_info:
                    bio, portfolio, experience, hourly_rate = freelancer_info
                    
                    st.header("Professional Information")
                    st.write(f"**Bio:**")
                    st.write(bio if bio else "No bio provided.")
                    st.write(f"**Portfolio:** {portfolio if portfolio else 'Not provided'}")
                    st.write(f"**Experience:** {experience} years")
                    st.write(f"**Hourly Rate:** ${hourly_rate}/hour")
                    
                    # Get skills
                    cursor.execute("""
                        SELECT s.skill_name
                        FROM freelancer_skills fs
                        JOIN skills s ON fs.skill_id = s.skill_id
                        WHERE fs.freelancer_id = %s
                    """, (st.session_state.user_id,))
                    
                    skills = cursor.fetchall()
                    if skills:
                        st.write("**Skills:**")
                        for skill in skills:
                            st.write(f"- {skill[0]}")
                    
                    # Add skills section
                    st.subheader("Add Skills")
                    st.info("Skill management functionality coming soon!")
        
        # Edit profile form
        if st.session_state.get('show_edit_form', False):
            st.header("Edit Profile")
            
            with st.form("edit_profile_form"):
                new_first_name = st.text_input("First Name", value=first_name)
                new_last_name = st.text_input("Last Name", value=last_name)
                new_email = st.text_input("Email", value=email)
                
                # Additional fields based on user type
                if user_type == 'client':
                    cursor.execute("""
                        SELECT company_name, business_type
                        FROM clients
                        WHERE client_id = %s
                    """, (st.session_state.user_id,))
                    
                    client_info = cursor.fetchone()
                    if client_info:
                        company_name, business_type = client_info
                        
                        new_company_name = st.text_input("Company Name", value=company_name)
                        new_business_type = st.text_input("Business Type", value=business_type)
                
                elif user_type == 'freelancer':
                    cursor.execute("""
                        SELECT bio, portfolio, experience, hourly_rate
                        FROM freelancers
                        WHERE freelancer_id = %s
                    """, (st.session_state.user_id,))
                    
                    freelancer_info = cursor.fetchone()
                    if freelancer_info:
                        bio, portfolio, experience, hourly_rate = freelancer_info
                        
                        new_bio = st.text_area("Bio", value=bio if bio else "")
                        new_portfolio = st.text_input("Portfolio URL", value=portfolio if portfolio else "")
                        new_experience = st.number_input("Years of Experience", min_value=0, value=experience)
                        new_hourly_rate = st.number_input("Hourly Rate ($)", min_value=0.0, value=hourly_rate, step=5.0)
                
                if st.form_submit_button("Save Changes"):
                    try:
                        # Update users table
                        cursor.execute("""
                            UPDATE users
                            SET first_name = %s, last_name = %s, email = %s
                            WHERE user_id = %s
                        """, (new_first_name, new_last_name, new_email, st.session_state.user_id))
                        
                        # Update user-specific table
                        if user_type == 'client':
                            cursor.execute("""
                                UPDATE clients
                                SET company_name = %s, business_type = %s
                                WHERE client_id = %s
                            """, (new_company_name, new_business_type, st.session_state.user_id))
                        
                        elif user_type == 'freelancer':
                            cursor.execute("""
                                UPDATE freelancers
                                SET bio = %s, portfolio = %s, experience = %s, hourly_rate = %s
                                WHERE freelancer_id = %s
                            """, (new_bio, new_portfolio, new_experience, new_hourly_rate, st.session_state.user_id))
                        
                        conn.commit()
                        st.success("Profile updated successfully!")
                        
                        # Update session state name
                        st.session_state.name = f"{new_first_name} {new_last_name}"
                        
                        # Hide the form
                        st.session_state.show_edit_form = False
                        st.rerun()
                    except Exception as e:
                        conn.rollback()
                        st.error(f"Error updating profile: {e}")
    
    # Show reviews section
    st.header("Reviews")
    cursor.execute("""
        SELECT u.first_name, u.last_name, r.rating, r.review_text, r.review_date
        FROM reviews r
        JOIN users u ON r.reviewer_id = u.user_id
        WHERE r.reviewee_id = %s
        ORDER BY r.review_date DESC
    """, (st.session_state.user_id,))
    
    reviews = cursor.fetchall()
    if reviews:
        for review in reviews:
            reviewer_name, reviewer_last, rating, review_text, review_date = review
            
            st.write(f"**{reviewer_name} {reviewer_last}** - {rating}/5 stars")
            st.write(f"*{review_date}*")
            st.write(review_text)
            st.write("---")
    else:
        st.info("No reviews yet.")

except Exception as e:
    st.error(f"Error: {e}")
finally:
    cursor.close()
    conn.close()