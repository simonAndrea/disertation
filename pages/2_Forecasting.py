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
    
def seasonality_plotting(formatted_data):
    try:
        with st.spinner('Generating seasonality plots...'):
            r_seasonality_func = robjects.globalenv['seasonality_checking']
            seasonality_obj = r_seasonality_func(formatted_data)

            weekly_plot = seasonality_obj['weekly_json'][0]
            monthly_plot = seasonality_obj['monthly_json'][0]


            weekly_fig_dict = json.loads(weekly_plot)
            monthly_fig_dict = json.loads(monthly_plot)
            
            # Remove frames and fix marker properties
            for trace in weekly_fig_dict["data"]:
                trace.pop("frame", None)
                if "marker" in trace:
                    if "colorbar" in trace["marker"]:
                        # Keep only valid colorbar properties
                        valid_colorbar = {}
                        if "ticktext" in trace["marker"]["colorbar"]:
                            valid_colorbar["ticktext"] = trace["marker"]["colorbar"]["ticktext"]
                        if "tickvals" in trace["marker"]["colorbar"]:
                            valid_colorbar["tickvals"] = trace["marker"]["colorbar"]["tickvals"]
                        # Replace the colorbar with cleaned version
                        trace["marker"]["colorbar"] = valid_colorbar

            # Do the same for monthly data
            for trace in monthly_fig_dict["data"]:
                trace.pop("frame", None)
                if "marker" in trace:
                    if "colorbar" in trace["marker"]:
                        valid_colorbar = {}
                        if "ticktext" in trace["marker"]["colorbar"]:
                            valid_colorbar["ticktext"] = trace["marker"]["colorbar"]["ticktext"]
                        if "tickvals" in trace["marker"]["colorbar"]:
                            valid_colorbar["tickvals"] = trace["marker"]["colorbar"]["tickvals"]
                        trace["marker"]["colorbar"] = valid_colorbar

            # Create separate Plotly figures from the dictionaries
            weekly_fig = go.Figure(weekly_fig_dict["data"])
            monthly_fig = go.Figure(monthly_fig_dict["data"])

            # Create a subplot figure with 2 rows
            fig = make_subplots(
                rows=2, cols=1, 
                shared_xaxes=False,
                vertical_spacing=0.2,
                subplot_titles=["Weekly Seasonality", "Monthly Seasonality"]
            )

            # Add traces for weekly data to the first row
            for trace in weekly_fig.data:
                fig.add_trace(trace, row=1, col=1)

            # Add traces for monthly data to the second row
            for trace in monthly_fig.data:
                fig.add_trace(trace, row=2, col=1)

            # Update layout with fixed styling
            fig.update_layout(
                height=800,
                yaxis=dict(
                    title="Value",
                    showgrid=True,
                    gridcolor='rgba(128, 128, 128, 0.2)'
                ),
                yaxis2=dict(
                    title="Value",
                    showgrid=True,
                    gridcolor='rgba(128, 128, 128, 0.2)'
                ),
                plot_bgcolor="white",
                paper_bgcolor="white",
                showlegend=True,
                font=dict(color="black"),
                margin=dict(t=100)
            )

            # Update x-axes separately
            fig.update_xaxes(showgrid=True, gridcolor='rgba(128, 128, 128, 0.2)', row=1, col=1)
            fig.update_xaxes(showgrid=True, gridcolor='rgba(128, 128, 128, 0.2)', row=2, col=1)

            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    except Exception as e:
        st.error(f"Error generating seasonality plots: {str(e)}")
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

        seasonality_plotting(formatted_data)

r_code()

