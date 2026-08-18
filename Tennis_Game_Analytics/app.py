import json
from pathlib import Path

import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Tennis Game Analytics",
    page_icon="🎾",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

EVENTS_FILE = BASE_DIR / "data" / "processed" / "events.json"
RESULTS_FILE = BASE_DIR / "data" / "processed" / "event_results.json"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    with open(EVENTS_FILE, "r", encoding="utf-8") as file:
        events = json.load(file)

    with open(RESULTS_FILE, "r", encoding="utf-8") as file:
        results = json.load(file)

    return events, results


events, results = load_data()


# ============================================================
# PREPARE DATA
# ============================================================

event_lookup = {
    event["event_id"]: event
    for event in events
}


match_rows = []

for result in results:

    event = event_lookup.get(result["event_id"])

    if not event:
        continue

    winner_id = result.get("winner_id")

    if winner_id == event.get("home_competitor_id"):
        winner_position = "Home"

    elif winner_id == event.get("away_competitor_id"):
        winner_position = "Away"

    else:
        winner_position = "Unknown"

    match_rows.append({
        "Event ID": event["event_id"],
        "Date": event["start_time"][:10],
        "Competition": event["competition_name"],
        "Home Player": event["home_competitor_name"],
        "Away Player": event["away_competitor_name"],
        "Home Score": result.get("home_score"),
        "Away Score": result.get("away_score"),
        "Winner": (
            event["home_competitor_name"]
            if winner_id == event.get("home_competitor_id")
            else event["away_competitor_name"]
            if winner_id == event.get("away_competitor_id")
            else "Unknown"
        ),
        "Winner Position": winner_position,
        "Venue": event["venue_name"],
        "City": event["city_name"],
        "Country": event["country_name"]
    })


matches_df = pd.DataFrame(match_rows)


events_df = pd.DataFrame(events)


# ============================================================
# HEADER
# ============================================================

st.title("🎾 Tennis Game Analytics")

st.markdown(
    """
    ### Interactive Tennis Data Analytics Dashboard

    Explore tennis events, match results, venues and competition
    information collected and processed from the SportRadar Tennis API.
    """
)

st.divider()


# ============================================================
# KPI SECTION
# ============================================================

total_events = len(events)

completed_results = len(results)

competitions = events_df["competition_name"].nunique()

venues = events_df["venue_id"].nunique()


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "🎾 Total Events",
        total_events
    )


with col2:
    st.metric(
        "🏆 Completed Results",
        completed_results
    )


with col3:
    st.metric(
        "🏅 Competitions",
        competitions
    )


with col4:
    st.metric(
        "📍 Venues",
        venues
    )


st.divider()


# ============================================================
# SIDEBAR FILTER
# ============================================================

st.sidebar.title("🔎 Filters")

competition_list = sorted(
    events_df["competition_name"].dropna().unique()
)

selected_competition = st.sidebar.selectbox(
    "Competition",
    ["All"] + competition_list
)


if selected_competition != "All":

    filtered_events = events_df[
        events_df["competition_name"] == selected_competition
    ]

    filtered_event_ids = filtered_events["event_id"].tolist()

    filtered_matches = matches_df[
        matches_df["Event ID"].isin(filtered_event_ids)
    ]

else:

    filtered_events = events_df

    filtered_matches = matches_df


# ============================================================
# EVENT OVERVIEW
# ============================================================

st.header("📊 Event Overview")


date_counts = (
    filtered_events
    .assign(Date=filtered_events["start_time"].str[:10])
    .groupby("Date")
    .size()
    .reset_index(name="Events")
)


if not date_counts.empty:

    st.subheader("Events by Date")

    st.bar_chart(
        date_counts.set_index("Date")["Events"]
    )

else:

    st.info("No events available for the selected competition.")


# ============================================================
# VENUE ANALYSIS
# ============================================================

st.header("📍 Venue Analysis")


venue_counts = (
    filtered_events
    .groupby("venue_name")
    .size()
    .reset_index(name="Events")
    .sort_values("Events", ascending=False)
)


col1, col2 = st.columns(2)


with col1:

    st.subheader("Events by Venue")

    if not venue_counts.empty:

        st.bar_chart(
            venue_counts.set_index("venue_name")["Events"]
        )


with col2:

    st.subheader("Venue Details")

    if not venue_counts.empty:

        st.dataframe(
            venue_counts,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# MATCH RESULTS
# ============================================================

st.header("🏆 Match Results")


if filtered_matches.empty:

    st.info(
        "No completed match results are available "
        "for the selected competition."
    )

else:

    display_columns = [
        "Date",
        "Competition",
        "Home Player",
        "Away Player",
        "Home Score",
        "Away Score",
        "Winner",
        "Winner Position",
        "Venue"
    ]

    st.dataframe(
        filtered_matches[display_columns],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# WINNER ANALYSIS
# ============================================================

st.header("🥇 Winner Analysis")


if not filtered_matches.empty:

    winner_counts = (
        filtered_matches["Winner"]
        .value_counts()
        .reset_index()
    )

    winner_counts.columns = [
        "Player",
        "Wins"
    ]

    col1, col2 = st.columns(2)


    with col1:

        st.subheader("Wins by Player")

        st.bar_chart(
            winner_counts.set_index("Player")["Wins"]
        )


    with col2:

        st.subheader("Winner Statistics")

        st.dataframe(
            winner_counts,
            use_container_width=True,
            hide_index=True
        )

else:

    st.info("No winner data available.")


# ============================================================
# HOME VS AWAY ANALYSIS
# ============================================================

st.header("🏠 Home vs Away Analysis")


if not filtered_matches.empty:

    position_counts = (
        filtered_matches["Winner Position"]
        .value_counts()
        .reset_index()
    )

    position_counts.columns = [
        "Position",
        "Wins"
    ]

    st.bar_chart(
        position_counts.set_index("Position")["Wins"]
    )

else:

    st.info("No match result data available.")


# ============================================================
# DETAILED EVENT DATA
# ============================================================

st.header("📅 All Tennis Events")


event_display_columns = [
    "start_time",
    "competition_name",
    "season_name",
    "home_competitor_name",
    "away_competitor_name",
    "venue_name",
    "city_name",
    "country_name"
]


st.dataframe(
    filtered_events[event_display_columns],
    use_container_width=True,
    hide_index=True
)


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.divider()

st.header("ℹ️ About This Project")

st.markdown(
    """
    **Tennis Game Analytics** is an end-to-end data analytics project.

    **Data Pipeline**

    SportRadar API → Raw JSON → Python Processing →
    MySQL Database → SQL Analysis → Python Analysis →
    Interactive Streamlit Dashboard

    **Technologies**

    - Python
    - MySQL
    - SQL
    - SportRadar API
    - Pandas
    - Matplotlib
    - Streamlit
    - JSON

    **Current collected dataset**

    - 28 tennis events
    - 2 completed match results
    - Hopman Cup competition
    - Multiple venues and competitors

    The dashboard displays only successfully collected match results.
    No artificial match results have been generated.
    """
)


st.caption(
    "Tennis Game Analytics | Labmentix Data Science Project"
)