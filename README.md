pip install streamlit pandas plotly sqlalchemy psycopg2-binary
   ```
3. Set up PostgreSQL database and configure the following environment variables:
   - DATABASE_URL: PostgreSQL database connection URL
   - PGHOST: Database host
   - PGPORT: Database port
   - PGUSER: Database user
   - PGDATABASE: Database name
   - PGPASSWORD: Database password

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