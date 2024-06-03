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

# Prepare heatmap data for Nivo
heatmap_data = pd.DataFrame(mock_data).groupby(['DATE', 'TYPE']).size().reset_index(name='count')
heatmap_data_pivot = heatmap_data.pivot(index='TYPE', columns='DATE', values='count').fillna(0)

# Convert pivot table to list of dictionaries
heatmap_data_list = heatmap_data_pivot.reset_index().melt(id_vars='TYPE').pivot(index='TYPE', columns='DATE', values='value').reset_index()
heatmap_data_list.columns.name = None  # Remove the index name
heatmap_data_for_nivo = heatmap_data_list.to_dict('records')


# Display the "Overview" tab
def overview_tab():
    st.title("Overview")
    # Creating columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Detected Media", total_detected_media, "+16.1% from last month")
        st.metric("Total Content Submitted", "50k", "+16.1% from last month")

    with col2:
        st.metric("Deepfakes Detected", "12.3K", "+15.2% from last month")
        st.metric("Total Claims Processed", "31.4K", "+14.6% from last month")

    with col3:
        st.metric("Detection Accuracy Rate", "97%", "+2% from last month")
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
    fig_line = px.line(time_series_data, x='DATE', y='count', color='STATUS', title='Claim Status Over Time')
    st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("Claim Status Distribution")
    fig_bar = px.bar(mock_df, x='STATUS', title='Claim Status Distribution', color='STATUS')
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.subheader("Heatmap of Detections Over Time")
    heatmap_data = mock_df.groupby(['DATE', 'TYPE']).size().reset_index(name='count')
    fig_heatmap = px.density_heatmap(heatmap_data, x='DATE', y='TYPE', z='count', title='Heatmap of Detections Over Time')
    st.plotly_chart(fig_heatmap, use_container_width=True)
    

# Detailed Reports Tab
def detailed_reports_tab():
    st.title("Detailed Reports")

    st.subheader("Media Type Distribution")
    with elements("detailed_pie_chart"):
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
    fig_line = px.line(time_series_data, x='DATE', y='count', color='STATUS', title='Claim Status Over Time')
    st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("Claim Status Distribution")
    fig_bar = px.bar(mock_df, x='STATUS', title='Claim Status Distribution', color='STATUS')
    st.plotly_chart(fig_bar, use_container_width=True)

     # Preparing data for Nivo Heatmap
    heatmap_data_for_nivo = heatmap_data_list.to_dict('records')
    date_columns = list(heatmap_data_list.columns[1:])

    st.subheader("Heatmap of Detections Over Time")
    with elements("detailed_heatmap"):
        with mui.Box(sx={"height": 500}):
            nivo.HeatMap(
                data=heatmap_data_for_nivo,
                keys=date_columns,
                indexBy="TYPE",
                margin={"top": 60, "right": 90, "bottom": 60, "left": 90},
                valueFormat=">-.2s",
                axisTop={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": -90,
                    "legend": '',
                    "legendOffset": 46,
                    "truncateTickAt": 0
                },
                axisRight={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": 'Media Type',
                    "legendPosition": 'middle',
                    "legendOffset": 70,
                    "truncateTickAt": 0
                },
                axisLeft={
                    "tickSize": 5,
                    "tickPadding": 5,
                    "tickRotation": 0,
                    "legend": 'Media Type',
                    "legendPosition": 'middle',
                    "legendOffset": -72,
                    "truncateTickAt": 0
                },
                colors={
                    "type": 'diverging',
                    "scheme": 'red_yellow_blue',
                    "divergeAt": 0.5,
                    "minValue": -100000,
                    "maxValue": 100000
                },
                emptyColor="#555555",
                legends=[
                    {
                        "anchor": 'bottom',
                        "translateX": 0,
                        "translateY": 30,
                        "length": 400,
                        "thickness": 8,
                        "direction": 'row',
                        "tickPosition": 'after',
                        "tickSize": 3,
                        "tickSpacing": 4,
                        "tickOverlap": False,
                        "tickFormat": '>-.2s',
                        "title": 'Value →',
                        "titleAlign": 'start',
                        "titleOffset": 4
                    }
                ],
            )

    st.subheader("Trend Analysis")
    trend_data = mock_df.groupby(['DATE', 'STATUS']).size().reset_index(name='count')
    fig_trend = px.line(trend_data, x='DATE', y='count', color='STATUS', title='Trend Analysis by Status')
    st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("Correlation Analysis")
    correlation_data = mock_df[['DATE', 'TYPE', 'STATUS', 'count']].copy()
    fig_corr = px.scatter_matrix(correlation_data, dimensions=['DATE', 'TYPE', 'STATUS', 'count'], title='Correlation Analysis')
    st.plotly_chart(fig_corr, use_container_width=True)

    st.subheader("Detailed Data Table")
    date_range = st.date_input("Select Date Range", [datetime(2024, 1, 1), datetime.now()])
    start_date, end_date = date_range
    filtered_df = mock_df[(mock_df['DATE'] >= pd.to_datetime(start_date)) & (mock_df['DATE'] <= pd.to_datetime(end_date))]
    st.dataframe(filtered_df)
    st.download_button(
        label="Download Data as CSV",
        data=filtered_df.to_csv().encode('utf-8'),
        file_name='detailed_report.csv',
        mime='text/csv',
    )



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

