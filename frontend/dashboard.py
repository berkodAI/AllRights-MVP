import streamlit_shadcn_ui as ui
import streamlit as st
import pandas as pd

# Sample data
data = [
    {"TYPE": "Image", "DATE": "2024-05-20", "FULL NAME": "John Doe", "STATUS": "Pending", "DUE DATE": "2024-05-25"},
    {"TYPE": "Audio", "DATE": "2024-05-21", "FULL NAME": "Jane Smith", "STATUS": "Approved", "DUE DATE": "2024-06-01"},
    {"TYPE": "Video", "DATE": "2024-05-22", "FULL NAME": "Michael Johnson", "STATUS": "Pending", "DUE DATE": "2024-05-30"},
    {"TYPE": "Image", "DATE": "2024-05-23", "FULL NAME": "Emily Brown", "STATUS": "Rejected", "DUE DATE": "2024-05-28"},
    {"TYPE": "Audio", "DATE": "2024-05-24", "FULL NAME": "David Wilson", "STATUS": "Approved", "DUE DATE": "2024-06-03"},
    {"TYPE": "Video", "DATE": "2024-05-25", "FULL NAME": "Sophia Martinez", "STATUS": "Pending", "DUE DATE": "2024-06-05"},
    {"TYPE": "Image", "DATE": "2024-05-26", "FULL NAME": "James Taylor", "STATUS": "Pending", "DUE DATE": "2024-06-02"},
    {"TYPE": "Audio", "DATE": "2024-05-27", "FULL NAME": "Olivia Garcia", "STATUS": "Approved", "DUE DATE": "2024-06-08"},
    {"TYPE": "Video", "DATE": "2024-05-28", "FULL NAME": "Daniel Rodriguez", "STATUS": "Pending", "DUE DATE": "2024-06-10"},
    {"TYPE": "Image", "DATE": "2024-05-29", "FULL NAME": "Emma Hernandez", "STATUS": "Rejected", "DUE DATE": "2024-06-04"},
]


def show_dashboard():

    # Add your dashboard UI code here
    ui.tabs(options=['Overview', 'Analytics', 'Reports', 'Notifications'], default_value='Overview', key="main_tabs")
    cols = st.columns([2, 2, 1])


    with cols[0]:
        ui.metric_card(title="Detected Media",
                        content="531.891K", 
                        description="+20.1% from last month", 
                        key="card1")
    with cols[1]:
        ui.metric_card(title="Media Type", 
                        content="Image", 
                        description="+10.9% from last month", 
                        key="card2")
    with cols[2]:
        # Date Picker
        dt = ui.date_picker(key="date_picker", mode="single", label="Date Picker")
        st.write("Date Value:", dt)

        # Date Range Picker
        dt2 = ui.date_picker(key="date_picker2", mode="range", label="Date Picker")
        st.write("Date Range:", dt2)




    # Display the sample data
    st.subheader("Claims")
    # Creating a DataFrame
    claims_df = pd.DataFrame(data)

    ui.table(data=claims_df, maxHeight=300)

