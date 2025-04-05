import streamlit as st
from utils.logger import logger


def add_filters(games_df: "pandas.DataFrame", players_df: "pandas.DataFrame") -> "pandas.DataFrame":
    """
    Renders date filter and player filter in the sidebar which can be used to filter the DataFrame.
    """
    # Create a date filter
    st.sidebar.header("Filter by Date Range")
    min_date = games_df["start_date"].min()
    max_date = games_df["start_date"].max()
    date_range = st.sidebar.date_input(
        "Select Date Range", 
        [min_date, max_date], 
        min_value=min_date, 
        max_value=max_date
    )

    # create player filter
    player_names = players_df["player_or_team_name"]
    selected_player_or_team = st.sidebar.multiselect(
        "Select Player", 
        options=player_names,
        default=[]
    )


    ####### Filter games_df based on the dates and selected player #######
    # use date filter only if both dates are selected
    filtered_df = games_df
    if(len(date_range) == 2):    
        filtered_df = games_df[
            (games_df["start_date"].dt.date >= date_range[0]) & (games_df["start_date"].dt.date <= date_range[1])
        ]

    # use player filter only if player is selected
    if len(selected_player_or_team) > 0:    
        filtered_df = filtered_df[
            (filtered_df["home_team_name"].isin(selected_player_or_team)) |
            (filtered_df["away_team_name"].isin(selected_player_or_team))
        ]

    return filtered_df
