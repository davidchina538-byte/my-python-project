import streamlit as st
import pandas as pd
import altair as alt  # ships with Streamlit, no extra install needed

# Days in calendar order (otherwise charts sort them alphabetically: Fri, Mon, Sat...)
DAY_ORDER = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

st.title("Ice Cream Shop: Weekly Sales")


# --- Load data -------------------------------------------------------------
# @st.cache_data loads the file once instead of on every rerun.
# Milestone 3: replace the pd.read_csv line with your boto3 + S3 code.
@st.cache_data
def load_data():
    return pd.read_csv("ice_cream_sales.csv")


df = load_data()

# --- Sidebar controls ------------------------------------------------------
st.sidebar.header("Filters")
flavor = st.sidebar.selectbox("Choose a flavor", sorted(df["Flavor"].unique()))
show_raw = st.sidebar.checkbox("Show raw data", value=False)

filtered = df[df["Flavor"] == flavor]

# --- Summary numbers -------------------------------------------------------
best_row = filtered.loc[filtered["ScoopsSold"].idxmax()]
col1, col2, col3 = st.columns(3)
col1.metric("Total scoops", int(filtered["ScoopsSold"].sum()))
col2.metric("Daily average", round(filtered["ScoopsSold"].mean(), 1))
col3.metric("Best day", best_row["Day"], f"{best_row['ScoopsSold']} scoops")

# --- Chart for the selected flavor ----------------------------------------
st.subheader(f"Scoops of {flavor} sold each day")
chart = (
    alt.Chart(filtered)
    .mark_bar()
    .encode(
        x=alt.X("Day", sort=DAY_ORDER),
        y="ScoopsSold",
        tooltip=["Day", "ScoopsSold"],
    )
)
st.altair_chart(chart, use_container_width=True)

# --- Compare all flavors ---------------------------------------------------
st.subheader("All flavors compared")
compare = (
    alt.Chart(df)
    .mark_line(point=True)
    .encode(
        x=alt.X("Day", sort=DAY_ORDER),
        y="ScoopsSold",
        color="Flavor",
        tooltip=["Day", "Flavor", "ScoopsSold"],
    )
)
st.altair_chart(compare, use_container_width=True)

# --- Optional raw data -----------------------------------------------------
if show_raw:
    st.write(f"Rows for {flavor}:")
    st.dataframe(filtered, hide_index=True)
    st.write("Full dataset:")
    st.dataframe(df, hide_index=True)
