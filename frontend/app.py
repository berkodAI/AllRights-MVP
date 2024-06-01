import sys
import os
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_elements import elements, mui

from PIL import Image
import pandas as pd

import requests
from io import BytesIO
from dashboard import main as display_dashboard
import plotly.graph_objects as go

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
                    image = Image.open(BytesIO(response.content))
                    
                    col = cols[i % len(cols)]
                    with col:
                        st.image(image, caption=result['title'], use_column_width=True)
                        st.write(f"[Link]({result['link']})")
                except Exception as e:
                    st.error(f"Error displaying image: {e}")
            
            # Create DataFrame with additional columns
            df_data = {
                'title': [],
                'link': [],
                'upload_date': [],
                'content_type': [],  
                'Deepfake': [],
                'Confidence': [],
                'Risk': [],
                'Comment': []
            }
            for result in results:
                df_data['title'].append(result['title'])
                df_data['link'].append(result['link'])
                df_data['upload_date'].append(result.get('upload_date', 'N/A'))
                content_type = 'Image' if result['thumbnail'].endswith(('jpg', 'jpeg', 'png')) else 'Video' if result['thumbnail'].endswith(('mp4', 'avi', 'mov')) else 'Image & Video'
                df_data['content_type'].append(content_type)
                
                # Analyze for deepfake detection
                try:
                    if content_type == 'Image':
                        input_image = Image.open(BytesIO(requests.get(result['thumbnail']).content))
                        confidences, _ = predict(input_image)
                        is_deepfake = confidences['fake'] > 0.5
                        df_data['Deepfake'].append('Yes' if is_deepfake else 'No')
                        df_data['Confidence'].append(confidences['fake'] if is_deepfake else confidences['real'])
                        df_data['Risk'].append('High' if is_deepfake else 'Low')
                        df_data['Comment'].append('Suspicious' if is_deepfake else 'Normal')
                    else:
                        # For videos, you can add a placeholder or handle differently
                        df_data['Deepfake'].append('N/A')
                        df_data['Confidence'].append(0.0)
                        df_data['Risk'].append('N/A')
                        df_data['Comment'].append('N/A')
                except Exception as e:
                    st.info(f"No face detected for '{result['title']}'")
                    df_data['Deepfake'].append('N/A')
                    df_data['Confidence'].append(0.0)
                    df_data['Risk'].append('N/A')
                    df_data['Comment'].append('N/A')
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, width=2500)  # Adjust width here
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
    st.set_page_config(page_title="AllRights - User Dashboard", layout="wide")

    # Include the Streamlit theme configuration
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css">
        """,
        unsafe_allow_html=True
    )

    # Include Bootstrap Icons
    st.markdown(
        """
        <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.7.2/font/bootstrap-icons.min.css" rel="stylesheet">
        """,
        unsafe_allow_html=True
    )
    # Display the navigation bar with Bootstrap classes and icons
    
    with st.sidebar:
        selected = option_menu(
            menu_title="AllRights",
            options=["Dashboard","Submit Content", "Scrape Content"],
            icons=["graph-up","cloud-upload", "search"],
            menu_icon="cast",
            default_index=0,
        )

    if selected == "Dashboard":
        st.title("Dashboard")

        display_dashboard()

    elif selected == "Submit Content":
        content_submission()

    elif selected == "Scrape Content":
        web_scraping()


if __name__ == '__main__':
    main()