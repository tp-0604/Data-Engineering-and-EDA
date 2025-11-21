import pandas as pd
from db_config import get_psycopg_conn, get_engine

print("Loading raw data from Postgres...")

conn = get_psycopg_conn()
df = pd.read_sql("SELECT * FROM customer;", conn)
conn.close()

print("Raw shape:", df.shape)

df.columns = df.columns.str.lower().str.replace(" ", "_")

# Fill numeric review_rating within category
df['review_rating'] = (
    df.groupby('category')['review_rating']
      .transform(lambda x: x.fillna(x.astype(float).mean()))
)

df = df.rename(columns={'purchase_amount_usd': 'purchase_amount'})

# Create age groups
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)

# Frequency mapping
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['frequency_of_purchases'] = df['frequency_of_purchases'].replace("", None)
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

# Drop unused column
if "promo_code_used" in df.columns:
    df.drop(columns=["promo_code_used"], inplace=True)

engine = get_engine()

print("Writing cleaned data back to Postgres as 'customer_eda' table...")
df.to_sql("customer_eda", engine, if_exists="replace", index=False)

print("EDA pipeline completed!")
