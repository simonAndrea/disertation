import os, pyodbc, pandas as pd, streamlit as st, plotly.express as px
from datetime import timedelta
import queries

st.set_page_config(
    page_title="OptiView",
    page_icon=":chart_with_upwards_trend:",
)

#Using CSS file
with open('main_style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.title(":bar_chart: Visualization Dashboards")

st.subheader('Total Sales Over Time')

def plot_sales_data(data, title):
    fig = px.line(data, x='Date', y='TotalSales', title=title)
    fig.update_traces(line=dict(color='#1C4E80'))
    fig.update_layout(
        xaxis=dict(
            tickfont=dict(color='#202020', size=14),
            title_font=dict(color='#202020'),
            tickformat='%Y-%m-%d'  # Format the date to show only year-month-day
        ),
        yaxis=dict(
            tickfont=dict(color='#202020', size=14),
            title_font=dict(color='#202020')
        )
    )
    st.plotly_chart(fig)


# Caching function for loading data (to prevent unnecessary reruns)
@st.cache_data(ttl=300, show_spinner=False)  # 5 minutes cache
def load_all_sales_data():
    all_data = queries.get_sales_data()
    all_data['Date'] = pd.to_datetime(all_data['Date'])
    return all_data

# Function that wraps everything (including session state management)
def date_range_plot():
    # Load all data to get max/min dates
    all_data = queries.get_sales_data()
    all_data['Date'] = pd.to_datetime(all_data['Date'])

    if all_data.empty:
        st.warning("No data available.")
        st.stop()

    max_date = all_data['Date'].max().date()
    min_date = all_data['Date'].min().date()

    # --- UI Section for Date Range ---
    st.markdown("#### Select Date Range")

    # Create 3 columns: start date, end date, and button
    col1, col2, col3 = st.columns([3, 3, 3])

    with col1:
        start_date = st.date_input(
            "Start Date",
            value=max_date - timedelta(days=6),
            min_value=min_date,
            max_value=max_date
        )

    with col2:
        end_date = st.date_input(
            "End Date",
            value=max_date,
            min_value=start_date,
            max_value=max_date
        )

    with col3:
        load_data = st.button("Load Sales Data")

    # Update the plot without rerunning the entire page
    if load_data:
        with st.spinner(f'Loading sales data from {start_date} to {end_date}...'):
            data = queries.get_sales_data(start_date=start_date, end_date=end_date + timedelta(days=1))
            if data.empty:
                st.info("No sales data found for the selected range.")
            else:
                plot_sales_data(data, f"Total Sales from {start_date} to {end_date}")

# --- Main ---
date_range_plot()

# Create a separator between the two visualizations
st.markdown("---")

# Top 10 Products section
st.subheader('Top 10 Products')

# Cache the top 10 products data
@st.cache_data(ttl=300, show_spinner=False)  # 5 minutes cache
def cached_top_10():
    return queries.getTop10Products()

def plotTopProducts():
    data = cached_top_10()
    fig = px.treemap(data,
                     path=['ItemName'], 
                     values='count',
                     color='count')
    st.plotly_chart(fig)

with st.spinner('Loading top 10 products...'):
    plotTopProducts()


#SITE PERFORMANCE
st.subheader('Site Performance by Total Amount')

def plotSitePerformance():
    data = queries.getSitePerformance()
    data['SiteId'] = data['SiteId'].astype(str)

    # Plot
    fig = px.bar(
        data,
        x='TotalAmount',
        y='SiteId',
        orientation='h',
        labels={'SiteId': 'Site', 'TotalAmount': 'Total Amount'},
    )

    fig.update_traces(marker_color='#153d64')

    fig.update_layout(
        yaxis_type='category',
        yaxis=dict(
            tickfont=dict(color='#000000', size=14),
            title_font=dict(color='#000000', size=14),
        ),
        xaxis=dict(
            tickfont=dict(color='#000000',size=14),
            title_font=dict(color='#000000', size=14),
        ))
    st.plotly_chart(fig)

with st.spinner('Loading site performance...'):
    plotSitePerformance()

#PAYMENT METHIODS
def plot_payment_methods(selected_date=None):
    data = queries.getPaymentMethodsByDateAndSite(selected_date)
    data['SiteId'] = data['SiteId'].astype(str)
    data['TotalPayment'] = data['TotalPayment'].astype(float)
    data['CashAmount'] = data['CashAmount'].astype(float)
    data['CardAmount'] = data['CardAmount'].astype(float)
    data['TicketAmount'] = data['TicketAmount'].astype(float)
    
    if data.empty:
        st.info("No payment data available for selected date.")
        return

    # Create stacked bar chart
    fig = px.bar(data, 
                 x='SiteId', 
                 y=['CashAmount', 'CardAmount', 'TicketAmount'],
                 labels={'value': 'Number of Transactions', 'SiteId': 'Site ID'},
                 color_discrete_sequence=['#0091D5', '#EA6A47', '#1C4E80'])
    
    fig.update_layout(
        xaxis_title="Site ID",
        yaxis_title="Number of Transactions",
        legend_title="Payment Method",
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        xaxis_type='category',
        yaxis=dict(
            tickfont=dict(color='#000000', size=14),
            title_font=dict(color='#000000', size=14),
        ),
        xaxis=dict(
            tickfont=dict(color='#000000',size=14),
            title_font=dict(color='#000000', size=14),
        ))
    
    
    st.plotly_chart(fig)


def plot_payment_method_distribution(selected_date=None):
    data = queries.getPaymentMethodsByDateAndSite(selected_date)

    # Assume data has a single row with columns: 'CashAmount', 'CardAmount', 'TicketAmount'
    payment_data = {
        'PaymentMethod': ['CashAmount', 'CardAmount', 'TicketAmount'],
        'Amount': [
            data['CashAmount'].sum(),
            data['CardAmount'].sum(),
            data['TicketAmount'].sum()
        ]
    }
    df = pd.DataFrame(payment_data)

    fig = px.pie(
        df,
        values='Amount',
        names='PaymentMethod',
        hole=0.6,
        color_discrete_sequence=['#0091D5', '#EA6A47', '#1C4E80'])

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        showlegend=True,
        legend_title="Payment Method",
        legend=dict(bgcolor='rgba(0,0,0,0)')
    )

    st.plotly_chart(fig)

