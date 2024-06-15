import sys
import os
import streamlit as st
from streamlit_option_menu import option_menu

from PIL import Image
import pandas as pd

import requests
from io import BytesIO
from dashboard import main as display_dashboard
from streamlit_uploads_library.library import Library

# Ensure the working directory is set to the project's root directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.deepfake_detection.detector import predict
from backend.scraping.scraper import scrape_and_return_image_urls
from backend.reporting.reporter import generate_report

def display_image(image_path):
    image = Image.open(image_path)
    st.image(image, caption='Uploaded Image', use_column_width=True)

def display_video(video_path):
    st.video(video_path)


import streamlit.components.v1 as components

def content_submission():
    st.subheader("Content Submission")
    content_file = st.file_uploader("Upload File", type=['mp4', 'mp3', 'jpg', 'png'])

    if st.button("Submit"):
        if content_file:
            file_path = f"{content_file.name}"
            with open(file_path, "wb") as f:
                print(file_path)
                f.write(content_file.getbuffer())

            st.success("Content submitted successfully")

            if content_file.type.startswith('image'):
                input_image = Image.open(file_path)
                confidences, face_with_mask = predict(input_image)

                col1, col2 = st.columns([2, 3]) 
                
                with col1:
                    st.subheader("Original Image")
                    st.image(input_image, caption='Uploaded Image', use_column_width=True)
                
                with col2:
                    st.subheader("Explainability")
                    # Resize the image to display it smaller
                    st.image(face_with_mask, caption='Face with Explainability', width=500)
                    
                    # Display confidence scores with custom progress bars
                    st.write("Confidence Scores:")
                    for label, confidence in confidences.items():
                        st.write(f"{label.capitalize()}:")
                        st.progress(confidence)  # Basic progress bar

                        # Custom progress bar with label and color
                        progress_html = f"""
                        <div style="margin-top: 10px; margin-bottom: 10px; width: 100%;">
                            <div style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
                                <div style="flex: 1; padding-right: 10px;">
                                    <span style="font-size: 14px; color: black;">{label.capitalize()}: {confidence:.2f}</span>
                                </div>
                                <div style="flex: 9; height: 20px; border-radius: 10px; background-color: {'#4CAF50' if label == 'real' else '#F44336'};">
                                    <div style="height: 100%; width: {confidence*100}%; background-color: {'#4CAF50' if label == 'real' else '#F44336'}; border-radius: 10px;"></div>
                                </div>
                            </div>
                        </div>
                        """
                        components.html(progress_html, height=25)  # Render HTML

            elif content_file.type.startswith('video'):
                # Handle video processing (you may need to modify the predict function accordingly)
                pass

        else:
            st.error("Please upload a file.")


