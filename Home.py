import os, pyodbc, pandas as pd, streamlit as st, matplotlib.pyplot as plt
from dotenv import load_dotenv

st.set_page_config(
    page_title="OptiView",
    page_icon=":chart_with_upwards_trend:",
)

#Using CSS file
with open('main_style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.title(":chart_with_upwards_trend: Welcome to OptiView!")


st.markdown("<hr style='border-top: 1px solid #d3d3d3; opacity: 0.5;'>", unsafe_allow_html=True)

st.subheader("Key Features:")
st.write("**Data Visualization:** Transform complex data sets into clear, intuitive visual representations that facilitate understanding and strategic decision-making across your organization.")
st.write("**Data Analysis:** Leverage advanced analytical tools to explore key performance indicators, identify trends, and uncover actionable insights that drive operational optimization.")
st.write("**Forecasting:** Utilize powerful predictive models to anticipate market fluctuations, forecast future business performance, and refine your long-term strategy.")