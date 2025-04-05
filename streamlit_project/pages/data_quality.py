import streamlit as st
from utils.logger import logger
from utils.filters import add_filters


def show_kpis(df):
    """
    Display key performance indicators.
    """
    st.write("Data KPIs")
    col1, col2, col3 = st.columns(3)

    col1.metric("Oldest match", str(df["start_datetime"].min()))
    col2.metric("Latest match", str(df["start_datetime"].max()))
    col3.metric("Match count", df.shape[0])

    matches_per_day = df.groupby("start_date").size().reset_index(name="count")
    st.line_chart(matches_per_day.set_index("start_date"))


if __name__ == "__main__":
    st.title("Data quality")

    if "game_data" and "player_data" in st.session_state:
        game_data_df = st.session_state["game_data"]
        player_data_df = st.session_state["player_data"]
 
        # add filters
        filtered_game_data_df = add_filters(game_data_df, player_data_df)

        st.subheader("Game data")

        # show filtered game data
        st.write(filtered_game_data_df)
        show_kpis(filtered_game_data_df)
    