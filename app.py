import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from db_config import get_psycopg_conn, get_engine

st.set_page_config(page_title="Customer Analytics", layout="wide")
st.title("📊 Customer Analytics Portal")
st.write("This dashboard loads cleaned data from Postgres and runs SQL queries dynamically.")

@st.cache_data
def load_data():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM customer_eda;", engine)
    df.columns = df.columns.str.lower()
    return df

with st.spinner("Loading data from Postgres..."):
    df = load_data()

st.success(f"Loaded {df.shape[0]} rows.")

def run_sql(query):
    conn = get_psycopg_conn()
    df_query = pd.read_sql(query, conn)
    conn.close()
    return df_query

tab_eda, tab_bq = st.tabs(["🔍 EDA Visualizations", "❓ Business Questions"])

with tab_eda:
    st.subheader("Preview of Cleaned Data")
    st.dataframe(df.head())

    st.markdown("### Summary Statistics")
    numeric_df = df.select_dtypes(include=[np.number])
    st.dataframe(numeric_df.describe())

    st.markdown("---")
    st.markdown("### Distributions")

    col1, col2 = st.columns(2)

    with col1:
        if "age" in df.columns:
            st.markdown("**Age distribution**")
            fig, ax = plt.subplots()
            sns.histplot(df["age"], kde=True, ax=ax)
            st.pyplot(fig)

    with col2:
        if "purchase_amount" in df.columns:
            st.markdown("**Purchase Amount Distribution**")
            fig, ax = plt.subplots()
            sns.histplot(df["purchase_amount"], kde=True, ax=ax)
            st.pyplot(fig)

    st.markdown("---")
    st.markdown("### Categorical")

    col3, col4, col5 = st.columns(3)

    with col3:
        if "gender" in df.columns:
            st.markdown("**Gender Distribution**")
            st.bar_chart(df["gender"].value_counts())

    with col4:
        if "category" in df.columns:
            st.markdown("**Top 10 Categories**")
            st.bar_chart(df["category"].value_counts().head(10))

    with col5:
        if "season" in df.columns:
            st.markdown("**Season Breakdown**")
            st.bar_chart(df["season"].value_counts())

    st.markdown("---")
    st.markdown("### Correlation Heatmap")
    if not numeric_df.empty:
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.heatmap(numeric_df.corr(), annot=False, cmap="coolwarm")
        st.pyplot(fig)

with tab_bq:
    st.subheader("Business Questions (SQL Powered)")

    questions = {
        "Revenue by gender": "q1",
        "Discount users who spent >= average": "q2",
        "Top 5 products by review rating": "q3",
        "Avg purchase: Standard vs Express": "q4",
        "Subscribers vs non-subscribers spend": "q5",
        "Products with highest % discounts": "q6",
        "Customer segmentation (new/returning/loyal)": "q7",
        "Top 3 products per category": "q8",
        "Repeat buyers by subscription": "q9",
        "Revenue by age group": "q10",
    }

    choice = st.selectbox("Select a question:", list(questions.keys()))
    q = questions[choice]

    show_sql = st.checkbox("Show SQL query", value=False)

    sql_queries = {

        "q1": """
            SELECT gender,
                   SUM(purchase_amount) AS revenue
            FROM customer_eda
            GROUP BY gender;
        """,

        "q2": """
            SELECT customer_id, purchase_amount
            FROM customer_eda
            WHERE discount_applied = 'Yes'
              AND purchase_amount >= (SELECT AVG(purchase_amount) FROM customer_eda);
        """,

        "q3": """
            SELECT item_purchased,
                   ROUND(AVG(review_rating)::numeric, 2) AS avg_rating
            FROM customer_eda
            GROUP BY item_purchased
            ORDER BY avg_rating DESC
            LIMIT 5;
        """,

        "q4": """
            SELECT shipping_type,
                   ROUND(AVG(purchase_amount)::numeric, 2) AS avg_purchase
            FROM customer_eda
            WHERE shipping_type IN ('Standard', 'Express')
            GROUP BY shipping_type;
        """,

        "q5": """
            SELECT subscription_status,
                   COUNT(customer_id) AS total_customers,
                   ROUND(AVG(purchase_amount)::numeric, 2) AS avg_spend,
                   ROUND(SUM(purchase_amount)::numeric, 2) AS total_revenue
            FROM customer_eda
            GROUP BY subscription_status;
        """,

        "q6": """
            SELECT item_purchased,
                   ROUND(
                        100.0 *
                        SUM(CASE WHEN discount_applied = 'Yes' THEN 1 ELSE 0 END)::numeric
                        / COUNT(*)
                   , 2) AS discount_rate
            FROM customer_eda
            GROUP BY item_purchased
            ORDER BY discount_rate DESC
            LIMIT 5;
        """,

        "q7": """
            WITH seg AS (
                SELECT customer_id,
                       previous_purchases,
                       CASE
                           WHEN previous_purchases = 1 THEN 'New'
                           WHEN previous_purchases BETWEEN 2 AND 10 THEN 'Returning'
                           ELSE 'Loyal'
                       END AS customer_segment
                FROM customer_eda
            )
            SELECT customer_segment, COUNT(*) AS count
            FROM seg
            GROUP BY customer_segment;
        """,

        "q8": """
            WITH ranked AS (
                SELECT category,
                       item_purchased,
                       COUNT(customer_id) AS total_orders,
                       ROW_NUMBER() OVER (
                           PARTITION BY category
                           ORDER BY COUNT(customer_id) DESC
                       ) AS rank
                FROM customer_eda
                GROUP BY category, item_purchased
            )
            SELECT category, item_purchased, total_orders
            FROM ranked
            WHERE rank <= 3
            ORDER BY category, total_orders DESC;
        """,

        "q9": """
            SELECT subscription_status,
                   COUNT(customer_id) AS repeat_buyers
            FROM customer_eda
            WHERE previous_purchases > 5
            GROUP BY subscription_status;
        """,

        "q10": """
            SELECT age_group,
                   SUM(purchase_amount) AS total_revenue
            FROM customer_eda
            GROUP BY age_group
            ORDER BY total_revenue DESC;
        """,

    }

    query_to_run = sql_queries[q]
    if show_sql:
        st.code(query_to_run, language="sql")

    result = run_sql(query_to_run)
    st.dataframe(result)