def web_scraping():
    st.subheader("Web Scraping")
    
    # Initialize session state variables
    if 'search_query' not in st.session_state:
        st.session_state.search_query = "Taylor Swift"
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'claimed' not in st.session_state:
        st.session_state.claimed = []

    search_query = st.text_input("Enter search query (default: Taylor Swift)", st.session_state.search_query)

    if st.button("Scrape"):
        st.session_state.search_query = search_query
        st.session_state.results = scrape_and_return_image_urls(search_query)
        st.session_state.claimed = [False] * len(st.session_state.results)

    if st.session_state.results is not None:
        st.success(f"Found {len(st.session_state.results)} results for '{st.session_state.search_query}'")
        
        # Initialize DataFrame data
        df_data = {
            'title': [],
            'URL': [],
            'upload_date': [],
            'content_type': [],  
            'Deepfake Detected': [],
            'Confidence': [],
            'Risk': [],
            'Comment': [],
            'Claim': []
        }

        cols = st.columns(2)
        for i, result in enumerate(st.session_state.results):
            try:
                image_url = result['thumbnail']
                response = requests.get(image_url)
                response.raise_for_status()  # Raise HTTPError for bad responses
                image = Image.open(BytesIO(response.content))
                resized_image = image.resize([250, 250])
                
                # Determine content type
                content_type = 'Image' if image_url.endswith(('jpg', 'jpeg', 'png')) else 'Video' if image_url.endswith(('mp4', 'avi', 'mov')) else 'Image & Video'
                
                # Deepfake detection placeholder
                is_deepfake, confidence, risk, comment = analyze_deepfake(image, content_type)
                
                df_data['title'].append(result['title'])
                df_data['URL'].append(result['link'])
                df_data['upload_date'].append(result.get('upload_date', 'N/A'))
                df_data['content_type'].append(content_type)
                df_data['Deepfake Detected'].append(is_deepfake)
                df_data['Confidence'].append(confidence)
                df_data['Risk'].append(risk)
                df_data['Comment'].append(comment)
                df_data['Claim'].append(f"claim_button_{i}")

                col = cols[i % 2]
                with col:
                    st.image(resized_image, use_column_width=True)
                    st.write(f"**Title:** {result['title']}")
                    st.write(f"**URL:** {result['link']}")
                    st.write(f"**Upload Date:** {result.get('upload_date', 'N/A')}")
                    st.write(f"**Content Type:** {content_type}")
                    st.write(f"**Deepfake Detected:** {is_deepfake}")
                    st.write(f"**Confidence:** {confidence}")
                    st.write(f"**Risk:** {risk}")
                    st.write(f"**Comment:** {comment}")

                    if st.session_state.claimed[i]:
                        view_button = st.button("View", key=f"view_button_{i}")
                        st.success(f"Claimed content: '{result['title']}'")
                        if view_button:
                            st.info(f"This content is under takedown process")
                    else:
                        if st.button("Claim", key=df_data['Claim'][-1]):
                            st.session_state.claimed[i] = True
                            st.rerun()
                    st.write("---")  # Separator between items

            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching image for '{result['title']}': {e}")
            except Exception as e:
                st.error(f"Error displaying image for '{result['title']}': {e}")

        df = pd.DataFrame(df_data)

    else:
        st.info("Enter a search query and click 'Scrape' to get results.")

def analyze_deepfake(image, content_type):
    """Placeholder function for deepfake analysis."""
    if content_type == 'Image':
        try:
            # Placeholder: Replace with actual deepfake detection logic
            confidences, _ = predict(image)
            is_deepfake = 'Yes' if confidences['fake'] > 0.5 else 'No'
            confidence = confidences['fake'] if is_deepfake == 'Yes' else confidences['real']
            risk = 'High' if is_deepfake == 'Yes' else 'Low'
            comment = 'Suspicious' if is_deepfake == 'Yes' else 'Normal'
        except Exception:
            is_deepfake = 'N/A'
            confidence = 0.0
            risk = 'N/A'
            comment = 'N/A'
    else:
        is_deepfake = 'N/A'
        confidence = 0.0
        risk = 'N/A'
        comment = 'N/A'
    return is_deepfake, confidence, risk, comment


def generate_report_ui():
    st.subheader("Generate Report")
    username = st.text_input("Enter Username")
    if st.button("Generate"):
        data = {"Username": username, "Report": "Sample Report"}
        generate_report(data)
        with open("report.pdf", "rb") as f:
            st.download_button("Download Report", f, file_name="report.pdf")

def main():
    st.set_page_config(
    page_title="AllRights - User Dashboard",
    page_icon="allrightslogo_small.png",
    layout="wide",
    initial_sidebar_state="expanded"
    )

    # Custom CSS for modern aesthetics
    st.markdown(
        """
        <style>
        /* Custom CSS for modern look */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
        }
        .sidebar .sidebar-content {
            background-color: #343a40;
            color: white;
        }
        .sidebar .sidebar-content .option-menu {
            margin-top: 20px;
        }
        .header, .footer {
            background-color: #343a40;
            color: white;
            text-align: center;
            padding: 10px;
        }
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;

        }
        .header {
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1000;
        }
        .content {
            margin-top: 60px;
            margin-bottom: 40px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Main content wrapper for spacing
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)

    st.sidebar.markdown("## User Profile")
    with st.sidebar:
        selected = option_menu(
            menu_title="Welcome, Taylor!",
            options=["Dashboard","Submit Content", "Detected Content"],
            icons=["graph-up","cloud-upload", "search"],
            menu_icon="person-bounding-box",
            default_index=0,
        )

    if selected == "Dashboard":
        display_dashboard()

    elif selected == "Submit Content":
        content_submission()
        st.text("") # leave a space
        library = Library(directory="../uploaded/taylor/")
        

    elif selected == "Detected Content":
        
        web_scraping()


if __name__ == '__main__':
    main()