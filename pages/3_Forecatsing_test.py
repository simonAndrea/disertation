import streamlit as st
import subprocess
import plotly.graph_objs as go
from plotly.subplots import make_subplots  # Add this import
import json

st.set_page_config(
    page_title="OptiView",
    page_icon=":chart_with_upwards_trend:",
)

# Using CSS file
with open('main_style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.title(":mag_right: Forecasting")

st.subheader("Time Series Plots")

try:
    with st.spinner('Generating time series plots...'):
        # Run the R script and capture its output
        process = subprocess.Popen(
            ["Rscript", "time_series_ploting.R"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            st.error(f"Error running R script: {stderr}")
        else:
            # Parse the JSON output from stdout
            json_start = stdout.find('{')
            if json_start >= 0:
                json_str = stdout[json_start:]
                plot_data = json.loads(json_str)
                
                # Create figure with 3 subplots
                fig = make_subplots(
                    rows=3, 
                    cols=1,
                    subplot_titles=("Daily Value", "Weekly Value", "Monthly Value"),
                    shared_xaxes=True,
                    vertical_spacing=0.1
                )
                
                # Add traces to appropriate subplots
                for i, trace in enumerate(plot_data['data'], 1):
                    if 'frame' in trace:
                        trace.pop('frame')
                    fig.add_trace(
                        go.Scatter(
                            x=trace.get('x', []),
                            y=trace.get('y', []),
                            mode=trace.get('mode', 'lines'),
                            name=trace.get('name', ''),
                            line=trace.get('line', {})
                        ),
                        row=i,
                        col=1
                    )
                
                # Update layout
                fig.update_layout(
                    height=900,
                    showlegend=False
                )
                
                # Display the figure
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("No valid JSON found in R script output")

except Exception as e:
    st.error(f"Error: {str(e)}")

st.subheader("Weekly Seasonality")
try:
    with st.spinner('Generating weekly seasonality plot...'):
        # Run the R script and capture its output
        process2 = subprocess.Popen(
            ["Rscript", "seasonality_plotting.R"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process2.communicate()

        if process2.returncode != 0:
            st.error(f"Error running R script: {stderr}")
        else:
            # Parse the JSON output from stdout
            json_start = stdout.find('{')
            if json_start >= 0:
                json_str = stdout[json_start:]
                plot_data = json.loads(json_str)
                
                fig = go.Figure()
                
                # Add trace
                fig.add_trace(
                    go.Line(
                        x=plot_data['data'][0].get('x', []),
                        y=plot_data['data'][0].get('y', [])
                    )
                )
                
                # Update layout
                fig.update_layout(
                    height=400,
                    showlegend=False,
                    xaxis_title="Day of Week",
                    yaxis_title="Average Value"
                    
                )
                
                # Display the figure
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("No valid JSON found in R script output")

except Exception as e:
    st.error(f"Error: {str(e)}")

st.subheader("ACF and PACF Plots")

try:
    with st.spinner('Generating ACF and PACF plots...'):
        process3 = subprocess.Popen(
            ["Rscript", "acf_plotting.R"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process3.communicate()

        if process3.returncode != 0:
            st.error(f"Error running R script: {stderr}")
        else:
            json_start = stdout.find('{')
            if json_start >= 0:
                json_str = stdout[json_start:]
                plot_data = json.loads(json_str)
                
                # Create figure with subplots
                fig = make_subplots(
                    rows=2, 
                    cols=1,
                    subplot_titles=("ACF", "PACF"),
                    vertical_spacing=0.2
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=plot_data['data'][0].get('x', []),
                        y=plot_data['data'][0].get('y', []),
                        mode='lines+markers',
                        name='ACF'
                    ),
                    row=1,
                    col=1
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=plot_data['data'][3].get('x', []),
                        y=plot_data['data'][3].get('y', []),
                        mode='lines+markers',
                        name='PACF'
                    ),
                    row=2,
                    col=1
                )
                
                # Update layout
                fig.update_layout(
                    height=600,
                    showlegend=False,
                    title_text="ACF and PACF Plots"
                )
                
                # Update y-axes labels
                fig.update_yaxes(title_text="ACF", row=1, col=1)
                fig.update_yaxes(title_text="PACF", row=2, col=1)
                
                # Display the figure
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("No valid JSON found in R script output")
except Exception as e:
    st.error(f"Error: {str(e)}")

st.subheader("Time Series Decomposition")

tab1, tab2 = st.tabs(["Classical Decomposition", "STL Decomposition"])
try:
    with tab1:
        with st.spinner('Generating classical decomposition plots ...'):
            process4 = subprocess.Popen(
                ["Rscript", "decomposition.R"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process4.communicate()
            if process4.returncode != 0:
                st.error(f"Error running R script: {stderr}")
            else:
                json_start = stdout.find('{')
                if json_start >= 0:
                    json_str = stdout[json_start:]
                    plot_data = json.loads(json_str)
                    # # Create figure with subplots
                    fig = make_subplots(
                        rows=4, 
                        cols=1,
                        subplot_titles=("Observed", "Trend", "Seasonal", "Residual"),
                        vertical_spacing=0.2
                    )
                    
                    for i in range(4):
                        fig.add_trace(
                            go.Scatter(
                                x=plot_data['data'][i].get('x', []),
                                y=plot_data['data'][i].get('y', []),
                                mode='lines',
                                name=plot_data['data'][i].get('name', '')
                            ),
                            row=i+1,
                            col=1
                        )
                    
                    # Update layout
                    fig.update_layout(
                        height=800,
                        showlegend=False
                    )
                    
                    # # Display the figure
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("No valid JSON found in R script output")

    with tab2:
        with st.spinner('Generating STL decomposition plots ...'):
            process4 = subprocess.Popen(
                ["Rscript", "stl_decomposition.R"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process4.communicate()
            if process4.returncode != 0:
                st.error(f"Error running R script: {stderr}")
            else:
                json_start = stdout.find('{')
                if json_start >= 0:
                    json_str = stdout[json_start:]
                    plot_data = json.loads(json_str)
                    # # Create figure with subplots
                    fig = make_subplots(
                        rows=4, 
                        cols=1,
                        subplot_titles=("Observed", "Trend", "Seasonal", "Residual"),
                        vertical_spacing=0.2
                    )
                    
                    for i in range(4):
                        fig.add_trace(
                            go.Scatter(
                                x=plot_data['data'][i].get('x', []),
                                y=plot_data['data'][i].get('y', []),
                                mode='lines',
                                name=plot_data['data'][i].get('name', '')
                            ),
                            row=i+1,
                            col=1
                        )
                    
                    # Update layout
                    fig.update_layout(
                        height=800,
                        showlegend=False
                    )
                    
                    # # Display the figure
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("No valid JSON found in R script output")

except Exception as e:
    st.error(f"Error: {str(e)}")


#FORECASTING
st.subheader("Forecasting")
arima, ets, rf, xgb = st.tabs(["ARIMA model", "Holt-Winter's model", "Random Forest model", "XGBoost model"])

with arima:
    try:
        with st.spinner('Generating ARIMA forecast...'):
            process5 = subprocess.Popen(
                ["Rscript", "arima.R"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process5.communicate()
            print(stdout)
            
            if process5.returncode != 0:
                st.error(f"Error running R script: {stderr}")
            else:
                json_start = stdout.find('{')
                if json_start >= 0:
                    json_str = stdout[json_start:]
                    plot_data = json.loads(json_str)
                    
                    # Create plotly figure
                    fig = go.Figure()
                    
                    # Add original data trace
                    fig.add_trace(
                        go.Scatter(
                            x=plot_data['original']['date'],
                            y=plot_data['original']['value'],
                            name='Original',
                            mode='lines',
                            line=dict(color='blue')
                        )
                    )
                    
                    # Add forecast trace
                    fig.add_trace(
                        go.Scatter(
                            x=plot_data['forecast']['date'],
                            y=plot_data['forecast']['value'],
                            name='Forecast',
                            mode='lines',
                            line=dict(color='red')
                        )
                    )
                    
                    # Update layout
                    fig.update_layout(
                        title="Forecast vs Original Values",
                        xaxis_title="Date",
                        yaxis_title="Value",
                        showlegend=True,
                        height=600
                    )
                    
                    # Display the figure
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("No valid JSON found in R script output")
    except Exception as e:
        st.error(f"Error: {str(e)}")
