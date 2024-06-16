import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt

def display_map(df: pd.DataFrame):
    st.header("Map of production places")
    color_scale = [(0, 'red'), (0.25,'orange'), (0.5,'black'), (0.75,'brown'), (1,'pink')]
    fig = px.scatter_mapbox(df, 
                            lat="latitude", 
                            lon="longitude", 
                            hover_name="system_id", 
                            hover_data=["system_id", "name", "address", "last_output", "system_DC_capacity_W", "country"],
                            color="num_outputs",
                            color_continuous_scale=color_scale,
                            #size="num_outputs",
                            zoom=3, 
                            height=750,
                            width=1000)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    # Load ids dataframe
    df = pd.read_csv("./data/ids.csv")

    st.set_page_config(layout="wide")

    # Set title
    st.markdown("<h1 style='text-align: center;'>PVOutput dataset analysis</h1>", unsafe_allow_html=True)
    #st.title("PVOutput dataset analysis")
    st.divider()

    # Raw dataframe
    st.header("Raw data - PVOutput ids")
    st.dataframe(df, use_container_width=True)
    st.divider()

    # Display map
    display_map(df)
    st.divider()

    # Display statistics
    st.header("Data statistics")
    col0, col1, col2, col3 = st.columns(4)
    col0.metric(label="Number of sites", value=f"{len(df.index)} sites")
    col1.metric(label="Coutries count", value=f"{len(np.unique(df['country']))} countries")
    col2.metric(label="Average number of outputs", value=f"{int(df.loc[:, 'num_outputs'].mean())} outputs")
    col3.metric(label="Average capacity", value=f"{int(df.loc[:, 'system_DC_capacity_W'].mean())} W")
    st.divider()


    # Data charts
    st.header("Data charts")
    st.subheader("Distribution by country")
    st.bar_chart(df["country"].value_counts(), color="#ab1b11cc", height=600)