import streamlit as st
import duckdb
from utils.logger import logger


def read_data_to_df(sql_query: str) -> "pandas.DataFrame":
    """
    Runs given SQL query and returns a pandas DataFrame.
    """
    logger.info(f"Executing SQL query: {sql_query}")
    conn = duckdb.connect('/data/tennisdb.duckdb')
    df = conn.execute(sql_query).fetch_df()
    conn.close()

    logger.info(f"Query executed successfully, retrieved {len(df)} rows")

    return df


def save_data_to_session_state() -> None:
    """
    Read game_data and player data from the database and store it in the session state.
    """

    if "game_data" not in st.session_state:
        df = read_data_to_df("select * from tennis_publish.played_matches")
        st.session_state["game_data"] = df
        logger.info("game_data loaded into session state")


    if "player_data" not in st.session_state:
        df = read_data_to_df("select * from tennis_publish.players")
        st.session_state["player_data"] = df
        logger.info("player_data loaded into session state")




if __name__ == "__main__":
    st.set_page_config(page_title="Tennis Dashboard 🎾", layout="wide")
    st.title('Analysis 📊')
    save_data_to_session_state()

    df = st.session_state["game_data"]
    st.write(df)
