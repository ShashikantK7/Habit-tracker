import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

def create_streak_chart(habit_data):
    """Create a line chart showing habit completion over time"""
    habit_data['date'] = pd.to_datetime(habit_data['date'])
    habit_data = habit_data.sort_values('date')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=habit_data['date'],
        y=habit_data['completed'].astype(int),
        mode='lines+markers',
        name='Completion',
        line=dict(color='#FF4B4B'),
        marker=dict(
            size=8,
            symbol='circle'
        )
    ))
    
    fig.update_layout(
        title='Habit Completion Over Time',
        xaxis_title='Date',
        yaxis_title='Completed',
        yaxis=dict(tickmode='array', tickvals=[0, 1], ticktext=['No', 'Yes']),
        showlegend=False,
        height=300
    )
    
    return fig

def create_completion_heatmap(tracking_data):
    """Create a calendar heatmap of habit completion"""
    tracking_data['date'] = pd.to_datetime(tracking_data['date'])
    daily_completion = tracking_data.groupby('date')['completed'].mean().reset_index()
    
    fig = px.scatter(
        daily_completion,
        x='date',
        y=[0] * len(daily_completion),
        color='completed',
        color_continuous_scale=['#FFE5E5', '#FF4B4B'],
        size=[20] * len(daily_completion)
    )
    
    fig.update_layout(
        title='Monthly Completion Heatmap',
        xaxis_title='',
        yaxis_title='',
        yaxis_visible=False,
        height=200,
        showlegend=False
    )
    
    return fig

def create_habit_summary(tracking_data):
    """Create a summary chart of habit completion rates"""
    completion_rates = (
        tracking_data.groupby('habit_name')['completed']
        .mean()
        .sort_values(ascending=True)
        .reset_index()
    )
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=completion_rates['completed'] * 100,
        y=completion_rates['habit_name'],
        orientation='h',
        marker_color='#FF4B4B'
    ))
    
    fig.update_layout(
        title='Habit Completion Rates',
        xaxis_title='Completion Rate (%)',
        yaxis_title='Habit',
        height=300,
        showlegend=False
    )
    
    return fig
