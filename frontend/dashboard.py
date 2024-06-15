import streamlit_shadcn_ui as ui
import streamlit as st
import pandas as pd
from streamlit_elements import elements, mui, nivo
from datetime import datetime, timedelta
import random
import numpy as np
from datetime import datetime
import plotly.express as px

import plotly.express as px
import plotly.graph_objs as go
import streamlit.components.v1 as components

# Generate mock data
def generate_mock_data(start_date, end_date, num_entries):
    date_range = pd.date_range(start_date, end_date)
    types = ["Image", "Audio", "Video"]
    statuses = ["Pending", "Removed", "Ready to Claim"]
    
    data = []
    for _ in range(num_entries):
        entry = {
            "TYPE": random.choice(types),
            "DATE": random.choice(date_range).strftime("%Y-%m-%d"),
            "STATUS": random.choice(statuses)
        }
        data.append(entry)
    return data

# Create mock data from January to the current date
mock_data = generate_mock_data("2024-01-01", datetime.now().strftime("%Y-%m-%d"), 11000)

# Calculate counts of each media type
media_counts = pd.Series([d['TYPE'] for d in mock_data]).value_counts().to_dict()
total_detected_media = sum(media_counts.values())

# Prepare data for pie chart with percentages
pie_data_with_percentage = [
    {"id": "Image", "label": "Image", "value": media_counts.get("Image", 0)},
    {"id": "Video", "label": "Video", "value": media_counts.get("Video", 0)},
    {"id": "Audio", "label": "Audio", "value": media_counts.get("Audio", 0)},
]

# Prepare data for line chart
mock_df = pd.DataFrame(mock_data)
mock_df['DATE'] = pd.to_datetime(mock_df['DATE'])
mock_df['count'] = 1

# Time series data
time_series_data = mock_df.groupby(['DATE', 'STATUS']).size().reset_index(name='count')


# Display the "Overview" tab
def overview_tab():
    st.title("Overview")
    # Creating columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Detected Media", total_detected_media, "+16.1% from last month")
        st.metric("Total Content Submitted", "8351", "+19.1% from last month")

    with col2:
        st.metric("Deepfakes Detected", "4231", "+15.2% from last month")
        st.metric("Total Claims Processed", "10083", "+14.6% from last month")

    with col3:
        st.metric("Detection Accuracy Rate", "99%", "+2% from last month")
        st.metric("Average Time to Process Claims", "5 days", "-10% from last month")

    st.subheader("Media Type Distribution")
    with elements("nivo_pie_chart"):
        with mui.Box(sx={"height": 300}):
            nivo.Pie(
                data=pie_data_with_percentage,
                margin={"top": 10, "right": 10, "bottom": 30, "left": 10},
                innerRadius=0.5,
                padAngle=0.7,
                cornerRadius=3,
                activeOuterRadiusOffset=8,
                colors={"scheme": "blues"},  # Change color scheme to blues
                borderWidth=1,
                borderColor={"from": "color", "modifiers": [["darker", 0.95]]},
                arcLabelsSkipAngle=10,
                arcLabelsTextColor={"from": "color", "modifiers": [["darker", 17]]},
                arcLabelsRadiusOffset=0.7,  # Adjust label position
                arcLabelsColor="black",  # Set label color to background
                arcLabelsFormat=".8f%%",  # Format label as percentage
                arcLinkLabelsSkipAngle=10,
                arcLinkLabelsTextColor="grey",
                arcLinkLabelsThickness=2,
                arcLinkLabelsColor="black",
                fill=[
                    {"match": {"id": "Image"}, "id": "#0A1F44"},
                    {"match": {"id": "Video"}, "id": "#B0B0B0"},
                    {"match": {"id": "Audio"}, "id": "#5A8CCB"},
                ],
                legends=[
                    {
                        "anchor": "right",
                        "direction": "column",
                        "justify": False,
                        "translateX": 55,
                        "translateY": 36,
                        "itemsSpacing": 4,
                        "itemWidth": 100,
                        "itemHeight": 18,
                        "itemTextColor": "#999",
                        "itemDirection": "left-to-right",
                        "itemOpacity": 1,
                        "symbolSize": 18,
                        "symbolShape": "circle",
                        "effects": [
                            {"on": "hover", "style": {"itemTextColor": "#090"}}
                        ],
                    }
                ],
            )
    st.subheader("Claim Status Over Time")
    fig_area = px.area(time_series_data, x='DATE', y='count', color='STATUS', title='Claim Status Over Time')
    st.plotly_chart(fig_area, use_container_width=True)

    
    

# Detailed Reports Tab
def detailed_reports_tab():
    
    st.subheader("Claim Status Over Time")
    fig_line = px.line(time_series_data, x='DATE', y='count', color='STATUS', title='Claim Status Over Time')
    st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("Claim Status Distribution")
    fig_bar = px.bar(mock_df, x='STATUS', title='Claim Status Distribution', color='STATUS')
    st.plotly_chart(fig_bar, use_container_width=True)


    st.subheader("Detailed Data Table")
    date_range = st.date_input("Select Date Range", [datetime(2024, 1, 1), datetime.now()])
    start_date, end_date = date_range
    filtered_df = mock_df[(mock_df['DATE'] >= pd.to_datetime(start_date)) & (mock_df['DATE'] <= pd.to_datetime(end_date))]

    # Generate HTML table with CSS for alignment
    table_html = """
    <style>
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    tr:hover {
        background-color: #ddd;
    }
    button {
        background-color: #0A1F44;
        color: white;
        padding: 5px 10px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 15px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
        border: none;
    }
    button_CLAIM {
        background-color: #FF2B2B;
        color: white;
        padding: 5px 10px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 15px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
        border: none;
    }
    </style>
    <table>
        <tr>
            <th>TYPE</th>
            <th>DATE</th>
            <th>STATUS</th>
            <th>FREQUENCY</th>
        </tr>
    """
    for idx, row in filtered_df.iterrows():
        table_html += generate_row_html(row)
    table_html += "</table>"

    # Display the HTML table in Streamlit
    components.html(table_html, height=600, scrolling=True)

    # CSV Download Button
    st.download_button(
        label="Download Data as CSV",
        data=filtered_df.to_csv().encode('utf-8'),
        file_name='detailed_report.csv',
        mime='text/csv',
    )

# Helper function to generate HTML for each row
def generate_row_html(row):
    buttons_html = ""
    if row["STATUS"] == "Ready to Claim":
        buttons_html = f"<button_CLAIM onclick='alert(\"Claimed row {row.name + 1}\")'>Claim</button_CLAIM>"
    else:
        buttons_html = f"<button onclick='alert(\"Viewing row {row.name + 1}\")'>View</button>"

    row_html = f"<tr>"
    for col in row.index:
        row_html += f"<td>{row[col]}</td>"
    row_html += f"<td>{buttons_html}</td>"
    row_html += f"</tr>"
    return row_html


# Run the app
def main():
    
    main_tabs = ["Overview", "Detailed Reports"]
    tab_selection = ui.tabs(options=main_tabs, default_value='Overview', key="main_tabs")
    
    if tab_selection == "Overview":
        overview_tab()
    elif tab_selection == "Detailed Reports":
        detailed_reports_tab()

if __name__ == "__main__":
    main()

