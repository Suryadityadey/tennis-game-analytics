# Tennis Game Analytics

## Project Overview

Tennis Game Analytics is a data analytics project that collects,
processes, stores, and analyzes tennis event data obtained from the
SportRadar Tennis API.

The project uses Python for data processing and analysis and MySQL
for structured data storage and SQL-based analytics.

## Objectives

- Collect tennis competition and event data.
- Process raw JSON data into structured datasets.
- Store tennis data in a relational MySQL database.
- Maintain relationships between competitions, competitors,
  venues, events, and results.
- Perform SQL-based analytics.
- Perform Python-based data analysis.
- Generate visualizations for tennis events and match results.
- Create a final analytical dashboard.

## Technologies Used

- Python
- MySQL
- SQL
- SportRadar Tennis API
- JSON
- Pandas / Python data-processing tools
- Matplotlib
- MySQL Connector
- python-dotenv

## Project Structure

```text
Tennis_Game_Analytics/
│
├── api/
│   ├── process_events.py
│   ├── process_event_results.py
│   └── collect_event_results.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│
├── analysis/
│   ├── analyze_data.py
│   ├── visualize_data.py
│   ├── dashboard.py
│   ├── events_by_date.png
│   ├── home_vs_away_wins.png
│   └── final_events_chart.png
│
├── config.py
├── .env
└── README.md