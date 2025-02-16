import pandas as pd
import os
from datetime import datetime, timedelta

class DataManager:
    def __init__(self):
        self.habits_file = "data/habits.csv"
        self.tracking_file = "data/tracking.csv"
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize CSV files if they don't exist"""
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists(self.habits_file):
            pd.DataFrame(columns=['habit_name', 'frequency', 'created_at']
            ).to_csv(self.habits_file, index=False)
            
        if not os.path.exists(self.tracking_file):
            pd.DataFrame(columns=['habit_name', 'date', 'completed']
            ).to_csv(self.tracking_file, index=False)
    
    def add_habit(self, habit_name: str, frequency: str):
        """Add a new habit"""
        habits = pd.read_csv(self.habits_file)
        if habit_name not in habits['habit_name'].values:
            new_habit = pd.DataFrame({
                'habit_name': [habit_name],
                'frequency': [frequency],
                'created_at': [datetime.now().strftime('%Y-%m-%d')]
            })
            habits = pd.concat([habits, new_habit], ignore_index=True)
            habits.to_csv(self.habits_file, index=False)
    
    def get_habits(self):
        """Get all habits"""
        return pd.read_csv(self.habits_file)
    
    def get_habit_status(self, habit_name: str, date: datetime.date):
        """Get completion status for a habit on a specific date"""
        tracking = pd.read_csv(self.tracking_file)
        date_str = date.strftime('%Y-%m-%d')
        status = tracking[
            (tracking['habit_name'] == habit_name) & 
            (tracking['date'] == date_str)
        ]
        return bool(status['completed'].iloc[0]) if not status.empty else False
    
    def update_habit_status(self, habit_name: str, date: datetime.date, completed: bool):
        """Update habit completion status"""
        tracking = pd.read_csv(self.tracking_file)
        date_str = date.strftime('%Y-%m-%d')
        
        # Remove existing entry if any
        tracking = tracking[
            ~((tracking['habit_name'] == habit_name) & 
              (tracking['date'] == date_str))
        ]
        
        # Add new entry
        new_entry = pd.DataFrame({
            'habit_name': [habit_name],
            'date': [date_str],
            'completed': [completed]
        })
        tracking = pd.concat([tracking, new_entry], ignore_index=True)
        tracking.to_csv(self.tracking_file, index=False)
    
    def get_current_streak(self, habit_name: str):
        """Calculate current streak for a habit"""
        tracking = pd.read_csv(self.tracking_file)
        habit_tracking = tracking[tracking['habit_name'] == habit_name].copy()
        habit_tracking['date'] = pd.to_datetime(habit_tracking['date'])
        habit_tracking = habit_tracking.sort_values('date', ascending=False)
        
        streak = 0
        today = datetime.now().date()
        
        for _, row in habit_tracking.iterrows():
            if row['completed'] and (today - row['date'].date()).days <= streak + 1:
                streak += 1
            else:
                break
                
        return streak
    
    def get_habit_history(self, habit_name: str):
        """Get complete history for a habit"""
        tracking = pd.read_csv(self.tracking_file)
        return tracking[tracking['habit_name'] == habit_name].copy()
    
    def get_all_tracking_data(self):
        """Get all tracking data"""
        return pd.read_csv(self.tracking_file)
