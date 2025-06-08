import streamlit as st
import os
from PIL import Image
import streamlit as st
from extractor import Extractor
from resume_summarizer import ResumeSummarizer
from resume_classifier import ResumeClassifier
import json
import os
import sqlite3
from datetime import datetime
import pandas as pd
from PIL import Image
import base64
import io
from config import *
import time
import pdf2image
import pdfplumber
import re
from storage import ResumeStorage
import tempfile

# Page config
st.set_page_config(
    page_title="Resume Skill Extractor",
    page_icon="📄",
    layout="wide"
)



# Initialize resume classifier and summarizer
classifier = ResumeClassifier()
summarizer = ResumeSummarizer()

# Add custom CSS for styling
# Custom CSS styling
st.markdown("""
<style>
    .stFileUploader {
        margin-bottom: 20px;
    }
    .stButton {
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

def check_auth():
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
        st.session_state['username'] = None
    
    if not st.session_state['authenticated']:
        return False
    return True

def login():
    """Login page"""
    st.title("🔒 Login")
    st.write("Please enter your credentials to access the application")
    
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("Username:")
    with col2:
        password = st.text_input("Password:", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "password":
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.success("Login successful!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Invalid credentials")

def logout():
    """Logout and clear session"""
    st.session_state['authenticated'] = False
    st.session_state['username'] = None
    st.success("Logged out successfully!")
    time.sleep(1)
    st.rerun()

def main():
    
    # Check authentication
    if not check_auth():
        login()
        return
    
    # Add logout button in sidebar
    st.sidebar.title("Welcome, HR")
    if st.sidebar.button("Logout", key="logout_btn"):
        logout()
        return
    st.sidebar.markdown("---")
    
    
    # Initialize extractor
    extractor = Extractor()

    # Initialize storage
    storage = ResumeStorage()

    # Sidebar with app info
    with st.sidebar:
        # Sidebar header
        st.sidebar.title("📄 Resume Skill Extractor")
        st.sidebar.write("Extract technical skills and contact information from PDF resumes")

        # About the App
        st.sidebar.header("About the App")
        st.sidebar.write("""
        This application helps extract technical skills and contact information from PDF resumes. 
        It uses advanced NLP techniques to identify and categorize skills, making it easier for 
        recruiters and hiring managers to quickly evaluate candidates.
        
        🚀 Built in just **9 hours of coding with AI assistance** and **15 hours of research and documentation**!
        """)

        # Features
        st.sidebar.header("Features")
        st.sidebar.markdown("""
        - PDF Resume Upload
        - Technical Skill Extraction
        - Contact Information Extraction
        - Persistent Storage
        - Search and Sort Functionality
        - Remarks System
        - Delete Functionality
        """)

        # Technical Details
        st.sidebar.header("Technical Details")
        st.sidebar.markdown("""
        **Backend:** Python with spaCy and NLTK for NLP
        
        **Frontend:** Streamlit for interactive web interface
        
        **Storage:** SQLite database for persistent storage
        """)

        st.sidebar.markdown("""---""")

        # Developer Information
        st.sidebar.header("Developer Information")
        
        # Developer Card
        st.sidebar.markdown("""
        <div style='background-color: #f0f4f8; padding: 20px; border-radius: 10px; margin: 15px 0; border: 1px solid #e0e5ec;'>
            <h3 style='color: #2c3e50; font-weight: 700;'>Developer Profile</h3>
            <div style='display: flex; flex-direction: column; gap: 15px;'>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <span style='font-weight: bold; color: #2c3e50;'>Name:</span>
                    <span style='color: #333;'>K R Vikram</span>
                </div>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <span style='font-weight: bold; color: #2c3e50;'>Email:</span>
                    <span style='color: #333;'>vikram.nitpy@gmail.com</span>
                </div>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <span style='font-weight: bold; color: #2c3e50;'>Phone:</span>
                    <span style='color: #333;'>+91 8309365005</span>
                </div>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <span style='font-weight: bold; color: #2c3e50;'>College:</span>
                    <span style='color: #333;'>NIT Puducherry</span>
                </div>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <img src='https://img.icons8.com/?size=100&id=1349&format=png&color=000000' alt='Portfolio' style='width: 20px; height: 20px;'>
                    <a href='https://krvikram.netlify.app/' target='_blank' style='text-decoration: none; color: #333;'>Portfolio</a>
                </div>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <img src='https://img.icons8.com/ios-filled/30/000000/github.png' alt='GitHub' style='width: 20px; height: 20px;'>
                    <a href='https://github.com/vikram-vikky2002' target='_blank' style='text-decoration: none; color: #333;'>GitHub</a>
                </div>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <img src='https://img.icons8.com/ios-filled/30/000000/linkedin.png' alt='LinkedIn' style='width: 20px; height: 20px;'>
                    <a href='https://www.linkedin.com/in/vikramkr2002' target='_blank' style='text-decoration: none; color: #333;'>LinkedIn</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # AI Assistant
        st.sidebar.markdown("""
        <div style='background-color: #f0f4f8; padding: 20px; border-radius: 10px; margin: 15px 0; border: 1px solid #e0e5ec;'>
            <h3 style='color: #2c3e50; font-weight: 700;'>AI Assistant</h3>
            <div style='display: flex; flex-direction: column; gap: 10px;'>
                <span style='color: #333;'>Cascade (Windsurf AI)</span>
                <div style='margin-top: 10px;'>
                    <span style='font-size: 0.9em; color: #333;'>This application was developed with the assistance of Cascade, an AI coding assistant from Windsurf. The AI helped with:</span>
                    <ul style='margin-top: 10px; color: #333;'>
                        <li>Designing the UI/UX</li>
                        <li>Implementing skill extraction logic</li>
                        <li>Adding search and filter functionality</li>
                        <li>Creating the storage system</li>
                        <li>Improving error handling</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        

    # Main content
    st.title("📄 Resume Skill Extractor")
    st.write("Upload a PDF resume to extract technical skills and contact information.")

    # File upload section
    uploaded_file = st.file_uploader(
        "Upload PDF Resume",
        type=["pdf"],
        help="Upload a PDF resume file"
    )

    # Process uploaded file if exists
    if uploaded_file is not None:
        # Save uploaded file to temp location
        tmp_file_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
        with open(tmp_file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        # Extract and display data
        if st.button("Extract Skills", key="extract_button"):
            try:
                # Extract data using our extractor
                result = extractor.extract_resume_data(tmp_file_path)
                
                if result:
                    # Show success message
                    st.success("Skills extracted successfully!")
                    
                    # Generate summary and classify resume
                    summary = summarizer.generate_summary(result)
                    category = classifier.classify_resume(result['skills'])
                    if isinstance(category, list):
                        category = ", ".join(category)
                    
                    # Save result with summary and category
                    result_id = storage.save_result(result, uploaded_file.name, summary, category)
                    
                    # Display results
                    st.subheader("Extracted Information")
                    st.write(f"**Name:** {result['name']}")
                    st.write(f"**Email:** {result['email']}")
                    st.write(f"**Phone:** {result['phone']}")
                    
                    # Display summary
                    st.subheader("Resume Summary")
                    st.write(summary)
                    
                    # Display category
                    st.subheader("Resume Classification")
                    category = classifier.classify_resume(result['skills'])
                    if isinstance(category, list):
                        st.write("Primary Categories:")
                        for cat in category:
                            st.write(f"- {cat}")
                            # Update category in storage
                            storage.update_category(result_id, cat)
                    else:
                        st.write(f"Primary Category: {category}")
                        # Update category in storage
                        storage.update_category(result_id, category)
                    
                    if result['skills']:
                        st.subheader("Skills Found")
                        for skill in result['skills']:
                            st.write(f"- {skill}")
                    
                    # Show category description
                    if isinstance(category, list):
                        for cat in category:
                            description = classifier.get_category_description(cat)
                            if description:
                                st.write(f"**{cat} Requirements:**\n{description}")
                    else:
                        description = classifier.get_category_description(category)
                        if description:
                            st.write(f"**{category} Requirements:**\n{description}")
                    
                    # Remarks section
                    st.subheader("📝 Add Remarks")
                    remarks = st.text_area(
                        "Add remarks about this candidate",
                        height=100,
                        key="new_remarks"
                    )
                    
                    if st.button("Save Remarks", key="save_new_remarks"):
                        if storage.update_remarks(result['id'], remarks):
                            st.success("Remarks saved successfully!")
                        else:
                            st.error("Failed to save remarks")
                else:
                    st.error("Failed to extract data from the resume")
                    
            except Exception as e:
                st.error(f"Error extracting data: {str(e)}")
                
            finally:
                # Clean up temporary file
                os.unlink(tmp_file_path)

    # Search and filter section
    st.markdown("---")
    st.header("🔍 Search & Filter")
    # Previous results section
    st.subheader("Previous Results")
    
    # Search and filter
    col1, col2 = st.columns(2)
    
    with col1:
        search_query = st.text_input("Search resumes...", "")
        
    with col2:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All Categories"] + list(classifier.classification_rules.keys())
        )
    
    sort_by = st.selectbox("Sort by", ["Date", "Name", "Filename", "Skills Count"])
    reverse = st.checkbox("Reverse order")

    # Previous results section
    st.markdown("---")
    st.header("📊 Previous Results")

    # Get results based on search    # Get results
    category = None if category_filter == "All Categories" else category_filter
    results = storage.search_results(search_query, category_filter=category)
    
    # Sort results
    if sort_by:
        if sort_by == "Date":
            results.sort(key=lambda x: x['timestamp'], reverse=not reverse)
        elif sort_by == "Name":
            results.sort(key=lambda x: x['data']['name'], reverse=reverse)
        elif sort_by == "Filename":
            results.sort(key=lambda x: x['filename'], reverse=reverse)
        elif sort_by == "Skills Count":
            results.sort(key=lambda x: len(x['data']['skills']), reverse=not reverse)
    
    # Display results
    if results:
        for result in results:
            with st.expander(f"{result['filename']}", expanded=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Name:** {result['data']['name']}")
                    st.write(f"**Email:** {result['data']['email']}")
                    st.write(f"**Phone:** {result['data']['phone']}")
                    st.write(f"**Skills:** {', '.join(result['data']['skills'])}")
                    
                    # Add category display
                    category = result.get('category', "Uncategorized")
                    st.write(f"**Category:** {category}")
                    
                    # Add summary display
                    summary = result.get('summary', "")
                    if summary:
                        st.subheader("Resume Summary")
                        st.write(summary)
                    
                    # Remarks section
                    current_remarks = result.get('remarks', '')
                    new_remarks = st.text_area(
                        "Add remarks about this candidate...",
                        value=current_remarks,
                        height=80,
                        key=f"remarks_{result['id']}"
                    )
                    
                    if st.button("Save Remarks", key=f"save_{result['id']}"):
                        if storage.update_remarks(result['id'], new_remarks):
                            st.success("Remarks saved successfully!")
                        else:
                            st.error("Failed to save remarks")
                
                with col2:
                    if st.button("Delete", key=f"delete_{result['id']}"):
                        if storage.delete_result(result['id']):
                            st.success("Result deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to delete result")
                    
                    st.write(f"**Date:** {result['timestamp']}")
                    st.write(f"**Skills:** {len(result['data']['skills'])}")
    else:
        st.info("No previous results found. Upload a resume to get started!")

if __name__ == "__main__":
    main()

    # Developer section
    st.markdown("---")
    
    # Create a container for the developer info
    with st.container():
        # Center the content
        st.markdown(
            """
            <style>
            .avatar-container {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                margin: 10px 0;
            }
            .avatar {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                overflow: hidden;
            }
            .avatar img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
            .developer-name {
                font-size: 14px;
                font-weight: bold;
            }
            </style>
            
            <div class="avatar-container">
                <span class="developer-name">Developed by Vikram K R</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    
