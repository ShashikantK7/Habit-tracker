import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar
from utils.data_manager import DataManager
from utils.visualizations import create_streak_chart, create_completion_heatmap, create_habit_summary

# Page configuration
st.set_page_config(
    page_title="Habit Tracker",
    page_icon="📊",
    layout="wide"
)

# Initialize data manager
data_manager = DataManager()

# Main title
st.title("📊 Habit Tracker")

# Sidebar for adding new habits
with st.sidebar:
    st.header("Add New Habit")
    new_habit = st.text_input("Habit Name")
    frequency = st.selectbox(
        "Frequency",
        ["Daily", "Weekly", "Monthly"]
    )
    
    if st.button("Add Habit"):
        if new_habit:
            data_manager.add_habit(new_habit, frequency)
            st.success(f"Added habit: {new_habit}")
        else:
            st.error("Please enter a habit name")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Track Your Habits")
    
    # Get all habits
    habits = data_manager.get_habits()
    
    if not habits.empty:
        # Date selector
        tracking_date = st.date_input(
            "Select Date",
            datetime.now().date()
        )
        
        # Create habit tracking form
        with st.form("habit_tracking"):
            for _, habit in habits.iterrows():
                habit_name = habit['habit_name']
                current_status = data_manager.get_habit_status(habit_name, tracking_date)
                completed = st.checkbox(
                    habit_name,
                    value=current_status
                )
                if completed != current_status:
                    data_manager.update_habit_status(habit_name, tracking_date, completed)
            
            st.form_submit_button("Save Progress")

with col2:
    st.subheader("Statistics")
    
    # Select habit for detailed view
    selected_habit = st.selectbox(
        "Select Habit",
        options=habits['habit_name'].tolist() if not habits.empty else []
    )
    
    if selected_habit:
        # Display streak
        current_streak = data_manager.get_current_streak(selected_habit)
        st.metric("Current Streak", f"{current_streak} days")
        
        # Display streak chart
        streak_chart = create_streak_chart(data_manager.get_habit_history(selected_habit))
        st.plotly_chart(streak_chart, use_container_width=True)

# Bottom section for overall progress
st.subheader("Monthly Overview")
if not habits.empty:
    # Create and display heatmap
    heatmap = create_completion_heatmap(data_manager.get_all_tracking_data())
    st.plotly_chart(heatmap, use_container_width=True)
    
    # Display habit summary
    summary_chart = create_habit_summary(data_manager.get_all_tracking_data())
    st.plotly_chart(summary_chart, use_container_width=True)
