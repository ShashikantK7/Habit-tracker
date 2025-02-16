from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models
import pandas as pd

class DataManager:
    def __init__(self):
        self.db = next(models.get_db())

    def add_habit(self, habit_name: str, frequency: str):
        """Add a new habit"""
        db_habit = models.Habit(
            habit_name=habit_name,
            frequency=frequency
        )
        self.db.add(db_habit)
        self.db.commit()
        self.db.refresh(db_habit)

    def get_habits(self):
        """Get all habits"""
        habits = self.db.query(models.Habit).all()
        return pd.DataFrame([{
            'habit_name': h.habit_name,
            'frequency': h.frequency,
            'created_at': h.created_at
        } for h in habits])

    def get_habit_status(self, habit_name: str, date: datetime.date):
        """Get completion status for a habit on a specific date"""
        tracking = (
            self.db.query(models.HabitTracking)
            .filter(
                models.HabitTracking.habit_name == habit_name,
                models.HabitTracking.date == date
            )
            .first()
        )
        return tracking.completed if tracking else False

    def update_habit_status(self, habit_name: str, date: datetime.date, completed: bool):
        """Update habit completion status"""
        tracking = (
            self.db.query(models.HabitTracking)
            .filter(
                models.HabitTracking.habit_name == habit_name,
                models.HabitTracking.date == date
            )
            .first()
        )

        if tracking:
            tracking.completed = completed
        else:
            tracking = models.HabitTracking(
                habit_name=habit_name,
                date=date,
                completed=completed
            )
            self.db.add(tracking)

        self.db.commit()

    def get_current_streak(self, habit_name: str):
        """Calculate current streak for a habit"""
        tracking_data = (
            self.db.query(models.HabitTracking)
            .filter(models.HabitTracking.habit_name == habit_name)
            .order_by(models.HabitTracking.date.desc())
            .all()
        )

        streak = 0
        today = datetime.now().date()

        for record in tracking_data:
            if record.completed and (today - record.date).days <= streak + 1:
                streak += 1
            else:
                break

        return streak

    def get_habit_history(self, habit_name: str):
        """Get complete history for a habit"""
        history = (
            self.db.query(models.HabitTracking)
            .filter(models.HabitTracking.habit_name == habit_name)
            .all()
        )
        return pd.DataFrame([{
            'habit_name': h.habit_name,
            'date': h.date,
            'completed': h.completed
        } for h in history])

    def get_all_tracking_data(self):
        """Get all tracking data"""
        tracking = self.db.query(models.HabitTracking).all()
        return pd.DataFrame([{
            'habit_name': t.habit_name,
            'date': t.date,
            'completed': t.completed
        } for t in tracking])

    def __del__(self):
        """Close database connection"""
        self.db.close()