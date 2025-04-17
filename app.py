# Libraries
import pandas as pd
import openai
import matplotlib.pyplot as plt
import os
import streamlit as st
from datetime import datetime
from pyngrok import ngrok
from dotenv import load_dotenv



# Step 1: Set up the OpenAI API Key
load_dotenv()
openai.api_key = os.getenv('OPEN_AI') 
if not openai.api_key:
    st.error("OpenAI API key not found. Set it as an environment variable 'OPEN_AI'.")
    st.stop()

# Step 2: Streamlit app setup
st.title("Duty-Free Sales Dashboard📊")
st.markdown("Build by Adriana PyArch for Travel Retail Romania! Analyze sales, trends and AI-powered promos 🚀")

# Step 3: File uploader
st.sidebar.header("Upload Data (Optional)")
uploaded_sales = st.sidebar.file_uploader("Upload Sales Data (Excel)", type=["xlsx"])
uploaded_promo = st.sidebar.file_uploader("Upload Promo Data (CSV)", type=["csv"])

# Step 4: Load data
@st.cache_data
def load_data(sales_file=None, promo_file=None):
    try:
        if sales_file:
            df = pd.read_excel(sales_file)
        else:
            df = pd.read_excel("duty_free_sales.xlsx")
        if promo_file:
            promo_df = pd.read_csv(promo_file)
        else:
            promo_df = pd.read_csv("promo.csv")
    except FileNotFoundError:
        st.error("Files not found. Upload the files here, please.")
        # Initialize empty DataFrames
        df = pd.DataFrame()
        promo_df = pd.DataFrame()
        st.stop()
    return df, promo_df

df, promo_df = load_data(uploaded_sales, uploaded_promo)

# Step 5: Mock external data (RAG)
external_data = pd.DataFrame({
    "Date": ["2025-05-01", "2025-05-15", "2025-06-01", "2025-06-10", "2025-06-20"],
    "Trend": [
        "20% increase predicted",
        "Summer duty-free promos trending",
        "Children's day, 1 June, Chocolate and Toys Boost",
        "Season festival boosts spirits",
        "Luxury sunglasses demand up"
    ]
})

# Step 6 Modular functions
def validate_data(dataframe):
    if len(dataframe) != 1000 or dataframe["Units Sold"].sum() != 31264:
        st.error("Data mismatch: Expected 1000 rows, 31264 units")
        return False
    return True

def predict(dataframe, external_data):
    avg_revenue = dataframe["Revenue (RON)"].sum() / 61  # Full period
    may_boost = 1.2  # 20% boost from travel
    june_boost = 1.15  # June 15% from festivals
    june_1_boost = june_boost + 0.1
    if "Chocolate and Toys Boost" in external_data["Trend"].values:
        june_1_boost += 0.05  # Extra 5% for June 1
    return {
        "May": avg_revenue * 31 * may_boost,
        "June": avg_revenue * 30 * june_boost,
        "June 1": avg_revenue * 1 * june_1_boost  # Extra spike
    }

def summarize(dataframe, trends, promo_data, external_data):
    try:
        total_revenue = dataframe["Revenue (RON)"].sum()
        total_margin = dataframe["Margin (RON)"].sum()
        total_units = dataframe["Units Sold"].sum()
        top_products = dataframe.groupby("Product")["Revenue (RON)"].sum().nlargest(3)

        # Step 7: Create a prompt for OpenAI
        prompt = (
            f"Travel Retail Romania - Duty-free sales report (March 1 - April 30, 2025):\n:"
            f"Total Revenue: {total_revenue:.2f} RON\n"
            f"Total Margin: {total_margin:.2f} RON\n"
            f"Total units sold: {total_units}\n"
            f"Top 3 Products:\n{top_products}\n"
            f"Trends:\n{trends.head(10)}...\n"
            f"Promo data:\n{promo_data}\n"
            f"External Trends:\n{external_data}\n"

            f"""Predict May 2025 sales, June 2025 sales, and June 1,
            2025 sales (highlight Children's Day chocolate/toys boost with 
            a specific revenue estimate e.g., ~147K RON). Suggest 3 promos for May and 3 for June, tailored to trends. 
            Focus on insights, avoid repeating numbers."""
        )

        # Use the new API interface
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful sales analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Error generating AI insights: {e}")
        return None

# Step 8: Sidebar for navigation
st.sidebar.header("Explore the Data")
options = ["Overview", "Trends", "Predictions", "Promos"]
choice = st.sidebar.selectbox("Select View", options)

#Step 9:Display content based on the selected option | Dashboard views
if choice == "Overview":
    st.header("Sales Overview")
    if validate_data(df):
        st.write(f"Total Revenue: {df['Revenue (RON)'].sum():.2f} RON")
        st.write(f"Total Margin: {df['Margin (RON)'].sum():.2f} RON")
        st.write(f"Total Units Sold: {df['Units Sold'].sum()}")
        top_products = df.groupby("Product")["Revenue (RON)"].sum().nlargest(3)
        st.write("**Top 3 Products**:")
        st.write(top_products)
        st.write("**Sample Data**")
        st.write(df.head())
    st.write("Overview trends are being analyzed...")  

elif choice == "Trends":
    st.header("Daily Sales Trends")
    daily_trends = df.groupby("Date")[["Revenue (RON)", "Margin (RON)"]].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(daily_trends.index, daily_trends["Revenue (RON)"], label="Revenue (RON)", color="blue")
    ax.plot(daily_trends.index, daily_trends["Margin (RON)"], label="Margin (RON)", color="green")
    ax.set_title("Daily Sales Trends (March 1 - April 30, 2025)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount (RON)")
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    fig.tight_layout()
    st.pyplot(fig)
    st.write("Trends data fetched successfully.")  

elif choice == "Predictions":
    st.header("Sales Predictions")
    predictions = predict(df, external_data)
    st.write(f"**May 2025**: {predictions['May']:.2f} RON")
    st.write(f"**June 2025**: {predictions['June']:.2f} RON")
    st.write(f"**June 1, 2025 (Children's Day)**: {predictions['June 1']:.2f} RON")
    st.write("Predictions generated based on external trends.")  

elif choice == "Promos":
    st.header("AI-Powered Promo Suggestions")
    with st.spinner("Generating AI insights..."):
        summary = summarize(df, df.groupby("Date")[["Revenue (RON)", "Margin (RON)"]].sum(), promo_df, external_data)
        st.write(summary)
    st.write("Promo suggestions are powered by AI.")  

#Step 10: External trends
st.sidebar.header("External Trends")
st.sidebar.write(external_data)


# Step 11: Footer
st.markdown("---")
st.markdown("👩‍💻 Built by Adriana PyArch for Travel Retail Romania")