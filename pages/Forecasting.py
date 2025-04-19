import os, pyodbc, pandas as pd, streamlit as st, plotly.express as px
from datetime import timedelta
import queries
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="OptiView",
    page_icon=":chart_with_upwards_trend:",
)

#Using CSS file
with open('main_style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.title(":mag_right: Forecasting")