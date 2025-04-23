import streamlit as st
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter
from datetime import datetime, timedelta
import queries
import pandas as pd
import json
from rpy2.robjects import StrVector
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

pandas2ri.activate()

def get_data():
    data = queries.get_forecast_data()
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.sort_values('Date')
    return data

def excel_date_to_datetime(excel_date):
                    base_date = datetime(1970, 1, 1)
                    delta = timedelta(days=excel_date - 2)  # Excel has a leap year bug
                    return base_date + delta


def convert_x_to_dates(x_values):
    return [excel_date_to_datetime(x).strftime('%Y-%m-%d') if x is not None else None for x in x_values]

def time_series_plotting(formatted_data):
    try:
        with st.spinner('Generating time series plots...'):              
            r_plot_func = robjects.globalenv['data_plotting']
            plot_obj = r_plot_func(formatted_data)
                
            fig_dict = json.loads(plot_obj['x']['data'][0])
               
            for trace in fig_dict["data"]:
                trace.pop("frame", None) 

            fig = go.Figure(data=fig_dict["data"])
            fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1)

            for idx, trace in enumerate(fig_dict["data"]):
                row = idx + 1  # Adjust the row number for each trace
                fig.add_trace(
                    go.Scatter(
                        x=convert_x_to_dates(trace["x"]),
                        y=trace["y"],
                        mode=trace["mode"],
                        line=trace["line"],
                        text=trace["text"],
                        hoverinfo=trace["hoverinfo"],
                        showlegend=trace["showlegend"],
                    ),
                    row=row, col=1 
                )

            fig.update_layout(
                font=dict(
                    color="black"  # Optional: set font color
                ),
                yaxis=dict(
                    title="Total Sales"
                )
            )

            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    except Exception as e:
            st.error(f"Error generating plots: {str(e)}")
            st.error(f"Error type: {type(e).__name__}")
            st.error(f"Error details: {str(e)}")
            return None

def r_code():
    with localconverter(robjects.default_converter + pandas2ri.converter):
        with open('forecasting.R', 'r') as f:
            r_script = f.read()

        robjects.r(r_script)
        data = get_data()

        # Format data using R function
        format_data = robjects.globalenv['format_data']
        formatted_data = format_data(data)

        time_series_plotting(formatted_data)

        

r_code()

