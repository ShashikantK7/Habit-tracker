# Habit Tracker

A Streamlit-based habit tracking application that helps you visualize and maintain your daily routines.

## Features

- Add and track multiple habits
- Daily/Weekly/Monthly habit tracking
- Visual progress tracking with interactive charts
- Streak tracking
- Monthly overview with heatmap
- PostgreSQL database for reliable data storage

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up PostgreSQL database and update environment variables
4. Run the application:
   ```bash
   streamlit run main.py
   ```

## Project Structure

```
├── data/              # Data storage
├── utils/             # Utility modules
│   ├── data_manager.py    # Database operations
│   ├── models.py          # Database models
│   └── visualizations.py  # Chart creation
├── main.py           # Main application
└── README.md         # Documentation
```

## Environment Variables

The following environment variables are required:
- DATABASE_URL: PostgreSQL database URL
- PGHOST: Database host
- PGPORT: Database port
- PGUSER: Database user
- PGDATABASE: Database name

## Built With

- [Streamlit](https://streamlit.io/) - Web framework
- [Plotly](https://plotly.com/) - Data visualization
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [Pandas](https://pandas.pydata.org/) - Data manipulation
