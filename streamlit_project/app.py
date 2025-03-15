import streamlit as st
import duckdb


def read_data_to_session_state() -> None:
    """
    Read data from the database and store it in the session state.
    """

    if "data" not in st.session_state:
        conn = duckdb.connect('/data/tennisdb.duckdb')
        query = "select * from tennis_publish.played_matches"
        df = conn.execute(query).fetch_df()
        conn.close()
        st.session_state["data"] = df
        print("Data loaded into session state")




if __name__ == "__main__":
    st.set_page_config(page_title="Tennis Dashboard 🎾", layout="wide")
    st.title('Analysis 📊')
    read_data_to_session_state()

    df = st.session_state["data"]
    st.write(df)
