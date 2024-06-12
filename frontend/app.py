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
    search_query = st.text_input("Enter search query (default: Taylor Swift)", "Taylor Swift")

    if st.button("Scrape"):
        results = scrape_and_return_image_urls(search_query)
        if results:
            st.success(f"Found {len(results)} results for '{search_query}'")
            
            cols = st.columns(4)
            for i, result in enumerate(results):
                try:
                    image_url = result['thumbnail']
                    response = requests.get(image_url)
                    response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
                    image = Image.open(BytesIO(response.content))
                    resized_image = image.resize([250, 250])
                    
                    col = cols[i % len(cols)]
                    with col:
                        st.image(resized_image, use_column_width=True)
                except requests.exceptions.ConnectionError as e:
                    st.error(f"Error fetching image for '{result['title']}': {e}")
                except Exception as e:
                    st.error(f"Error displaying image for '{result['title']}': {e}")
            
            # Create DataFrame with additional columns
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
            for i, result in enumerate(results):
                df_data['title'].append(result['title'])
                df_data['URL'].append(result['link'])
                df_data['upload_date'].append(result.get('upload_date', 'N/A'))
                content_type = 'Image' if result['thumbnail'].endswith(('jpg', 'jpeg', 'png')) else 'Video' if result['thumbnail'].endswith(('mp4', 'avi', 'mov')) else 'Image & Video'
                df_data['content_type'].append(content_type)
                
                # Analyze for deepfake detection
                try:
                    if content_type == 'Image':
                        input_image = Image.open(BytesIO(requests.get(result['thumbnail']).content))
                        confidences, _ = predict(input_image)
                        is_deepfake = confidences['fake'] > 0.5
                        df_data['Deepfake Detected'].append('Yes' if is_deepfake else 'No')
                        df_data['Confidence'].append(confidences['fake'] if is_deepfake else confidences['real'])
                        df_data['Risk'].append('High' if is_deepfake else 'Low')
                        df_data['Comment'].append('Suspicious' if is_deepfake else 'Normal')
                    else:
                        df_data['Deepfake Detected'].append('N/A')
                        df_data['Confidence'].append(0.0)
                        df_data['Risk'].append('N/A')
                        df_data['Comment'].append('N/A')
                except Exception as e:
                    st.info(f"No face detected for '{result['title']}'")
                    df_data['Deepfake Detected'].append('N/A')
                    df_data['Confidence'].append(0.0)
                    df_data['Risk'].append('N/A')
                    df_data['Comment'].append('N/A')
                
                # Add a Claim button for each row
                df_data['Claim'].append(f"claim_button_{i}")
            
            df = pd.DataFrame(df_data)
            
            # Display the DataFrame and add Claim buttons
            for index, row in df.iterrows():
                st.write(f"Title: {row['title']}")
                st.write(f"URL: {row['URL']}")
                st.write(f"Upload Date: {row['upload_date']}")
                st.write(f"Content Type: {row['content_type']}")
                st.write(f"Deepfake Detected: {row['Deepfake Detected']}")
                st.write(f"Confidence: {row['Confidence']}")
                st.write(f"Risk: {row['Risk']}")
                st.write(f"Comment: {row['Comment']}")
                
                claim_button = st.button("Claim", key=row['Claim'])
                if claim_button:
                    st.success(f"Claimed content: {row['title']}")

                st.write("---")  # Separator between rows

        else:
            st.error("No results found.")



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