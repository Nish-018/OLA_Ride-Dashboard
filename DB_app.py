import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sqlalchemy import create_engine # pyright: ignore[reportMissingImports]

def load_css():
    st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #2c2f4a, #4a5ea8);
        color: #ffffff;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f2235, #2c2f4a);
    }

    .metric-card {
        background: #0f172a;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        text-align: center;
    }

    .metric-title {
        font-size: 14px;
        color: #94a3b8;
    }

    .metric-value {
        font-size: 36px;
        font-weight: bold;
        color: white;
    }
                
                
    </style>
    """, unsafe_allow_html=True)




st.set_page_config(
    page_title="OLA Ride Analytics",
    layout="wide"
)

load_css()

df = pd.read_csv("D:\Labmentrix Projects\Jupyter\OLA_Dataset.csv")  

st.sidebar.markdown("## 🔍 Filters")

booking_status = st.sidebar.multiselect(
    "Booking Status",
    options=sorted(df["Booking_Status"].dropna().unique()),
    placeholder="Choose options",
    key="filter_booking_status"
)

vehicle_type = st.sidebar.multiselect(
    "Vehicle Type",
    options=sorted(df["Vehicle_Type"].dropna().unique()),
    placeholder="Choose options",
    key="filter_vehicle_type"
)

payment_method = st.sidebar.multiselect(
    "Payment Method",
    options=sorted(df["Payment_Method"].dropna().unique()),
    placeholder="Choose options",
    key="filter_payment_method"
)



col1, col2 = st.columns([1, 6])

with col1:
    st.image("D:/Labmentrix Projects/Jupyter/Olalogo.png", width=160)

with col2:
    st.markdown("## Ride Analytics Dashboard")


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overall", "Vehicle Type", "Revenue", "Cancellation", "Ratings"
])


def kpi(title, value):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)



# DB connection
engine = create_engine("postgresql+psycopg2://postgres:Chia2@localhost:5432/ola_ride")
with tab1:
    st.header("Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        kpi("Total Rides", 4597)
    with col2:
        kpi("Completed Rides", 4314)
    with col3:
        kpi("Incomplete Rides", 283)
    with col4:
        kpi("Cancelled Rides", 0)
    with col5:
        kpi("Cancellation Rate (%)", "0.0")
    

# Overall Trends

    st.header("Overall Ride Trends")
    fig = px.line(df.groupby("Booking_Date").size().reset_index(name="total_rides"),x="Booking_Date",y="total_rides",
    title="Overall Ride Trends",
    labels={"Booking_Date": "Date","total_rides": "Number of Rides"})
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("📄 OLA Ride Data Preview")
    st.dataframe(df, use_container_width=True)


    top_customers = pd.read_sql("""SELECT "Customer_ID",SUM("Booking_Value"::NUMERIC) AS total_spent FROM public.ola
    WHERE "Booking_Status" = 'Success' GROUP BY "Customer_ID" ORDER BY total_spent DESC LIMIT 5;""", engine)
    st.title("Top 5 customers")
    st.dataframe(top_customers)

    
    

    
# Vehicle Type

with tab2:
    st.title("Vehicle Type Analysis")
    vehicle_df = (df.groupby("Vehicle_Type", as_index=False)["Ride_Distance"].sum())
    fig = px.bar(vehicle_df,x="Vehicle_Type",y="Ride_Distance",text="Ride_Distance",
    labels={"Vehicle_Type": "Vehicle Type","Ride_Distance": "Total Ride Distance (km)"})
    st.plotly_chart(fig, use_container_width=True)

# Revenue

with tab3:
    st.header("Revenue Analysis")
    revenue_df = (df[df["Booking_Status"] == "Success"].groupby("Payment_Method", as_index=False)["Booking_Value"].sum().rename(columns={"Booking_Value": "revenue"}))
    fig = px.bar(revenue_df,x="Payment_Method",y="revenue",text="revenue",title="Revenue by Payment Method",
    labels={"Payment_Method": "Payment Method","revenue": "Total Revenue (₹)"})
    fig.update_traces(texttemplate="₹ %{text:,.0f}", textposition="outside")
    fig.update_layout(plot_bgcolor="#0f172a",paper_bgcolor="#0f172a",font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

    st.title("Ride Distance")
    
    ride_distance_df = (df.groupby("Booking_Date", as_index=False)["Ride_Distance"].sum())
    
    import plotly.express as px
    fig = px.line(ride_distance_df, x="Booking_Date", y="Ride_Distance",title="Ride Distance Trend",
    labels={ "Booking_Date": "Date","Ride_Distance": "Total Ride Distance (km)"})
    
    st.plotly_chart(fig, use_container_width=True)

# Cancellation

with tab4:
    st.header("Cancellation Analysis")
    cust_cancel_df = (df[(df["Booking_Status"] == "Canceled by Customer") &(df["Canceled_Rides_by_Customer"].notna())].groupby("Canceled_Rides_by_Customer", as_index=False).size().rename(columns={"size": "Total"}))
    fig1 = px.bar(
    cust_cancel_df,
    x="Canceled_Rides_by_Customer",
    y="Total",
    text="Total",
    title="Customer Cancellation Reasons",
    labels={
        "Canceled_Rides_by_Customer": "Cancellation Reason",
        "Total": "Number of Rides"})
    fig1.update_traces(marker_color="#38bdf8",texttemplate="%{text:,}",textposition="outside")
    fig1.update_layout(plot_bgcolor="#0f172a",paper_bgcolor="#0f172a",font=dict(color="white"),title_font_size=24,
    xaxis=dict( tickangle=-35,showgrid=False),
    yaxis=dict(showgrid=True,gridcolor="rgba(255,255,255,0.1)"))
    st.plotly_chart(fig1, use_container_width=True)

    driver_cancel_df = (df[(df["Booking_Status"] == "Canceled by Driver") &(df["Canceled_Rides_by_Driver"].notna())].groupby("Canceled_Rides_by_Driver", as_index=False).size().rename(columns={"size": "Total"}))
    fig2 = px.bar(driver_cancel_df,x="Canceled_Rides_by_Driver",y="Total",text="Total",title="Driver Cancellation Reasons",
    labels={"Canceled_Rides_by_Driver": "Cancellation Reason","Total": "Number of Rides"})
    fig2.update_traces( marker_color="#387a7d",texttemplate="%{text:,}",textposition="outside")
    fig2.update_layout(plot_bgcolor="#0f172a",paper_bgcolor="#0f172a",
    font=dict(color="white"),title_font_size=24,
    xaxis=dict(tickangle=-35,showgrid=False),
    yaxis=dict(showgrid=True,gridcolor="rgba(255,255,255,0.1)"))
    st.plotly_chart(fig2, use_container_width=True)
    
# Ratings

with tab5:
    st.title("Driver Ratings")
    driver_ratings = pd.read_sql("""SELECT "Driver_Ratings"::NUMERIC FROM public.ola
    WHERE "Driver_Ratings" IS NOT NULL
      AND "Driver_Ratings" <> 'null'; """, engine)
    fig, ax = plt.subplots()
    sns.histplot(driver_ratings["Driver_Ratings"], bins=5, ax=ax)
    st.pyplot(fig)
    st.title("Customer Ratings")
    customer_ratings = pd.read_sql("""SELECT "Customer_Rating"::NUMERIC FROM public.ola WHERE "Customer_Rating" IS NOT NULL
      AND "Customer_Rating" <> 'null';""", engine)
    fig, ax = plt.subplots()
    sns.histplot(customer_ratings["Customer_Rating"], bins=5, ax=ax)
    st.pyplot(fig)
