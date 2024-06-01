import streamlit_shadcn_ui as ui
import streamlit as st
import pandas as pd
from streamlit_elements import elements, mui, nivo
from collections import defaultdict
from datetime import datetime, timedelta
import random

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

# Prepare data for pie chart
pie_data = [
    {"id": "Image", "label": "Image", "value": media_counts.get("Image", 0), "color": "hsl(309, 70%, 50%)"},
    {"id": "Video", "label": "Video", "value": media_counts.get("Video", 0), "color": "hsl(229, 70%, 50%)"},
    {"id": "Audio", "label": "Audio", "value": media_counts.get("Audio", 0), "color": "hsl(78, 70%, 50%)"},
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
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        # Two rows for the first column
        st.metric("Detected Media", "531.891K", "+20.1% from last month")
        st.write("")  # Add some space between cards
        st.metric("Deepfakes Detected", "12.3K", "+15.2% from last month")

    with col2:
        # Two rows for the second column
        st.metric("Total Detected", "250k", "+16.1% from last month")
        st.write("")  # Add some space between cards
        st.metric("Total Claimed", "31.4K", "+14.6% from last month")

    with col3:
        with elements("nivo_pie_chart"):
            with mui.Box(sx={"height": 300}):
                nivo.Pie(
                    data=pie_data,
                    margin={"top": 5, "right": 10, "bottom": 30, "left": 30},
                    innerRadius=0.5,
                    padAngle=0.7,
                    cornerRadius=3,
                    activeOuterRadiusOffset=8,
                    borderWidth=1,
                    borderColor={"from": "color", "modifiers": [["darker", 0.8]]},
                    arcLinkLabelsSkipAngle=10,
                    arcLinkLabelsTextColor="grey",
                    arcLinkLabelsThickness=2,
                    arcLinkLabelsColor={"from": "color"},
                    arcLabelsSkipAngle=10,
                    arcLabelsTextColor={"from": "color", "modifiers": [["darker", 4]]},
                    defs=[
                        {
                            "id": "dots",
                            "type": "patternDots",
                            "background": "inherit",
                            "color": "rgba(255, 255, 255, 0.3)",
                            "size": 4,
                            "padding": 1,
                            "stagger": True,
                        },
                        {
                            "id": "lines",
                            "type": "patternLines",
                            "background": "inherit",
                            "color": "rgba(255, 255, 255, 0.3)",
                            "rotation": -45,
                            "lineWidth": 6,
                            "spacing": 10,
                        },
                    ],
                    fill=[
                        {"match": {"id": "Image"}, "id": "dots"},
                        {"match": {"id": "Video"}, "id": "dots"},
                        {"match": {"id": "Audio"}, "id": "lines"},
                    ],
                    legends=[
                        {
                            "anchor": "left",
                            "direction": "column",
                            "justify": False,
                            "translateX": 0,
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
    
        # Creating a DataFrame
        claims_df = pd.DataFrame(mock_data)

        ui.table(data=claims_df, maxHeight=300)          
        

# Display the "Reports" tab
def reports_tab():
    st.title("Reports")
    # Add the reports UI code here
    st.write("This is the Reports tab.")


# Run the app
def main():
    
    main_tabs = ["Overview", "Reports"]
    tab_selection = ui.tabs(options=main_tabs, default_value='Overview', key="main_tabs")
    
    if tab_selection == "Overview":
        overview_tab()
    elif tab_selection == "Reports":
        reports_tab()

if __name__ == "__main__":
    main()

