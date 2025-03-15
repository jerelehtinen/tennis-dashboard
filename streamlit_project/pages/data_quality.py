import streamlit as st



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


def date_filter():
    # Create a date filter
    st.sidebar.header("Filter by Date Range")
    min_date = df["start_date"].min()
    max_date = df["start_date"].max()

    date_range = st.sidebar.date_input(
        "Select Date Range", 
        [min_date, max_date], 
        min_value=min_date, 
        max_value=max_date
    )

    # filter df only if both dates are selected
    filtered_df = df
    if(len(date_range) == 2):    
        filtered_df = df[
            (df["start_date"].dt.date >= date_range[0]) & (df["start_date"].dt.date <= date_range[1])
        ]

    return filtered_df


def player_filter():
    st.sidebar.header("Filter by Player")

if __name__ == "__main__":
    st.title("Data quality")
    st.write("Validate data quality")

    if "data" in st.session_state:
        df = st.session_state["data"]

        # filter data
        filtered_df = date_filter()
        st.write(filtered_df)

        show_kpis(filtered_df)

    