st.subheader('Payment Methods Analysis')

# Place the date input above the charts
selected_date = st.date_input(
    "#### Select Date",
    value=pd.Timestamp('2020-07-01').date(),
    min_value=pd.Timestamp('2020-07-01').date(),
    max_value=pd.Timestamp('2022-06-30').date()
)

# Convert date once for both charts
selected_date = pd.to_datetime(selected_date).date()

with st.spinner('Loading payment methods data...'):
    plot_payment_methods(selected_date)

with st.spinner('Loading payment method distribution...'):
    plot_payment_method_distribution(selected_date)


#MEMBERSHIP
st.subheader('Membership Card Performance')

def plot_membership_performance():
    # Get data
    data = queries.getMembership()
    
    # Create membership type labels
    data['member_type'] = data['CardTypeId'].map({
        17: 'Employee',
        24: 'Fidelity',
        None: 'No Card'
    }).fillna('No Card')
    
    # Create box plot
    fig = px.violin(
        data,
        x="member_type",
        y="TotalPayment",
        color="member_type",
        box=True,  # Still shows inner box plot
        points="suspectedoutliers",  # Or False to hide outliers
        color_discrete_sequence=['#1C4E80', '#0091D5', '#EA6A47'],
        title="Cart Value Distribution by Membership Type (Violin Plot)"
    )
    
    # Update layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,  # Hide legend since color shows membership type
        xaxis_title="Membership Type",
        yaxis_title="Cart Value",
        xaxis=dict(
            tickfont=dict(color='#202020', size=14),
            title_font=dict(color='#202020', size=14),
        ),
        yaxis=dict(
            tickfont=dict(color='#202020', size=14),
            title_font=dict(color='#202020', size=14),
        )
    )
    
    st.plotly_chart(fig)

with st.spinner('Loading membership performance...'):   
    plot_membership_performance()
# Create a separator between the two visualizations


def plot_membership_histogram():
    # Add dropdown for membership type selection
    membership_type = st.selectbox(
        "Select Membership Type",
        options=['Employee', 'Fidelity', 'No Card'],
        key='membership_histogram_selector'
    )
    
    # Get filtered data based on selection
    data = queries.getMembershipForHistogram(membership_type)
    
    if data.empty:
        st.info("No data available for selected membership type.")
        return
    
    # Create histogram
    fig = px.histogram(
        data,
        x="TotalPayment",
        nbins=100,  # Adjust number of bins
        opacity=0.75,
        color_discrete_sequence=['#0091D5'],
        title=f"Distribution of Cart Values - {membership_type} Members",
        labels={"TotalPayment": "Cart Value"}
    )
    
    # Update layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        bargap=0.1,
        xaxis_title="Cart Value",
        yaxis_title="Count",
        showlegend=False,
        xaxis=dict(
            tickfont=dict(color='#202020', size=14),
            title_font=dict(color='#202020', size=14),
        ),
        yaxis=dict(
            tickfont=dict(color='#202020', size=14),
            title_font=dict(color='#202020', size=14),
        )
    )
    
    st.plotly_chart(fig)

with st.spinner('Loading histogram...'):
        plot_membership_histogram()