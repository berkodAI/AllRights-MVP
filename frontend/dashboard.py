import streamlit_shadcn_ui as ui
import streamlit as st
import pandas as pd
from streamlit_elements import elements, mui, nivo
from collections import defaultdict
from datetime import datetime, timedelta
import random
import numpy as np
from datetime import datetime
import plotly.express as px

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
mock_data = generate_mock_data("2024-01-01", datetime.now().strftime("%Y-%m-%d"), 100)

# Calculate counts of each media type
media_counts = pd.Series([d['TYPE'] for d in mock_data]).value_counts().to_dict()
total_detected_media = sum(media_counts.values())

# Define the color palette
primary_color = "#0A1F44"
secondary1_color = "#B0B0B0"
secondary2_color = "#5A8CCB"

# Prepare data for pie chart with percentages
pie_data_with_percentage = [
    {"id": "Image", "label": "Image", "value": media_counts.get("Image", 0)},
    {"id": "Video", "label": "Video", "value": media_counts.get("Video", 0)},
    {"id": "Audio", "label": "Audio", "value": media_counts.get("Audio", 0)},
]

# Preprocess data to aggregate counts by month and STATUS
status_counts = defaultdict(lambda: defaultdict(int))
for entry in mock_data:
    month = datetime.strptime(entry["DATE"], "%Y-%m-%d").strftime("%Y-%m")
    status = entry["STATUS"]
    status_counts[month][status] += 1

# Prepare data for Nivo Line chart
line_data = []
statuses = ["Pending", "Removed", "Ready to Claim"]
for status in statuses:
    line_data.append({
        "id": status,
        "data": [{"x": month, "y": status_counts[month].get(status, 0)} for month in sorted(status_counts.keys())]
    })


# Display the "Overview" tab
def overview_tab():
    st.title("Overview")
    # Creating columns
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        # Two rows for the first column
        st.metric("Total Detected", "50k", "+16.1% from last month")
        st.write("")  # Add some space between cards
        st.write("")  # Add some space between cards
        st.write("")  # Add some space between cards
        st.metric("Deepfakes Detected", "12.3K", "+15.2% from last month")
        
        
        

    with col2:
        # Two rows for the second column
        st.metric("Total Content Submitted", "50k", "+16.1% from last month")
        st.write("")  # Add some space between cards
        st.write("")  # Add some space between cards
        st.write("")  # Add some space between cards
        st.metric("Total Claims Processed", "31.4K", "+14.6% from last month")
    

    with col3:
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
                        {"match": {"id": "Image"}, "id": primary_color},
                        {"match": {"id": "Video"}, "id": secondary1_color},
                        {"match": {"id": "Audio"}, "id": secondary2_color},
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
        
    st.subheader("Claims")  
    col_line, col_table = st.columns(2)
    
    with col_line:
        with elements("nivo_line_chart"):
            with mui.Box(sx={"height": 500}):
                nivo.Line(
                    data=line_data,
                    margin={"top": 60, "right": 120, "bottom": 50, "left": 50},
                    xScale={"type": "point"},
                    yScale={
                        "type": "linear",
                        "min": "auto",
                        "max": "auto",
                        "stacked": False,
                        "reverse": False
                    },
                    yFormat=" >-.2f",
                    axisTop=None,
                    axisRight=None,
                    axisBottom={
                        "tickSize": 15,
                        "tickPadding": 8,
                        "tickRotation": 1,
                        "legendOffset": 39,
                        "legendPosition": "middle"
                    },
                    axisLeft={
                        "tickSize": 15,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legendOffset": -10,
                        "legendPosition": "middle"
                    },
                    pointSize=10,
                    pointColor={"theme": "background"},
                    pointBorderWidth=2,
                    pointBorderColor={"from": "serieColor"},
                    pointLabel="y",
                    pointLabelYOffset=-12,
                    useMesh=True,
                    legends=[
                        {
                            "anchor": "top-right",
                            "direction": "column",
                            "justify": False,
                            "translateX": 90,
                            "translateY": 180,
                            "itemsSpacing": 1,
                            "itemDirection": "left-to-right",
                            "itemWidth": 80,
                            "itemHeight": 30,
                            "itemOpacity": 1.2,
                            "symbolSize": 25,
                            "symbolShape": "circle",
                            "symbolBorderColor": "rgba(0, 0, 0, .5)",
                            "effects": [
                                {
                                    "on": "hover",
                                    "style": {
                                        "itemBackground": "rgba(0, 0, 0, .03)",
                                        "itemOpacity": 1
                                    }
                                }
                            ]
                        }
                    ],
                    theme={
                        "axis": {
                            "legend": {
                                "text": {
                                    "fontSize": 16
                                }
                            },
                            "ticks": {
                                "text": {
                                    "fontSize": 16
                                }
                            }
                        }
                    }
                )

    
    with col_table:
        # Calculate counts of each status for claimed media
        claimed_status_counts = pd.Series([d['STATUS'] for d in mock_data]).value_counts().to_dict()

        # Prepare data for the detailed pie chart
        detailed_pie_data = [
            {"id": status, "label": status, "value": claimed_status_counts.get(status, 0)} 
            for status in statuses
        ]
        
        # Display a detailed pie chart for claimed media
        with elements("detailed_pie_chart"):
            with mui.Box(sx={"height": 300}):
                nivo.Pie(
                    data=detailed_pie_data,
                    margin={"top": 5, "right": 10, "bottom": 30, "left": 30},
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
                    legends=[
                        {
                            "anchor": "right",
                            "direction": "column",
                            "justify": False,
                            "translateX": 35,
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
                                {"on": "hover", "style": {"itemTextColor": "#000"}}
                            ],
                        }
                    ],
                )

# Display the "Reports" tab
def reports_tab():
    st.title("Reports")
    # Add the reports UI code here
    # Creating a DataFrame
    claims_df = pd.DataFrame(mock_data)

    st.dataframe(claims_df)



# Run the app
def main():
    
    main_tabs = ["Overview", "Detailed Reports"]
    tab_selection = ui.tabs(options=main_tabs, default_value='Overview', key="main_tabs")
    
    if tab_selection == "Overview":
        overview_tab()
    elif tab_selection == "Detailed Reports":
        reports_tab()

if __name__ == "__main__":
    main()

